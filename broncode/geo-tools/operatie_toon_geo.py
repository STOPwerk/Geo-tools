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

from typing import Dict, List, Tuple

from shapely.geometry import mapping

from applicatie_meldingen import Meldingen
from applicatie_operatie import Operatie
from applicatie_request import Parameters
from data_gio import GeoData
from weergave_kaart import KaartGenerator
from weergave_webpagina import WebpaginaGenerator

class GeoViewer (Operatie):
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
        # Geometrie specificatie
        self._Geometrie : GeoData = None
        # Namen van de geometrische data voor kaartweergave
        self._DataNamen : Dict[int,str] = None
        # Namen waaronder de te gebruiken symbolisatie is geregistreerd
        self._SymbolisatieNamen : Dict[int,str] = None
        # Naam van de "dikke pen"-randen afgeleid van de geometrische data
        self._RandDataNaam : str = None
        # Naam van de symbolisatie voor de "dikke pen"-randen afgeleid van de geometrische data
        self._RandSymbolisatieNaam : str = None

    def _VoerUit (self):
        """Voer het request uit"""
        if self.Request.LeesString ("beschrijving"):
            self.Generator.VoegHtmlToe ('<p>' + self.Request.LeesString ("beschrijving") + '</p>') 

        if self._Geometrie is None:
            self.Log.Informatie ("Lees het GIO, gebiedsmarkering of effectgebied")
            self._Geometrie = GeoData.LeesGeoBestand (self.Request, 'geometrie', True)
            if self._Geometrie is None:
                return False
            if self._Geometrie.Soort == 'GIO-wijziging':
                self.Log.Fout ("Kan deze geo-informatie niet weergeven: " + self._Geometrie.Soort)
                return False

        symbolisatieVereist = False
        if self._Geometrie.Soort == 'GIO-versie' and not self._Geometrie.AttribuutNaam is None:
            self.Log.Informatie ('GIO heeft per locatie een ' + self._Geometrie.AttribuutNaam + ' - een symbolisatie is nodig om dat weer te geven')
            symbolisatieVereist = True

        if self._SymbolisatieNamen is None:
            self.Log.Informatie ("Lees de symbolisatie (indien aanwezig)")
            symbolisatie = self.Request.LeesBestand ("symbolisatie", False)
            if symbolisatie is None:
                if symbolisatieVereist:
                    self.Log.Waarschuwing ('Geen symbolisatie beschikbaar - gebruik de standaard symbolisatie voor geometrieën')
                else:
                    self.Log.Informatie ('Geen symbolisatie beschikbaar - gebruik de standaard symbolisatie voor geometrieën')
            else:
                self.Log.Informatie ("Symbolisatie ingelezen uit '" + self.Request.Bestandsnaam ("symbolisatie")+ "'")
            if symbolisatie is None:
                self._SymbolisatieNamen = self.Kaartgenerator.VoegDefaultSymbolisatieToe (self._Geometrie) 
            else:
                naam = self.Kaartgenerator.VoegSymbolisatieToe (symbolisatie)
                self._SymbolisatieNamen = { 0: naam, 1: naam, 2: naam }

        self.Generator.VoegHtmlToe ('Bestand: ' + self.Request.Bestandsnaam ('geometrie'))


        if self._Geometrie.Soort == 'GIO-versie' and not self._Geometrie.JuridischeNauwkeurigheid is None:
            self._MaakRanden ()

        self.Log.Informatie ('Maak de kaartweergave')
        self._DataNamen = self.Kaartgenerator.VoegGeoDataToe (self._Geometrie)
        kaart = KaartGenerator.Kaart (self.Kaartgenerator)
        kaart.ZoomTotNauwkeurigheid (True)
        if not self._RandDataNaam is None:
            kaart.VoegLaagToe ('Juridische nauwkeurigheid', self._RandDataNaam, self._RandSymbolisatieNaam, True, False)
        kaart.VoegLagenToe (self._Geometrie.Soort, self._DataNamen, self._SymbolisatieNamen)
        kaart.Toon ()

        if self._Geometrie.Soort == 'GIO-versie' and not self._Geometrie.JuridischeNauwkeurigheid is None:
            self.Log.Informatie ('Toon GIO met schaalafhankelijkheid')
            self.Generator.VoegHtmlToe ('<p>De GIO is met een juridische nauwkeurigheid van ' + str(self._Geometrie.JuridischeNauwkeurigheid) +  ''' decimeter opgesteld.
            Een GIO-viewer zou dat kunnen laten zien en/of gebruiken om het maximale zoom-niveau in te perken. Een viewer kan ook andere schaal-afhankelijke vereenvoudigingen doorvoeren,
            bijvoorbeeld vereenvoudiging van geometrieën en/of het clusteren van vrijwel onzichtbare geometrieën, zoals in deze kaart gedaan is:.</p>''')

            kaart = KaartGenerator.Kaart (self.Kaartgenerator)
            kaart.ZoomTotNauwkeurigheid (False)
            schaalafhankelijk = self.Kaartgenerator.MaakSchaalafhankelijkeGeometrie (self._Geometrie)
            self.Kaartgenerator.VoegSchaalafhankelijkeLocatiesToe (kaart, self._Geometrie.Soort, schaalafhankelijk, self._SymbolisatieNamen)
            self.Kaartgenerator.VoegSchaalafhankelijkeMarkeringenToe (kaart, self._Geometrie.Soort, schaalafhankelijk, self.Kaartgenerator.VoegWijzigMarkeringToe (0, True))
            kaart.Toon ()

        self.Log.Detail ('Maak de pagina af')
        self.Generator.LeesCssTemplate ('resultaat')
        return True

#======================================================================
#
# Maak de "dikke randen" voor de juridische nauwkeurigheid
#
#======================================================================
    def _MaakRanden (self):
        if self._RandSymbolisatieNaam is None:
            self._RandSymbolisatieNaam = self.Kaartgenerator.VoegUniformeSymbolisatieToe (2, '#cccccc', '#000000', '0.5')
        if not self._RandDataNaam is None:
            return

        randen = GeoData ()
        randen.Locaties = { 2: [] }
        enkelvoudig = self._Geometrie.MaakLijstVanGeometrieen ()[0]
        for dimensie in sorted (enkelvoudig.keys (), reverse=True):
            for geometrie in enkelvoudig[dimensie]:
                rand = GeoData.MaakShapelyShape (geometrie.Geometrie).buffer (0.05 * self._Geometrie.JuridischeNauwkeurigheid)
                if dimensie == 2:
                    rand = rand.difference (GeoData.MaakShapelyShape (geometrie.Geometrie).buffer (-0.05 * self._Geometrie.JuridischeNauwkeurigheid))
                randen.Locaties[2].append ({ 
                    'type': 'Feature', 
                    'geometry': mapping (rand)
                })
        self._RandDataNaam = self.Kaartgenerator.VoegGeoDataToe (randen)[2]
