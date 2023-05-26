#==============================================================================
#
# Omzetting van vlak-data naar GIO's en symbolisatie voor testen en voorbeelden
#
# Bron: PDOK en OpenDataSoft (relatie gemeente - provincie)
# Opgehaald op 02-12-2022
#
# Gemeentes als vlakken; multi-vlakken gegroepeerd per provincie
#
# Symbolen uit de STOP-TPOD symbolenbibliotheek
#
#==============================================================================
from typing import Dict, List

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
testscenario_dir = os.path.join (datadir, "..", "..", "..", "docs", "Demo", "Gemeenten 2017-2023")

was_jaar = 2017
wordt_jaar = 2023

toepassingsnauwkeurigheid = 100 # centimeter


symbolisatie = Symbolisatie (os.path.join (datadir, 'Gemeentes_Vlaksymbolen.json'))

ns_gml="{http://www.opengis.net/gml/3.2}"
ns_kad="{http://www.kadaster.nl/kad/pdok}"

# key = jaar, value = info + geometrie van gemeente
gemeenten : Dict[int,List[object]]= {}
# key = groepID, value = naam
alle_gio_delen : Dict[str,str] = {}
# key = jaar, key = groepID, value = naam
gio_delen : Dict[int,Dict[str,str]]= {}
# key = jaar, key = gmcode, value = shapely-geometrie
shapes : Dict[int,Dict[str,object]]= {}
for jaar in [was_jaar, wordt_jaar]:
    # Vereenvoudig de XML eerst
    with open (os.path.join (datadir, 'Gemeentegrenzen_' + str(jaar) + '.gml'), 'r') as gml_file:
        xml = gml_file.read ()
    for zoek, vervang in {
        # tot 2021
        '"EPSG': '"urn:ogc:def:crs:EPSG:',
        '<gml:featureMember>': '', '</gml:featureMember>': '',
        '<gml:multiSurfaceProperty>': '', '</gml:multiSurfaceProperty>': '',
        '<gml:surfaceProperty>': '', '</gml:surfaceProperty>': '',
        'gml:patches': 'gml:surfaceMembers',
        'gml:Surface': 'gml:MultiSurface',
        'gml:PolygonPatch': 'gml:Polygon',
        # vanaf 2022
        '<bgp:gemeenteMember>': '', '</bgp:gemeenteMember>': '',
        'bg:GemeenteGebied': 'kad:Gemeenten',
        'bg:code': 'kad:Code',
        'bg:naam': 'kad:Gemeentenaam',
        '<bg:geometrie>': '','</bg:geometrie>': '',
        '<bg:VlakOfMultiVlak>': '','</bg:VlakOfMultiVlak>': ''
                          }.items():
        xml = xml.replace (zoek, vervang)
    try:
        gml = ET.fromstring (xml)
    except Exception as e:
        with open (os.path.join (datadir, 'Gemeentegrenzen_' + str(jaar) + '.fout.xml'), 'w') as xml_file:
            xml_file.write (xml)
        raise e

    ditJaar_gemeenten : List[object] = []
    # key is GM-code, value is groepID
    ditJaar_gio_delen : Dict[str,str] = {}
    # key is GM-code, value is groepID
    ditJaar_shapes : Dict[str,str] = {}
    for gem in gml.findall (ns_kad + 'Gemeenten'):
        code = int (gem.find (ns_kad + 'Code').text)
        naam = gem.find (ns_kad + 'Gemeentenaam').text
        gmcode = 'GM' + str(code).zfill(4)
        groepID = ditJaar_gio_delen.get (gmcode)
        if groepID is None:
            groepID = gmcode
            bekende_naam = alle_gio_delen.get (groepID)
            if not bekende_naam is None:
                if bekende_naam != naam:
                    # Hernoemd GIO-deel
                    groepID = gmcode + '_hernoemd'
                    alle_gio_delen[groepID] = naam
            else:
                alle_gio_delen[groepID] = naam
            ditJaar_gio_delen[gmcode] = groepID
        else:
            raise "Dubbele GMcode " + gmcode + " in " + str(jaar)

        geo = gem.find (ns_gml + 'MultiSurface')
        members = geo.findall (ns_gml + 'surfaceMember')
        if len (members) > 0:
            geo = ET.fromstring ('<MultiSurface srsName="urn:ogc:def:crs:EPSG::28992" xmlns="http://www.opengis.net/gml/3.2"><surfaceMembers></surfaceMembers></MultiSurface>')
            geo_collection = geo.find (ns_gml + 'surfaceMembers')
            for member in members:
                pol = member.find (ns_gml + 'MultiSurface').find (ns_gml + 'surfaceMembers').find (ns_gml + 'Polygon')
                geo_collection.append (pol)
        else:
            geo = geo.find (ns_gml + 'surfaceMembers').find (ns_gml + 'Polygon')
            geo.attrib["srsName"] = "urn:ogc:def:crs:EPSG::28992"

        geoXml = ET.tostring (geo, encoding='unicode')
        try:
            ditJaar_shapes[gmcode] = shape (parse (geoXml))
        except Exception as e:
            raise Exception (str(jaar) + '/' + gmcode + ' gml: ' + str (e))
        ditJaar_gemeenten.append ({
            'GM': gmcode,
            'GIODeel': groepID,
            'Naam': naam,
            'Geometrie': geoXml
        })

    ditJaar_gemeenten.sort (key = lambda g: g['GM'])
    gemeenten[jaar] = ditJaar_gemeenten
    gio_delen[jaar] = ditJaar_gio_delen
    shapes[jaar] = ditJaar_shapes

#==============================================================================
#
# Bepaal gewijzigde shapes
#
#==============================================================================

geometrie_index = 0
# key is gmcode, value is geometrie_index
manifestOngewijzigd : Dict[str,int] = {}

for gmcode in sorted (shapes[was_jaar].keys ()):
    wordt_shape = shapes[wordt_jaar].get (gmcode)
    if not wordt_shape is None:
        was_shape = shapes[was_jaar][gmcode]
        if not was_shape.buffer (-0.05 * toepassingsnauwkeurigheid).difference (wordt_shape.buffer (0.05 * toepassingsnauwkeurigheid)).is_empty:
            continue
        if not wordt_shape.buffer (-0.05 * toepassingsnauwkeurigheid).difference (was_shape.buffer (0.05 * toepassingsnauwkeurigheid)).is_empty:
            continue
        geometrie_index += 1
        manifestOngewijzigd[gmcode] = geometrie_index


#==============================================================================
#
# Schrijf GIO's
#
#==============================================================================
def __GIO (jaar, geometrie_index):
    gioPad = os.path.join (testscenario_dir, 'gemeenten_' + str(jaar) + '.gml')
    os.makedirs (os.path.dirname (gioPad), exist_ok=True)
    with open (gioPad, 'w', encoding='utf-8') as gml_file:
        gml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<geo:GeoInformatieObjectVersie schemaversie="1.3.0"
      xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
      xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
      xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/"
      xmlns:gml="http://www.opengis.net/gml/3.2">
    <geo:FRBRWork>/join/id/regdata/mnre0001/1851/gemeenten</geo:FRBRWork>
    <geo:FRBRExpression>/join/id/regdata/mnre0001/1851/gemeenten/nld@''' + str(jaar) + '''</geo:FRBRExpression>
    <geo:groepen>''')
        for code in gio_delen[jaar].values ():
            gml_file.write ('''
        <geo:Groep>
            <geo:groepID>''' + str(code) + '''</geo:groepID>
            <geo:label>''' + alle_gio_delen[code] + '''</geo:label>
        </geo:Groep>''')
        gml_file.write ('''
    </geo:groepen>''')

        gml_file.write ('''
    <geo:locaties>''')


        for gem in gemeenten[jaar]:
            index = manifestOngewijzigd.get (gem['GM'])
            if index is None:
                geometrie_index += 1
                index = geometrie_index
            gml_file.write ('''
            <geo:Locatie>
                <geo:wId>''' + str(index) + '''</geo:wId>
                <geo:naam>''' + gem['Naam'] + '''</geo:naam>
                <geo:geometrie>
                    <basisgeo:Geometrie>
                        <basisgeo:id>37b0a09f-36a0-4e69-80c2-''' + str(index).zfill(12) + '''</basisgeo:id>
                        <basisgeo:geometrie>''')
            gml_file.write (gem['Geometrie'])
            gml_file.write ('''
                        </basisgeo:geometrie>
                    </basisgeo:Geometrie>
                </geo:geometrie>
                <geo:groepID>''' + gem['GIODeel'] + '''</geo:groepID>
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
symbolisatie.MaakSymbolisatie (os.path.join (testscenario_dir,'gemeenten_symbolisatie.xml'), 'groepID', alle_gio_delen)
