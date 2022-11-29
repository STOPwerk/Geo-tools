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

import json
import os

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from maak_gio_wijziging import GIOWijzigingMaker
from weergave_webpagina import WebpaginaGenerator

class Voorbeeld (GIOWijzigingMaker):
#======================================================================
#
# Webpagina's
#
#======================================================================
    @staticmethod
    def SelectieHtml():
        lijst = None
        for idx, voorbeeldDir in enumerate (Voorbeeld._VoorbeeldenLijst ()):
            if lijst is None:
                lijst = '<ul>'
            lijst += '<li><a href="start_voorbeeld?index=' + str(idx) + '">' + voorbeeldDir.name + '</a> (<a href="@@@GeoTools_Url@@@tree/main/broncode/geo-tools/voorbeelden/' + voorbeeldDir.name + '">bronbestanden</a>)</li>'

        generator = WebpaginaGenerator ("Selecteer een voorbeeld")
        html = generator.LeesHtmlTemplate ('selectie', False)
        html = html.replace ('<!--LIJST-->', '(Geen voorbeelden beschikbaar op dit moment)' if lijst is None else lijst + '</ul>')
        generator.VoegHtmlToe (html)
        return generator.Html ()

    @staticmethod
    def VoerUit(request : Parameters):
        # Haal het voorbeeld op
        lijst = Voorbeeld._VoorbeeldenLijst ()
        idx = request.LeesString ("index")
        if idx is None or int(idx) < 0 or int(idx) >= len (lijst):
            generator = WebpaginaGenerator ("Voorbeeld onbekend")
            generator.VoegHtmlToe ('Het voorbeeld is niet bekend. Selecteer een <a href="voorbeeld">ander voorbeeld</a>.')
            return generator.Html ()
        voorbeeldNaam = lijst[int(idx)].name
        voorbeeldPad = lijst[int(idx)].path

        # Voer het voorbeeld uit
        log = Meldingen (True)
        try:
            log.Informatie ('Voer het voorbeeld "' + voorbeeldNaam + '" uit')
            uitTevoeren = Voorbeeld._MaakParameters (log, voorbeeldPad, voorbeeldNaam)
            if not uitTevoeren is None:
                # Voer het voorbeeld uit
                return GIOWijzigingMaker.ResultaatHtml (uitTevoeren, log)
        except Exception as e:
            log.Fout ("Oeps, deze fout is niet verwacht: " + str(e))

        # Als we hier komen is het voorbeeld niet goed
        generator = WebpaginaGenerator (voorbeeldNaam)
        generator.VoegHtmlToe ('<p>Dit is onze fout! Het voorbeeld kan niet uitgevoerd worden. Excuus daarvoor. Misschien is een <a href="voorbeeld">ander voorbeeld</a> ook interessant? Voor de goede orde volgt nog een verslag van de uitvoering van het lezen van het voorbeeld.</p>')
        log.MaakHtml (generator, None, "De uitvoering is afgebroken.")
        return generator.Html ()

#======================================================================
#
# Implementatie
#
#======================================================================
    @staticmethod
    def _VoorbeeldenLijst ():
        """Maak de lijst met voorbeelden"""
        voorbeeldenPad = os.path.join (os.path.dirname (os.path.abspath (__file__)), 'voorbeelden')
        return list (sorted ([f for f in os.scandir(voorbeeldenPad) if f.is_dir()], key=lambda f: f.name))

    @staticmethod
    def _MaakParameters (log : Meldingen, voorbeeldPad : str, voorbeeldNaam : str) -> Parameters:
        """Lees de specificaties van de voorbeelden"""
        parameters = Parameters ({ 'titel': voorbeeldNaam }, None, voorbeeldPad)
        parameters.KanBestandenSchrijven = False

        def __LeesSpecificatie (bestandsNaam, beschrijving):
            specificatiePad = os.path.join (voorbeeldPad, bestandsNaam)
            if not os.path.isfile (specificatiePad):
                log.Fout ('Geen specificatiebestand voor het ' + beschrijving)
                return None
            try:
                with open (specificatiePad, "r") as json_file:
                    data = json.load (json_file)
                if isinstance (data, dict):
                     return data
                log.Fout ('Kan specificatiebestand voor het ' + beschrijving + ' niet lezen (geen JSON object)')
            except Exception as e:
                log.Fout ('Kan specificatiebestand voor het ' + beschrijving + ' niet lezen: ' + str(e))

        specificatie = __LeesSpecificatie ('maak_gio_wijziging.json', 'maken van een GIO-wijziging')
        if specificatie is None:
            return
        parameters._FormData["was"] = specificatie.get ("was")
        parameters._FormData["wordt"] = specificatie.get ("wordt")
        parameters._FormData["persistente_id"] = specificatie.get ("persistente_id")
        parameters._FormData["nauwkeurigheid"] = specificatie.get ("nauwkeurigheid")

        specificatie = __LeesSpecificatie ('toon_gio_wijziging.json', 'tonen van een GIO-wijziging')
        if specificatie is None:
            return
        parameters._FormData["symbolisatie"] = specificatie.get ("symbolisatie")

        return parameters
