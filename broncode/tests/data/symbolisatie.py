#==============================================================================
#
# Maken van symbolisatie, gebruikt door de data conversie scripts
#
#==============================================================================
from typing import Dict, List, Set, Tuple

import json
import os

class Symbolisatie:

    def __init__ (self, symbolenPad):
        with open (symbolenPad, 'r') as json_file:
            symbolen = json.load (json_file)
        self._Symbolen = [s["Symbolizer"] for s in sorted (symbolen, key = lambda s: s["Code"])]
        self._Symbolisaties = {}
        self._AlleWaarden = { }
        self._GIOPerMap = { }
        # Per map met GIO's: het gemeenschappelijke symbolisatiebestand (na MaakSymbolisaties)
        self._MapSymbolisatie = {}

    def GIOMappen (self):
        return self._GIOPerMap.keys ()

    def SymbolisatiePad (self, mapPad, padPrefix):
        pad = self._MapSymbolisatie.get (mapPad)
        if not pad is None:
            return padPrefix + os.path.basename (pad)
        return None

    def StartGio (self, gioPad, propertyNaam):
        self._HuidigeGIO = None
        self._HuidigePropNaam = propertyNaam
        mapPad = os.path.dirname (gioPad)
        symbolisatiePad = None if propertyNaam is None else os.path.splitext (gioPad)[0] + '_symbolisatie.xml'
        if not symbolisatiePad is None:
            self._HuidigeGIO = set ()
            self._Symbolisaties[symbolisatiePad] = (propertyNaam, self._HuidigeGIO)
            self._HuidigeMapWaarden = self._AlleWaarden.get (mapPad)
            if self._HuidigeMapWaarden is None:
                self._HuidigeMapWaarden = set ()
                self._AlleWaarden[mapPad] = (propertyNaam, self._HuidigeMapWaarden)
            else:
                self._HuidigeMapWaarden = self._HuidigeMapWaarden[1]

        gios = self._GIOPerMap.get (mapPad)
        if gios is None:
            self._GIOPerMap[mapPad] = [gioPad]
        else:
            gios.append (gioPad)

    def GIOWaarde (self, waarde):
        if not isinstance (waarde, str):
            waarde = str(waarde)
        self._HuidigeGIO.add (waarde)
        self._HuidigeMapWaarden.add (waarde)
        return '''
                <geo:''' + self._HuidigePropNaam + '>' + waarde + '</geo:' + self._HuidigePropNaam + '>'

    def MaakSymbolisaties (self, waswordtSymbolisatieFilenaam):
        symboolIndex = {}
        for mapPad, waarden in self._AlleWaarden.items ():
            symboolIndex[mapPad] = { w: idx % len (self._Symbolen) for idx, w in enumerate (sorted (waarden[1])) }
            self._MapSymbolisatie[mapPad] = os.path.join (mapPad, waswordtSymbolisatieFilenaam)
            self._Symbolisaties[self._MapSymbolisatie[mapPad]] = waarden

        for symbolisatiePad, selectie in self._Symbolisaties.items():
            symIndex = symboolIndex[os.path.dirname (symbolisatiePad)]
            with open (symbolisatiePad, 'w', encoding='utf-8') as xml_file:
                xml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<FeatureTypeStyle version="1.1.0" 
    xmlns="http://www.opengis.net/se"
    xmlns:ogc="http://www.opengis.net/ogc">
    <FeatureTypeName>geo:Locatie</FeatureTypeName>
    <SemanticTypeIdentifier>geo:''' + selectie[0] + '</SemanticTypeIdentifier>')

                for waarde in selectie[1]:
                    xml_file.write ('''
    <Rule>
        <Name>''' + waarde + '''</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>''' + selectie[0] + '''</ogc:PropertyName> 
                <ogc:Literal>''' + waarde + '''</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
        ''' + self._Symbolen[symIndex[waarde]] + '''
    </Rule>''')

                xml_file.write ('''
</FeatureTypeStyle>''')

    def MaakSymbolisatie (self, symbolisatiePad : str, attribuutnaam : str, waardeNaam : Dict[str,str]):
        with open (symbolisatiePad, 'w', encoding='utf-8') as xml_file:
            xml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
<FeatureTypeStyle version="1.1.0" 
    xmlns="http://www.opengis.net/se"
    xmlns:ogc="http://www.opengis.net/ogc">
    <FeatureTypeName>geo:Locatie</FeatureTypeName>
    <SemanticTypeIdentifier>geo:''' + attribuutnaam + '</SemanticTypeIdentifier>')

            symIndex = 0
            for waarde, naam in waardeNaam.items ():
                xml_file.write ('''
    <Rule>
        <Name>''' + naam + '''</Name>
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>''' + attribuutnaam + '''</ogc:PropertyName> 
                <ogc:Literal>''' + waarde + '''</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
        ''' + self._Symbolen[symIndex] + '''
    </Rule>''')
                symIndex += 1
                if symIndex >= len (self._Symbolen):
                    symIndex = 0

            xml_file.write ('''
</FeatureTypeStyle>''')

    def MaakReadme (self, mapPad, tekst):
        mdPad = os.path.join (*mapPad, "README.md")
        os.makedirs (os.path.dirname (mdPad), exist_ok=True)
        with open (mdPad, 'w', encoding='utf-8') as md_file:
            md_file.write (tekst)

    def MaakSpecificatie (self, mapPad, relatiefPad, jsonSpec):
        specPad = os.path.join (mapPad, *relatiefPad)
        os.makedirs (os.path.dirname (specPad), exist_ok=True)
        with open (specPad, 'w', encoding='utf-8') as json_file:
            json.dump (jsonSpec, json_file, indent=4, ensure_ascii=False)
