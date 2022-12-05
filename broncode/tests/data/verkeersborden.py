#==============================================================================
#
# Omzetting van punt-data naar GIO's en symbolisatie voor testen en voorbeelden
#
# Bron: https://data.ndw.nu/api/rest/static-road-data/traffic-signs/v1/current-state?rvv_code=B07
# Opgehaald op 17-11-2022
#
# STOP-borden in Nederland
#
# Symbolen uit de STOP-TPOD symbolenbibliotheek
#
#==============================================================================
import json
import os

from symbolisatie import Symbolisatie

#==============================================================================
#
# Initialisatie van alle data
#
#==============================================================================
datadir = os.path.dirname (os.path.realpath (__file__))
voorbeelden_dir = os.path.join (datadir, "..", "..", "geo-tools", "voorbeelden")

with open (os.path.join (datadir, 'verkeersborden_STOP.json'), 'r') as json_file:
    data = json.load (json_file)

borden = [{
            "x": pt["location"]["rd"]["x"],
            "y": pt["location"]["rd"]["y"],
            "gemeente": pt["location"]["county"]["code"],
            "jaar": int(pt["details"]["first_seen"][6:10])
          } 
          for pt in data]

gio_delen = ['Standaardbeheer', 'Gemeentelijk beheer', 'Centraal beheer', 'Tijdelijk beheer', 'Decentraal beheer']
gemeenteIndex = { g: i % 10 for i, g in enumerate (sorted (list(set (b["gemeente"] for b in borden))))}
gemeenteFilter = [lambda idx: None, lambda idx: None if idx == 0 else 4-idx if idx in [1,3] else 9-idx if idx in [6,8] else idx % 5, lambda idx: None if idx == 9 else idx % 5]

levensduur = 100
jaren = list (sorted (list(set (b["jaar"] for b in borden))))

wasFilter = lambda j: j <= 2019
wordtFilter = lambda j: j <= 2016 or j >= 2020

symbolisatie = Symbolisatie (os.path.join (datadir, 'verkeersborden_puntsymbolen.json'))

#==============================================================================
#
# Schrijf GIO's
#
#==============================================================================
def __GIO (subdir, multi, gemeente, jaar, beschrijving, filename, version, filter, idprefix = '0'):
    gioPad = os.path.join (voorbeelden_dir, subdir, filename)
    os.makedirs (os.path.dirname (gioPad), exist_ok=True)
    with open (gioPad, 'w', encoding='utf-8') as gml_file:
        gml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<geo:GeoInformatieObjectVersie schemaversie="1.3.0"
      xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
      xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
      xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/"
      xmlns:gml="http://www.opengis.net/gml/3.2">
    <geo:FRBRWork>/join/id/regdata/mnre9999/2022/stopborden</geo:FRBRWork>
    <geo:FRBRExpression>/join/id/regdata/mnre9999/2022/stopborden/nld@''' + version + '''</geo:FRBRExpression>''')

        symbolisatie.StartGio (gioPad, 'groepID' if gemeente > 0 else 'kwantitatieveNormwaarde' if jaar else None, beschrijving)

        if gemeente > 0:
            gml_file.write ('''
    <geo:groepen>''')
            for i in range (0, len (gio_delen)):
                if not gemeenteFilter[gemeente](i) is None:
                    gml_file.write ('''
        <geo:Groep>
            <geo:groepID>g''' + str(i+1) + '''</geo:groepID>
            <geo:label>''' + gio_delen[i] + '''</geo:label>
        </geo:Groep>''')
            gml_file.write ('''
    </geo:groepen>''')

        if jaar:
            gml_file.write ('''
    <geo:normlabel>Te vervangen voor</geo:normlabel>''')

        gml_file.write ('''
    <geo:locaties>''')
        def __Locatie (index, borden, gemeenteIdx, jaar):
            if len(borden) == 0:
                return
            gml_file.write ('''
            <geo:Locatie>
                <geo:geometrie>
                    <basisgeo:Geometrie>
                        <basisgeo:id>37b0a09f-36a0-4e69-80c0-''' + idprefix + str(index).zfill(11) + '''</basisgeo:id>
                        <basisgeo:geometrie>''')
            if len(borden) == 1:
                gml_file.write ('''
                            <gml:Point srsName="urn:ogc:def:crs:EPSG::28992">
                                <gml:pos>''' + borden[0]['x'] + ' ' + borden[0]['y'] + '''</gml:pos>
                            </gml:Point>''')
            else:
                gml_file.write ('''
                            <gml:MultiPoint srsName="urn:ogc:def:crs:EPSG::28992">
                                <gml:pointMembers>''')
                for b in borden:
                    gml_file.write ('''
                                    <gml:Point>
                                        <gml:pos>''' + b['x'] + ' ' + b['y'] + '''</gml:pos>
                                    </gml:Point>''')
                gml_file.write ('''
                                </gml:pointMembers>
                            </gml:MultiPoint>''')
            gml_file.write ('''
                        </basisgeo:geometrie>
                    </basisgeo:Geometrie>
                </geo:geometrie>''')
            if not gemeenteIdx is None:
                gml_file.write (symbolisatie.GIOWaarde ('g' + str (gemeenteIdx+1)))
            elif jaar:
                gml_file.write (symbolisatie.GIOWaarde (borden[0]['jaar'] + levensduur))
            gml_file.write ('''
            </geo:Locatie>''')


        index = 0
        if multi:
            if gemeente == 0 and not jaar:
                __Locatie (1, [b for b in borden if filter(b["jaar"])], None, False)
            else:
                for g, idx in gemeenteIndex.items ():
                    if jaar:
                        for j in jaren:
                            index += 1
                            if filter(j):
                                __Locatie (index, [b for b in borden if b["gemeente"] == g and b["jaar"] == j], None, jaar)
                    else:
                        index += 1
                        gemeenteIdx = None
                        if gemeente:
                            gemeenteIdx = gemeenteFilter[gemeente](idx)
                            if gemeenteIdx is None:
                                continue
                        __Locatie (index, [b for b in borden if b["gemeente"] == g and filter(b["jaar"])], gemeenteIdx, False)
        else:
            for b in borden:
                index += 1
                idx = gemeenteFilter[gemeente](gemeenteIndex[b["gemeente"]])
                if filter(b["jaar"]) and (gemeente == 0 or not idx is None):
                    __Locatie (index, [b], idx, jaar)

        gml_file.write ('''
    </geo:locaties>
</geo:GeoInformatieObjectVersie>
    ''')

__GIO ('07 punten - geometrie', False, 0, False, 'Originele versie van de GIO met alleen geometrie. Elk punt is een aparte GIO-Locatie.', 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('07 punten - geometrie', False, 0, False, 'Nieuwe versie van de GIO met alleen geometrie. Elk punt is een aparte GIO-Locatie.', 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('07 punten - multi-geometrie', True, 0, False, 'Originele versie van de GIO met alleen geometrie. Alle punt zijn ondergebracht in een enkele GIO-Locatie.', 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('07 punten - multi-geometrie', True, 0, False, 'Nieuwe versie van de GIO met alleen geometrie. Alle punten zijn ondergebracht in een enkele GIO-Locatie.', 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('07 punten - geometrie - nieuwe id', False, 0, False, 'Originele versie van de GIO met alleen geometrie. Elk punt is een aparte GIO-Locatie.', 'verkeersborden_STOP_was.gml', '2019;was', wasFilter, '1')
__GIO ('07 punten - geometrie - nieuwe id', False, 0, False, 'Nieuwe versie van de GIO met alleen geometrie. Elk punt is een aparte GIO-Locatie met een nieuwe basisgeo-ID die verschilt van de originele GIO, ook al is de locatie van het punt niet gewijzigd.', 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter, '2')

__GIO ('08 punten - GIO-delen', False, 1, False, 'Originele versie van de GIO met GIO-delen. Elk punt is een aparte GIO-Locatie.', 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('08 punten - GIO-delen', False, 2, False, 'Nieuwe versie van de GIO met GIO-delen. Elk punt is een aparte GIO-Locatie.', 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('08 punten - GIO-delen - multi-geometrie', True, 1, False, 'Originele versie van de GIO met GIO-delen. Elk GIO-deel is een aparte GIO-Locatie met één of meer punten.', 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('08 punten - GIO-delen - multi-geometrie', True, 2, False, 'Nieuwe versie van de GIO met GIO-delen. Elk GIO-deel is een aparte GIO-Locatie met één of meer punten.', 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('08 punten - GIO-delen - nieuwe id', False, 1, False, 'Originele versie van de GIO met GIO-delen. Elk punt is een aparte GIO-Locatie.', 'verkeersborden_STOP_was.gml', '2019;was', wasFilter, '1')
__GIO ('08 punten - GIO-delen - nieuwe id', False, 2, False, 'Nieuwe versie van de GIO met GIO-delen. Elk punt is een aparte GIO-Locatie met een nieuwe basisgeo-ID die verschilt van de originele GIO, ook al is de locatie van het punt niet gewijzigd.', 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter, '2')

__GIO ('09 punten - normwaarden', False, 0, True, 'Originele versie van de GIO met normwaarden. Elk punt is een aparte GIO-Locatie.', 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('09 punten - normwaarden', False, 0, True, 'Nieuwe versie van de GIO met normwaarden. Elk punt is een aparte GIO-Locatie.', 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('09 punten-multi - normwaarden', True, 0, True, 'Originele versie van de GIO met normwaarden. De punten zijn per normwaarde gecombineerd in één GIO-Locatie met één of meer punten.', 'verkeersborden_STOP_was', '2019;was', wasFilter)
__GIO ('09 punten-multi - normwaarden', True, 0, True, 'Nieuwe versie van de GIO met normwaarden. De punten zijn per normwaarde gecombineerd in één GIO-Locatie met één of meer punten.', 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('09 punten-multi - normwaarden - nieuwe id', False, 0, True, 'Originele versie van de GIO met normwaarden. Elk punt is een aparte GIO-Locatie.', 'verkeersborden_STOP_was.gml', '2019;was', wasFilter, '1')
__GIO ('09 punten-multi - normwaarden - nieuwe id', False, 0, True, 'Nieuwe versie van de GIO met normwaarden. Elk punt is een aparte GIO-Locatie met een nieuwe basisgeo-ID die verschilt van de originele GIO, ook al is de locatie van het punt niet gewijzigd.', 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter, '2')

#==============================================================================
#
# Symbolisaties en specificaties
#
#==============================================================================
symbolisatie.MaakSymbolisaties ('verkeersborden_STOP_was_wordt_symbolisatie.xml')

symbolisatie.MaakToonGeoSpecificaties (10)

for mapPad in symbolisatie.GIOMappen ():
    with open (os.path.join (mapPad, 'maak_gio_wijziging.json'), 'w', encoding='utf-8') as json_file:
        json.dump ({
            'was': 'verkeersborden_STOP_was.gml', 
            'wordt': 'verkeersborden_STOP_was.gml', 
            'nauwkeurigheid': '10',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad),
            'wijziging': 'verkeersborden_STOP_was_wordt.gml'
        }, json_file)
    with open (os.path.join (mapPad, 'toon_gio_wijziging.json'), 'w', encoding='utf-8') as json_file:
        json.dump ({
            'was': 'verkeersborden_STOP_was.gml', 
            'wijziging': 'verkeersborden_STOP_was_wordt.gml',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad)
        }, json_file)
