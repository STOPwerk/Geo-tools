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

#==============================================================================
#
# Initialisatie van alle data
#
#==============================================================================
datadir = os.path.dirname (os.path.realpath (__file__))
voorbeelden_dir = os.path.join (datadir, "..", "..", "..", "..", "voorbeelden", "punten")

with open (os.path.join (datadir, 'verkeersborden_STOP.json'), 'r') as json_file:
    data = json.load (json_file)

borden = [{
            "x": pt["location"]["rd"]["x"],
            "y": pt["location"]["rd"]["y"],
            "gemeente": pt["location"]["county"]["code"],
            "jaar": int(pt["details"]["first_seen"][6:10])
          } 
          for pt in data]

gemeenten = { i: g for i, g in enumerate (sorted (list(set (b["gemeente"] for b in borden))))}
gemeenteIndex = {g: str(i) for i, g in gemeenten.items ()}

levensduur = 100
jaren = list (sorted (list(set (b["jaar"] for b in borden))))

wasFilter = lambda j: j <= 2019
wordtFilter = lambda j: j <= 2016 or j >= 2020

with open (os.path.join (datadir, 'puntsymbolen.json'), 'r') as json_file:
    symbolen = json.load (json_file)
symbolen = [s["symbol"] for s in sorted (symbolen, key = lambda s: s["code"])]

#==============================================================================
#
# Schrijf GIO's
#
#==============================================================================
def __GIO (subdir, gemeente, jaar, filename, version, filter):
    os.makedirs (os.path.join (voorbeelden_dir, subdir), exist_ok=True)
    with open (os.path.join (voorbeelden_dir, subdir, filename), 'w') as gml_file:
        gml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<geo:GeoInformatieObjectVersie schemaversie="1.3.0"
      xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
      xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
      xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/"
      xmlns:gml="http://www.opengis.net/gml/3.2">
    <geo:FRBRWork>/join/id/regdata/mnre9999/2022/stopborden</geo:FRBRWork>
    <geo:FRBRExpression>/join/id/regdata/mnre9999/2022/stopborden/nld@''' + version + '''</geo:FRBRExpression>''')

        if gemeente:
            gml_file.write ('''
    <geo:groepen>''')
            for i in sorted (gemeenten.keys ()):
                gml_file.write ('''
        <geo:Groep>
            <geo:groepID>g''' + str(i) + '''</geo:groepID>
            <geo:label>''' + gemeenten[i] + '''</geo:label>
        </geo:Groep>''')
            gml_file.write ('''
    </geo:groepen>''')

        if jaar:
            gml_file.write ('''
    <geo:eenheidlabel>Jaar</geo:eenheidlabel>
    <geo:normlabel>Te vervangen voor</geo:normlabel>''')

        gml_file.write ('''
    <geo:locaties>''')
        index = 0
        for b in borden:
            index += 1
            if filter(b["jaar"]):
                gml_file.write ('''
        <geo:Locatie>
            <geo:geometrie>
                <basisgeo:Geometrie>
                    <basisgeo:id>37b0a09f-36a0-4e69-80c1-''' + str(index).zfill(12) + '''</basisgeo:id>
                    <basisgeo:geometrie>
                        <gml:Point srsName="urn:ogc:def:crs:EPSG::28992">
                            <gml:pos>''' + b['x'] + ' ' + b['y'] + '''</gml:pos>
                        </gml:Point>
                    </basisgeo:geometrie>
                </basisgeo:Geometrie>
            </geo:geometrie>''')
                if gemeente:
                    gml_file.write ('''
            <geo:groepID>g''' + gemeenteIndex[b['gemeente']] + '</geo:groepID>')
                if jaar:
                    gml_file.write ('''
            <geo:kwantitatieveNormwaarde>''' + str(b['jaar'] + levensduur) + '</geo:kwantitatieveNormwaarde>')
                gml_file.write ('''
        </geo:Locatie>''')
        gml_file.write ('''
    </geo:locaties>
</geo:GeoInformatieObjectVersie>
    ''')

__GIO ('geometrie', False, False, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('geometrie', False, False, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)

__GIO ('GIO-delen', True, False, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('GIO-delen', True, False, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)

__GIO ('normwaarden', False, True, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('normwaarden', False, True, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)

#==============================================================================
#
# Symbolisaties
#
#==============================================================================
with open (os.path.join (voorbeelden_dir, 'GIO-delen', 'verkeersborden_STOP.xml'), 'w') as xml_file:
    xml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<FeatureTypeStyle version="1.1.0" 
    xmlns="http://www.opengis.net/se"
    xmlns:ogc="http://www.opengis.net/ogc">
    <FeatureTypeName>geo:Locatie</FeatureTypeName>
    <SemanticTypeIdentifier>geo:groepID</SemanticTypeIdentifier>''')

    idx = 0
    for i in sorted (gemeenten.keys ()):
        xml_file.write ('''
    <Rule>
        <Name>''' + gemeenten[i] + '''</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>groepID</ogc:PropertyName> 
                <ogc:Literal>''' + str(i) + '''</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
''' + symbolen[idx] + '''
    </Rule>''')
        idx += 1
        if idx >= len (symbolen):
            idx = 0

    xml_file.write ('''
</FeatureTypeStyle>''')

def __NormwaardeSymbolen (voor, filter):
    with open (os.path.join (voorbeelden_dir, 'normwaarden', 'verkeersborden_STOP_' + voor + '.xml'), 'w') as xml_file:
        xml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
    <FeatureTypeStyle version="1.1.0" 
        xmlns="http://www.opengis.net/se"
        xmlns:ogc="http://www.opengis.net/ogc">
        <FeatureTypeName>geo:Locatie</FeatureTypeName>
        <SemanticTypeIdentifier>geo:groepID</SemanticTypeIdentifier>''')

        idx = 0
        for jaar in jaren:
            if filter (jaar):
                xml_file.write ('''
        <Rule>
            <Name>''' + str(jaar + levensduur) + '''</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>kwantitatieveNormwaarde</ogc:PropertyName> 
                    <ogc:Literal>''' + str(jaar + levensduur) + '''</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
''' + symbolen[idx] + '''
        </Rule>''')
            idx += 1
            if idx >= len (symbolen):
                idx = 0

        xml_file.write ('''
    </FeatureTypeStyle>''')

__NormwaardeSymbolen ('was', wasFilter)
__NormwaardeSymbolen ('wordt', wordtFilter)
__NormwaardeSymbolen ('was_wordt', lambda j: True)
