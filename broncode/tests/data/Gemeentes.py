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

symbolisatie = Symbolisatie (os.path.join (datadir, 'Gemeentes_Vlaksymbolen.json'))

jaren = [2017, 2018, 2019, 2020, 2021, 2022]

gio_delen = {
        20: "Groningen",
        21: "Friesland",
        22: "Drenthe",
        23: "Overijssel",
        24: "Flevoland",
        25: "Gelderland",
        26: "Utrecht",
        27: "Noord-Holland",
        28: "Zuid-Holland",
        29: "Zeeland",
        30: "Noord-Brabant",
        31: "Limburg"
    }

gemeente_provincie = {}
for jaar in jaren:
    with open (os.path.join (datadir, 'Gemeente_Provincie_' + str(jaar) + '.json'), 'r') as json_file:
        data = json.load (json_file)
    for gem in data:
        gm = int (gem["ID"])
        pv = int (gem["PV"])
        pvnu = gemeente_provincie.get (gm)
        if pvnu is None:
            gemeente_provincie[gm] = pv
        elif pvnu != pv:
            raise 'Oeps'

ns_gml="{http://www.opengis.net/gml/3.2}"
ns_kad="{http://www.kadaster.nl/kad/pdok}"

gemeenten = {}
for jaar in jaren:
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
        raise str(e)

    ditJaar = {}
    index = 0
    for gem in gml.findall (ns_kad + 'Gemeenten'):
        code = int (gem.find (ns_kad + 'Code').text)
        naam = gem.find (ns_kad + 'Gemeentenaam').text
        normwaarde = code % len (symbolisatie._Symbolen)
        gmcode = 'GM' + str(code).zfill(4)
        pvcode = gemeente_provincie[code]
        lijst = ditJaar.get (pvcode)
        if lijst is None:
            ditJaar[pvcode] = lijst = []

        geo = gem.find (ns_gml + 'MultiSurface')
        members = geo.findall (ns_gml + 'surfaceMember')
        if len (members) > 0:
            geo = []
            for member in members:
                pol = member.find (ns_gml + 'MultiSurface').find (ns_gml + 'surfaceMembers').find (ns_gml + 'Polygon')
                geo.append (pol)
        else:
            geo = [geo.find (ns_gml + 'surfaceMembers').find (ns_gml + 'Polygon')]

        for pol in geo:
            pol.attrib["srsName"] = "urn:ogc:def:crs:EPSG::28992"
            polXml = ET.tostring (pol, encoding='unicode')
            try:
                parse (polXml)
            except Exception as e:
                raise jaar + '/' + gmcode + ' gml: ' + str (e)
            lijst.append ({
                'ID': index,
                'Code': gmcode,
                'Naam': naam,
                'Geometrie': polXml,
                'Normwaarde': normwaarde
            })
            index += 1
    gemeenten[jaar] = ditJaar

#==============================================================================
#
# Schrijf GIO's
#
#==============================================================================
symbolisaties = {}

def __GIO (subdir, jaar, multiVlakken, attribuut, beschrijving):
    gioPad = os.path.join (voorbeelden_dir, subdir, 'gemeenten_' + str(jaar) + '.gml')
    os.makedirs (os.path.dirname (gioPad), exist_ok=True)
    with open (gioPad, 'w', encoding='utf-8') as gml_file:
        gml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<geo:GeoInformatieObjectVersie schemaversie="1.3.0"
      xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
      xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
      xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/"
      xmlns:gml="http://www.opengis.net/gml/3.2">
    <geo:FRBRWork>/join/id/regdata/mnre9999/1851/gemeenten</geo:FRBRWork>
    <geo:FRBRExpression>/join/id/regdata/mnre9999/1851/gemeenten/nld@''' + str(jaar) + '''</geo:FRBRExpression>''')

        symbolisatie.StartGio (gioPad, 'groepID' if attribuut == 1 else 'kwantitatieveNormwaarde' if attribuut == 2 else None, beschrijving)

        if attribuut == 1:
            gml_file.write ('''
    <geo:groepen>''')
            for code, naam in gio_delen.items ():
                gml_file.write ('''
        <geo:Groep>
            <geo:groepID>PV''' + str(code) + '''</geo:groepID>
            <geo:label>''' + naam + '''</geo:label>
        </geo:Groep>''')
            gml_file.write ('''
    </geo:groepen>''')

        elif attribuut == 2:
            gml_file.write ('''
    <geo:eenheidlabel>%</geo:eenheidlabel>
    <geo:normlabel>Norm GM</geo:normlabel>''')

        gml_file.write ('''
    <geo:locaties>''')

        def __Locatie (pvcode, gemeenten):
            gml_file.write ('''
            <geo:Locatie>''')
            if not multiVlakken:
                gml_file.write ('''
                <geo:naam>''' + gemeenten[0]['Naam'] + '</geo:naam>')
            gml_file.write ('''
                <geo:geometrie>
                    <basisgeo:Geometrie>
                        <basisgeo:id>37b0a09f-36a0-4e69-80c2-''' + str(jaar).zfill(6) + str(gemeenten[0]['ID']).zfill(6) + '''</basisgeo:id>
                        <basisgeo:geometrie>''')
            if len(gemeenten) > 1:
                geometrie = ET.fromstring ('<MultiSurface srsName="urn:ogc:def:crs:EPSG::28992" xmlns="http://www.opengis.net/gml/3.2"><surfaceMembers></surfaceMembers></MultiSurface>')
                members = geometrie.find (ns_gml + 'surfaceMembers')
                for gem in gemeenten:
                    members.append (ET.fromstring (gem['Geometrie']))
                geometrie = ET.tostring (geometrie, encoding='unicode')
            else:
                geometrie = gemeenten[0]['Geometrie']
            gml_file.write (geometrie)
            gml_file.write ('''
                        </basisgeo:geometrie>
                    </basisgeo:Geometrie>
                </geo:geometrie>''')
            if attribuut == 1:
                gml_file.write (symbolisatie.GIOWaarde ('PV' + str(pvcode)))
            elif attribuut == 2:
                gml_file.write (symbolisatie.GIOWaarde (gemeenten[0]['Normwaarde']))
            gml_file.write ('''
            </geo:Locatie>''')

        if multiVlakken:
            if attribuut == 0:
                alle = []
                for gems in gemeenten[jaar].values ():
                    alle.extend (gems)
                __Locatie (1, alle)
            elif attribuut == 1:
                for pvcode, gems in gemeenten[jaar].items ():
                    __Locatie (pvcode, gems)
            else:
                gemeentenPerNormwaarde = {}
                for pvcode, gems in gemeenten[jaar].items ():
                    for gem in gems:
                        lijst = gemeentenPerNormwaarde.get (gem["Normwaarde"])
                        if lijst is None:
                            gemeentenPerNormwaarde[gem["Normwaarde"]] = [gem]
                        else:
                            lijst.append (gem)
                for gems in gemeentenPerNormwaarde.values ():
                    __Locatie (None, gems)
        else:
            for pvcode, gems in gemeenten[jaar].items ():
                for gem in gems:
                    __Locatie (pvcode, [gem])

        gml_file.write ('''
    </geo:locaties>
</geo:GeoInformatieObjectVersie>
    ''')

for jaar in jaren:
    __GIO ('01 vlakken - geometrie', jaar, False, 0, 'GIO met alleen geometrie voor het jaar ' + str(jaar) + '. Elk vlak heeft een eigen GIO-Locatie, en elk jaar worden de basisgeo-IDs opnieuw toegekend..')
    __GIO ('01 vlakken - geometrie - multi-geometrie', jaar, True, 0, 'GIO met alleen geometrie voor het jaar ' + str(jaar) + '. Alle vlakken worden in één GIO-Locatie gecombineerd die elk jaar een nieuwe basisgeo-ID krijgt.')

    __GIO ('02 vlakken - GIO-delen', jaar, False, 1, 'GIO met HIO-delen voor het jaar ' + str(jaar) + '. Elk vlak heeft een eigen GIO-Locatie, en elk jaar worden de basisgeo-IDs opnieuw toegekend..')
    __GIO ('02 vlakken - GIO-delen - multi-geometrie', jaar, True, 1, 'GIO met GIO-delen voor het jaar ' + str(jaar) + '. Elk GIO-deel correspondeert met één GIO-Locatie, met één of meer vlakken, die elk jaar een nieuwe basisgeo-ID krijgt.')

    __GIO ('03 vlakken - normwaarden', jaar, False, 2, 'GIO met normwaarden voor het jaar ' + str(jaar) + '. Elk vlak heeft een eigen GIO-Locatie, en elk jaar worden de basisgeo-IDs opnieuw toegekend..')
    __GIO ('03 vlakken - normwaarden - multi-geometrie', jaar, True, 2, 'GIO met normwaarden voor het jaar ' + str(jaar) + '. Elke normwaarde correspondeert met één GIO-Locatie, met één of meer vlakken, die elk jaar een nieuwe basisgeo-ID krijgt.')

#==============================================================================
#
# Symbolisaties en specificaties
#
#==============================================================================
symbolisatie.MaakSymbolisaties ('gemeenten_alle_jaren_symbolisatie.xml')

symbolisatie.MaakToonGeoSpecificaties (10)

for mapPad in symbolisatie.GIOMappen ():
    with open (os.path.join (mapPad, 'maak_gio_wijziging.json'), 'w', encoding='utf-8') as json_file:
        json.dump ([*[{
            'was': 'gemeenten_' + str(jaar-1) + '.gml', 
            'wordt': 'gemeenten_' + str(jaar) + '.gml', 
            'nauwkeurigheid': '10',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad),
            'wijziging': 'gemeenten_' + str(jaar-1) + '_' + str(jaar) + '.gml'
        } for jaar in jaren if jaar != jaren[0]],
        {
            'was': 'gemeenten_' + str(jaren[0]) + '.gml', 
            'wordt': 'gemeenten_' + str(jaren[-1]) + '.gml', 
            'nauwkeurigheid': '10',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad),
            'wijziging': 'gemeenten_' + str(jaren[0]) + '_' + str(jaren[-1]) + '.gml'
        }], json_file)
    with open (os.path.join (mapPad, 'toon_gio_wijziging.json'), 'w', encoding='utf-8') as json_file:
        json.dump ([*[{
            'was': 'gemeenten_' + str(jaar-1) + '.gml', 
            'wijziging': 'gemeenten_' + str(jaar-1) + '_' + str(jaar) + '.gml',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad),
        } for jaar in jaren if jaar != jaren[0]],
        {
            'was': 'gemeenten_' + str(jaren[0]) + '.gml', 
            'wijziging': 'gemeenten_' + str(jaren[0]) + '_' + str(jaren[-1]) + '.gml',
            'symbolisatie': symbolisatie.MapSymbolisatie.get (mapPad)
        }], json_file)
