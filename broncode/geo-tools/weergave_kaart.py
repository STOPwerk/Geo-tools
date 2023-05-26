#======================================================================
#
# Hulpklasse om een of meer kaartweergaven te maken in een webpagina.
#
#======================================================================

from typing import Dict, List, Set, Tuple

from shapely.geometry import mapping

import json
import math
import re

from applicatie_request import Parameters
from data_geodata import GeoData, Attribuut
from weergave_webpagina import WebpaginaGenerator

#----------------------------------------------------------------------
#
# Generator voor kaarten in de webpagina
#
#----------------------------------------------------------------------
class KaartGenerator:

#region Initialisatie / cache
    class Cache:
        def __init__ (self, generator : WebpaginaGenerator):
            """Instantie met gegevens die door opeenvolgende operaties gedeeld moeten worden"""
            # Generator om de resultaat-pagina te maken
            self._Generator = generator
            # Status attribuut voor het opnemen van de nodige scripts/css
            # self._WebpaginaKanKaartTonen
            # Status van het toevoegen van de default symbolen
            self._DefaultSymbolenToegevoegd : Dict[int,str] = {}
            # Index voor het uitdelen van unieke namen
            self._NaamIndex = 0
            # Dimensie van alle datalagen
            self._Dimensie : Dict[str,int] = {}
            # Bounding box van alle datalagen
            self._BoundingBox : Dict[str,List[float]] = {}


    def __init__ (self, request : Parameters, generator : WebpaginaGenerator):
        """Maak een instantie van de kaartgenerator aan

        Argumenten:

        request Parameters  Parameters van het request
        generator WebpaginaGenerator De generator voor de webpagina.
        """
        self._Request = request
        self._Log = request.Log
        self._Generator = generator
        self._Cache = KaartGenerator.Cache (generator)

    def IsVoortzettingVan (self, generator : 'KaartGenerator') -> 'KaartGenerator':
        """Laat deze generator doorgaan waar de andere generator opgehouden is"""
        self._Cache = generator._Cache
        self._Generator = generator._Generator
        return self

    def _InitialiseerWebpagina (self):
        """Voeg de bestanden toe nodig om OpenLayers kaarten op te nemen in de webpagina
        """
        if not hasattr (self._Cache, '_WebpaginaKanKaartTonen'):
            setattr (self._Cache, '_WebpaginaKanKaartTonen', True)
            self._Generator.LeesCssTemplate ('ol')
            self._Generator.LeesJSTemplate ("ol", True, True)
            self._Generator.LeesJSTemplate ("sldreader", True, True)
            self._Generator.LeesCssTemplate ("kaart")
            self._Generator.LeesJSTemplate ("kaart", True, True)
            self._Generator.LeesCssTemplate ("resultaat")
            self._Generator.LeesJSTemplate ("resultaat")
#endregion

#----------------------------------------------------------------------
#
# GeoData voor gebruik in kaart in de webpagina
#
#----------------------------------------------------------------------
#region Wegschrijven als JSON voor kaart in de webpagina

    def VoegGeoDataToe (self, geoData : GeoData) -> Dict[int,str]:
        """Voeg de geo-gegevens uit een GIO of gebied toe aan de data beschikbaar in de resultaatpagina;

        Argumenten:

        geoData GeoData  Een geo-data object waarvan de locaties op de kaart weergegeven moeten worden

        Geeft de namen terug die gebruikt moet worden om de gegevens aan een kaart te koppelen
        """
        if geoData is None:
            self._Log.Detail ('Geen geo-data beschikbaar dus niet toegevoegd aan de kaartgegevens')
            return
        if not geoData._KaartgegevensNamen is None:
            # Is al eerder geregistreerd
            return geoData._KaartgegevensNamen

        self._Cache._NaamIndex += 1
        geoData._KaartgegevensNamen = {}
        for dimensie, locaties in geoData.Locaties.items ():
            gegevensNaam = 'data' + str(self._Cache._NaamIndex) + '_' + str(dimensie)
            geoData._KaartgegevensNamen[dimensie] = gegevensNaam
            self._Cache._Dimensie[gegevensNaam] = dimensie
            self._Log.Detail ('VoegGeoDataToe: ' + gegevensNaam)

            collectie = {
                'type' : 'FeatureCollection',
                'crs': { 'type': 'name', 'properties': { 'name': 'urn:ogc:def:crs:EPSG::28992' } },
                'features' : locaties
            }
            # Bepaal de properties die op de kaart getoond kan worden
            if len (geoData.Attributen) > 0:
                collectie['properties'] = {a.Tag : [a.Label, '' if a.Eenheid is None else a.Eenheid] for a in geoData.Attributen.values ()} 

            if not geoData.GIODelen is None:
                collectie['properties']['GIO-deel'] = ['GIO-deel', '']
                collectie['features'] = []
                for locatie in locaties:
                    toon = locatie.copy ()
                    toon['properties'] = locatie['properties'].copy ()
                    toon['properties']['GIO-deel'] = geoData.GIODelen[toon['properties']['groepID']].Label
                    collectie['features'].append (toon)

            # Bepaal de bounding box van de hele collectie
            bbox = None
            for locatie in locaties:
                locatieShape = GeoData.MaakShapelyShape (locatie)
                if not locatieShape.is_empty:
                    locatieBBox = locatieShape.bounds
                    if bbox is None:
                        bbox = list (locatieBBox)
                    else:
                        bbox = [
                                bbox[0] if bbox[0] < locatieBBox[0] else locatieBBox[0],
                                bbox[1] if bbox[1] < locatieBBox[1] else locatieBBox[1],
                                bbox[2] if bbox[2] > locatieBBox[2] else locatieBBox[2],
                                bbox[3] if bbox[3] > locatieBBox[3] else locatieBBox[3]
                            ]
            if not bbox is None:
                collectie['bbox'] = bbox
                self._Cache._BoundingBox[gegevensNaam] = bbox

            # Voeg toe aan de scripts van de pagina
            self._InitialiseerWebpagina ()
            self._Generator.VoegSlotScriptToe ('\nKaartgegevens.Instantie.VoegDataToe ("' + gegevensNaam + '",\n' + json.dumps (collectie, cls=KaartGenerator._JsonGeoEncoder, ensure_ascii=False) + '\n);\n')
            self._Log.Detail ('GeoData toegevoegd: ' + gegevensNaam)
        return geoData._KaartgegevensNamen

    class _JsonGeoEncoder (json.JSONEncoder):
        def default(self, o):
            """Objecten worden niet meegenomen"""
            return None
#endregion

#----------------------------------------------------------------------
#
# Symbolisatie voor gebruik in kaart in de webpagina
#
#----------------------------------------------------------------------
#region Symbolisatie

    def VoegDefaultSymbolisatieToe (self, dimensie) -> str:
        """Voeg de default symbolisatie toe voor de geodata
        
        Argumenten:

        dimensie int  Dimensie waarvoor de default symbolisatie toegevoegd moet worden

        Geeft de naam terug die gebruikt moet worden om de symbolisatie aan geodata voor een kaart te koppelen
        """
        return self.VoegUniformeSymbolisatieToe (dimensie, "#0000FF", "#0000CD")

    def VoegUniformeSymbolisatieToe (self, dimensie : int, vulkleur: str, randkleur: str, opacity : str = '1') -> str:
        """Voeg een STOP symbolisatie toe voor gebruik in kaarten.

        Argumenten:

        dimensie int  De dimensie van de geodata
        vulkleur str  De #hexcode van de te gebruiken kleur voor de opvulling van een symbool.
        randkleur str  De #hexcode van de te gebruiken kleur voor de rand van een symbool.

        Geeft de naam terug die gebruikt moet worden om de symbolisatie aan geodata voor een kaart te koppelen
        """
        key = str(dimensie) + vulkleur + '\n' + randkleur + '\n' + opacity
        naam = self._Cache._DefaultSymbolenToegevoegd.get (key)
        if naam is None:
            if dimensie == 0:
                rule = '''
    <Rule>
        <Name>Punt</Name>
        <PointSymbolizer>
            <Graphic>
                <Mark>
                    <WellKnownName>square</WellKnownName>
                    <Fill>
                        <SvgParameter name="fill">''' + vulkleur + '''</SvgParameter>
                        <SvgParameter name="fill-opacity">''' + opacity + '''</SvgParameter>
                    </Fill>
                    <Stroke>
                        <SvgParameter name="stroke">''' + randkleur + '''</SvgParameter>
                        <SvgParameter name="stroke-opacity">1</SvgParameter>
                        <SvgParameter name="stroke-width">1</SvgParameter>
                    </Stroke>
                </Mark>
                <Size>12</Size>
                <Rotation>0</Rotation>
            </Graphic>
        </PointSymbolizer>
    </Rule>'''
            elif dimensie == 1:
                rule = '''
    <Rule>
        <Name>Lijn</Name>
        <LineSymbolizer>
            <Stroke>
                <SvgParameter name="stroke">''' + randkleur + '''</SvgParameter>
                <SvgParameter name="stroke-opacity">1</SvgParameter>
                <SvgParameter name="stroke-width">3</SvgParameter>
                <SvgParameter name="stroke-linecap">butt</SvgParameter>
            </Stroke>
        </LineSymbolizer>
    </Rule>'''
            elif dimensie == 2:
                rule = '''
    <Rule>
        <Name>Vlak</Name>
        <PolygonSymbolizer>
            <Fill>
                <SvgParameter name="fill">''' + vulkleur + '''</SvgParameter>
                <SvgParameter name="fill-opacity">''' + opacity + '''</SvgParameter>
            </Fill>
            <Stroke>
                <SvgParameter name="stroke">''' + randkleur + '''</SvgParameter>
                <SvgParameter name="stroke-opacity">1</SvgParameter>
                <SvgParameter name="stroke-width">3</SvgParameter>
                <SvgParameter name="stroke-linejoin">round</SvgParameter>
            </Stroke>
        </PolygonSymbolizer>
    </Rule>'''
            self._Cache._DefaultSymbolenToegevoegd[key] = naam =  self.VoegSymbolisatieToe (KaartGenerator._MaakFeatureTypeStyle ([rule]))
        return naam


    def VoegSymbolisatieToe (self, symbolisatie : str):
        """Voeg een STOP symbolisatie toe voor gebruik in kaarten.

        Argumenten:

        naam str  De naam die gebruikt moet worden om de symbolisatie toe te passen
        symbolisatie str  De XML van een STOP symbolisatie module.

        Geeft de naam terug die gebruikt moet worden om de symbolisatie aan geodata voor een kaart te koppelen
        """
        # Verwijder <?xml ?> regel indien aanwezig
        if symbolisatie is None:
            self._Log.Detail ('Geen symbolisatie beschikbaar dus niet toegevoegd aan de kaartgegevens')
            return
        symbolisatie = KaartGenerator._StripHeader.sub ('', symbolisatie)

        # Voeg toe aan de scripts van de pagina
        self._InitialiseerWebpagina ()
        self._Cache._NaamIndex += 1
        naam = 'sym' + str(self._Cache._NaamIndex)
        self._Generator.VoegSlotScriptToe ('\nKaartgegevens.Instantie.VoegSymbolisatieToe ("' + naam + '",`' + symbolisatie + '`);\n')
        return naam

    _StripHeader = re.compile ("^\s*<\?\s*[^>]+>\s*\n")

    @staticmethod
    def _MaakFeatureTypeStyle (rules : List[str]):
        """Verpak de rules in een FeatureTypeStyle, dus als STOP module"""
        return '''<FeatureTypeStyle version="1.1.0"
    xmlns="http://www.opengis.net/se"
    xmlns:ogc="http://www.opengis.net/ogc">
    <FeatureTypeName>geo:Locatie</FeatureTypeName>
    <SemanticTypeIdentifier>geo:geometrie</SemanticTypeIdentifier>''' + '''
'''.join (rules) + '''
</FeatureTypeStyle>'''

    def VoegWijzigMarkeringToe (self, dimensie : int, revisie : bool = False):
        """Voeg de symbolisatie voor de speciale wijzigmarkeringen toe en geef de naam terug"""
        key  = 'WM' + str(dimensie) + str(revisie)
        naam = self._Cache._DefaultSymbolenToegevoegd.get (key)
        if naam is None:
            self._Cache._DefaultSymbolenToegevoegd[key] = naam = self.VoegSymbolisatieToe (KaartGenerator.WijzigMarkeringSymbolisatie (dimensie, revisie))
        return naam

    @staticmethod
    def WijzigMarkeringSymbolisatie (dimensie : int, revisie : bool = False):
        """Geef de symbolisatie voor de speciale wijzigmarkeringen"""
        return KaartGenerator._MaakFeatureTypeStyle ([KaartGenerator._RevisieMarkeringSymbolisatie[dimensie] if revisie else KaartGenerator._WijzigMarkeringSymbolisatie[dimensie]])

    _WijzigMarkeringSymbolisatie = { 0: '''
    <Rule>
        <Name>Punt</Name>
        <PointSymbolizer>
            <Graphic>
                <Mark>
                    <WellKnownName>star</WellKnownName>
                    <Fill>
                        <SvgParameter name="fill">#000000</SvgParameter>
                        <SvgParameter name="fill-opacity">1</SvgParameter>
                    </Fill>
                </Mark>
                <Size>35</Size>
                <Rotation>0</Rotation>
            </Graphic>
        </PointSymbolizer>
        <PointSymbolizer>
            <Graphic>
                <Mark>
                    <WellKnownName>star</WellKnownName>
                    <Fill>
                        <SvgParameter name="fill">#00A800</SvgParameter>
                        <SvgParameter name="fill-opacity">1</SvgParameter>
                    </Fill>
                </Mark>
                <Size>29</Size>
                <Rotation>0</Rotation>
            </Graphic>
        </PointSymbolizer>
        <PointSymbolizer>
            <Graphic>
                <Mark>
                    <WellKnownName>circle</WellKnownName>
                    <Fill>
                        <SvgParameter name="fill">#A80000</SvgParameter>
                        <SvgParameter name="fill-opacity">1</SvgParameter>
                    </Fill>
                </Mark>
                <Size>11</Size>
                <Rotation>0</Rotation>
            </Graphic>
        </PointSymbolizer>
    </Rule>''',
     1: '''
    <Rule>
        <Name>Lijn</Name>
        <LineSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#000000</CssParameter>
                <CssParameter name="stroke-width">5</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
            </Stroke>
        </LineSymbolizer>
        <LineSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#A80000</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
            </Stroke>
        </LineSymbolizer>
        <LineSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#00A800</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
                <CssParameter name="stroke-dasharray">5 8</CssParameter>
            </Stroke>
        </LineSymbolizer>
    </Rule>''',
     2: '''
    <Rule>
        <Name>Vlak</Name>
        <PolygonSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#000000</CssParameter>
                <CssParameter name="stroke-width">5</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
            </Stroke>
        </PolygonSymbolizer>
        <PolygonSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#A80000</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
            </Stroke>
        </PolygonSymbolizer>
        <PolygonSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#00A800</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
                <CssParameter name="stroke-dasharray">5 8</CssParameter>
            </Stroke>
        </PolygonSymbolizer>
    </Rule>'''
    }

    _RevisieMarkeringSymbolisatie = { 0: '''
    <Rule>
        <Name>Punt</Name>
        <PointSymbolizer>
            <Graphic>
                <Mark>
                    <WellKnownName>star</WellKnownName>
                    <Fill>
                        <SvgParameter name="fill">#007bc7</SvgParameter>
                        <SvgParameter name="fill-opacity">1</SvgParameter>
                    </Fill>
                </Mark>
                <Size>35</Size>
                <Rotation>0</Rotation>
            </Graphic>
        </PointSymbolizer>
        <PointSymbolizer>
            <Graphic>
                <Mark>
                    <WellKnownName>star</WellKnownName>
                    <Fill>
                        <SvgParameter name="fill">#b2d7ee</SvgParameter>
                        <SvgParameter name="fill-opacity">1</SvgParameter>
                    </Fill>
                </Mark>
                <Size>29</Size>
                <Rotation>0</Rotation>
            </Graphic>
        </PointSymbolizer>
        <PointSymbolizer>
            <Graphic>
                <Mark>
                    <WellKnownName>circle</WellKnownName>
                    <Fill>
                        <SvgParameter name="fill">#007bc7</SvgParameter>
                        <SvgParameter name="fill-opacity">1</SvgParameter>
                    </Fill>
                </Mark>
                <Size>11</Size>
                <Rotation>0</Rotation>
            </Graphic>
        </PointSymbolizer>
        <PointSymbolizer>
            <Graphic>
                <Mark>
                    <WellKnownName>circle</WellKnownName>
                    <Fill>
                        <SvgParameter name="fill">#b2d7ee</SvgParameter>
                        <SvgParameter name="fill-opacity">1</SvgParameter>
                    </Fill>
                </Mark>
                <Size>7</Size>
                <Rotation>0</Rotation>
            </Graphic>
        </PointSymbolizer>
    </Rule>''',
     1: '''
    <Rule>
        <Name>Lijn</Name>
        <LineSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#007bc7</CssParameter>
                <CssParameter name="stroke-width">5</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
            </Stroke>
        </LineSymbolizer>
        <LineSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#b2d7ee</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
            </Stroke>
        </LineSymbolizer>
    </Rule>''',
     2: '''
    <Rule>
        <Name>Vlak</Name>
        <PolygonSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#007bc7</CssParameter>
                <CssParameter name="stroke-width">5</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
            </Stroke>
        </PolygonSymbolizer>
        <PolygonSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#b2d7ee</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
            </Stroke>
        </PolygonSymbolizer>
    </Rule>'''
    }
#endregion

#======================================================================
#
# Weergave op de kaart
#
#======================================================================

#----------------------------------------------------------------------
#
# Kaart in webpagina
#
#----------------------------------------------------------------------
#region Kaart in webpagina
    class Kaart:
        def __init__ (self, generator : 'KaartGenerator'):
            """Maak een nieuwe kaart om dadelijk te tonen"""
            self._Generator = generator
            self._Generator._InitialiseerWebpagina ()
            self._Generator._Cache._NaamIndex += 1
            # Initialisatie van de kaartlagen (per dimensie)
            self._InitialisatieScripts = { 0 : '', 1: '', 2: '' }
            self._DimensieLaatsteWijzigingInitialisatieScripts = None
            # Bounding box van alle lagen tot nu toe
            self._BoundingBox = None
            # Opties om door te geven aan de kaart
            self._Opties = {
                'kaartelementId': 'kaart_' + str(self._Generator._Cache._NaamIndex),
                'kaartelementWidth': 900,
                'kaartelementHeight': 600
            }
            nauwkeurigheid = self._Generator._Request.LeesString ("toepassingsnauwkeurigheid");
            if not nauwkeurigheid is None:
                self._Opties['toepassingsnauwkeurigheid'] = int (nauwkeurigheid)
            self._Generator._Log.Detail ("Prepareer kaart " + self._Opties['kaartelementId'])


        def VoegLagenToe (self, naam : str, dataNamen : Dict[int,str], symbolisatieNamen : Dict[int,str], inControls : bool = False, toonInitieel : bool = True, negeerBBox : bool = False, postLaag = None):
            """Voeg alle GeoData locaties met symbolisatie toe aan de kaart
            
            Argumenten:

            naam str  Naam van de kaart zoals gebruikt bij de weergave van properties en bij het aan/uit zetten van lagen
            dataNamen Dict[int,str]  Namen van de geodata die getoond moet worden, zoals verkregen uit de VoegGeoDataToe
            symbolisatieNamen Dict[int,str]  Namen van de symbolisatie, zoals verkregen uit een van de Voeg*Toe methoden
            inControls bool  Geeft aan dat de laag aan/uit gezet kan worden door de eindgebruiker
            toonInitieel bool  Geeft aan dat de kaart bij weergave ven de kaart zichtbaar moet zijn.
            negeerBBox bool  Negeer de uitgestrektheid van de laag voor de bepaling van de initiële kaartview
            postLaag lambda  Methode die aangeroepen wordt nadat een kaartlaag is toegevoegd, met als argument de dimensie 
                             van de geometrie in de toegevoegde laag.
            """
            for dimensie, dataNaam in dataNamen.items ():
                self.VoegLaagToe (naam, dataNaam, symbolisatieNamen.get (dimensie), inControls, toonInitieel, negeerBBox)
                if not postLaag is None:
                    postLaag (dimensie)


        def VoegLaagToe (self, naam : str, dataNaam : str, symbolisatieNaam : str, inControls : bool = False, toonInitieel : bool = True, negeerBBox : bool = False):
            """Voeg data met symbolisatie toe aan de kaart
            
            Argumenten:

            naam str  Naam van de kaart zoals gebruikt bij de weergave van properties en bij het aan/uit zetten van lagen
            dataNaam str  Naam van de geodata die getoond moet worden, zoals verkregen uit de VoegGeoDataToe
            symbolisatieNaam str  Naam van de symbolisatie, zoals verkregen uit een van de Voeg*Toe methoden
            inControls bool  Geeft aan dat de laag aan/uit gezet kan worden door de eindgebruiker
            toonInitieel bool  Geeft aan dat de kaart bij weergave ven de kaart zichtbaar moet zijn.
            negeerBBox bool  Negeer de uitgestrektheid van de laag voor de bepaling van de initiële kaartview
            """
            self._Generator._Log.Detail ("Voeg laag toe: '" + naam + "' (" + dataNaam + ")")
            self._DimensieLaatsteWijzigingInitialisatieScripts= self._Generator._Cache._Dimensie[dataNaam]
            self._InitialisatieScripts[self._DimensieLaatsteWijzigingInitialisatieScripts] += ';\nkaart.VoegLaagToe ("' + naam + '", "' + dataNaam + '", "' + symbolisatieNaam + '")'
            if inControls:
                self.LaatsteLaagInControls (toonInitieel)
            if not negeerBBox:
                bbox = self._Generator._Cache._BoundingBox.get (dataNaam)
                if not bbox is None:
                    if self._BoundingBox is None:
                        self._BoundingBox = bbox
                    else:
                        self._BoundingBox = [
                                self._BoundingBox[0] if self._BoundingBox[0] < bbox[0] else bbox[0],
                                self._BoundingBox[1] if self._BoundingBox[1] < bbox[1] else bbox[1],
                                self._BoundingBox[2] if self._BoundingBox[2] > bbox[2] else bbox[2],
                                self._BoundingBox[3] if self._BoundingBox[3] > bbox[3] else bbox[3]
                            ]

        def LaatsteLaagInControls (self, toonInitieel : bool = True):
            """Geeft aan dat de laatst toegevoegde laag aan/uit gezet kan worden door de eindgebruiker
            
            Argumenten:

            toonInitieel bool  Geeft aan dat de kaart bij weergave ven de kaart zichtbaar moet zijn.
            """
            self._InitialisatieScripts[self._DimensieLaatsteWijzigingInitialisatieScripts] += '.AlsAanUitLaag (' + ('true' if toonInitieel else 'false') + ')'


        def VoegOudLaagToe (self, naam : str, dataNaam : str, symbolisatieNaam : str, inControls : bool = False, toonInitieel : bool = True):
            """Voeg data met symbolisatie toe aan de kaart als een oude/was-laag
            
            Argumenten:

            naam str  Naam van de kaart zoals gebruikt bij de weergave van properties (wordt " (oud)" achter gezet) en bij het aan/uit zetten van lagen
            dataNaam str  Naam van de geodata die getoond moet worden, zoals verkregen uit de VoegGeoDataToe
            symbolisatieNaam str  Naam van de symbolisatie, zoals verkregen uit een van de Voeg*Toe methoden
            inControls bool  Geeft aan dat de laag aan/uit gezet kan worden door de eindgebruiker
            toonInitieel bool  Geeft aan dat de kaart bij weergave ven de kaart zichtbaar moet zijn.
            """
            self.VoegLaagToe (naam, dataNaam, symbolisatieNaam, inControls, toonInitieel)
            self.LaatsteLaagAlsOud ()

        def LaatsteLaagAlsOud (self):
            """Geeft aan dat de laatst toegevoegde laag een oude/was-laag is.
            """
            self._InitialisatieScripts[self._DimensieLaatsteWijzigingInitialisatieScripts] += '.AlsOudLaag ()'

        def VoegNieuwLaagToe (self, naam : str, dataNaam : str, symbolisatieNaam : str, inControls : bool = False, toonInitieel : bool = True):
            """Voeg data met symbolisatie toe aan de kaart als een nieuwe/wordt-laag
            
            Argumenten:

            naam str  Naam van de kaart zoals gebruikt bij de weergave van properties (wordt " (nieuw)" achter gezet) en bij het aan/uit zetten van lagen
            dataNaam str  Naam van de geodata die getoond moet worden, zoals verkregen uit de VoegGeoDataToe
            symbolisatieNaam str  Naam van de symbolisatie, zoals verkregen uit een van de Voeg*Toe methoden
            inControls bool  Geeft aan dat de laag aan/uit gezet kan worden door de eindgebruiker
            toonInitieel bool  Geeft aan dat de kaart bij weergave ven de kaart zichtbaar moet zijn.
            """
            self.VoegLaagToe (naam, dataNaam, symbolisatieNaam, inControls, toonInitieel)
            self.LaatsteLaagAlsNieuw ()

        def LaatsteLaagAlsNieuw (self):
            """Geeft aan dat de laatst toegevoegde laag een nieuwe/wordt-laag is.
            """
            self._InitialisatieScripts[self._DimensieLaatsteWijzigingInitialisatieScripts] += '.AlsNieuwLaag ()'

        def LaatsteLaagZoomLevel (self, minZoom : int, maxZoom : int):
            """Geeft aan dat de laatst toegevoegde laag alleen in het aangegeven bereik van zoom levels getoond mag worden.

            Argumenten:

            minZoom int  Het meest uitgezoomde zoom-leve waarop de kaart getoond mag worden, of None als er geen bepering is
            mazZoom int  Het meest ingezoomde zoom-leve waarop de kaart getoond mag worden, of None als er geen bepering is
            """
            self._InitialisatieScripts[self._DimensieLaatsteWijzigingInitialisatieScripts] += '.LimiteerZoomLevel (' + str(0 if minZoom is None else minZoom) + ', ' + str(100 if maxZoom is None else maxZoom) + ')'

        def ZoomTotNauwkeurigheid (self, extraZoom : bool):
            """Geeft aan dat het maximale zoom level overen moet komen met de toepassingsnauwkeurigheid
            
            Argumenten:

            extraZoom bool  Geeft aan dat er extra zoom levels moeten zijn zodat het effect van de toepassingsnauwkeurigheid te zien is
            """
            nauwkeurigheid = self._Generator._Request.ToepassingsnauwkeurigheidInCentimeter (False)
            if nauwkeurigheid is None:
                self._Opties.pop ('maxZoom', None)
            else:
                maxZoom = 22 - math.floor(math.log2(nauwkeurigheid))
                self._Opties['maxZoom'] = (22 if maxZoom > 22 else maxZoom) + (4 if extraZoom else 0)

        def Toon (self):
            """Toon een kaart op de huidige plaats in de webpagina"""
            self._Generator._Log.Detail ("Toon kaart " + self._Opties['kaartelementId'])
            self._Generator._Generator.VoegHtmlToe (self._Generator._Generator.LeesHtmlTemplate ("kaart", False).replace ('<!--ID-->', self._Opties['kaartelementId']))
            if not self._BoundingBox is None:
                self._Opties['bbox'] = self._BoundingBox
            
            self._Generator._Generator.VoegSlotScriptToe ('\nwindow.addEventListener("load", function () {\nvar kaart = new Kaart ()' + ''.join (self._InitialisatieScripts[d] for d in [2,1,0]) + ';\nkaart.Toon (' + json.dumps (self._Opties) + ');\n});')
#endregion

#----------------------------------------------------------------------
#
# Zoom-gerelateerde functionaliteit
#
#----------------------------------------------------------------------
#region Zoom levels
    @staticmethod
    def MaximaalZoomLevel (nauwkeurigheidCentimeter : int):
        """Maximaal zoom level voor een GIO bij gegeven nauwkeurigheid.
        
        Argumenten:

        nauwkeurigheidCentimeter int  Toepassingsnauwkeurigheid van de GIO.
        """
        maxZoom = 22 - math.floor(math.log2(10*nauwkeurigheidCentimeter))
        return 22 if maxZoom > 22 else maxZoom

    @staticmethod
    def ZoomLevelDetailPerMeter (zoomLevel : int):
        """Geef de kleinst zichtbare details voor een zoomlevel bij gegeven nauwkeurigheid
        
        Argumenten:

        zoomLevel int  Zoom level, kan niet groter zijn dan MaximaalZoomLevel
        """
        return 0.1 * math.pow (2, (22 - zoomLevel) if zoomLevel < 22 else 0)
#endregion

#region Grid met tegels (voor clustering van geometrieën en markeringen)
    @staticmethod
    def _GridCelNaarRD (dpm : float, cel : Tuple[int,int]) -> List[float]:
        """Conversie van grid cellen naar de coördinaten van het centrum van de cellen:

        Argumenten:
        dpm float  Uitkomst van ZoomLevelDetailPerMeter
        cel (x,y) Index van de cel als gemaat door _GridCelVoorPunt

        Geeft terug: De coördinaten van het centrum van de cel
        """
        return [KaartGenerator._GridCenterX + cel[0] * dpm, KaartGenerator._GridCenterY + cel[1] * dpm]

    @staticmethod
    def _PastGeometrieInGridCel (dpm : float, locatie) -> Tuple[Tuple[int,int],int,int]:
        """Bekijk welke cellen bedekt worden door de geometrie. Geeft de cel met kleinste X,Y terug, en het aantal cellen in X en in Y.


        Argumenten:
        dpm float  Uitkomst van ZoomLevelDetailPerMeter
        locatie object  Locatie van GeoData
        """
        locatieShape = GeoData.MaakShapelyShape (locatie)
        cel = KaartGenerator._GridCelVoorPunt (dpm, [locatieShape.bounds[0], locatieShape.bounds[1]])
        dx = KaartGenerator._GridCelVoorPunt (dpm, [locatieShape.bounds[2], locatieShape.bounds[1]])[0] - cel[0] + 1
        dy = KaartGenerator._GridCelVoorPunt (dpm, [locatieShape.bounds[0], locatieShape.bounds[3]])[1] - cel[1] + 1
        return (cel, dx, dy)

    @staticmethod
    def _GridCelVoorPunt (dpm : float, coords : List[float]) -> Tuple[int,int]:
        """Geef terug in welke grid cel een punt ligt.

        Argumenten:
        dpm float  Uitkomst van ZoomLevelDetailPerMeter
        coords [.,.]  Coördinaten van het punt
        """
        x = round ((coords[0] - KaartGenerator._GridCenterX) / dpm)
        y = round ((coords[1] - KaartGenerator._GridCenterY) / dpm)
        return (x,y)

    _GridCenterX = 142735.75
    _GridCenterY = 470715.91
#endregion

#region Clustering van punten en vereenvoudiging van features

    class CelData:
        def __init__ (self, rdX, rdY):
            """Maak data voor een nieuwe grid cel"""
            self.Aantal = 1
            self._SomX = rdX
            self._SomY = rdY

        def VoegToe (self, rdX, rdY):
            """Voeg een geometrie met gegeven positie toe aan de grid cel"""
            self.Aantal += 1
            self._SomX += rdX
            self._SomY += rdY

        def Combineer (self, data : 'CelData'):
            """Combineer grid data"""
            if not data is None:
                self.Aantal += data.Aantal
                self._SomX += data._SomX
                self._SomY += data._SomY
                return True
            return False

        def CelX (self):
            """Bepaal de gewogen X-positie van de geometrieën"""
            return math.floor (self._SomX / self.Aantal)
        def CelY (self):
            """Bepaal de gewogen Y-positie van de geometrieën"""
            return math.floor (self._SomY / self.Aantal)

    class SchaalafhankelijkeGeometrie:
        def __init__ (self):
            # Het zoom-level waarvoor deze geo-data is gemaakt.
            # Zoom-level is zoals gebruikt in OpenLayers.
            self.VoorZoomLevel = None
            # De overgebleven vereenvoudigde/schaalafhankelijke features
            self.Features : GeoData = None
            # Geeft aan waar in een grid hoeveel geometrieën gelokaliseerd zijn die in verband met 
            # de resolutie niet meer getoond worden.
            # Dit zijn (X,Y) coordinaten in een grid met cellen:
            # - Lengte en breedte zijn ZoomLevelDetailPerMeter
            # - Centrum van de cel is _GridCenterX + X * ZoomLevelDetailPerMeter, _GridCenterY + Y * ZoomLevelDetailPerMeter
            self.MarkeringenGridCel : GeoData = None

    class SchaalafhankelijkeGeoData:
        def __init__ (self, bronData : GeoData):
            # GeoData waarvoor de schaalafhankelijke features gemaakt worden
            self.BronData : GeoData = bronData
            self.Nauwkeurigheid : float = None
            # De schaalafhankelijke geodata per zomlevel, voor oplopende zoomlevel. De brondata is hierin als eerste opgenomen.
            self.ZoomLevels : List[KaartGenerator.SchaalafhankelijkeGeometrie] = []
            # Naam van de kaart zoals gebruikt bij het aan/uit zetten van lagen
            self.Naam = None
            # Geeft aan dat de laag aan/uit gezet kan worden door de eindgebruiker
            self.InControls = False
            # Geeft aan dat de kaart bij weergave ven de kaart zichtbaar moet zijn.
            self.ToonInitieel = False

    def MaakSchaalafhankelijkeGeometrie (self, geoData : GeoData, naam : str, inControls : bool = False, toonInitieel : bool = True) -> SchaalafhankelijkeGeoData:
        """Vereenvoudig de geometrieën in de locaties voor weergave, waarbij
        voor lagere zoom-levels (verder uitgezoomd) minder detail getoond wordt.

        Argumenten:

        geoData GeoData  De geoData die schaalafhankelijk weergegeven moeten worden.
        naam str  Naam van de kaart zoals gebruikt bij de weergave van properties (wordt " (nieuw)" achter gezet) en bij het aan/uit zetten van lagen
        inControls bool  Geeft aan dat de laag aan/uit gezet kan worden door de eindgebruiker
        toonInitieel bool  Geeft aan dat de kaart bij weergave ven de kaart zichtbaar moet zijn.

        Geeft de vereenvoudigde geometrieën en markers als GeoData terug.
        """
        nauwkeurigheid = geoData.Toepassingsnauwkeurigheid
        if nauwkeurigheid is None:
            nauwkeurigheid = self._Request.ToepassingsnauwkeurigheidInCentimeter (False)
            if nauwkeurigheid is None:
                nauwkeurigheid = 10
        self._Log.Detail ("Maak schaalafhankelijke geometrie met toepassingsnauwkeurigheid " + str (nauwkeurigheid) + " centimeter")
        resultaat = KaartGenerator.SchaalafhankelijkeGeoData (geoData)
        resultaat.Nauwkeurigheid = nauwkeurigheid
        resultaat.Naam = naam
        resultaat.InControls = inControls
        resultaat.ToonInitieel = toonInitieel

        # Meest ingezoomde laag zijn de originele features
        ditNiveau = KaartGenerator.SchaalafhankelijkeGeometrie ()
        ditNiveau.Features = geoData
        resultaat.ZoomLevels.append (ditNiveau)

        # Ga uit van de enkelvoudige geometrieën voor punten, hou de geometrieën voor lijnen en vlakken
        geometrieVoorgaandNiveau : Dict[int,List[GeoData.EnkeleGeometrie]] = geoData.MaakLijstVanGeometrieen ({0})[0]

        halveExtraMarkerSchaal = 5 # Factor om ervoor te zorgen dat er geen geometrieën achter de markers verdwijnen; geheel getal
        minimaleCelGrootte = 3 # Als een geometrie binnen minimaleCelGrootte x minimaleCelGrootte vellen ligt, dan wordt de geometrie vervangen door een marker

        # Key = (x,y) van cel, value = aantal geometrieën, som van X, som van Y
        markeringenVoorgaandeNiveau : Dict[Tuple[int,int], KaartGenerator.CelData] = {}
        voorgaandeCelDeler = 2
        for zoomLevel in range (self.MaximaalZoomLevel (nauwkeurigheid), 0, -1):
            locatiesAndersDanVoorgaande = False
            cellenAndersDanVoorgaande = False

            # Neem de grid cellen uit het voorgaande niveau over op dit niveau
            markeringenDitNiveau : Dict[Tuple[int,int], KaartGenerator.CelData]= {}
            for celVoorgaandNiveau, voorgaandeData in markeringenVoorgaandeNiveau.items ():
                celDitNiveau = (celVoorgaandNiveau[0] // voorgaandeCelDeler, celVoorgaandNiveau[1] // voorgaandeCelDeler)
                data = markeringenDitNiveau.get (celDitNiveau)
                if data is None:
                    markeringenDitNiveau[celDitNiveau] = voorgaandeData
                else:
                    cellenAndersDanVoorgaande = True # Dit niveau beslaat minder cellen
                    data.Combineer (voorgaandeData)

            dpm = self.ZoomLevelDetailPerMeter (zoomLevel)
            geometrieDitNiveau : Dict[int,List[GeoData.EnkeleGeometrie]] = {}
            # puntCellen zijn cellen voor de geometrieën in deze zoomlaag die mogelijk alleen in een cel liggen
            puntCellen : Dict[Tuple[int,int], GeoData.EnkeleGeometrie] = {}
            for dimensie, enkeleGeometrieen in geometrieVoorgaandNiveau.items ():
                if len (enkeleGeometrieen) == 0:
                    continue
                geometrieDitNiveau[dimensie] = []
                if dimensie == 0:
                    # Behandel punten niet meer als losse geometrie als er meerdere in een grid cel vallen
                    for enkeleGeometrie in enkeleGeometrieen:
                        punt = enkeleGeometrie.Geometrie['geometry']['coordinates']
                        cel = self._GridCelVoorPunt (dpm, punt)
                        data = markeringenDitNiveau.get (cel)
                        if not data is None:
                            # Er zijn al meer punten in deze cel
                            data.VoegToe (punt[0], punt[1])
                            locatiesAndersDanVoorgaande = cellenAndersDanVoorgaande = True # Dit niveau heeft minder punten
                        else:
                            # Tot nu toe het enige punt
                            puntCellen[cel] = enkeleGeometrie
                            # Voeg het wel alvast als markeringpunt toe, zodat de samenvoeging van naburige cellen uitgevoerd kan worden
                            data = KaartGenerator.CelData (punt[0], punt[1])
                            markeringenDitNiveau[cel] = data
                else:
                    # Laat een lijn-locatie of vlak-locatie weg als het helemaal in een grid cel valt
                    for enkeleGeometrie in enkeleGeometrieen:
                        cel, dx, dy = self._PastGeometrieInGridCel (dpm, enkeleGeometrie.Geometrie)
                        if dx <= minimaleCelGrootte and dy <= minimaleCelGrootte:
                            # Ja, laat de geometrie weg
                            data = markeringenDitNiveau.get (cel)
                            shape = GeoData.MaakShapelyShape (enkeleGeometrie.Geometrie)
                            if data is None:
                                markeringenDitNiveau[cel] = KaartGenerator.CelData ((shape.bounds[0] + shape.bounds[2])/2, (shape.bounds[1] + shape.bounds[3])/2)
                            else:
                                data.VoegToe ((shape.bounds[0] + shape.bounds[2])/2, (shape.bounds[1] + shape.bounds[3])/2)
                            locatiesAndersDanVoorgaande= cellenAndersDanVoorgaande = True # Dit niveau heeft minder geometrieën
                        else:
                            # Nee, simplificeer de geometrie
                            vorigeShape = GeoData.MaakShapelyShape (enkeleGeometrie.Geometrie)
                            shape = vorigeShape.simplify (dpm)
                            if not shape.__eq__ (vorigeShape):
                                locatiesAndersDanVoorgaande = True # Andere geometrie
                                enkeleGeometrie.Geometrie = {
                                    'type': 'Feature',
                                    'geometry': mapping(shape),
                                    '_shape': shape
                                }
                            geometrieDitNiveau[dimensie].append (enkeleGeometrie)

            # Het is nu mogelijk dat twee nabije geometrieën in twee naburige cellen terecht
            # komen, bijv met x-index = 127 en x = 128. Het volgende zoomniveau zijn het nog
            # steeds twee cellen, met x-index 63 en 64. Combineer daarom steeds naburige cellen,
            # daardoor zal de versmelting van naburige geometrieën wel plaatsvinden. Bovendien
            # wordt de afstand tussen naburige markers daardoor groter
            samengevoegd : Dict[Tuple[int,int], KaartGenerator.CelData] = {} 
            for cel in list (markeringenDitNiveau.keys ()):
                data = markeringenDitNiveau.pop (cel, None)
                if not data is None:
                    for dx in range (-2 - halveExtraMarkerSchaal, 2 + halveExtraMarkerSchaal): # Combineer 4x4 cellen
                        for dy in range (-2 - halveExtraMarkerSchaal, 2 + halveExtraMarkerSchaal):
                            if dx == 0 and dy == 0:
                                continue
                            buur = (cel[0] + dx, cel[1] + dy)
                            if data.Combineer (markeringenDitNiveau.pop (buur, None)):
                                cellenAndersDanVoorgaande = True

                    if data.Aantal == 1 and cel in puntCellen:
                        # Dit moet een punt in een enkele grid cel zijn
                        geometrieDitNiveau[0].append (puntCellen.pop (cel))
                    else:
                        # Ken dat toe aan de juiste grid cel
                        centercel = self._GridCelVoorPunt (dpm, [data.CelX (), data.CelY ()])
                        samengevoegd[centercel] = data
            markeringenDitNiveau = samengevoegd
            if len (puntCellen):
                # Sommige punten zijn samengevoegd in een enkele cel
                locatiesAndersDanVoorgaande = True

            if locatiesAndersDanVoorgaande or cellenAndersDanVoorgaande:
                # Maak een nieuw niveau aan
                ditNiveau = KaartGenerator.SchaalafhankelijkeGeometrie ()
                ditNiveau.VoorZoomLevel = zoomLevel
                if locatiesAndersDanVoorgaande:
                    ditNiveau.Features = GeoData ()
                    ditNiveau.Features.Attributen = geoData.Attributen
                    ditNiveau.Features.Locaties = { dimensie : [{
                                        'type': 'Feature',
                                        'properties': enkeleGeometrie.Locatie.get ('properties'),
                                        'geometry': enkeleGeometrie.Geometrie['geometry'],
                                        '_shape': enkeleGeometrie.Geometrie.get('_shape')
                                    } for enkeleGeometrie in enkeleGeometrieen] for dimensie, enkeleGeometrieen in geometrieDitNiveau.items () }

                if cellenAndersDanVoorgaande:
                    ditNiveau.MarkeringenGridCel = GeoData ()
                    ditNiveau.MarkeringenGridCel.Attributen = { 'n': Attribuut ('n',  'Aantal niet-getoonde locaties') }
                    ditNiveau.MarkeringenGridCel.Locaties = { 0: [{
                        'type': 'Feature',
                        'properties': { 'n': data.Aantal },
                        'geometry': {
                            'type': 'Point',
                            'coordinates': self._GridCelNaarRD (dpm, cel)
                        }
                    } for cel, data in markeringenDitNiveau.items ()] }

                resultaat.ZoomLevels.append (ditNiveau)

            geometrieVoorgaandNiveau = geometrieDitNiveau
            markeringenVoorgaandeNiveau = markeringenDitNiveau

        return resultaat

    def VoegSchaalafhankelijkeLocatiesToe (self, kaart : Kaart, schaalafhankelijk: SchaalafhankelijkeGeoData, symbolisatieNamen : Dict[int,str]):
        """Voeg de schaalafhankelijke kaartlagen aan de kaart toe; ze moeten eerder zijn gemaakt via MaakSchaalafhankelijkeGeometrie.

        Argumenten:

        kaart Kaart  Kaart waaraan de locaties toegevoegd moeten worden
        schaalafhankelijk SchaalafhankelijkeGwoData De schaalafhankelijke geo-informatie waarvan de locaties aan de kaart toegevoegd moeten worden.
        symbolisatieNamen Dict[int,str] De namen van de symbolisatie (verkregen via een van de Voeg*Toe methoden) teruggeeft.
        """
        def __PostLaag (dimensie):
            if not postLaag is None:
                postLaag (schaalafhankelijk.ZoomLevels[0].Features)

        voorgaandeZoom = None
        for geschaald in schaalafhankelijk.ZoomLevels:
            if not geschaald.Features is None:
                if not geschaald.VoorZoomLevel is None:
                    # Niet voor de eerste laag, dat is brondata
                    kaart.LaatsteLaagZoomLevel (geschaald.VoorZoomLevel, voorgaandeZoom)
                voorgaandeZoom = geschaald.VoorZoomLevel
                dataNamen = self.VoegGeoDataToe (geschaald.Features)
                kaart.VoegLagenToe (schaalafhankelijk.Naam, dataNamen, symbolisatieNamen, schaalafhankelijk.InControls, schaalafhankelijk.ToonInitieel)
        if not voorgaandeZoom is None:
            kaart.LaatsteLaagZoomLevel (None, voorgaandeZoom)

    def VoegSchaalafhankelijkeMarkeringenToe (self, kaart : Kaart, schaalafhankelijk : SchaalafhankelijkeGeoData, symbolisatieNaam :  str):
        """Voeg de schaalafhankelijke (punt)markeringen aan de kaart toe; ze moeten eerder zijn gemaakt via MaakSchaalafhankelijkeGeometrie.

        Argumenten:

        kaart Kaart  Kaart waaraan de markeringen toegevoegd moeten worden
        schaalafhankelijk SchaalafhankelijkeGeoData De schaalafhankelijke geo-informatie waarvan de markeringen aan de kaart toegevoegd moeten worden.
        symbolisatieNaam str  Naam van de (punt)symbolisatie (verkregen via een van de Voeg*Toe methoden).
        """
        voorgaandeZoom = None
        for geschaald in schaalafhankelijk.ZoomLevels:
            if not geschaald.MarkeringenGridCel is None:
                if not voorgaandeZoom is None:
                    kaart.LaatsteLaagZoomLevel (geschaald.VoorZoomLevel, voorgaandeZoom)
                dataNamen = self.VoegGeoDataToe (geschaald.MarkeringenGridCel)
                kaart.VoegLagenToe (schaalafhankelijk.Naam, dataNamen, { 0: symbolisatieNaam }, schaalafhankelijk.InControls, schaalafhankelijk.ToonInitieel)
                voorgaandeZoom = geschaald.VoorZoomLevel
        if not voorgaandeZoom is None:
            kaart.LaatsteLaagZoomLevel (None, voorgaandeZoom)
#endregion

