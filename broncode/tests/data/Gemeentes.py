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

    ditJaar = []
    index = 0
    for gem in gml.findall (ns_kad + 'Gemeenten'):
        code = int (gem.find (ns_kad + 'Code').text)
        naam = gem.find (ns_kad + 'Gemeentenaam').text
        normwaarde = code % len (symbolisatie._Symbolen)
        gmcode = 'GM' + str(code).zfill(4)
        pvcode = gemeente_provincie[code]

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
            ditJaar.append ({
                'ID': index,
                'GM': gmcode,
                'PV': pvcode,
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

def __GIO (subdir, jaar, multiVlakken, attribuut):
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

        symbolisatie.StartGio (gioPad, 'groepID' if attribuut in [1,3] else 'kwantitatieveNormwaarde' if attribuut == 2 else None)

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

        elif attribuut == 3:
            gemeente_groepen = { gem["GM"]: gem["Naam"] for gem in gemeenten[jaar] }
            gml_file.write ('''
    <geo:groepen>''')
            for code, naam in gemeente_groepen.items ():
                gml_file.write ('''
        <geo:Groep>
            <geo:groepID>''' + str(code) + '''</geo:groepID>
            <geo:label>''' + naam + '''</geo:label>
        </geo:Groep>''')
            gml_file.write ('''
    </geo:groepen>''')

        gml_file.write ('''
    <geo:locaties>''')


        def __Locatie (gioDeelCode, samengevoegdeGemeenten):
            gml_file.write ('''
            <geo:Locatie>''')
            if not multiVlakken:
                gml_file.write ('''
                <geo:naam>''' + samengevoegdeGemeenten[0]['Naam'] + '</geo:naam>')
            gml_file.write ('''
                <geo:geometrie>
                    <basisgeo:Geometrie>
                        <basisgeo:id>37b0a09f-36a0-4e69-80c2-''' + str(jaar).zfill(6) + str(samengevoegdeGemeenten[0]['ID']).zfill(6) + '''</basisgeo:id>
                        <basisgeo:geometrie>''')
            if len(samengevoegdeGemeenten) > 1:
                geometrie = ET.fromstring ('<MultiSurface srsName="urn:ogc:def:crs:EPSG::28992" xmlns="http://www.opengis.net/gml/3.2"><surfaceMembers></surfaceMembers></MultiSurface>')
                members = geometrie.find (ns_gml + 'surfaceMembers')
                for gem in samengevoegdeGemeenten:
                    members.append (ET.fromstring (gem['Geometrie']))
                geometrie = ET.tostring (geometrie, encoding='unicode')
            else:
                geometrie = samengevoegdeGemeenten[0]['Geometrie']
            gml_file.write (geometrie)
            gml_file.write ('''
                        </basisgeo:geometrie>
                    </basisgeo:Geometrie>
                </geo:geometrie>''')
            if attribuut == 1:
                gml_file.write (symbolisatie.GIOWaarde ('PV' + str(gioDeelCode)))
            elif attribuut == 2:
                gml_file.write (symbolisatie.GIOWaarde (samengevoegdeGemeenten[0]['Normwaarde']))
            elif attribuut == 3:
                gml_file.write (symbolisatie.GIOWaarde (gioDeelCode))
            gml_file.write ('''
            </geo:Locatie>''')

        if multiVlakken:
            if attribuut == 0:
                __Locatie (1, gemeenten[jaar])
            elif attribuut == 1:
                gemeentenPerProvincie = {}
                for gem in gemeenten[jaar]:
                    lijst = gemeentenPerProvincie.get (gem["PV"])
                    if lijst is None:
                        gemeentenPerProvincie[gem["PV"]] = [gem]
                    else:
                        lijst.append (gem)
                for gems in gemeentenPerProvincie.values ():
                    __Locatie (gems[0]["PV"], gems)
            elif attribuut == 2:
                gemeentenPerNormwaarde = {}
                for gem in gemeenten[jaar]:
                    lijst = gemeentenPerNormwaarde.get (gem["Normwaarde"])
                    if lijst is None:
                        gemeentenPerNormwaarde[gem["Normwaarde"]] = [gem]
                    else:
                        lijst.append (gem)
                for gems in gemeentenPerNormwaarde.values ():
                    __Locatie (None, gems)
            else:
                raise 'Oeps'
        else:
            if attribuut == 3:
                for gem in gemeenten[jaar]:
                    __Locatie (gem["GM"], [gem])
            else:
                for gem in gemeenten[jaar]:
                    __Locatie (gem["PV"], [gem])

        gml_file.write ('''
    </geo:locaties>
</geo:GeoInformatieObjectVersie>
    ''')

symbolisatie.MaakReadme ([voorbeelden_dir, '01 demo - gemeentegrenzen'], '''#GIO met de gemeentegrenzen

Demonstratie van het nut van GIO-wijzigingen/geo-renvooi. Als er relatief kleine wijzigingen in een 
GIO worden vastgesteld, dan is het voor eenieder lastig te doorgronden wat er gewijzigd is. Door
in een besluit de wijziging in de GIO (naast de wijziging van de tekst) in renvooi weer te geven
wordt wel duidelijk wat de wijziging inhoudt.

De gekozen manier van opstellen en presenteren van de GIO-wijziging is (net als renvooi voor te tekst)
geschikt om geautomatiseerd te worden uitgevoerd. De GIO kan (op dezelfde manier als tekst van een regeling)
geconsolideerd worden.
''')
for jaar in jaren:
    __GIO ('01 demo - gemeentegrenzen', jaar, False, 3)

symbolisatie.MaakReadme ([voorbeelden_dir, '02 vlakken - geometrie'], '''#GIO met alleen geometrie

Dit is een technisch voorbeeld om geo-renvooi te demonstreren voor een GIO met alleen geometrie bestaande uit gebieden.

De geometrieën bestaan uit gebieden. Elk gebied is een aparte GIO-Locatie.
Ook als de geometrie van een gebied niet wijzigt in een volgende versie, dan heeft het gebied toch een andere basisgeometrie-ID.
''')
symbolisatie.MaakReadme ([voorbeelden_dir, '02 vlakken - geometrie - multi-geometrie'], '''#GIO met alleen geometrie

Dit is een technisch voorbeeld om voor een GIO met alleen geometrie te demonstreren dat het combineren van alle geometrie
in een enkele multi-geometrie tot een onnodig druk kaartbeeld leidt.

De geometrieën bestaan uit gebieden. Alle gebieden zijn ondergebracht in een enkele GIO-Locatie.
De basisgeo-ID van de geometrie is in elke GIO-versie verschillend.
''')
for jaar in jaren:
    __GIO ('02 vlakken - geometrie', jaar, False, 0)
    __GIO ('02 vlakken - geometrie - multi-geometrie', jaar, True, 0)

symbolisatie.MaakReadme ([voorbeelden_dir, '03 vlakken - GIO-delen'], '''#GIO met GIO-delen

Dit is een technisch voorbeeld om geo-renvooi te demonstreren voor een GIO met GIO-delen bestaande uit gebieden.

De geometrieën bestaan uit gebieden. Elk gebied is een aparte GIO-Locatie.
Ook als de geometrie van een gebied niet wijzigt in een volgende versie, dan heeft het gebied toch een andere basisgeometrie-ID.
''')
symbolisatie.MaakReadme ([voorbeelden_dir, '03 vlakken - GIO-delen - multi-geometrie'], '''#GIO met GIO-delen

Dit is een technisch voorbeeld om voor een GIO met GIO-delen te demonstreren dat het combineren van alle geometrie
in multi-geometrieën tot een onnodig druk kaartbeeld leidt.

De geometrieën bestaan uit gebied. Alle gebieden zijn ondergebracht in een enkele GIO-Locatie per GIO-deel.
De basisgeo-ID van de geometrie is in elke GIO-versie verschillend.
''')
for jaar in jaren:
    __GIO ('03 vlakken - GIO-delen', jaar, False, 1)
    __GIO ('03 vlakken - GIO-delen - multi-geometrie', jaar, True, 1)

symbolisatie.MaakReadme ([voorbeelden_dir, '04 vlakken - normwaarden'], '''#GIO met normwaarden

Dit is een technisch voorbeeld om geo-renvooi te demonstreren voor een GIO met normwaarden voor uit gebieden.

De geometrieën bestaan uit gebieden. Elk gebied is een aparte GIO-Locatie.
Ook als de geometrie van een gebied niet wijzigt in een volgende versie, dan heeft het gebied toch een andere basisgeometrie-ID.
''')
symbolisatie.MaakReadme ([voorbeelden_dir, '04 vlakken - normwaarden - multi-geometrie'], '''#GIO met normwaarden

Dit is een technisch voorbeeld om voor een GIO met normwaarden te demonstreren dat het combineren van alle geometrie
in multi-geometrieën tot een onnodig druk kaartbeeld leidt.

De geometrieën bestaan uit gebieden. Alle gebieden zijn ondergebracht in een enkele GIO-Locatie per normwaarde.
De basisgeo-ID van de geometrie is in elke GIO-versie verschillend.
''')
for jaar in jaren:
    __GIO ('03 vlakken - normwaarden', jaar, False, 2)
    __GIO ('03 vlakken - normwaarden - multi-geometrie', jaar, True, 2)

#==============================================================================
#
# Symbolisaties en specificaties
#
#==============================================================================
symbolisatie.MaakSymbolisaties ('gemeenten_alle_jaren_symbolisatie.xml')

nauwkeurigheid = 10

for mapPad in symbolisatie.GIOMappen ():
    for specPad, relPad in [(mapPad, '../'), 
                            (os.path.join ('tests', 'voorbeelden', os.path.basename (mapPad)), 
                             os.path.join ('..','..', '..', '..', 'geo-tools', 'voorbeelden', os.path.basename (mapPad)) + '/')]:
        symbolisatiePad = symbolisatie.SymbolisatiePad (mapPad, relPad)
        for jaar in jaren:
            symbolisatie.MaakSpecificatie (specPad, [str(jaar), 'toon_geo.json'], {
                    'geometrie': relPad + 'gemeenten_' + str(jaar) + '.gml', 
                    'symbolisatie': None if symbolisatiePad is None else relPad + 'gemeenten_' + str(jaar) + '_symbolisatie.xml',
                    'nauwkeurigheid': nauwkeurigheid
                })
            if jaar == jaren[0]:
                continue
            symbolisatie.MaakSpecificatie (specPad, [str(jaar), 'maak_gio_wijziging.json'], {
                'was': relPad + 'gemeenten_' + str(jaar-1) + '.gml', 
                'wordt': relPad + 'gemeenten_' + str(jaar) + '.gml', 
                'nauwkeurigheid': nauwkeurigheid,
                'symbolisatie': symbolisatiePad,
                'wijziging': relPad + 'gemeenten_' + str(jaar-1) + '_' + str(jaar) + '.gml'
            })
            symbolisatie.MaakSpecificatie (specPad, [str(jaar), 'toon_gio_wijziging.json'], {
                'was': relPad + 'gemeenten_' + str(jaar-1) + '.gml', 
                'wijziging': relPad + 'gemeenten_' + str(jaar-1) + '_' + str(jaar) + '.gml',
                'symbolisatie': symbolisatiePad
            })
        symbolisatie.MaakSpecificatie (specPad, [str(jaren[-1]) + '_' + str(jaren[0]), 'maak_gio_wijziging.json'], {
            'was': relPad + 'gemeenten_' + str(jaren[0]) + '.gml', 
            'wordt': relPad + 'gemeenten_' + str(jaren[-1]) + '.gml', 
            'nauwkeurigheid': nauwkeurigheid,
            'symbolisatie': symbolisatiePad,
            'wijziging': relPad + 'gemeenten_' + str(jaren[0]) + '_' + str(jaren[-1]) + '.gml'
        })
        symbolisatie.MaakSpecificatie (specPad, [str(jaren[-1]) + '_' + str(jaren[0]), 'toon_gio_wijziging.json'], {
            'was': relPad + 'gemeenten_' + str(jaren[0]) + '.gml', 
            'wijziging': relPad + 'gemeenten_' + str(jaren[0]) + '_' + str(jaren[-1]) + '.gml',
            'symbolisatie': symbolisatiePad
        })
