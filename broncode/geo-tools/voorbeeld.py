#======================================================================
#
# /voorbeeld
#
#======================================================================
#
# Script om een voorbeeld te selecteren en daarvoor de GIO-wijziging
# te maken en te tonen.
#
#======================================================================

from typing import List

import json
import os

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from gio_wijziging import GIOWijziging
from maak_gio_wijziging import GIOWijzigingMaker
from toon_geo import GeoViewer
from toon_gio_wijziging import GIOWijzigingViewer
from weergave_webpagina import WebpaginaGenerator

class Voorbeeld (GIOWijzigingMaker):
#======================================================================
#
# Webpagina's
#
#======================================================================
    @staticmethod
    def SelectieHtml():
        lijst = Voorbeeld._VoorbeeldenLijst ().Html ()

        generator = WebpaginaGenerator ("Selecteer een voorbeeld")
        html = generator.LeesHtmlTemplate ('selectie', False)
        html = html.replace ('<!--LIJST-->', '(Geen voorbeelden beschikbaar op dit moment)' if lijst == '' else lijst)
        generator.VoegHtmlToe (html)
        return generator.Html ()

    @staticmethod
    def VoerUit(request : Parameters):
        # Haal het voorbeeld op
        lijst = Voorbeeld._VoorbeeldenLijst ()
        idx = int (request.LeesString ("index"))
        if idx is None or int(idx) < 0 or int(idx) >= len (lijst.AlleSpecificaties):
            generator = WebpaginaGenerator ("Voorbeeld onbekend")
            generator.VoegHtmlToe ('Het voorbeeld is niet bekend. Selecteer een <a href="voorbeeld">ander voorbeeld</a>.')
            return generator.Html ()

        specificatie = lijst.AlleSpecificaties[idx]

        log = Meldingen (True)
        try:
            log.Detail ('Is het resultaat van het voorbeeld "' + specificatie.Titel + '" beschikbaar?')
            resultaatPagina = os.path.splitext (specificatie.Pad)[0] + "_resultaat.html"
            if os.path.isfile (resultaatPagina):
                # Toon de pagina die voorberekend is
                with open (resultaatPagina, 'r') as html_file:
                    return html_file.read ()

            # Voer het voorbeeld uit
            request = Parameters.Lees (log, specificatie.Pad)
            if not request is None:
                log.Informatie ('Voer het voorbeeld "' + specificatie.Titel + '" uit')
                return specificatie.VoerUit (request, log)

        except Exception as e:
            log.Fout ("Oeps, deze fout is niet verwacht: " + str(e))

        # Als we hier komen is het voorbeeld niet goed
        generator = WebpaginaGenerator ('Voorbeeld #' + str (idx))
        generator.VoegHtmlToe ('<p>Dit is onze fout! Het voorbeeld kan niet uitgevoerd worden. Excuus daarvoor. Misschien is een <a href="voorbeeld">ander voorbeeld</a> ook interessant? Voor de goede orde volgt nog een verslag van de uitvoering van het lezen van het voorbeeld.</p>')
        log.MaakHtml (generator, None, "De uitvoering is afgebroken.")
        return generator.Html ()

#======================================================================
#
# Implementatie
#
#======================================================================
    class VoorbeeldSpecificatie:
        def __init__ (self, specFilePath, volgorde, titel, uitvoering, index):
            self.Pad = specFilePath
            self.Titel = titel
            self.Index = index
            self.Volgorde = volgorde
            self.VoerUit = uitvoering

        def Html (self):
            return '<a href="start_voorbeeld?index=' + str(self.Index) + '">' + self.Titel + '</a>'

    class VoorbeeldDirectory:
        def __init__ (self, path, name, top):
            self.Pad = path
            self.Naam = None if top is None else name
            self.BronUrl = '@@@GeoTools_Url@@@tree/main/broncode/geo-tools/voorbeelden' if top is None else top.BronUrl + '/' + name
            self.IsDataBron = False # Bevat data bestanden, is eerste niveau directory
            self.Voorbeelden = []
            self.Specificaties : List[Voorbeeld.VoorbeeldSpecificatie] = []
            self.AlleSpecificaties : List[Voorbeeld.VoorbeeldSpecificatie] = []
            for fd in sorted (os.scandir(self.Pad), key=lambda f: f.name):
                if fd.is_dir ():
                    vb = Voorbeeld.VoorbeeldDirectory (fd.path, fd.name, self if top is None else top)
                    self.Voorbeelden.append (vb)
                    if top is None:
                        vb.IsDataBron = True
                elif not top is None and fd.is_file ():
                    maker = Voorbeeld.VoorbeeldDirectory._Specs.get (fd.name)
                    if not maker is None:
                        spec = Voorbeeld.VoorbeeldSpecificatie (fd.path, maker[0], maker[1], maker[2], len (top.AlleSpecificaties))
                        top.AlleSpecificaties.append (spec)
                        self.Specificaties.append (spec)

        _Specs = {
                'gio_wijziging.json' : (1, "Toon de GIO;s, maak en toon de GIO-wijziging(en)", GIOWijziging.ResultaatHtml),
                'toon_geo.json' : (2, 'Toon de GIO', GeoViewer.ResultaatHtml), 
                'maak_gio_wijziging.json' : (3, 'Maak de GIO-wijziging', GIOWijzigingMaker.ResultaatHtml), 
                'toon_gio_wijziging.json' : (4, 'Toon de GIO-wijziging', GIOWijzigingViewer.ResultaatHtml)
            } 

        def Html (self):
            html = ''
            if not self.Naam is None:
                html += '<li>'
                if len (self.Specificaties) == 1:
                    html += '<a href="start_voorbeeld?index=' + str(self.Specificaties[0].Index) + '">' + self.Naam + '</a>'
                else:
                    html += self.Naam
                if self.IsDataBron:
                    html += ' (zie <a href="' + self.BronUrl + '">bronbestanden</a> voor een beschrijving)'
            if len (self.Voorbeelden) > 0:
                html += '<ul>'
                for sp in self.Voorbeelden:
                    html += sp.Html ()
                html += '</ul>'
            if len (self.Specificaties) > 1:
                html += ': ' + ', '.join (sp.Html () for sp in sorted (self.Specificaties, key = lambda s: s.Volgorde))
            if not self.Naam is None:
                html += '</li>'
            return html

    @staticmethod
    def _VoorbeeldenLijst () -> VoorbeeldDirectory:
        """Maak de lijst met voorbeelden"""
        voorbeeldenPad = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'voorbeelden')
        return Voorbeeld.VoorbeeldDirectory(voorbeeldenPad, None, None)

