#======================================================================
#
# /toon_geo
#
#======================================================================
#
# Script om een GIO of gebiedmarkering/effectgebied te tonen in een 
# viewer.
#
#======================================================================

import json

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from geo_manipulatie import GeoManipulatie
from weergave_webpagina import WebpaginaGenerator

class GeoViewer (GeoManipulatie):
#======================================================================
#
# Webpagina's
#
#======================================================================
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("Tonen van een GIO-versie of gebieden")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters, log: Meldingen = None):
        return GeoViewer (request, log).VoerUit ()

#======================================================================
#
# Implementatie
#
#======================================================================
    def __init__(self, request : Parameters, log: Meldingen):
        super ().__init__ ("Geo-informatie in beeld", "Geo-informatie - geen beeld", request, log)

    def _VoerUit (self):
        """Voer het request uit"""
        self.Log.Informatie ("Lees het GIO, gebiedsmarkering of effectgebied")
        gio = self.LeesGeoBestand ('geometrie', True)
        if gio is None:
            return False
        if gio.Soort == 'GIO-wijziging':
            self.Log.Fout ("Kan deze geo-informatie niet weergeven: " + gio.Soort)
            return False
        self.Log.Informatie (gio.Soort + ' ingelezen')

        symbolisatieVereist = False
        if gio.Soort == 'GIO' and not gio.AttribuutNaam is None:
            self.Log.Informatie ('GIO heeft per locatie een ' + gio.AttribuutNaam + ' - een symbolisatie is nodig om dat weer te geven')
            symbolisatieVereist = True

        self.Log.Informatie ("Lees de symbolisatie (indien aanwezig)")
        symbolisatie = self.Request.LeesBestand (self.Log, "symbolisatie", False)
        if symbolisatie is None:
            if symbolisatieVereist:
                self.Log.Waarschuwing ('Geen symbolisatie beschikbaar - gebruik de standaard symbolisatie voor geometrieën')
            else:
                self.Log.Informatie ('Geen symbolisatie beschikbaar - gebruik de standaard symbolisatie voor geometrieën')
        else:
            self.Log.Detail ('Symbolisatie ingelezen')


        self.Log.Informatie ('Maak de kaartweergave')
        self.VoegGeoDataToe ('gio', gio.Locaties)
        if not symbolisatie is None:
            symbolisatieNaam = "sym"
            self.VoegSymbolisatieToe (symbolisatieNaam, symbolisatie)
        else:
            symbolisatieNaam = self.VoegDefaultSymbolisatieToe (gio)
        self.ToonKaart ("kaart", "kaart", 'kaart.VoegOnderlaagToe ("' + gio.Soort + '", "gio", "' + symbolisatieNaam + '");')

        self.Log.Detail ('Maak de pagina af')
        self.Generator.LeesCssTemplate ('resultaat')
        return True

