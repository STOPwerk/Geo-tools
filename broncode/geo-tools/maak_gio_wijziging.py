#======================================================================
#
# /maak_gio_wijziging
#
#======================================================================
#
# Script om een GIO-wijziging samen te stellen uit een was- en 
# een wordt-versie van een GIO.
#
#======================================================================

from typing import List, Dict, Tuple
from uuid import uuid4

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from geo_manipulatie import GeoManipulatie
from weergave_webpagina import WebpaginaGenerator

class GIOWijzigingMaker (GeoManipulatie):
#======================================================================
#
# Webpagina's
#
#======================================================================
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("Bepaling van een GIO-wijziging")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters, log: Meldingen = None):
        return GIOWijzigingMaker (request, log).VoerUit ()

#======================================================================
#
# Implementatie
#
#======================================================================
    def __init__(self, request : Parameters, log: Meldingen):
        super ().__init__ ("GIO-wijziging", "GIO-wijziging - geen resultaat", request, log)
        # Was-versie van de GIO
        self._Was : GeoManipulatie.GeoData = None
        # Naam om de was-data in de kaart te tonen
        self._WasDataNaam : str = None
        # Wordt-versie van de GIO
        self._Wordt : GeoManipulatie.GeoData = None
        # Naam om de wordt-data in de kaart te tonen
        self._WordtDataNaam : str = None
        # Maan waaronder de te gebruiken symbolisatie voor zowel de was- als wordt-versie is geregistreerd
        self._SymbolisatieNaam : str = None
        # Geeft aan of een ongewijzigde geometrie in zowel de was- als wordt-versie dezelfde id heeft
        self._PersistenteId = False
        # Geeft de juridische nauwkeurigheid van de geometrie aan
        self._Nauwkeurigheid = None
        # Gegevens waaruit de GIO-wijziging wordt samengesteld
        self._Wijzigingen = GIOWijzigingMaker.Wijzigingen ()

    def _VoerUit (self):
        """Voer het request uit"""
        if not self._LeesBestandenEnSpecificatie  ():
            return False

        einde = self.Generator.StartSectie ("<h3>Bepaling GIO wijziging</h3>", True)

        self._InitialiseerWebpagina ()
        self.Generator.LeesCssTemplate ('resultaat')
        symbolisatie = self.Request.LeesBestand (self.Log, "symbolisatie", False)
        self._SymbolisatieNaam = self.VoegDefaultSymbolisatieToe (self._Was) if symbolisatie is None else self.VoegSymbolisatieToe (symbolisatie)

        self._BepaalWijzigingen ()

        self.Generator.VoegHtmlToe (einde)

        return True


    def _LeesBestandenEnSpecificatie (self):
        """Lees de specificatie en GIO's en valideeer de invoer"""
        succes = True
        self.Log.Informatie ("Lees de was-versie van de GIO")

        valideerGIOs = True
        self._Was = self.LeesGeoBestand ('was', True)
        if self._Was is None:
            return False
        if self._Was.Soort != 'GIO':
            self.Log.Fout ("Het bestand bevat geen GIO maar: " + self._Was.Soort)
            succes = False
            valideerGIOs = False

        self.Log.Informatie ("Lees de wordt-versie van de GIO")
        self._Wordt = self.LeesGeoBestand ('wordt', True)
        if self._Wordt is None:
            return False
        if self._Wordt.Soort != 'GIO':
            self.Log.Fout ("Het bestand bevat geen GIO maar: " + self._Wordt.Soort)
            succes = False
            valideerGIOs = False

        if valideerGIOs:
            if self._Was.Dimensie != self._Wordt.Dimensie:
                self.Log.Fout ("De was- en wordt-versie moeten allebei uitsluitend vlakken, lijnen of punten hebben")
                succes = False
            if self._Was.AttribuutNaam != self._Wordt.AttribuutNaam:
                self.Log.Fout ("De was- en wordt-versie moeten allebei uitsluitend geometrie, GIO-delen of normwaarden hebben")
                succes = False

        self.Log.Informatie ("Lees de symbolisatie (indien aanwezig)")
        self._Symbolisatie = self.Request.LeesBestand (self.Log, "symbolisatie", False)
        if not self._Symbolisatie is None:
            self.Log.Detail ('Symbolisatie ingelezen')

        if self.Request.LeesString ('nauwkeurigheid') is None:
            self.Log.Fout ("De nauwkeurigheid is niet opgegeven in de specificatie")
            succes = False

        return succes

#======================================================================
#
# Bepaling van wijzigingen tussen twee GIO's
#
#======================================================================
    class Wijzigingen:

        def __init__ (self):
            # De locaties uit de was-versie die in de GIO-wijziging opgenomen moet worden
            self.WasLocaties = []
            # De locaties uit de wordt-versie die in de GIO-wijziging opgenomen moet worden
            self.WordtLocaties = []
            # De basisgeometrie-ID van een locatie uit de wordt-versie (key) waarvan alle geometrieën met bijbehorende
            # attribuutwaarde corresponderen met een onveranderde (binnen de nauwkeurigheid) geometrie van de 
            # was-versie. De value zijn de basisgeometrie-ID van de locatie(s) uit de was-versie.
            self.OngewijzigdeWordtLocatieId : Dict[str,List[str]]
            # De juridisch ongewijzigde locaties in de wordt-versie die een revisie 
            # zijn van de locaties in de was-versie, d.w.z. alleen van naam verschillen.
            self.WordtRevisies = []
            # De gedetecteerde wijzigingen. Dit zijn ofwel gebieden ofwel punten.
            self.Markering = GeoManipulatie.GeoData ()

    def _BepaalWijzigingen (self) -> Wijzigingen:
        """Bepaal de wijzigingen tussen twee versies van een GIO"""
        self.Generator.VoegHtmlToe ('''<p>Voor de bepaling van een GIO-wijziging wordt de elders beschreven <a href="@@@GeoTools_Url@@@wiki/Maak-gio-wijziging" target="_blank">procedure</a> gevolgd.
In onderstaande kaart wordt links de was-versie, rechts de wordt-versie van de GIO getoond.
Beweeg de schuif om meer of minder van elke versie te zien. Klik op een ''' + self._Was.GeometrieNaam (False) + ' voor aanvullende details</p>\n')
        self._WasDataNaam = self.VoegGeoDataToe (self._Was)
        self._WordtDataNaam = self.VoegGeoDataToe (self._Wordt)
        self.ToonKaart ('kaart.VoegOudLaagToe ("Was-versie", "' + self._WasDataNaam + '", "' + self._SymbolisatieNaam + '").VoegNieuwLaagToe ("Wordt-versie", "' + self._WordtDataNaam + '", "' + self._SymbolisatieNaam + '");')

        self._ManifestOngewijzigdeGeometrieen ()

    #------------------------------------------------------------------
    #
    # Verwerk persistente ID: basisgeo-ID die zowel in de was-
    # als wordt-versie voorkomen.
    #
    #------------------------------------------------------------------
    def _ManifestOngewijzigdeGeometrieen (self):
        self.Log.Informatie ('Onderzoek de locaties met manifest ongewijzigde geometrieën')
        wasLocaties = { locatie['properties']['id'] : locatie for locatie in self._Was.Locaties}
        wordtLocaties = { locatie['properties']['id'] : locatie for locatie in self._Wordt.Locaties}

        # Bepaal of en hoe de locaties met manifest ongewijzigde geometrie muteren
        manifestOngewijzigdId = set ()
        ongewijzigd = []
        for wasId, wasLocatie in wasLocaties.items ():
            wordtLocatie = wordtLocaties.get (wasId)
            if not wordtLocatie is None:
                manifestOngewijzigdId.add (wasId)

                isGewijzigd = False if self._Was.AttribuutNaam is None else bool (wasLocatie['properties'][self._Was.AttribuutNaam] != wordtLocatie['properties'][self._Was.AttribuutNaam])
                if isGewijzigd:
                    self._Wijzigingen.WasLocaties.append (wasLocatie)
                    self._Wijzigingen.WordtLocaties.append (wordtLocatie)
                    self._Wijzigingen.Markering.Locaties.extend (self.SplitsMultiGeometrie (wasLocatie))

                elif wasLocatie['properties'].get ('naam') != wordtLocatie['properties'].get ('naam'):
                    self._Wijzigingen.WordtRevisies.append (wordtLocatie)
                else:
                    ongewijzigd.append (wasLocatie)

        # De overgebleven locaties zijn:
        self._Was.Locaties = [l for l in self._Was.Locaties if not l['properties']['id'] in manifestOngewijzigdId]
        self._Wordt.Locaties = [l for l in self._Wordt.Locaties if not l['properties']['id'] in manifestOngewijzigdId]

        # Neem de resultaten van deze stap in de resultaatpagina
        if len (manifestOngewijzigdId) == 0:
            self.Generator.VoegHtmlToe ('''<p>Er zijn geen locaties gevonden met een manifest ongewijzigde geometrie, dus locaties die in de was- en wordt-versie dezelfde basisgeometrie-ID hebben.</p>''')
        else:
            self.Generator.VoegHtmlToe ('<p> Er ' + ('is één locatie' if len(manifestOngewijzigdId) == 1 else 'zijn ' + str(len(manifestOngewijzigdId)) + ' locaties') + '''gevonden 
met een manifest ongewijzigde geometrie, dus locaties die in de was- en wordt-versie dezelfde basisgeometrie-ID hebben:
<ul>''')
            if not self._Was.AttribuutNaam is None:
                self.Generator.VoegHtmlToe ('<li>' + str(len(self._Wijzigingen.WasLocaties)) + ' met een gewijzigde ' + self._Was.AttribuutNaam + ';</li>')
            self.Generator.VoegHtmlToe ('<li>' + str(len(self._Wijzigingen.WordtRevisies)) + ''' met een gewijzigde naam;</li>
<li>''' + str(len (ongewijzigd)) + ''' ongewijzigd</li></ul>
In onderstaande kaart zijn deze locaties opgenomen.
</p>\n''')
            kaartScript = ''
            if len (ongewijzigd) > 0:
                dataSet = GeoManipulatie.GeoData () 
                dataSet.Attributen = self._Was.Attributen
                dataSet.Locaties = ongewijzigd
                kaartScript += 'kaart.VoegOnderlaagToe ("Juridisch ongewijzigd", "' + self.VoegGeoDataToe (dataSet) + '", "' + self._SymbolisatieNaam + '", true, true);'

            if len (self._Wijzigingen.Markering.Locaties) > 0:
                kvSym = self.VoegUniformeSymbolisatieToe (self._Was.Dimensie, "#D80073", "#A50040")
                kaartScript += 'kaart.VoegOnderlaagToe ("Gewijzigd (exclusief revisies)", "' + self.VoegGeoDataToe (self._Wijzigingen.Markering) + '", "' + kvSym + '", true, true);'

            if len (self._Wijzigingen.WordtRevisies) > 0:
                dataSet.Attributen = {}
                dataSet.Locaties = self._Wijzigingen.WordtRevisies
                kvSym = self.VoegUniformeSymbolisatieToe (self._Was.Dimensie, "#DAE8FC", "#6C8EBF")
                kaartScript += 'kaart.VoegOnderlaagToe ("Revisies", "' + self.VoegGeoDataToe (dataSet) + '", "' + kvSym + '", true, true);'
            self.ToonKaart (kaartScript)
