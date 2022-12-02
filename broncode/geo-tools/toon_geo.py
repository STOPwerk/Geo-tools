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
        super ().__init__ ("Geo-informatie in beeld", "Geo-informatie - geen beeld", request, log, True)

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

        einde = None
        if not self.RequestIndex is None:
            einde = self.Generator.StartSectie ('<h3>Bestand #1</h3>', True)

        self.Log.Informatie ('Maak de kaartweergave')
        dataNaam = self.VoegGeoDataToe (gio)
        symbolisatieNaam = self.VoegDefaultSymbolisatieToe (gio) if symbolisatie is None else self.VoegSymbolisatieToe (symbolisatie)
        self.ToonKaart ('kaart.VoegOnderlaagToe ("' + gio.Soort + '", "' + dataNaam + '", "' + symbolisatieNaam + '");')

        if gio.Soort == 'GIO' and not self.NauwkeurigheidInMeter () is None:
            self.Log.Informatie ('Valideer de GIO')
            lijst = self.MaakLijstVanGeometrieen (gio)
            problemen, tekennauwkeurigheid = self.ValideerGIO (lijst, gio.Dimensie)
            if problemen is None:
                self.Generator.VoegHtmlToe ('<p>Het GIO kan gebruikt worden voor de bepaling van een GIO-wijziging bij tekennauwkeurigheid ' + self.Request.LeesString ("nauwkeurigheid") + '</p>')
            else:
                self.Generator.VoegHtmlToe ('<p>Het GIO kan <b>niet</b> gebruikt worden voor de bepaling van een GIO-wijziging bij tekennauwkeurigheid ' + self.Request.LeesString ("nauwkeurigheid") + ". ")
                if not tekennauwkeurigheid is None:
                    self.Generator.VoegHtmlToe ('Het GIO kan wel> gebruikt worden met een tekennauwkeurigheid van ' + str(tekennauwkeurigheid))
                self.Generator.VoegHtmlToe ('</p><p>De plaatsen waar geometrieën voor problemen zorgen:')
                geomNaam = self.VoegGeometrieToeAlsData (problemen)
                geomSym = self.VoegUniformeSymbolisatieToe (1 if gio.Dimensie == 1 else 2, "#ff0000", "#800000")
                self.ToonKaart ('kaart.VoegOnderlaagToe ("' + gio.Soort + '", "' + dataNaam + '", "' + symbolisatieNaam + '");kaart.VoegOnderlaagToe ("' + gio.Soort + '", "' + geomNaam + '", "' + geomSym + '");')

        self.Log.Detail ('Maak de pagina af')
        self.Generator.VoegHtmlToe (einde)
        self.Generator.LeesCssTemplate ('resultaat')
        return True

