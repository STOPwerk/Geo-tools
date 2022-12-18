#======================================================================
#
# /toon_gio_wijziging
#
#======================================================================
#
# Script om een GIO-wijziging samen met een was- en een wordt-versie 
# van de GIO te tonen in een viewer. De wordt-versie wordt afgeleid
# uit de wijziging en was-versie.
#
#======================================================================

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from geo_manipulatie import GeoManipulatie
from weergave_webpagina import WebpaginaGenerator

class GIOWijzigingViewer (GeoManipulatie):
#======================================================================
#
# Webpagina's
#
#======================================================================
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("Tonen van een GIO-wijziging")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters, log: Meldingen = None):
        return GIOWijzigingViewer (request, log).VoerUit ()

#======================================================================
#
# Implementatie
#
#======================================================================
    def __init__(self, request : Parameters, log: Meldingen):
        super ().__init__ ("GIO-wijziging in beeld", "GIO-wijziging - geen beeld", request, log)
        # Was-versie van de GIO
        self._Was : GeoManipulatie.GeoData = None
        # Naam waaronder de te gebruiken symbolisatie voor zowel de was- als wordt-versie is geregistreerd
        self._SymbolisatieNaam : str = None
        # De resulterende GIO-wijziging
        self._Wijziging : GeoManipulatie.GeoData = None
        # Wordt-versie van de GIO, gereconstrueerd uit de was en de GIO-wijziging
        self._Wordt : GeoManipulatie.GeoData = None
        # Naam om de wordt-data in de kaart te tonen
        self._WordtDataNaam : str = None

    def _VoerUit (self, titelOperatie : str = None):
        """Voer het request uit"""
        if not self._LeesBestandenEnSpecificatie  ():
            return False
        if not self._MaakWordtVersie ():
            return False

        self._InitialiseerWebpagina ()
        einde = self.Generator.StartSectie ("Weergave van de GIO-wijziging" if titelOperatie is None else "<h3>" + titelOperatie + "</h3>", True)
        if self.Request.LeesString ("beschrijving"):
            self.Generator.VoegHtmlToe ('<p>' + self.Request.LeesString ("beschrijving") + '</p>') 
        self._ToonGIOWijziging ()
        self.Generator.VoegHtmlToe (einde);

        einde = self.Generator.StartSectie ("Reconstructie van de wordt-versie", True)
        self._ToonWordtVersie ()
        self.Generator.VoegHtmlToe (einde);

        return True


    def _LeesBestandenEnSpecificatie (self):
        """Lees de specificatie en GIO's en valideeer de invoer"""
        succes = True

        valideerGIOs = True
        if self._Was is None:
            self.Log.Informatie ("Lees de was-versie van de GIO")
            def __BewaarGML (gml):
                if self.Request.IsOnlineOperatie:
                    self._WasGML = gml
            self._Was = self.LeesGeoBestand ('was', True, __BewaarGML)
            if self._Was is None:
                return False
            if self._Was.Soort != 'GIO':
                self.Log.Fout ("Het bestand bevat geen GIO maar: " + self._Was.Soort)
                succes = False
                valideerGIOs = False

        if self._Wijziging is None:
            self.Log.Informatie ("Lees de GIO-wijziging")
            self._Wijziging = self.LeesGeoBestand ('wijziging', True)
            if self._Wijziging is None:
                return False
            if self._Wijziging.Soort != 'GIO-wijziging':
                self.Log.Fout ("Het bestand bevat geen GIO-wijziging maar: " + self._Wordt.Soort)
                succes = False
                valideerGIOs = False

        if valideerGIOs:
            if self._Was.ExpressionId != self._Wijziging.Was.ExpressionId:
                self.Log.Fout ("De was-versie heeft een andere expression-identificatie dan het origineel van de GIO-wijziging")
                succes = False
            if self._Was.Dimensie != self._Wijziging.Dimensie:
                self.Log.Fout ("De was-versie en GIO-wijziging moeten allebei uitsluitend vlakken, lijnen of punten hebben")
                succes = False
            if self._Was.AttribuutNaam != self._Wijziging.AttribuutNaam:
                self.Log.Fout ("De was-versie en GIO-wijziging moeten allebei uitsluitend geometrie, GIO-delen of normwaarden hebben")
                succes = False

        if self._SymbolisatieNaam is None:
            self.Log.Informatie ("Lees de symbolisatie (indien aanwezig)")
            symbolisatie = self.Request.LeesBestand (self.Log, "symbolisatie", bool (not self._Wijziging.AttribuutNaam is None))
            if self.Request.IsOnlineOperatie:
                self._SymbolisatieXML = symbolisatie
            self._SymbolisatieNaam = self.VoegDefaultSymbolisatieToe (self._Was) if symbolisatie is None else self.VoegSymbolisatieToe (symbolisatie)

        return succes

#======================================================================
#
# Reconstructie van de wordt-versie
#
#======================================================================
    def _MaakWordtVersie (self):
        succes = True

        self._Wordt = GeoManipulatie.GeoData ()
        self._Wordt.Attributen = self._Wijziging.Wordt.Attributen
        self._Wordt.AttribuutNaam = self._Wijziging.Wordt.AttribuutNaam
        self._Wordt.Dimensie = self._Wijziging.Wordt.Dimensie
        self._Wordt.EenheidID = self._Wijziging.EenheidID
        self._Wordt.EenheidLabel = self._Wijziging.EenheidLabel
        self._Wordt.ExpressionId = self._Wijziging.Wordt.ExpressionId
        if not self._Wijziging.GIODelen is None:
            self._Wordt.GIODelen = { i : GeoManipulatie.GIODeel(i, g.Label) for i, g in self._Wijziging.GIODelen.items () if g.WijzigActie != 'verwijder'}
        self._Wordt.NormID = self._Wijziging.NormID
        self._Wordt.NormLabel = self._Wijziging.NormLabel
        self._Wordt.Soort = 'GIO'
        self._Wordt.Tekennauwkeurigheid = self._Wijziging.Tekennauwkeurigheid
        self._Wordt.WorkId = self._Wijziging.WorkId

        locaties = {locatie['properties']['id'] : locatie for locatie in self._Was.Locaties }

        for locatie in self._Wijziging.Was.Locaties:
            if locaties.pop (locatie['properties']['id'], None) is None:
                self.Log.Fout ("GIO-wijziging verwijdert een locatie met basisgeometrie-ID '" + locatie['properties']['id'] + "' die niet voorkomt in de originele versie")
                succes = False

        revisie_was_id = set ()
        for locatie in self._Wijziging.WordtRevisies.Locaties:
            revisie_was_id.update (locatie['properties']['isRevisieVan'])
        for was_id in revisie_was_id:
            if locaties.pop (was_id, None) is None:
                self.Log.Fout ("GIO-wijziging reviseert een locatie met basisgeometrie-ID '" + was_id + "' die niet (meer) voorkomt in de originele versie")
                succes = False

        toegevoegd = set ()
        for locatie in self._Wijziging.WordtRevisies.Locaties:
            wordt_id = locatie['properties']['id']
            if wordt_id in toegevoegd:
                self.Log.Fout ("GIO-wijziging bevat twee revisies met basisgeometrie-ID '" + wordt_id + "'")
                succes = False
            else:
                toegevoegd.add (wordt_id)
                locaties[wordt_id] = locatie

        for locatie in self._Wijziging.Wordt.Locaties:
            wordt_id = locatie['properties']['id']
            if wordt_id in toegevoegd:
                self.Log.Fout ("GIO-wijziging voegt een locaties toe met basisgeometrie-ID '" + wordt_id + "' die dubbel in de GIO-wijziging voorkomt (als voegtoe en/of reviseer)")
                succes = False
            else:
                toegevoegd.add (wordt_id)
                locaties[wordt_id] = locatie

        self._Wordt.Locaties = list (locaties.values ())

        return succes

    def _ToonWordtVersie (self):
        self.Generator.VoegHtmlToe ('''<p>Door combinatie van de originele GIO-versie en de GIO-wijziging kan de nieuwe versie gereconstrueerd worden.
De volgorde van de Locaties in de GIO hoeft niet overeen te komen met de volgorde in de GIO-versie die voor de bepaling van de GIO-wijziging
is gebruikt, of (voor de behouden locaties) voor de locaties in de originele versie.</p>''')
        gml = self.SchrijfGIO (self._Wordt)
        self._ToonResultaatInTekstvak (gml, 'Wordt_versie.gml', 'xml')

#======================================================================
#
# Weergave van de GIO-wijziging
#
#======================================================================
    def _ToonGIOWijziging (self):
        pass
