#======================================================================
#
# /gio_wijziging
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
        # Symbolisatie voor zowel de was- als wordt-versie; kan None zijn
        self._Symbolisatie : str = None
        # Maan waaronder de te gebruiken symbolisatie voor zowel de was- als wordt-versie is geregistreerd
        self._SymbolisatieNaam : str = None
        # Geeft aan of een ongewijzigde geometrie in zowel de was- als wordt-versie dezelfde id heeft
        self._PersistenteId = False
        # Geeft de juridische nauwkeurigheid van de geometrie aan
        self._Nauwkeurigheid = None

    def _VoerUit (self):
        """Voer het request uit"""
        if not self._LeesBestandenEnSpecificatie  ():
            return False

        einde = self.Generator.StartSectie ("<h3>Bepaling GIO wijziging</h3>", True)

        self._ToonWasWordtKaart ()

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

        self._PersistenteId = not self.Request.LeesString ('persistente_id') == 'false'
        self._Nauwkeurigheid = self.Request.LeesString ('nauwkeurigheid')
        if valideerGIOs:
            if self._Nauwkeurigheid is None:
                if not self._PersistenteId or self._Was.Dimensie > 0:
                    self.Log.Fout ("De nauwkeurigheid is niet opgegeven in de specificatie")
                    succes = False
            else:
                self._Nauwkeurigheid = float (self._Nauwkeurigheid)

        return succes

    def _ToonWasWordtKaart (self):
        """Toon de was en de wordt in één kaart als startpunt van de afleiding"""
        self.Log.Informatie ('Laat de was- en wordt-versie als aangeleverd zien in één kaart')
        self._InitialiseerWebpagina ()
        self.Generator.LeesCssTemplate ('resultaat')

        if not self._SymbolisatieNaam is None:
            self._SymbolisatieNaam = self.VoegDefaultSymbolisatieToe (self._Was) if self._Symbolisatie is None else self.VoegSymbolisatieToe (self._Symbolisatie)
        self._WasDataNaam = self.VoegGeoDataToe (self._Was)
        self._WordtDataNaam = self.VoegGeoDataToe (self._Wordt)

        self.Generator.VoegHtmlToe ('''<p>Links de was-versie, rechts de wordt-versie van de GIO.
Beweeg de schuif om meer of minder van elke versie te zien. Klik op een ''' + self._Was.GeometrieNaam (False) + ' voor aanvullende details</p>\n')
        self.ToonKaart ('kaart.VoegOudLaagToe ("Was-versie", "' + self._WasDataNaam + '", "' + self._SymbolisatieNaam + '").VoegNieuwLaagToe ("Wordt-versie", "' + self._WordtDataNaam + '", "' + self._SymbolisatieNaam + '");')

#======================================================================
#
# Bepaling van wijzigingen tussen twee GIO's
#
#======================================================================
    class Wijzigingen:

        def __init__ (self):
            """Maak een instantie van de rapportage van de verschillen"""
            # De basisgeometrie-ID van de locaties die zowel in de was- als in de wordt-versie zitten,
            # en die ongewijzigd wijn
            self.PersistenteId : List[str] = []
            # De basisgeometrie-ID van een locatie in de was-versie (key) die binnen de nauwkeurigheid gelijk is 
            # aan de locatie in de wordt versie (basisgeometrie-ID is value).
            # De persistenteId zijn hierin niet meegenomen
            self.OngewijzigdeId : Dict[str,str] = []
            # De basisgeometrie-ID van juridisch ongewijzigde locaties in de wordt-versie die een revisie 
            # zijn van de locaties in de was-versie.
            self.Revisies : List[str] = []
            # De gedetecteerde wijzigingen. De key is de oude en nieuwe "waarde" van de locatie, 
            # de value is een lijst met locaties met alleen geometrie en een UUID. De "waarde"
            # is ofwel de normwaarde, ofwel de groepID, ofwel 1 voor alleen de geometrie. De waarde 
            # is None als de was- of wordt-versie voor de locaties geen "waarde" heeft (dus in de was- 
            # c.q. wordt-versie was er geen geometrie die de locatie bevatte, maar in de andere versie wel)..
            self.Wijzigingen = Dict[Tuple[str,str],List[object]]

    class _LocatieData:
        def __init__(self, locatie, attribuutNaam, bepaalRevisie):
            self.Locatie = locatie
            self.Waarde = 1 if attribuutNaam is None else locatie.propreties[attribuutNaam],
            self.Naam = locatie.propreties.get('naam') if bepaalRevisie else None

    def _BepaalWijzigingen (self, wasVersie : GeoManipulatie.GeoData, wordtVersie: GeoManipulatie.GeoData, persistenteId : bool, alleenGeometrie: bool, bepaalRevisie: bool) -> Wijzigingen:
        """Bepaal de wijzigingen tussen twee versies van een GIO

        Argumenten:

        wasVersie GeoData  De originele/was-versie van de GIO
        wordtVersie GeoData  De gewijzigde/wordt-versie van de GIO
        persistenteId bool  Ga ervan uit dat dezelfde geometrie in was- en wordt-versie dezelfde basisgeometrie-ID heeft, 
                            dus dat een verschillende basisgeometrie-ID een wijziging van geometrie impliceert. De wijziging
                            van oude naar nieuwe geometrie kan alsnog zo klein zijn de twee IDs in OngewijzigdeId terecht komen.
        bepaalRevisie bool  Ga voor de ongewijzigde locaties na of de naam gewijzigd is in de wordt versie; dat is de enige
                            revisie die op dit moment mogelijk is.
        """
        wijzigingen = GIOWijzigingMaker.Wijzigingen ()

        # Selecteer de relevante data uit de was- en wordt-versie
        attribuutNaam = None if alleenGeometrie else wasVersie.AttribuutNaam
        wasData = {l.propreties['id'] : GIOWijzigingMaker._LocatieData (l, attribuutNaam, bepaalRevisie) for l in wasVersie.Locaties }
        wordtData = {l.propreties['id'] : GIOWijzigingMaker._LocatieData (l, attribuutNaam, bepaalRevisie) for l in wordtVersie.Locaties }

        # Zoek naar persistente IDs
        wasGedaan = []
        for wasId, wasLocatie in wasData.items ():
            wordtLocatie = wordtData.get (wasId)
            if not wordtLocatie is None:
                if wordtLocatie.waarde == wasLocatie.waarde:
                    # Ongewijzigde geometrie en waarde
                    wijzigingen.PersistenteId.append (wasId)
                else:
                    # Ongewijzigde geometrie, gewijzigde waarde
                    wijziging = (wasLocatie.waarde, wordtLocatie.waarde)
                    lijst = wijzigingen.Wijzigingen.get (wijziging)
                    if lijst == None:
                        wijzigingen.Wijzigingen[wijziging] = lijst = []
                    lijst.append (wordtLocatie.locatie)
                # De wordt-geometrie hoeft niet meer meegenomen te worden
                wordtData.pop (wasId)
                # De was trouwens ook niet
                wasGedaan.append (wasId)
        for wasId in wasGedaan:
            wasData.pop (wasId)

        # Gebruik nu de geo-operaties om verdere verschillen te vinden
        if wasVersie.Dimensie == 0:
            wijzigingen = self._BepaalWijzigingenVoorPunten (wijzigingen, wasVersie, wordtVersie, persistenteId)
        elif wasVersie.Dimensie == 1:
            wijzigingen = self._BepaalWijzigingenVoorLijnen (wijzigingen, wasVersie, wordtVersie, persistenteId)
        elif wasVersie.Dimensie == 2:
            wijzigingen = self._BepaalWijzigingenVoorVlakken (wijzigingen, wasVersie, wordtVersie, persistenteId)

        # Revisie: alle ongewijzigde locaties waarvan de naam verschilt tussen een was- en wordt-versie.
        if not wijzigingen is None and bepaalRevisie:
            for wordtId in wijzigingen.PersistenteId:
                if wasData[wordtId].naam != wordtData[wordtId].naam:
                    wijzigingen.Revisies.append (wordtId)
            for wasId, wordtId in wijzigingen.OngewijzigdeId.items ():
                if wasData[wasId].naam != wordtData[wordtId].naam:
                    wijzigingen.Revisies.append (wordtId)

        return wijzigingen


    def _BepaalWijzigingenVoorPunten (self, wijzigingen: Wijzigingen, wasVersie : Dict[str,_LocatieData], wordtVersie: Dict[str,_LocatieData], persistenteId : bool):

        pass

    def _BepaalWijzigingenVoorLijnen (self, wijzigingen: Wijzigingen, wasVersie : Dict[str,_LocatieData], wordtVersie: Dict[str,_LocatieData], persistenteId : bool):
        raise 'Niet geïmplementeerd'

    def _BepaalWijzigingenVoorVlakken (self, wijzigingen: Wijzigingen, wasVersie : Dict[str,_LocatieData], wordtVersie: Dict[str,_LocatieData], persistenteId : bool):
        raise 'Niet geïmplementeerd'
