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

    def _VoerUit (self):
        """Voer het request uit"""
        if not self._LeesBestandenEnSpecificatie  ():
            return False
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

        self._PersistenteId = not self.Request.LeesString ('persistente_id') == 'false'
        self._Nauwkeurigheid = self.Request.LeesString ('nauwkeurigheid')
        if valideerGIOs and self._Nauwkeurigheid is None:
            if not self._PersistenteId or self._Was.Dimensie > 0:
                self.Log.Fout ("De nauwkeurigheid is niet opgegeven in de specificatie")
                succes = False

        return succes
