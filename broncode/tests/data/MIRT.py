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
import json
import os
from xml.etree import ElementTree as ET

from pygml.parse import parse

from symbolisatie import Symbolisatie

#==============================================================================
#
# Initialisatie van alle data
#
#==============================================================================
datadir = os.path.dirname (os.path.realpath (__file__))
voorbeelden_dir = os.path.join (datadir, "..", "..", "geo-tools", "voorbeelden")

symbolisatie = Symbolisatie (os.path.join (datadir, 'MIRT_Lijnsymbolen.json'))

jaren = [2017, 2018, 2019, 2020, 2021, 2022]

ns_gml="{http://www.opengis.net/gml/3.2}"
ns_mirt="{http://mirt}"

mirt = {}
realisatie_jaar = {}
gio_delen = set ()
for jaar in jaren:
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

    ditJaar = {}
    index = 0
    for gem in gml:
        code = gem.find (ns_mirt + 'mirtnrid').text.strip ()
        realisatie = gem.find (ns_mirt + 'startreali').text.strip ()
        fase = gem.find (ns_mirt + 'fase').text
        if fase == "Realisatie" or fase == "Aanleg" or realisatie != '':
            if realisatie == '':
                realisatie = realisatie_jaar.get (code)
                if realisatie is None:
                    realisatie = jaar
            try:
                realisatie = int (realisatie)
            except:
                realisatie = jaar
            realisatie_jaar[code] = realisatie
        else:
            realisatie = None
        onderwerp = gem.find (ns_mirt + 'onderwerp').text
        gio_delen.add (onderwerp)
        lijst = ditJaar.get (onderwerp)
        if lijst is None:
            ditJaar[onderwerp] = lijst = []

        geo = list(gem.find (ns_mirt + 'shape'))[0]
        if geo.tag == ns_gml + 'MultiCurve':
            geo = [m.find (ns_gml + 'LineString') for m in geo.findall (ns_gml + 'curveMember')]
        else:
            geo = [geo]

        for lijn in geo:
            lijn.attrib["srsName"] = "urn:ogc:def:crs:EPSG::28992"
            lijnXml = ET.tostring (lijn, encoding='unicode')
            try:
                parse (lijnXml)
            except Exception as e:
                raise jaar + '/' + str(code) + ' gml: ' + str (e)
            lijst.append ({
                'ID': index,
                'Naam': gem.find (ns_mirt + 'project').text,
                'GIOdeel' : onderwerp,
                'Geometrie': lijnXml,
                'Normwaarde': realisatie
            })
            index += 1
    mirt[jaar] = ditJaar

gio_delen = { gd: idx for idx, gd in enumerate (sorted (gio_delen)) }

#==============================================================================
#
# Schrijf GIO's
#
#==============================================================================
def __GIO (subdir, jaar, multiLijnen, attribuut, beschrijving):
    gioPad = os.path.join (voorbeelden_dir, subdir, 'mirt_' + str(jaar) + '.gml')
    os.makedirs (os.path.dirname (gioPad), exist_ok=True)
    with open (gioPad, 'w', encoding='utf-8') as gml_file:
        gml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<geo:GeoInformatieObjectVersie schemaversie="1.3.0"
      xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
      xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
      xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/"
      xmlns:gml="http://www.opengis.net/gml/3.2">
    <geo:FRBRWork>/join/id/regdata/mnre9999/1839/mirt</geo:FRBRWork>
    <geo:FRBRExpression>/join/id/regdata/mnre9999/1839/mirt/nld@''' + str(jaar) + '''</geo:FRBRExpression>''')

        symbolisatie.StartGio (gioPad, 'groepID' if attribuut == 1 else 'kwantitatieveNormwaarde' if attribuut == 2 else None, beschrijving)

        if attribuut == 1:
            gml_file.write ('''
    <geo:groepen>''')
            for naam, code in gio_delen.items ():
                gml_file.write ('''
        <geo:Groep>
            <geo:groepID>Onderwerp''' + str(code) + '''</geo:groepID>
            <geo:label>''' + naam + '''</geo:label>
        </geo:Groep>''')
            gml_file.write ('''
    </geo:groepen>''')

        elif attribuut == 2:
            gml_file.write ('''
    <geo:normlabel>Realisatie</geo:normlabel>''')

        gml_file.write ('''
    <geo:locaties>''')

        def __Locatie (onderwerpIndex, projecten):
            gml_file.write ('''
            <geo:Locatie>''')
            if not multiLijnen:
                gml_file.write ('''
                <geo:naam>''' + projecten[0]['Naam'] + '</geo:naam>')
            gml_file.write ('''
                <geo:geometrie>
                    <basisgeo:Geometrie>
                        <basisgeo:id>37b0a09f-36a0-4e69-80c2-''' + str(jaar).zfill(6) + str(projecten[0]['ID']).zfill(6) + '''</basisgeo:id>
                        <basisgeo:geometrie>''')
            if len(projecten) > 1:
                geometrie = ET.fromstring ('<MultiCurve srsName="urn:ogc:def:crs:EPSG::28992" xmlns="http://www.opengis.net/gml/3.2"><curveMembers></curveMembers></MultiCurve>')
                members = geometrie.find (ns_gml + 'curveMembers')
                for gem in projecten:
                    members.append (ET.fromstring (gem['Geometrie']))
                geometrie = ET.tostring (geometrie, encoding='unicode')
            else:
                geometrie = projecten[0]['Geometrie']
            gml_file.write (geometrie)
            gml_file.write ('''
                        </basisgeo:geometrie>
                    </basisgeo:Geometrie>
                </geo:geometrie>''')
            if attribuut == 1:
                gml_file.write (symbolisatie.GIOWaarde ('Onderwerp' + str(onderwerpIndex)))
            elif attribuut == 2:
                gml_file.write (symbolisatie.GIOWaarde (projecten[0]['Normwaarde']))
            gml_file.write ('''
            </geo:Locatie>''')

        if multiLijnen:
            if attribuut == 0:
                alle = []
                for m in mirt[jaar].values ():
                    alle.extend (m)
                __Locatie (1, alle)
            elif attribuut == 1:
                for onderwerp, projecten in mirt[jaar].items ():
                    __Locatie (gio_delen[onderwerp], projecten)
            else:
                projectPerNormwaarde = {}
                for onderwerp, projecten in mirt[jaar].items ():
                    for project in projecten:
                        if not project["Normwaarde"] is None:
                            lijst = projectPerNormwaarde.get (project["Normwaarde"])
                            if lijst is None:
                                projectPerNormwaarde[project["Normwaarde"]] = [project]
                            else:
                                lijst.append (project)
                for projecten in projectPerNormwaarde.values ():
                    __Locatie (None, projecten)
        else:
            if attribuut == 2:
                for onderwerp, projecten in mirt[jaar].items ():
                    for project in projecten:
                        if not project["Normwaarde"] is None:
                            __Locatie (gio_delen[onderwerp], [project])
            else:
                for onderwerp, projecten in mirt[jaar].items ():
                    for project in projecten:
                        __Locatie (gio_delen[onderwerp], [project])

        gml_file.write ('''
    </geo:locaties>
</geo:GeoInformatieObjectVersie>
    ''')

for jaar in jaren:
    __GIO ('04 lijnen - geometrie', jaar, False, 0, 'GIO met alleen geometrie voor het jaar ' + str(jaar) + '. Elke lijn heeft een eigen GIO-Locatie, en elk jaar worden de basisgeo-IDs opnieuw toegekend..')
    __GIO ('04 lijnen - geometrie - multi-geometrie', jaar, True, 0, 'GIO met alleen geometrie voor het jaar ' + str(jaar) + '. Alle lijnen worden in één GIO-Locatie gecombineerd die elk jaar een nieuwe basisgeo-ID krijgt.')

    __GIO ('05 lijnen - GIO-delen', jaar, False, 1, 'GIO met HIO-delen voor het jaar ' + str(jaar) + '. Elke lijn heeft een eigen GIO-Locatie, en elk jaar worden de basisgeo-IDs opnieuw toegekend..')
    __GIO ('05 lijnen - GIO-delen - multi-geometrie', jaar, True, 1, 'GIO met GIO-delen voor het jaar ' + str(jaar) + '. Elk GIO-deel correspondeert met één GIO-Locatie, met één of meer lijnen, die elk jaar een nieuwe basisgeo-ID krijgt.')

    __GIO ('06 lijnen - normwaarden', jaar, False, 2, 'GIO met normwaarden voor het jaar ' + str(jaar) + '. Elke lijn heeft een eigen GIO-Locatie, en elk jaar worden de basisgeo-IDs opnieuw toegekend..')
    __GIO ('06 lijnen - normwaarden - multi-geometrie', jaar, True, 2, 'GIO met normwaarden voor het jaar ' + str(jaar) + '. Elke normwaarde correspondeert met één GIO-Locatie, met één of meer lijnen, die elk jaar een nieuwe basisgeo-ID krijgt.')

#==============================================================================
#
# Symbolisaties en specificaties
#
#==============================================================================
symbolisatie.MaakSymbolisaties ('mirt_alle_jaren_symbolisatie.xml')

symbolisatie.MaakToonGeoSpecificaties (10)

for mapPad in symbolisatie.GIOMappen ():
    with open (os.path.join (mapPad, 'maak_gio_wijziging.json'), 'w', encoding='utf-8') as json_file:
        json.dump ([*[{
            'was': 'mirt_' + str(jaar-1) + '.gml', 
            'wordt': 'mirt_' + str(jaar) + '.gml', 
            'nauwkeurigheid': '10',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad),
            'wijziging': 'mirt_' + str(jaar-1) + '_' + str(jaar) + '.gml'
        } for jaar in jaren if jaar != jaren[0]],
        {
            'was': 'mirt_' + str(jaren[0]) + '.gml', 
            'wordt': 'mirt_' + str(jaren[-1]) + '.gml', 
            'nauwkeurigheid': '10',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad),
            'wijziging': 'mirt_' + str(jaren[0]) + '_' + str(jaren[-1]) + '.gml'
        }], json_file)
    with open (os.path.join (mapPad, 'toon_gio_wijziging.json'), 'w', encoding='utf-8') as json_file:
        json.dump ([*[{
            'was': 'mirt_' + str(jaar-1) + '.gml', 
            'wijziging': 'mirt_' + str(jaar-1) + '_' + str(jaar) + '.gml',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad),
        } for jaar in jaren if jaar != jaren[0]],
        {
            'was': 'mirt_' + str(jaren[0]) + '.gml', 
            'wijziging': 'mirt_' + str(jaren[0]) + '_' + str(jaren[-1]) + '.gml',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad)
        }], json_file)
