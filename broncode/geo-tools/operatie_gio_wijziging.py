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
from applicatie_operatie import Operatie
from applicatie_request import Parameters
from data_geodata import GeoData
from operatie_maak_gio_wijziging import MaakGIOWijziging
from operatie_toon_geo import ToonGeo
from operatie_toon_gio_wijziging import ToonGIOWijziging

class GIOWijziging (Operatie):
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
    def __init__(self, request : Parameters, log: Meldingen, defaultTitel = None, titelBijFout = None):
        super ().__init__ (request, log, "GIO-wijziging" if defaultTitel is None else defaultTitel, "GIO-wijziging - geen resultaat" if titelBijFout is None else titelBijFout)
        # Geometrie specificatie voor de GIO's
        self._Geometrie : Dict[str,GeoData] = {}

    def _VoerUit (self):
        self.Generator.VoegHtmlToe ('<p>Inhoudsopgave? <span id="accordion-sluiten" class="aslink">Verberg</span> alle teksten.</p>')
        if self.Request.LeesString ("beschrijving"):
            einde = self.Generator.StartToelichting ('Beschrijving van dit scenario')
            self.Generator.VoegHtmlToe (self.Request.LeesString ("beschrijving")) 
            self.Generator.VoegHtmlToe (einde)

        def __Waarde (spec, key):
            x = spec.get (key)
            if x is None:
                x = self.Request._FormData.get (key)
            return x

        succes = True

        #--------------------------------------------------------------
        #
        # Tonen van GIO's
        #
        #--------------------------------------------------------------
        gioLijst = self.Request._FormData['geometrie']
        if len (gioLijst) > 0:
            self.Generator.VoegHtmlToe ('<div class="sectie_toon_geo"><h2>Geo-informatieobjecten</h2>')
            altDiv = 0
            for gio in gioLijst:
                if altDiv == 0:
                    altDiv = 1
                else:
                    self.Generator.VoegHtmlToe ('</div><div class="sectie_toon_geo_alt' + str(altDiv) + '">')
                    altDiv = 3 - altDiv

                request = Parameters (self.Log, {}, None, self.Request._Pad)
                request.KanBestandenSchrijven = False
                request._FormData["geometrie"] = gio["pad"]
                request._FormData["beschrijving"] = gio.get ("beschrijving")
                request._FormData["symbolisatie"] = __Waarde (gio, "symbolisatie")
                request._FormData["juridische-nauwkeurigheid"] = __Waarde (gio, "juridische-nauwkeurigheid")
                request._FormData["toon-gio-schaalafhankelijk"] = __Waarde (gio, "toon-gio-schaalafhankelijk")
                request._FormData["kwaliteitscontrole"] = __Waarde (gio, "kwaliteitscontrole")

                self.Log.Informatie ("Toon GIO: '" + gio["pad"] + "'")
                uitvoerder = ToonGeo (request, self.Log)
                uitvoerder.IsVoortzettingVan (self)
                uitvoerder._Geometrie = self._Geometrie.get (gio["pad"])

                einde = self.Generator.StartSectie ("<h3>" + request.Bestandsnaam ('geometrie', False) + "</h3>", True)
                succes = uitvoerder._VoerUit ()
                self.Generator.VoegHtmlToe (einde)
                if not succes:
                    break

                self._Geometrie[gio["pad"]] = uitvoerder._Geometrie

            self.Generator.VoegHtmlToe ('</div>')

        #--------------------------------------------------------------
        #
        # Maken van GIO-wijzigingen
        #
        #--------------------------------------------------------------
        maakWijzigingLijst = self.Request._FormData.get ('wijziging')
        toonWijzigingLijst = []
        if succes and not maakWijzigingLijst is None and len (maakWijzigingLijst) > 0:
            self.Generator.VoegHtmlToe ('<div class="sectie_maak_gio_wijziging"><h2>Maak GIO-wijziging</h2>')
            altDiv = 0
            for wijziging in maakWijzigingLijst:
                if altDiv == 0:
                    altDiv = 1
                else:
                    self.Generator.VoegHtmlToe ('</div><div class="sectie_maak_gio_wijziging_alt' + str(altDiv) + '">')
                    altDiv = 3 - altDiv

                request = Parameters (self.Log, {}, None, self.Request._Pad)
                request.KanBestandenSchrijven = False
                request._FormData["was"] = wijziging["was"]
                request._FormData["wordt"] = wijziging["wordt"]
                request._FormData["beschrijving"] = wijziging.get ("beschrijving")
                request._FormData["symbolisatie"] = __Waarde (wijziging, "symbolisatie")
                request._FormData["toon-gio-wijziging"] = False
                request._FormData["juridische-nauwkeurigheid"] = __Waarde (wijziging, "juridische-nauwkeurigheid")

                self.Log.Informatie ("Maak GIO-wijziging: '" + wijziging["was"] + "' &rarr; '" + wijziging["was"] + "'")
                uitvoerder = MaakGIOWijziging (request, self.Log)
                uitvoerder.IsVoortzettingVan (self)
                uitvoerder._Was = self._Geometrie.get (wijziging["was"])
                uitvoerder._Wordt = self._Geometrie.get (wijziging["wordt"])

                wijziging["wijziging"] = request.Bestandsnaam ('was', False) + ' &rarr; ' + request.Bestandsnaam ('wordt', False)
                succes = uitvoerder._VoerUit (wijziging["wijziging"])
                if not succes:
                    break

                self._Geometrie[wijziging["was"]] = uitvoerder._Was
                request._FormData["toon-gio-wijziging"] = __Waarde (wijziging, "toon-gio-wijziging")
                request._FormData["beschrijving"] = wijziging.get ("beschrijving-toon")
                if not uitvoerder._Wijziging is None and request.IsOptie ("toon-gio-wijziging", False):
                    wijziging["data"] = uitvoerder._Wijziging
                    toonWijzigingLijst.append (wijziging)

            self.Generator.VoegHtmlToe ('</div>')

        #--------------------------------------------------------------
        #
        # Tonen van GIO-wijzigingen
        #
        #--------------------------------------------------------------
        if succes and len(toonWijzigingLijst) > 0:
            self.Generator.VoegHtmlToe ('<div class="sectie_toon_gio_wijziging"><h2>Toon GIO-wijziging</h2>')
            altDiv = 0
            for wijziging in toonWijzigingLijst:
                if altDiv == 0:
                    altDiv = 1
                else:
                    self.Generator.VoegHtmlToe ('</div><div class="sectie_toon_gio_wijziging_alt' + str(altDiv) + '">')
                    altDiv = 3 - altDiv

                request = Parameters (self.Log, {}, None, self.Request._Pad)
                request.KanBestandenSchrijven = False
                request._FormData["was"] = wijziging["was"]
                request._FormData["symbolisatie"] = __Waarde (wijziging, "symbolisatie")

                self.Log.Informatie ("Toon GIO-wijziging: '" + wijziging["wijziging"] + "'")
                uitvoerder = ToonGIOWijziging (request, self.Log)
                uitvoerder.IsVoortzettingVan (self)
                uitvoerder._Was = self._Geometrie.get (wijziging["was"])
                uitvoerder._Wijziging = wijziging["data"]

                succes = uitvoerder._VoerUit (wijziging["wijziging"])
                if not succes:
                    break

            self.Generator.VoegHtmlToe ('</div>')

        return succes
