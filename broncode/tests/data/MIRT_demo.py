#==============================================================================
#
# Omzetting van lijn-data naar GIO's en symbolisatie voor testen en voorbeelden
#
# Symbolen uit de STOP-TPOD symbolenbibliotheek
#
#==============================================================================
from typing import Dict, List, Set

import os
from xml.etree import ElementTree as ET

from pygml.parse import parse
from shapely.geometry import shape

from symbolisatie import Symbolisatie

#==============================================================================
#
# Initialisatie van alle data
#
#==============================================================================
datadir = os.path.dirname (os.path.realpath (__file__))
testscenario_dir = os.path.join (datadir, "..", "..", "geo-tools", "voorbeelden", "01 Demo - GIO-wijziging en geo-renvooi", "MIRT 2017-2022")

was_jaar = 2019
wordt_jaar = 2022

juridischeNauwkeurigheid = 50 # decimeter

met_normwaarde = False


symbolisatie = Symbolisatie (os.path.join (datadir, 'MIRT_Lijnsymbolen.json'))

ns_gml="{http://www.opengis.net/gml/3.2}"
ns_mirt="{http://mirt}"

# key = jaar, value = info + geometrie van project
mirt : Dict[int,List[object]] = {}
# key = jaar, key = gmcode, value = shapely-geometrie
shapes : Dict[int,Dict[str,object]]= {}
alle_realisatie : Set[int] = set ()
for jaar in [was_jaar, wordt_jaar]:
    # Vereenvoudig de XML eerst
    with open (os.path.join (datadir, 'MIRT_' + str(jaar) + '.gml'), 'r') as gml_file:
        xml = gml_file.read ()
    for zoek, vervang in {
        '"EPSG': '"urn:ogc:def:crs:EPSG:',
        '<wfs:member>': '', '</wfs:member>': '',
                          }.items():
        xml = xml.replace (zoek, vervang)
    try:
        gml = ET.fromstring (xml)
    except Exception as e:
        with open (os.path.join (datadir, 'MIRT_' + str(jaar) + '.fout.xml'), 'w') as xml_file:
            xml_file.write (xml)
        raise str(e)

    ditJaar : List[object] = []
    # key is code, value is shape
    ditJaar_shapes : Dict[str,str] = {}

    for prj in gml:
        code = prj.find (ns_mirt + 'mirtnrid').text.strip ()
        if code in ditJaar_shapes:
            raise "Dubbele code " + code + " in " + str(jaar)

        realisatie = prj.find (ns_mirt + 'startreali').text.strip ()
        fase = prj.find (ns_mirt + 'fase').text
        if fase == "Realisatie" or fase == "Aanleg" or realisatie != '':
            if realisatie == '':
                realisatie = jaar
            try:
                realisatie = int (realisatie)
            except:
                realisatie = jaar
        else:
            realisatie = jaar + 5
        alle_realisatie.add (realisatie)

        geo = list(prj.find (ns_mirt + 'shape'))[0]
        geo.attrib["srsName"] = "urn:ogc:def:crs:EPSG::28992"
        geoXml = ET.tostring (geo, encoding='unicode')
        try:
            ditJaar_shapes[code] = shape (parse (geoXml))
        except Exception as e:
            raise Exception (str(jaar) + '/' + code + ' gml: ' + str (e))

        ditJaar.append ({
            'Code' : code,
            'Naam': prj.find (ns_mirt + 'project').text,
            'Geometrie': geoXml,
            'Normwaarde': realisatie
        })

    mirt[jaar] = ditJaar
    shapes[jaar] = ditJaar_shapes

#==============================================================================
#
# Bepaal gewijzigde shapes
#
#==============================================================================

geometrie_index = 0
# key is code, value is geometrie_index
manifestOngewijzigd : Dict[str,int] = {}

for code in sorted (shapes[was_jaar].keys ()):
    wordt_shape = shapes[wordt_jaar].get (code)
    if not wordt_shape is None:
        was_shape = shapes[was_jaar][code]
        if not was_shape.difference (wordt_shape.buffer (0.05 * juridischeNauwkeurigheid)).is_empty:
            continue
        if not wordt_shape.difference (was_shape.buffer (0.05 * juridischeNauwkeurigheid)).is_empty:
            continue
        geometrie_index += 1
        manifestOngewijzigd[code] = geometrie_index


#==============================================================================
#
# Schrijf GIO's
#
#==============================================================================
def __GIO (jaar, geometrie_index : int):
    gioPad = os.path.join (testscenario_dir, 'mirt_' + str(jaar) + '.gml')
    os.makedirs (os.path.dirname (gioPad), exist_ok=True)
    with open (gioPad, 'w', encoding='utf-8') as gml_file:
        gml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<geo:GeoInformatieObjectVersie schemaversie="1.3.0"
      xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
      xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
      xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/"
      xmlns:gml="http://www.opengis.net/gml/3.2">
    <geo:FRBRWork>/join/id/regdata/mnre1130/1839/mirt</geo:FRBRWork>
    <geo:FRBRExpression>/join/id/regdata/mnre1130/1839/mirt/nld@''' + str(jaar) + '''</geo:FRBRExpression>''')
        if met_normwaarde:
            gml_file.write ('''
    <geo:normlabel>Realisatie</geo:normlabel>''')
        gml_file.write ('''
    <geo:locaties>''')

        for prj in mirt[jaar]:
            index = manifestOngewijzigd.get (prj['Code'])
            if index is None:
                geometrie_index += 1
                index = geometrie_index
            gml_file.write ('''
            <geo:Locatie>
                <geo:naam>''' + prj['Naam'] + '''</geo:naam>
                <geo:geometrie>
                    <basisgeo:Geometrie>
                        <basisgeo:id>37b0a09f-36a0-4e69-80c2-''' + str(index).zfill(12) + '''</basisgeo:id>
                        <basisgeo:geometrie>''')
            gml_file.write (prj['Geometrie'])
            gml_file.write ('''
                        </basisgeo:geometrie>
                    </basisgeo:Geometrie>
                </geo:geometrie>''')
            if met_normwaarde:
                gml_file.write ('''
                <geo:kwantitatieveNormwaarde>''' + str(prj['Normwaarde']) + '''</geo:kwantitatieveNormwaarde>''')
            gml_file.write ('''
            </geo:Locatie>''')

        gml_file.write ('''
    </geo:locaties>
</geo:GeoInformatieObjectVersie>
    ''')
        return geometrie_index

for jaar in [was_jaar, wordt_jaar]:
    geometrie_index = __GIO (jaar, geometrie_index)


#==============================================================================
#
# Symbolisatie
#
#==============================================================================
symPad = os.path.join (testscenario_dir,'mirt_symbolisatie.xml')
if met_normwaarde:
    symbolisatie.MaakSymbolisatie (symPad, 'kwantitatieveNormwaarde', { str(r): str(r) for r in sorted (alle_realisatie) })
else:
    with open (symPad, 'w', encoding='utf-8') as sym_file:
        sym_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<FeatureTypeStyle version="1.1.0" xmlns="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc">
	<FeatureTypeName>geo:Locatie</FeatureTypeName>
	<SemanticTypeIdentifier>geo:geometrie</SemanticTypeIdentifier>
	<Rule>
		<Name>Lijn</Name>
		<LineSymbolizer>
			<Name>Lijn</Name>
			<Stroke>
				<SvgParameter name="stroke">#6c8ebf</SvgParameter>
				<SvgParameter name="stroke-opacity">1</SvgParameter>
				<SvgParameter name="stroke-width">3</SvgParameter>
				<SvgParameter name="stroke-linejoin">round</SvgParameter>
			</Stroke>
		</LineSymbolizer>
	</Rule>
</FeatureTypeStyle>''')
