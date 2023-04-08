#======================================================================
#
# Gemeenschappelijke code voor alle geo-gerelateerde operaties
# die resulteren in weergave van geo-informatie.
#
#======================================================================

from typing import Dict, List, Set, Tuple

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from weergave_kaart import KaartGenerator
from weergave_webpagina import WebpaginaGenerator

class Operatie:
#======================================================================
#
# Uitvoeren van de operatie
#
#======================================================================
#region Uitvoeren van de operatie

    def __init__ (self, defaultTitel, titelBijFout, request : Parameters, log: Meldingen = None):
        """Maak een instantie van de geo-operatie aan

        Argumenten:

        defaultTitel str  Titel van de webpagina als de titel niet is meegegeven bij de invoer
        titelBijFout str  Titel van de webpagina als er een fout optreedt en alleen de log getoond wordt
        request Parameters  De parameters vor het web request
        log Meldingen of bool  Geeft de meldingen die voor deze operatie gebruikt moeten worden. Als het een bool is, dan geeft het aan of de tijd opgenomen moet worden in de meldingen.
        """
        self._TitelBijFout = titelBijFout
        self.Request = request
        # Meldingen voor de uitvoering van de operatie
        self.Log = Meldingen (False) if log is None else Meldingen (log) if isinstance (log, bool) else log
        self.Request.Log = self.Log
        # Titel als doorgegeven in het request
        self.Titel = self.Request.LeesString ('titel')
        # Generator om de resultaat-pagina te maken
        self.Generator = WebpaginaGenerator (defaultTitel if self.Titel is None else self.Titel)
        # Kaartgenerator
        self.Kaartgenerator = KaartGenerator (self.Request, self.Generator)

    def IsVoortzettingVan (self, operatie : 'Operatie') -> 'Operatie':
        """Laat deze operatie doorgaan waar de andere operatie opgehouden is"""
        self.Kaartgenerator.IsVoortzettingVan (operatie.Kaartgenerator)
        self.Generator = operatie.Generator
        return self

    def VoerUit(self):
        """Maak de webpagina aan"""
        self.Log.Informatie ("Geo-tools (@@@GeoTools_Url@@@) versie @@@VERSIE@@@.")
        try:
            # _VoerUit moet in een afgeleide klasse worden geïmplementeerd
            if self._VoerUit ():
                self.Log.Informatie ("De verwerking is voltooid.")
                self.Generator.VoegHtmlToe ("<p>&nbsp;</p>")
                einde = self.Generator.StartSectie ("<h3>Verslag van de verwerking</h3>")
            else:
                self.Log.Fout ("De verwerking is afgebroken.")
                self.Generator.VoegHtmlToe ("<p><b>De verwerking is afgeboken!</b></p>")
                einde = self.Generator.StartSectie ("<h3>Verslag van de incomplete verwerking</h3>")

            self.Generator.VoegHtmlToe ("<p>&nbsp;</p>")
            self.Log.MaakHtml (self.Generator, None)
            self.Generator.VoegHtmlToe (einde)
            return self.Generator.Html ()
        except Exception as e:
            self.Log.Fout ("Oeps, deze fout is niet verwacht: " + str(e))
            generator = WebpaginaGenerator (self._TitelBijFout)
            self.Log.MaakHtml (generator, None, "De verwerking is afgebroken.")
            return generator.Html ()
#endregion

#----------------------------------------------------------------------
#
# Niet-kaartgerelateerde hulpfuncties
#
#----------------------------------------------------------------------
#region Niet-kaartgerelateerde hulpfuncties
    def _ToonResultaatInTekstvak (self, tekst, filenaam : str, dataType : str, elementNaam : str = None, toon : bool = True):
        self._Cache._NaamIndex += 1
        elementId = 'resultaat_' + str(self._Cache._NaamIndex)
        self.Generator.VoegHtmlToe ('<textarea id="' + elementId + '" class="resultaat"')
        if not elementNaam is None:
            self.Generator.VoegHtmlToe (' name="' + elementNaam + '"')
        if not toon:
            self.Generator.VoegHtmlToe (' style="display: none;"')
        self.Generator.VoegHtmlToe ('>\n' + tekst.replace ('<', '&lt;').replace ('>', '&gt;') + '\n</textarea>\n')
        if toon:
            self.Generator.VoegHtmlToe ('<div><a data-copy="' + elementId + '" href="#">Kopieer</a> of <a data-download_' + dataType + '="' + elementId + '" data-filenaam="' + filenaam + '" href="#">download</a></div>\n')
#endregion

