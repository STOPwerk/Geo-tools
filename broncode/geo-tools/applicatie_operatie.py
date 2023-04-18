#======================================================================
#
# Gemeenschappelijke code voor alle geo-gerelateerde operaties
# die resulteren in weergave van geo-informatie.
#
#======================================================================

from typing import Dict, List, Set, Tuple

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from data_geodata import GeoData
from weergave_kaart import KaartGenerator
from weergave_webpagina import WebpaginaGenerator

class Operatie:
#======================================================================
#
# Uitvoeren van de operatie
#
#======================================================================
#region Uitvoeren van de operatie

    def __init__ (self, request : Parameters, log: Meldingen = None, defaultTitel = None, titelBijFout = None):
        """Maak een instantie van de geo-operatie aan

        Argumenten:

        defaultTitel str  Titel van de webpagina als de titel niet is meegegeven bij de invoer
        titelBijFout str  Titel van de webpagina als er een fout optreedt en alleen de log getoond wordt
        request Parameters  De parameters vor het web request
        log Meldingen of bool  Geeft de meldingen die voor deze operatie gebruikt moeten worden. Als het een bool is, dan geeft het aan of de tijd opgenomen moet worden in de meldingen.
        """
        self.Request = request
        # Meldingen voor de uitvoering van de operatie
        self.Log = Meldingen (False) if log is None else Meldingen (log) if isinstance (log, bool) else log
        self.Request.Log = self.Log
        # Titel als doorgegeven in het request
        self.Titel = self.Request.LeesString ('titel')
        # Generator om de resultaat-pagina te maken
        self.Generator = WebpaginaGenerator (defaultTitel if self.Titel is None else self.Titel)
        self._TitelBijFout = titelBijFout if self.Titel is None else self.Titel + " maar niet heus"
        # Kaartgenerator
        self.Kaartgenerator = KaartGenerator (self.Request, self.Generator)
        # Namen waaronder de te gebruiken symbolisatie is geregistreerd
        self._SymbolisatieNamen : Dict[int,str] = None

    def IsVoortzettingVan (self, operatie : 'Operatie') -> 'Operatie':
        """Laat deze operatie doorgaan waar de andere operatie opgehouden is"""
        self.Kaartgenerator.IsVoortzettingVan (operatie.Kaartgenerator)
        self.Generator = operatie.Generator
        return self

    def VoerUit(self):
        """Maak de webpagina aan"""
        self.Log.Informatie ("Geo-tools (https://github.com/STOPwerk/Geo-tools/) versie 2023-04-18 13:36:54.")
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
# Hulpfuncties
#
#----------------------------------------------------------------------
#region Niet-kaartgerelateerde hulpfuncties
    def _ToonResultaatInTekstvak (self, tekst, filenaam : str, dataType : str, elementNaam : str = None, toon : bool = True):
        """"Maak een tekstvak in de resulterende webpagina en toon daarin JSON of XML. De inhoud van het tekstvak
        kan gekopieerd of gedownload worden.

        Argumenten:

        tekst str  Inhoud van het tekstvak
        dataType 'json' of 'xml'  Format van de tekst
        elementnaam str  Naam van het textarea element
        toon bool  Geeft aan of het een zichtbaar (in plaats van verborgen) form-veld is.
        """
        self.Kaartgenerator._Cache._NaamIndex += 1
        elementId = 'resultaat_' + str(self.Kaartgenerator._Cache._NaamIndex)
        self.Generator.VoegHtmlToe ('<textarea id="' + elementId + '" class="resultaat"')
        if not elementNaam is None:
            self.Generator.VoegHtmlToe (' name="' + elementNaam + '"')
        if not toon:
            self.Generator.VoegHtmlToe (' style="display: none;"')
        self.Generator.VoegHtmlToe ('>\n' + tekst.replace ('<', '&lt;').replace ('>', '&gt;') + '\n</textarea>\n')
        if toon:
            self.Generator.VoegHtmlToe ('<div><a data-copy="' + elementId + '" href="#">Kopieer</a> of <a data-download_' + dataType + '="' + elementId + '" data-filenaam="' + filenaam + '" href="#">download</a></div>\n')

    def _InitSymbolisatieNamen (self, voorGeoData : List[GeoData]):
        """Voeg de symbolisatie toe voor de geometrieën in de geo-data. Als symbolisatiebestand(en) opgegeven zijn, dan worden die gebruikt.
    
        Argumenten:
        voorGeoData GeoData[] Lijst met geodata waarvoor de symbolisatie gebruikt gaat worden

        Als resultaat worden de _SymbolisatieNamen gezet"""
        if not self._SymbolisatieNamen is None:
            return
        self._SymbolisatieNamen = {}

        aanwezigeTypen = set (dim for gd in voorGeoData for dim in gd.Locaties.keys ())

        self.Log.Informatie ("Lees de symbolisatie (indien aanwezig)")
        def _VerwerkSymbolisatie (bestandsnaam, symbolisatie):
            if symbolisatie.find ("PolygonSymbolizer") > 0:
                self.Log.Informatie ("Symbolisatie voor vlakken ingelezen uit '" + bestandsnaam + "'")
                dimensie = 2
            elif symbolisatie.find ("LineSymbolizer") > 0:
                self.Log.Informatie ("Symbolisatie voor lijnen ingelezen uit '" + bestandsnaam + "'")
                dimensie = 1
            elif symbolisatie.find ("PointSymbolizer") > 0:
                self.Log.Informatie ("Symbolisatie voor punten ingelezen uit '" + bestandsnaam + "'")
                dimensie = 0
            else:
                self.Log.Informatie ("Symbolisatie voor onbekende geometrieën genegeerd; ingelezen uit '" + bestandsnaam + "'")
                return
            if dimensie in aanwezigeTypen:
                naam = self.Kaartgenerator.VoegSymbolisatieToe (symbolisatie)
                self._SymbolisatieNamen [dimensie] = naam
            else:
                self.Log.Waarschuwing ("Symbolisatie niet gebruikt omdat dit type geometrie niet aanwezig is; ingelezen uit '" + bestandsnaam + "'")
        self.Request.LeesBestanden ("symbolisatie", _VerwerkSymbolisatie)

        for vereisteType in set (dim for gd in voorGeoData if not gd.AttribuutNaam is None for dim in gd.Locaties.keys ()):
            if not vereisteType in self._SymbolisatieNamen:
                self.Log.Waarschuwing ('Geen symbolisatie beschikbaar voor ' + GeoData.GeometrieNaam (vereisteType, True) + ' - gebruik de standaard symbolisatie')

        for dimensie in aanwezigeTypen:
            if not dimensie in self._SymbolisatieNamen:
                self._SymbolisatieNamen[dimensie] = self.Kaartgenerator.VoegDefaultSymbolisatieToe (dimensie)

#endregion
