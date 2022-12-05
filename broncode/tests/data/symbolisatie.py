#==============================================================================
#
# Maken van symbolisatie, gebruikt door de data conversie scripts
#
#==============================================================================
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
        self.MapSymbolisatie = {}

    def GIOMappen (self):
        return self._GIOPerMap.keys ()

    def MapGIOs (self, mapPad):
        gios = self._GIOPerMap.get (mapPad)
        if not gios is None:
            return [p for p,b in gios]
        return []

    def StartGio (self, gioPad, propertyNaam, beschrijving):
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
            self._GIOPerMap[mapPad] = [(gioPad, beschrijving)]
        else:
            gios.append ((gioPad, beschrijving))

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
            self.MapSymbolisatie[mapPad] = os.path.join (mapPad, waswordtSymbolisatieFilenaam)
            self._Symbolisaties[self.MapSymbolisatie[mapPad]] = waarden

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

    def MaakToonGeoSpecificaties (self, nauwkeurigheid):
        for mapPad, gioPadenEnBeschrijving in self._GIOPerMap.items ():
            symbolisatiePad = self.MapSymbolisatie.get (mapPad)
            with open (os.path.join (mapPad, 'toon_geo.json'), 'w', encoding='utf-8') as json_file:
                json.dump ([{
                    'geometrie': os.path.basename (pad),
                    'symbolisatie': symbolisatiePad,
                    'nauwkeurigheid': str(nauwkeurigheid),
                    'beschrijving' : beschrijving
                } for pad, beschrijving in gioPadenEnBeschrijving], json_file)
