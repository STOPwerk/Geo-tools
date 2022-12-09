#======================================================================
#
# gio_wijziging
#
#======================================================================
#
# Script om de drie operaties /toon_geo, /maak_gio_wijziging en
# /toon_gio_wijziging in één operatie uit te voeren. Online alleen
# beschikbaar voor de voorbeelden: de specificaties zijn niet via een
# online form in te vullen.
#
#======================================================================

from typing import Dict

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from geo_manipulatie import GeoManipulatie
from maak_gio_wijziging import GIOWijzigingMaker
from toon_geo import GeoViewer
from toon_gio_wijziging import GIOWijzigingViewer

class GIOWijziging (GeoManipulatie):
#======================================================================
#
# Webpagina ondersteuning
#
#======================================================================
    @staticmethod
    def ResultaatHtml(request : Parameters, log: Meldingen = None):
        return GIOWijziging (request, log).VoerUit ()

#======================================================================
#
# Implementatie
#
#======================================================================
    def __init__(self, request : Parameters, log: Meldingen):
        super ().__init__ ("GIO-wijziging", "GIO-wijziging - geen resultaat", request, log)
        # Geometrie specificatie voor de GIO's
        self._Geometrie : Dict[str,GeoManipulatie.GeoData] = {}
        # Naam van de GIO data voor kaartweergave
        self._DataNaam : Dict[str,str] = {}
        # Naam waaronder de te gebruiken symbolisatie voor alle GIO-versies is geregistreerd
        self._SymbolisatieNaam : str = None

    def _VoerUit (self):
        self.Generator.VoegHtmlToe ('<p>Inhoudsopgave? <span id="accordion-sluiten" class="aslink">Verberg</span> alle teksten.</p>')
        if self.Request.LeesString ("beschrijving"):
            einde = self.Generator.StartToelichting ('Beschrijving van dit scenario')
            self.Generator.VoegHtmlToe (self.Request.LeesString ("beschrijving")) 
            self.Generator.VoegHtmlToe (einde)

        #--------------------------------------------------------------
        #
        # Tonen van GIO's
        #
        #--------------------------------------------------------------
        self.Generator.VoegHtmlToe ('<div class="sectie_toon_geo"><h1>Geo-informatieobjecten</h1>')
        altDiv = 0
        for gio in self.Request._FormData['geometrie']:
            if altDiv == 0:
                altDiv = 1
            else:
                self.Generator.VoegHtmlToe ('</div><div class="sectie_toon_geo_alt' + str(altDiv) + '">')
                altDiv = 3 - altDiv

            request = Parameters ({}, None, self.Request._Pad)
            request._FormData["geometrie"] = gio["pad"]
            request._FormData["beschrijving"] = gio.get ("beschrijving")
            request._FormData["symbolisatie"] = self.Request._FormData.get ("symbolisatie")
            request._FormData["nauwkeurigheid"] = self.Request._FormData.get ("nauwkeurigheid")
            uitvoerder = GeoViewer (request, self.Log)
            uitvoerder.Generator = self.Generator
            uitvoerder._SymbolisatieNaam = self._SymbolisatieNaam

            einde = self.Generator.StartSectie ("<h3>" + request.Bestandsnaam ('geometrie') + "</h3>", True)
            if not uitvoerder._VoerUit ():
                return False
            self._Geometrie[gio["pad"]] = uitvoerder._Geometrie
            self._DataNaam[gio["pad"]] = uitvoerder._DataNaam
            self._SymbolisatieNaam = uitvoerder._SymbolisatieNaam

        self.Generator.VoegHtmlToe ('</div>')

        #--------------------------------------------------------------
        #
        # Maken van GIO-wijzigingen
        #
        #--------------------------------------------------------------
        self.Generator.VoegHtmlToe ('<div class="sectie_maak_gio_wijziging"><h1>Maak GIO-wijziging</h1>')
        altDiv = 0
        for wijziging in self.Request._FormData['wijziging']:
            if altDiv == 0:
                altDiv = 1
            else:
                self.Generator.VoegHtmlToe ('</div><div class="sectie_maak_gio_wijziging_alt' + str(altDiv) + '">')
                altDiv = 3 - altDiv

            request = Parameters ({}, None, self.Request._Pad)
            request._FormData["was"] = wijziging["was"]
            request._FormData["wordt"] = wijziging["wordt"]
            request._FormData["beschrijving"] = wijziging.get ("beschrijving")
            request._FormData["symbolisatie"] = self.Request._FormData.get ("symbolisatie")
            request._FormData["nauwkeurigheid"] = self.Request._FormData.get ("nauwkeurigheid")
            uitvoerder = GIOWijzigingMaker (request, self.Log)
            uitvoerder.Generator = self.Generator
            uitvoerder._Was = self._Geometrie.get (wijziging["was"])
            uitvoerder._WasDataNaam = self._DataNaam.get (wijziging["was"])
            uitvoerder._Wordt = self._Geometrie.get (wijziging["wordt"])
            uitvoerder._WordtDataNaam = self._DataNaam.get (wijziging["wordt"])
            uitvoerder._SymbolisatieNaam = self._SymbolisatieNaam

            wijziging["wijziging"] = request.Bestandsnaam ('was') + ' &rarr; ' + request.Bestandsnaam ('wordt')
            einde = self.Generator.StartSectie ("<h3>" + wijziging["wijziging"] + "</h3>", True)
            if not uitvoerder._VoerUit ():
                return False
            wijziging["data"] = uitvoerder._Wijziging
            self._Geometrie[wijziging["was"]] = uitvoerder._Was
            self._DataNaam[wijziging["was"]] = uitvoerder._WasDataNaam

        self.Generator.VoegHtmlToe ('</div>')

        #--------------------------------------------------------------
        #
        # Tonen van GIO-wijzigingen
        #
        #--------------------------------------------------------------
        self.Generator.VoegHtmlToe ('<div class="sectie_toon_gio_wijziging"><h1>Toon GIO-wijziging</h1>')
        altDiv = 0
        for wijziging in self.Request._FormData['wijziging']:
            if altDiv == 0:
                altDiv = 1
            else:
                self.Generator.VoegHtmlToe ('</div><div class="sectie_toon_gio_wijziging_alt' + str(altDiv) + '">')
                altDiv = 3 - altDiv

            request = Parameters ({}, None, self.Request._Pad)
            uitvoerder.Generator = self.Generator
            request._FormData["was"] = wijziging["was"]
            request._FormData["symbolisatie"] = self.Request._FormData.get ("symbolisatie")
            uitvoerder = GIOWijzigingViewer (request, self.Log)
            uitvoerder.Generator = self.Generator
            uitvoerder._SymbolisatieNaam = self._SymbolisatieNaam
            uitvoerder._Was = self._Geometrie.get (wijziging["was"])
            uitvoerder._WasDataNaam = self._DataNaam.get (wijziging["was"])
            uitvoerder._Wijziging = wijziging["data"]

            einde = self.Generator.StartSectie ("<h3>" + wijziging["wijziging"] + "</h3>", True)
            if not uitvoerder._VoerUit ():
                return False
            self._Geometrie[gio["pad"]] = uitvoerder._Geometrie
            self._DataNaam[gio["pad"]] = uitvoerder._DataNaam
            self._SymbolisatieNaam = uitvoerder._SymbolisatieNaam

        self.Generator.VoegHtmlToe ('</div>')
