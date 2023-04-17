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
testscenario_dir = os.path.join (datadir, "..", "..", "..", "docs", "01 Demo - GIO-wijziging en geo-renvooi", "STOP borden")

normwaarde = lambda jaar: 2024 if jaar < 2004 else jaar + 20

with open (os.path.join (datadir, 'verkeersborden_STOP.json'), 'r') as json_file:
    data = json.load (json_file)

borden = [{
            "id": idx,
            "x": pt["location"]["rd"]["x"],
            "y": pt["location"]["rd"]["y"],
            "jaar": int(pt["details"]["first_seen"][6:10])
          } 
          for idx, pt in enumerate (data)]

wasFilter = lambda j: j != 2015
wordtFilter = lambda j: True

numInBeide = 0
distributie = {}
for bord in borden:
    waarde = normwaarde (bord['jaar'])
    distributie[waarde] = 1 if distributie.get (waarde) is None else distributie[waarde] + 1
    if wasFilter (bord['jaar']):
        bord['was'] = waarde
        if wordtFilter (bord['jaar']):
            numInBeide += 1
            if numInBeide % 100 == 0:
                waarde += 1
            bord['wordt'] = waarde
    elif wordtFilter (bord['jaar']):
        bord['wordt'] = waarde

symbolisatie = Symbolisatie (os.path.join (datadir, 'verkeersborden_puntsymbolen.json'))

#==============================================================================
#
# Schrijf GIO's
#
#==============================================================================

def __GIO (versie, waardeVeld):
    gioPad = os.path.join (testscenario_dir, 'stopborden_' + versie + '.gml')
    os.makedirs (os.path.dirname (gioPad), exist_ok=True)
    with open (gioPad, 'w', encoding='utf-8') as gml_file:
        gml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<geo:GeoInformatieObjectVersie schemaversie="1.3.0"
      xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
      xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
      xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/"
      xmlns:gml="http://www.opengis.net/gml/3.2">
    <geo:FRBRWork>/join/id/regdata/mnre1034/2022/stopborden</geo:FRBRWork>
    <geo:FRBRExpression>/join/id/regdata/mnre1034/2022/stopborden/nld@''' + versie + '''</geo:FRBRExpression>
    <geo:normlabel>Te vervangen voor</geo:normlabel>
    <geo:locaties>''')

        for bord in borden:
            if waardeVeld in bord:
                gml_file.write ('''
        <geo:Locatie>
            <geo:geometrie>
                <basisgeo:Geometrie>
                    <basisgeo:id>37b0a09f-36a0-4e69-80c0-''' + str(bord['id']).zfill(12) + '''</basisgeo:id>
                    <basisgeo:geometrie>
                        <gml:Point srsName="urn:ogc:def:crs:EPSG::28992">
                            <gml:pos>''' + bord['x'] + ' ' + bord['y'] + '''</gml:pos>
                        </gml:Point>
                    </basisgeo:geometrie>
                </basisgeo:Geometrie>
            </geo:geometrie>
            <geo:kwantitatieveNormwaarde>''' + str(bord[waardeVeld]) + '''</geo:kwantitatieveNormwaarde>
        </geo:Locatie>''')

        gml_file.write ('''
    </geo:locaties>
</geo:GeoInformatieObjectVersie>
    ''')

__GIO ('1', 'was')
__GIO ('2', 'wordt')


#==============================================================================
#
# Symbolisatie
#
#==============================================================================

alleNormwaarden = set (bord['was'] for bord in borden if 'was' in bord).union (bord['wordt'] for bord in borden if 'wordt' in bord)
symbolisatie.MaakSymbolisatie (os.path.join (testscenario_dir,'stopborden_symbolisatie.xml'), 'kwantitatieveNormwaarde', { str(r): str(r) for r in sorted (alleNormwaarden) })
