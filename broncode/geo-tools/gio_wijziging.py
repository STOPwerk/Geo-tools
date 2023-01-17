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
        # Naam waaronder de te gebruiken symbolisatie is geregistreerd
        self._SymbolisatieNaam : Dict[str,str] = {}

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
            return x if not x is None and x else None

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

                request = Parameters ({}, None, self.Request._Pad)
                request.KanBestandenSchrijven = False
                request._FormData["geometrie"] = gio["pad"]
                request._FormData["beschrijving"] = gio.get ("beschrijving")
                symbolisatie = __Waarde (gio, "symbolisatie")
                request._FormData["symbolisatie"] = symbolisatie
                request._FormData["teken-nauwkeurigheid"] = __Waarde (gio, "teken-nauwkeurigheid")

                self.Log.Informatie ("Toon GIO: '" + gio["pad"] + "'")
                uitvoerder = GeoViewer (request, self.Log)
                uitvoerder._GebruikCache (self._Cache)
                uitvoerder._Geometrie = self._Geometrie.get (gio["pad"])
                if not symbolisatie is None:
                    uitvoerder._SymbolisatieNaam = self._SymbolisatieNaam.get (symbolisatie)

                einde = self.Generator.StartSectie ("<h3>" + request.Bestandsnaam ('geometrie', False) + "</h3>", True)
                succes = uitvoerder._VoerUit ()
                self.Generator.VoegHtmlToe (einde)
                if not succes:
                    break

                self._Geometrie[gio["pad"]] = uitvoerder._Geometrie
                if not symbolisatie is None:
                    self._SymbolisatieNaam[symbolisatie] = uitvoerder._SymbolisatieNaam

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

                request = Parameters ({}, None, self.Request._Pad)
                request.KanBestandenSchrijven = False
                request._FormData["was"] = wijziging["was"]
                request._FormData["wordt"] = wijziging["wordt"]
                request._FormData["beschrijving"] = wijziging.get ("beschrijving")
                symbolisatie = __Waarde (gio, "symbolisatie")
                request._FormData["symbolisatie"] = symbolisatie
                request._FormData["teken-nauwkeurigheid"] = __Waarde (wijziging, "teken-nauwkeurigheid")

                self.Log.Informatie ("Maak GIO-wijziging: '" + wijziging["was"] + "' &rarr; '" + wijziging["was"] + "'")
                uitvoerder = GIOWijzigingMaker (request, self.Log)
                uitvoerder._GebruikCache (self._Cache)
                uitvoerder._Was = self._Geometrie.get (wijziging["was"])
                uitvoerder._Wordt = self._Geometrie.get (wijziging["wordt"])
                if not symbolisatie is None:
                    uitvoerder._SymbolisatieNaam = self._SymbolisatieNaam.get (symbolisatie)

                wijziging["wijziging"] = request.Bestandsnaam ('was', False) + ' &rarr; ' + request.Bestandsnaam ('wordt', False)
                succes = uitvoerder._VoerUit (wijziging["wijziging"])
                if not succes:
                    break

                self._Geometrie[wijziging["was"]] = uitvoerder._Was
                if not symbolisatie is None:
                    self._SymbolisatieNaam[symbolisatie] = uitvoerder._SymbolisatieNaam
                request._FormData["toon"] = wijziging.get ("toon")
                if not uitvoerder._Wijziging is None and request.LeesString ("toon", True) != 'false':
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

                request = Parameters ({}, None, self.Request._Pad)
                request.KanBestandenSchrijven = False
                request._FormData["was"] = wijziging["was"]
                symbolisatie = __Waarde (gio, "symbolisatie")
                request._FormData["symbolisatie"] = symbolisatie

                self.Log.Informatie ("Toon GIO-wijziging: '" + wijziging["wijziging"] + "'")
                uitvoerder = GIOWijzigingViewer (request, self.Log)
                uitvoerder._GebruikCache (self._Cache)
                uitvoerder._Was = self._Geometrie.get (wijziging["was"])
                uitvoerder._Wijziging = wijziging["data"]
                if not symbolisatie is None:
                    uitvoerder._SymbolisatieNaam = self._SymbolisatieNaam.get (symbolisatie)

                succes = uitvoerder._VoerUit (wijziging["wijziging"])
                if not succes:
                    break

                if not symbolisatie is None:
                    self._SymbolisatieNaam[symbolisatie] = uitvoerder._SymbolisatieNaam

            self.Generator.VoegHtmlToe ('</div>')

        return succes
