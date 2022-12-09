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
        # Naam om de was-data in de kaart te tonen
        self._WasDataNaam : str = None
        # Naam waaronder de te gebruiken symbolisatie voor zowel de was- als wordt-versie is geregistreerd
        self._SymbolisatieNaam : str = None
        # De resulterende GIO-wijziging
        self._Wijziging : GeoManipulatie.GeoData = None
        # Wordt-versie van de GIO, gereconstrueerd uit de was en de GIO-wijziging
        self._Wordt : GeoManipulatie.GeoData = None
        # Naam om de wordt-data in de kaart te tonen
        self._WordtDataNaam : str = None

    def _VoerUit (self):
        pass
