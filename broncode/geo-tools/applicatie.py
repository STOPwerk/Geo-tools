#======================================================================
#
# Startpunt van een applicatie om de Python scripts te testen
#
#----------------------------------------------------------------------
#
# De opgegeven directory en evt subdirectories worden nagelopen en
# overal waar een test.json gevonden wordt, wordt de test
# ingelezen en uitgevoerd. Subdirectories van mappen waar test.json
# in staat worden niet onderzocht.
#
#======================================================================

import getopt
import inspect
import json
import os.path
from pickle import NONE
import sys

#======================================================================
# Initialisatie van de applicatie.
#======================================================================
# Voeg het pad toe voor alle applicatie modules
script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append (script_dir)

helptekst = '''
applicatie_test.py [--help|-h] [--alle|-a] [--meldingen|-m meldingen_pad] directory_pad [directory_pad ..]

directory_pad     Pad naar een directory met een test waarvoor de applicatie uitgevoerd moet worden
-h of --help      Toon deze tekst
-a of --alle      Kijk ook in subdirectories voor testen
-t of --testen    De scenario's zijn unit testen. Sla resultaten op als json en vergelijk ze met de verwachte resultaten.
-m of --meldingen Bewaar de log van de uitvoering van de applicatie in de meldingen_pad directory, niet in de systeem-tempdirectory
'''
# De paden naar de directories
directory_paden = []
# Geeft aan of de specificaties test cases zijn
testen = False
# Geeft aan of de directory recursief doorzocht moet worden.
recursie = False
# Pad waar de meldingen terecht moeten komen; None is tempdir
meldingen_pad = None
try:
    (opts, args) = getopt.getopt(sys.argv[1:], "ahm:t", ["alle", "help", "meldingen=", "testen"])
except getopt.GetoptError:
    print (helptekst)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print (helptekst)
        sys.exit()
    elif opt in ('-t', '--testen'):
        testen = True
        recursie = True
    elif opt in ('-a', '--alle'):
        recursie = True
    elif opt in ('-m', '--meldingen'):
        meldingen_pad = arg
for arg in args:
    if not os.path.isdir (arg):
        print ("Geen directory: " + arg)
    else:
        directory_paden.append (arg)

if len(directory_paden) == 0:
    print (helptekst)
    sys.exit(2)

#======================================================================
# Uitvoeren van de applicatie.
#======================================================================
from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from weergave_webpagina import WebpaginaGenerator

from toon_geo import GeoViewer
from maak_gio_wijziging import GIOWijzigingMaker
from toon_gio_wijziging import GIOWijzigingViewer

log = Meldingen (True)

def __VoerTestUit (directory_pad, operatieNaam, methode):
    specificatiePad = os.path.join (directory_pad, operatieNaam + '.json')
    if os.path.exists (specificatiePad):
        # Potentiële test gevonden; lees specificatie
        try:
            with open (specificatiePad, 'r') as json_file:
                specificatie = json.load (json_file)
        except Exception as e:
            log.Fout ('Bestand "' + specificatiePad + '" is geen JSON bestand: ' + str(e))
            return
        if not isinstance (specificatie, dict):
            log.Fout ('Bestand "' + specificatiePad + '" is geen specificatie want de inhoud is geen JSON object')
            return

        # Voer de operatie uit
        log.Informatie ('Voer ' + operatieNaam + ' uit met specificatie "' + specificatiePad + '"')
        testlog = Meldingen (False) if testen else None
        actueelPad = os.path.join (directory_pad, operatieNaam + '_' + ('actueel' if testen else 'resultaat') + '.html')
        try:
            if os.path.isfile (actueelPad):
                os.remove (actueelPad)
        except Exception as e:
            log.Fout ('Kan voorgaand resultaat (' + actueelPad + ') niet weggooien: ' + str(e))
        try:
            actueel = methode (Parameters.Maak (specificatie, None, directory_pad), testlog)
        except Exception as e:
            log.Fout ('Oeps, dat ging niet goed: ' + str(e))
            if not testlog is None:
                testlog.Fout ('Oeps, dat ging niet goed: ' + str(e))
            actueel = None

        if actueel is None:
            log.Fout ('Uitvoering faalt: geen webpagina geproduceerd')
            if not testlog is None:
                testlog.Fout ('Uitvoering faalt: geen webpagina geproduceerd')
        else:
            try:
                if not testen or not testlog.HeeftFouten ():
                    with open (actueelPad, 'w', encoding='utf-8') as html_file:
                        html_file.write (actueel)
                    if testen:
                        verwachtPad = os.path.join (directory_pad, operatieNaam + '_verwacht.html')
                        if os.path.isfile (verwachtPad):
                            with open (verwachtPad, 'r', encoding='utf-8') as html_file:
                                verwacht = html_file.read ()
                            if len (verwacht.strip ()) == 0:
                                log.Informatie ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueelPad) + '" target="_blank">Actuele</a> uitkomst voor test "' + directory_pad + '"')
                            elif actueel == verwacht:
                                log.Informatie ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueelPad) + '" target="_blank">Actuele</a> en verwachte uitkomst zijn gelijk voor test "' + directory_pad + '"')
                            else:
                                log.Fout ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueelPad) + '" target="_blank">Actuele</a> en <a href="' + WebpaginaGenerator.UrlVoorPad (verwachtPad) + '" target="_blank">verwachte</a> uitkomst verschillen voor test "' + directory_pad + '"')
                        else:
                            log.Waarschuwing ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueelPad) + '" target="_blank">Actuele</a> maar geen verwachte uitkomst voor test "' + directory_pad + '"')
                    else:
                        log.Informatie ('Uitvoering geslaagd; zie <a href="' + WebpaginaGenerator.UrlVoorPad (actueelPad) + '" target="_blank">resultaat</a>')

            except Exception as e:
                log.Fout ('Oeps, resultaatafhandeling ging niet goed: ' + str(e))

        if testen:
            try:
                # Vergelijk de fouten/waarschuwingen met de verwachte fouten/waarschuwingen
                actueelLogPad = os.path.join (directory_pad, operatieNaam + '_log_actueel.json')
                with open (actueelLogPad, 'w', encoding='utf-8') as json_file:
                     json_file.write (json.dumps (testlog.FoutenWaarschuwingen (), indent=4, cls=JsonClassEncoder, ensure_ascii=False))
                verwachtLogPad = os.path.join (directory_pad, operatieNaam + '_log_verwacht.json')
                if os.path.isfile (verwachtLogPad):
                    with open (verwachtLogPad, 'r', encoding='utf-8') as json_file:
                        verwachteLog = json_file.read ().strip ()
                    if len (verwachteLog) == 0:
                        log.Informatie ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueelLogPad) + '" target="_blank">Actuele</a> meldingen voor test "' + directory_pad + '"')
                    else:
                        verwachteLog = json.dumps (json.loads (verwachteLog), indent=4, cls=JsonClassEncoder, ensure_ascii=False)
                        with open (actueelLogPad, 'r', encoding='utf-8') as json_file:
                            actueleLog = json_file.read ()
                        if actueleLog == verwachteLog:
                            log.Informatie ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueelLogPad) + '" target="_blank">Actuele</a> en verwachte meldingen zijn gelijk voor test "' + directory_pad + '"')
                        else:
                            log.Fout ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueelLogPad) + '" target="_blank">Actuele</a> en <a href="' + WebpaginaGenerator.UrlVoorPad (verwachtLogPad) + '" target="_blank">verwachte</a> meldingen verschillen voor test "' + directory_pad + '"')
                else:
                    log.Waarschuwing ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueelLogPad) + '" target="_blank">Actuele</a> maar geen verwachte meldingen voor test "' + directory_pad + '"')
            except Exception as e:
                log.Fout ('Oeps, vergelijken van meldingen ging niet goed: ' + str(e))

    else:
        log.Detail ('Geen ' + operatieNaam + '.json gevonden in: "' + directory_pad + '"')
        if recursie:
            # Kijk in subdirectories
            for dir in os.scandir(directory_pad):
                if dir.is_dir():
                    __VoerTestUit (dir.path, operatieNaam, methode)

class JsonClassEncoder(json.JSONEncoder):

    def default(self, o):
        """Overschrijft standaard serialisatie van objecten"""
        data = {}
        for key in sorted (o.__dict__.keys()): # Sorteer zodat de JSON er hetzelfde uitziet ongeacht implementatie
            if key[0:1] == '_':
                continue
            value = o.__dict__[key]
            if value is None:
                continue
            data[key] = value
        return data


for directory_pad in directory_paden:
    __VoerTestUit (directory_pad, 'toon_geo', GeoViewer.ResultaatHtml)
    __VoerTestUit (directory_pad, 'maak_gio_wijziging', GIOWijzigingMaker.ResultaatHtml)
    __VoerTestUit (directory_pad, 'toon_gio_wijziging', GIOWijzigingViewer.ResultaatHtml)

log.ToonHtml (meldingen_pad)
