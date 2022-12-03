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

with open (os.path.join (datadir, 'verkeersborden_puntsymbolen.json'), 'r') as json_file:
    symbolen = json.load (json_file)
symbolen = [s["symbol"] for s in sorted (symbolen, key = lambda s: s["code"])]

#==============================================================================
#
# Schrijf GIO's
#
#==============================================================================
def __GIO (subdir, multi, gemeente, jaar, filename, version, filter, idprefix = '0'):
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
    <geo:eenheidlabel>Jaar</geo:eenheidlabel>
    <geo:normlabel>Te vervangen voor</geo:normlabel>''')

        gml_file.write ('''
    <geo:locaties>''')
        def __Locatie (index, borden, gemeente, jaar):
            if len(borden) == 0:
                return
            gml_file.write ('''
            <geo:Locatie>
                <geo:geometrie>
                    <basisgeo:Geometrie>
                        <basisgeo:id>37b0a09f-36a0-4e69-80c1-''' + str(index).zfill(11) + '''</basisgeo:id>
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
            if not gemeente is None:
                gml_file.write ('''
                <geo:groepID>g''' + str (gemeente+1) + '</geo:groepID>')
            if jaar:
                gml_file.write ('''
                <geo:kwantitatieveNormwaarde>''' + str(borden[0]['jaar'] + levensduur) + '</geo:kwantitatieveNormwaarde>')
            gml_file.write ('''
            </geo:Locatie>''')


        index = 0
        if multi:
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

__GIO ('07 punten - geometrie', False, 0, False, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('07 punten - geometrie', False, 0, False, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('07 punten-multi - geometrie', True, 0, False, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('07 punten-multi - geometrie', True, False, 0, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('07 punten - geometrie - nieuwe id', False, 0, False, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter, '1')
__GIO ('07 punten - geometrie - nieuwe id', False, 0, False, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter, '2')

__GIO ('08 punten - GIO-delen', False, 1, False, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('08 punten - GIO-delen', False, 2, False, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('08 punten-multi - GIO-delen', True, 1, False, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('08 punten-multi - GIO-delen', True, 2, False, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('08 punten - GIO-delen - nieuwe id', False, 1, False, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter, '1')
__GIO ('08 punten - GIO-delen - nieuwe id', False, 2, False, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter, '2')

__GIO ('09 punten - normwaarden', False, 0, True, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('09 punten - normwaarden', False, 0, True, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('09 punten-multi - normwaarden', True, 0, True, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter)
__GIO ('09 punten-multi - normwaarden', True, 0, True, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter)
__GIO ('09 punten-multi - normwaarden - nieuwe id', False, 0, True, 'verkeersborden_STOP_was.gml', '2019;was', wasFilter, '1')
__GIO ('09 punten-multi - normwaarden - nieuwe id', False, 0, True, 'verkeersborden_STOP_wordt.gml', '2022;wordt', wordtFilter, '2')

#==============================================================================
#
# Symbolisaties
#
#==============================================================================
def __GroepIDSymbolen (voor, gemeente):
    for subdir in ['08 punten - GIO-delen', '08 punten-multi - GIO-delen', '08 punten - GIO-delen - nieuwe id']:
        with open (os.path.join (voorbeelden_dir, subdir, 'verkeersborden_STOP_' + voor + '.xml'), 'w') as xml_file:
            xml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
        <FeatureTypeStyle version="1.1.0" 
            xmlns="http://www.opengis.net/se"
            xmlns:ogc="http://www.opengis.net/ogc">
            <FeatureTypeName>geo:Locatie</FeatureTypeName>
            <SemanticTypeIdentifier>geo:groepID</SemanticTypeIdentifier>''')

            idx = 0
            for i in range (0, len (gio_delen)):
                if not gemeenteFilter[gemeente](i) is None:
                    xml_file.write ('''
            <Rule>
                <Name>''' + gio_delen[i] + '''</Name>
                <ogc:Filter>
                    <ogc:PropertyIsEqualTo>
                        <ogc:PropertyName>groepID</ogc:PropertyName> 
                        <ogc:Literal>g''' + str(i+1) + '''</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                </ogc:Filter>
        ''' + symbolen[idx] + '''
            </Rule>''')
                idx += 1
                if idx >= len (symbolen):
                    idx = 0

            xml_file.write ('''
        </FeatureTypeStyle>''')
__GroepIDSymbolen ('was', 1)
__GroepIDSymbolen ('wordt', 2)
__GroepIDSymbolen ('was_wordt', 2)

def __NormwaardeSymbolen (voor, filter):
    for subdir in ['09 punten - normwaarden', '09 punten-multi - normwaarden', '09 punten-multi - normwaarden - nieuwe id']:
        with open (os.path.join (voorbeelden_dir, subdir, 'verkeersborden_STOP_' + voor + '.xml'), 'w') as xml_file:
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
