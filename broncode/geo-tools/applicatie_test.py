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
-m of --meldingen Bewaar de log van de uitvoering van de applicatie in de meldingen_pad directory, niet in de systeem-tempdirectory
'''
# De paden naar de directories
directory_paden = []
# Geeft aan of de directory recursief doorzocht moet worden.
recursie = False
# Pad waar de meldingen terecht moeten komen; None is tempdir
meldingen_pad = None
try:
    (opts, args) = getopt.getopt(sys.argv[1:], "ahm:", ["alle", "help", "meldingen="])
except getopt.GetoptError:
    print (helptekst)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print (helptekst)
        sys.exit()
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

from gio_wijziging_maker import GIOWijzigingMaker

log = Meldingen (True)

testrunner = {
    'gio_wijziging_maker': GIOWijzigingMaker.ResultaatHtml
}

def __VoerTestUit (directory_pad):
    testSpec = os.path.join (directory_pad, 'test.json')
    if os.path.exists (testSpec):
        # Potentiële test gevonden
        try:
            with open (testSpec, 'r') as json_file:
                spec = json.load (json_file)
        except Exception as e:
            log.Fout ('Bestand "' + testSpec + '" is geen JSON bestand: ' + str(e))
            return
        if not isinstance (spec, dict):
            log.Fout ('Bestand "' + testSpec + '" is geen test specificatie want de inhoud is geen JSON object')
        elif not "test" in spec or not isinstance (spec["test"], str):
            log.Fout ('Bestand "' + testSpec + '" is geen test specificatie want het JSON object bevat geen "test" met een string waarde')

        else:
            methode = testrunner.get (spec["test"])
            if methode is None:
                log.Waarschuwing ('Bestand "' + testSpec + '" is voor een onbekende test "' + spec["test"] + '"')
            else:
                log.Informatie ('Test ' + spec["test"] + ' met specificatie "' + testSpec + '"')
                try:
                    html = methode (Parameters (spec, None, directory_pad))
                except Exception as e:
                    log.Fout ('Oeps, dat ging niet goed: ' + str(e))
                    html = None
                if html is None:
                    log.Fout ('Test faalt: geen webpagina geproduceerd')
                else:
                    try:
                        actueel = os.path.join (directory_pad, 'test_actueel.html')
                        with open (actueel, 'w', encoding='utf-8') as html_file:
                            html_file.write (html)
                        verwacht = os.path.join (directory_pad, 'test_verwacht.html')
                        if os.path.isfile (verwacht):
                            with open (verwacht, 'w', encoding='utf-8') as html_file:
                                verwachtHtml = html_file.read ()
                            if html == verwachtHtml:
                                log.Informatie ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueel) + '" target="_blank">Actuele</a> en verwachte uitkomst zijn gelijk voor test "' + directory_pad + '"')
                            else:
                                log.Informatie ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueel) + '" target="_blank">Actuele</a> en <a href="' + WebpaginaGenerator.UrlVoorPad (verwacht) + '" target="_blank">verwachte</a> uitkomst verschillen voor test "' + directory_pad + '"')
                        else:
                            log.Waarschuwing ('<a href="' + WebpaginaGenerator.UrlVoorPad (actueel) + '" target="_blank">Actuele</a> maar geen verwachte uitkomst voor test "' + directory_pad + '"')

                    except Exception as e:
                        log.Fout ('Oeps, resultaatafhandeling ging niet goed: ' + str(e))

    else:
        log.Detail ('Geen test.json gevonden in: "' + directory_pad + '"')
        if recursie:
            # Kijk in subdirectories
            for dir in os.scandir(directory_pad):
                if dir.is_dir():
                    __VoerTestUit (dir.path)


for directory_pad in directory_paden:
    __VoerTestUit (directory_pad)

log.ToonHtml (meldingen_pad)
