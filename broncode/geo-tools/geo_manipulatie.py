#======================================================================
#
# Gemeenschappelijke code voor alle geo-gerelateerde operaties
# en weergave van geo-informatie.
#
#======================================================================

from typing import Dict, List, Tuple

import pygml
from shapely.geometry import shape
import json
import re
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from weergave_webpagina import WebpaginaGenerator

class GeoManipulatie:
#======================================================================
#
# Maken van een webpagina
#
#======================================================================
    def __init__ (self, defaultTitel, titelBijFout, request : Parameters, log: Meldingen = None):
        """Maak een instantie van de geo-operatie aan

        Argumenten:

        defaultTitel str  Titel van de webpagina als de titel niet is meegegeven bij de invoer
        titelBijFout str  Titel van de webpagina als er een fout optreedt en alleen de log getoond wordt
        request Parameters  De parameters vor het web request
        log Meldingen of bool  Geeft de meldingen die voor deze operatie gebruikt moeten worden. Als het een bool is, dan geeft het aan of de tijd opgenomen moet worden in de meldingen.
        """
        self._TitelBijFout = titelBijFout
        # Request waarvoor de operatie uitgevoerd wordt
        self.Request = request
        # Meldingen voor de uitvoering van het request
        self.Log = Meldingen (False) if log is None else Meldingen (log) if isinstance (log, bool) else log
        # Titel als doorgegeven in het request
        self.Titel = request.LeesString ('titel')
        # Generator om de resultaat-pagina te maken
        self.Generator = WebpaginaGenerator (defaultTitel if self.Titel is None else self.Titel)
        # Status attribuut voor het opnemen van de nodige scripts/css
        # self._WebpaginaKanKaartTonen
        # Status van het toevoegen van de default symbolen
        self._DefaultSymbolenToegevoegd : Dict[int,str] = {}
        # Index voor het uitdelen van unieke namen
        self._NaamIndex = 0

    def VoerUit(self):
        """Maak de webpagina aan"""
        self.Log.Informatie ("Geo-tools (@@@GeoTools_Url@@@) versie @@@VERSIE@@@.")
        try:
            # _VoerUit moet in een afgeleide klasse worden geïmplementeerd
            if self._VoerUit ():
                self.Log.Informatie ("De verwerking is voltooid.")
                einde = self.Generator.StartSectie ("<h3>Verslag van de verwerking</h3>")
            else:
                self.Log.Fout ("De verwerking is afgebroken.")
                einde = self.Generator.StartSectie ("<h3>Verslag van de incomplete verwerking</h3>")

            self.Log.MaakHtml (self.Generator, None)
            self.Generator.VoegHtmlToe (einde)
            return self.Generator.Html ()
        except Exception as e:
            self.Log.Fout ("Oeps, deze fout is niet verwacht: " + str(e))
            generator = WebpaginaGenerator (self._TitelBijFout)
            self.Log.MaakHtml (generator, None, "De verwerking is afgebroken.")
            return generator.Html ()

#======================================================================
#
# Geo-data
#
#======================================================================

#----------------------------------------------------------------------
#
# Interne representatie van een GIO/gebied
#
#----------------------------------------------------------------------
    class Attribuut:
        def __init__(self, tag : str, label: str = None, eenheid : str = None):
            """Maak een instantie van de informatie over een attribuut
            
            Argumenten:

            tag str  Naam voor de eigenschap in de json data en evt in de GML-data
            label str  Naam van het attribuut, te gebruiken als prefix voor een waarde van het attribuut
            eenheid str  Eenheid voor de waarde van het attribuut
            """
            self.Tag = tag
            self.Label = tag if label is None else label
            self.Eenheid = eenheid

    class GeoData:
        def __init__(self):
            # Geeft de bron aan: Gebied, GIO of GIO-wijziging
            self.Soort : str = None
            #----------------------------------------------------------
            # Voor een GIO-versie of GIO-wijziging
            #----------------------------------------------------------
            # De work-identificatie van de GIO
            self.WorkId : str = None
            # Geeft aan of er een waarde met de locatie geassocieerd is (groepID, normwaarde).
            # Zo nee, dan is dit None. Zo ja, dan staat er de naam van het waarde-element
            self.AttribuutNaam : str = None
            #----------------------------------------------------------
            # Voor een GIO-versie
            #----------------------------------------------------------
            # De expression-identificatie van de GIO
            self.ExpressionId : str = None
            # De vaststellingscontext van de GIO (indien bekend)
            self.Vaststellingscontext : Element = None
            #----------------------------------------------------------
            # Voor een GIO-versie, effectgebied, gebiedsmarkering
            #----------------------------------------------------------
            # Geeft aan of er Locaties/Gebieden zijn met een naam.
            # Zo nee, dan is dit None. Zo ja, dan staat er de naam van het element met het label/naam
            self.LabelNaam : str = None
            # De locaties/gebieden in in-memory format
            self.Locaties = []
            # De dimensie van de geometrie: 0 = punt, 1 = lijn, 2  = vlak
            self.Dimensie : int = None
            # De attributen voor de data; key = tag naam
            self.Attributen : Dict[str,GeoManipulatie.Attribuut] = {}
            #----------------------------------------------------------
            # Voor een GIO-wijziging
            #----------------------------------------------------------
            # De was-locaties
            self.Was : GeoManipulatie.GeoData = None 
            # De wordt-locaties
            self.Wordt : GeoManipulatie.GeoData = None 
            # De wijzig-markering indien aanwezig
            self.WijzigMarkering : GeoManipulatie.GeoData = None

        def GeometrieNaam (self, meervoud: bool) -> str:
            """Geeft de gewone naam voor de geometrieën in de geo-data, in enkel- of meervoud."""
            if self.Dimensie == 0:
                return "punten" if meervoud else "punt"
            if self.Dimensie == 1:
                return "lijnen" if meervoud else "lijn"
            if self.Dimensie == 2:
                return "vlakken" if meervoud else "vlak"

#----------------------------------------------------------------------
#
# Inlezen van GML
#
#----------------------------------------------------------------------
    def LeesGeoBestand (self, key : str, verplicht : str) -> GeoData:
        """Lees de inhoud van een GIO, effectgebied of gebiedsmarkering.
        Het bestand wordt gevonden aan de hand van de specificatie key / input type="file" control naam.

        Argumenten:

        key str        Key waarvoor de data opgehaald moet worden
        verplicht bool Geeft aan dat het bestand aanwezig moet zijn (dus niet optioneel is)

        Geeft de inhoud van het bestand als GeoData terug, of None als er geen bestand/data is of als er een fout optreedt
        """
        self.Log.Detail ("Lees het GIO, gebiedsmarkering of effectgebied")
        gml = self.Request.LeesBestand (self.Log, key, verplicht)
        if not gml is None:
            data = self._LeesGeoData (gml)
            if data is None:
                self.Log.Fout ("Het GIO, gebiedsmarkering of effectgebied '" + self.Request.Bestandsnaam (key) + "' kan niet ingelezen worden")
            else:
                self.Log.Informatie (data.Soort + " ingelezen uit '" + self.Request.Bestandsnaam (key) + "'")
                return data

    def _LeesGeoData (self, gml) -> GeoData:
        """Lees de GML in als een GIO"""
        # Lees de XML
        try:
            geoXml = ElementTree.fromstring (gml)
        except Exception as e:
            self.Log.Fout ("GML is geen valide XML: " + str(e))
            return
        data = GeoManipulatie.GeoData ()
        data.Attributen['id'] = GeoManipulatie.Attribuut ('id', "ID")
        succes = True

        # Vertaal naar GeoData afhankelijk van het bronformaat
        if geoXml.tag == GeoManipulatie._GeoNS + 'Gebiedsmarkering' or geoXml.tag == GeoManipulatie._GeoNS + 'Effectgebied':
            # Gebiedsmarkering of effectgebied: alleen geometrie met optioneel een label
            data.Soort = 'Gebiedsmarkering' if geoXml.tag == GeoManipulatie._GeoNS + 'Gebiedsmarkering' else 'Effectgebied'
            if not self._LeesLocaties (data, geoXml, GeoManipulatie._GeoNS + 'Gebied', 'label'):
                succes = False
            elif len (data.Locaties) == 0:
                self.Log.Waarschuwing ("Gebiedsmarkering/effectgebied bevat geen gebieden")
                succes = False
            elif data.Dimensie != 2:
                self.Log.Fout ("Gebiedsmarkering/effectgebied mag alleen vlakken bevatten")
                succes = False
        else:
            mutatie = None
            if geoXml.tag == GeoManipulatie._GeoNS + 'GeoInformatieObjectVaststelling':
                data.Vaststellingscontext = geoXml.find (GeoManipulatie._GeoNS + 'context')
                geoXml = geoXml.find (GeoManipulatie._GeoNS + 'vastgesteldeVersie')
                if not geoXml is None:
                    mutatie = geoXml.find (GeoManipulatie._GeoNS + 'GeoInformatieObjectMutatie')
                    geoXml = geoXml.find (GeoManipulatie._GeoNS + 'GeoInformatieObjectVersie') if mutatie is None else mutatie
            elif geoXml.tag != GeoManipulatie._GeoNS + 'GeoInformatieObjectVersie':
                geoXml = None
            if geoXml is None:
                self.Log.Fout ("GML wordt niet herkend als een GIO, gebiedsmarkering of effectgebied")
                return

            # GIO-versie of GIO-wijziging
            elt = geoXml.find (GeoManipulatie._GeoNS + 'FRBRWork')
            if not elt is None:
                data.WorkId = elt.text
            else:
                self.Log.Fout ("GIO-versie bevat geen FRBRWork")
                succes = False
            normLabel = None
            elt = geoXml.find (GeoManipulatie._GeoNS + 'normlabel')
            if not elt is None:
                normLabel = elt.text
            eenheidLabel = None
            elt = geoXml.find (GeoManipulatie._GeoNS + 'eenheidlabel')
            if not elt is None:
                eenheidLabel = elt.text

            if mutatie is None:
                # Het is een GIO-versie
                data.Soort = 'GIO'
                elt = geoXml.find (GeoManipulatie._GeoNS + 'FRBRExpression')
                if not elt is None:
                    data.ExpressionId = elt.text
                else:
                    self.Log.Fout ("GIO-versie bevat geen FRBRExpression")
                    succes = False
                if not self._LeesLocaties (data, geoXml.find (GeoManipulatie._GeoNS + 'locaties'), GeoManipulatie._GeoNS + 'Locatie', 'naam', ['groepID', 'kwalitatieveNormwaarde', 'kwantitatieveNormwaarde']):
                    succes = False
                elif len (data.Locaties) == 0:
                    self.Log.Fout ("GIO bevat geen locaties")
                    succes = False
            else:
                # Het is een GIO-wijziging
                data.Soort = 'GIO-wijziging'
                locatiesZijnValide = True

                # Lees de was-sectie in
                geoXml = mutatie.find (GeoManipulatie._GeoNS + 'was')
                if not geoXml is None:
                    geoXml = geoXml.find (GeoManipulatie._GeoNS + 'Selectie')
                if geoXml is None:
                    self.Log.Fout ("GIO-wijziging bevat geen was-informatie")
                    succes = False
                    locatiesZijnValide = False
                else:
                    data.Was = GeoManipulatie.GeoData ()
                    data.Was.WorkId = data.WorkId 
                    elt = geoXml.find (GeoManipulatie._GeoNS + 'FRBRExpression')
                    if not elt is None:
                        data.Was.ExpressionId = elt.text
                    else:
                        self.Log.Fout ("Was-versie bevat geen FRBRExpression")
                        succes = False
                    if not self._LeesLocaties (data.Was, geoXml.find (GeoManipulatie._GeoNS + 'locaties'), GeoManipulatie._GeoNS + 'Locatie', 'naam', ['groepID', 'kwalitatieveNormwaarde', 'kwantitatieveNormwaarde']):
                        succes = False
                        locatiesZijnValide = False

                # Lees de wordt-sectie in
                geoXml = mutatie.find (GeoManipulatie._GeoNS + 'wordt')
                if not geoXml is None:
                    geoXml = geoXml.find (GeoManipulatie._GeoNS + 'Selectie')
                if geoXml is None:
                    self.Log.Fout ("GIO-wijziging bevat geen wordt-informatie")
                    succes = False
                    locatiesZijnValide = False
                else:
                    data.Wordt = GeoManipulatie.GeoData ()
                    data.Wordt.WorkId = data.WorkId 
                    elt = geoXml.find (GeoManipulatie._GeoNS + 'FRBRExpression')
                    if not elt is None:
                        data.Wordt.ExpressionId = elt.text
                    else:
                        self.Log.Fout ("Wordt-versie bevat geen FRBRExpression")
                        succes = False
                    if not self._LeesLocaties (data.Wordt, geoXml.find (GeoManipulatie._GeoNS + 'locaties'), GeoManipulatie._GeoNS + 'Locatie', 'naam', ['groepID', 'kwalitatieveNormwaarde', 'kwantitatieveNormwaarde']):
                        succes = False
                        locatiesZijnValide = False

                # Verifieer de consistentie tussen was en wordt
                if locatiesZijnValide:
                    if data.Was.AttribuutNaam is None:
                        if not data.Wordt.AttribuutNaam is None:
                            self.Log.Fout ("Was-versie heeft alleen geometrie, wordt-versie heeft " + data.Wordt.AttribuutNaam)
                            succes = False
                    elif data.Wordt.AttribuutNaam is None:
                        self.Log.Fout ("Wordt-versie heeft alleen geometrie, was-versie heeft " + data.Was.AttribuutNaam)
                        succes = False
                    elif data.Was.AttribuutNaam != data.Wordt.AttribuutNaam:
                        self.Log.Fout ("Was-versie heeft " + data.Was.AttribuutNaam + ", wordt-versie heeft " + data.Was.AttribuutNaam)
                        succes = False
                    if len (data.Was.Locaties) == 0 and len (data.Wordt.Locaties) == 0:
                        self.Log.Fout ("GIO-wijziging bevat geen wijzigingen")
                        succes = False
                        locatiesZijnValide = False
                    else:
                        if data.Was.Dimensie is None:
                            data.Dimensie = data.Wordt.Dimensie
                        else:
                            data.Dimensie = data.Was.Dimensie
                            if not data.Wordt.Dimensie is None and data.Was.Dimensie != data.Wordt.Dimensie:
                                self.Log.Fout ("Was-versie en wordt-versie moeten dezelfde soorten geometrieën bevatten (punten, lijnen of vlakken)")
                                succes = False
                                locatiesZijnValide = False

                if locatiesZijnValide:
                    # Lees de wijzigmarkering in
                    geoXml = mutatie.find (GeoManipulatie._GeoNS + 'wijzigmarkering')
                    if data.Dimensie == 0:
                        if not geoXml is None:
                            self.Log.Fout ("wijzigmarkering mag niet aanwezig zijn want de GIO bestaat uit punten")
                            succes = False
                    elif geoXml is None:
                        self.Log.Fout ("wijzigmarkering moet aanwezig zijn want de GIO bestaat uit lijnen of vlakken")
                        succes = False
                    else:
                        data.WijzigMarkering = GeoManipulatie.GeoData ()
                        if not self._LeesLocaties (data.WijzigMarkering, geoXml, GeoManipulatie._GeoNS + 'Gebied', 'label'):
                            succes = False
                        elif len (data.WijzigMarkering.Locaties) == 0:
                            self.Log.Fout ("wijzigmarkering moet vlakken bevatten want de GIO bestaat uit lijnen of vlakken")
                            succes = False
                        elif not data.WijzigMarkering.Dimensie is None and data.WijzigMarkering.Dimensie != 2:
                            self.Log.Fout ("wijzigmarkering mag alleen vlakken bevatten")
                            succes = False

            if data.AttribuutNaam == 'groepID':
                data.Attributen[data.AttribuutNaam] = GeoManipulatie.Attribuut (data.AttribuutNaam, 'GIO-deel')
            elif not data.AttribuutNaam  is None:
                data.Attributen[data.AttribuutNaam] = GeoManipulatie.Attribuut (data.AttribuutNaam, 'Normwaarde' if normLabel is None else normLabel, eenheidLabel)

        if not data.LabelNaam is None:
            data.Attributen[data.LabelNaam] = GeoManipulatie.Attribuut (data.LabelNaam, 'Naam')

        if succes:
            return data

    def _LeesLocaties (self, data : GeoData, geoXml: Element, locatieElement, labelNaam, attribuutNamen : List[str] = []):
        succes = True
        # Foutmeldigen worden maar één keer gedaan
        foutmeldingen = set ()
        heeftAttribuut = None
        bekende_id = set ()
        for locatie in [] if geoXml is None else geoXml.findall (locatieElement):
            # Lees de geometrie van een locatie
            geometrie = locatie.find (GeoManipulatie._GeoNS + 'geometrie')
            basisgeo_id = None
            if not geometrie is None:
                geometrie = geometrie.find (GeoManipulatie._BasisgeoNS + 'Geometrie')
            if not geometrie is None:
                basisgeo_id = geometrie.find (GeoManipulatie._BasisgeoNS + 'id')
                geometrie = geometrie.find (GeoManipulatie._BasisgeoNS + 'geometrie')
                if basisgeo_id is None:
                    foutmeldingen.add ('Basisgeometrie-id is verplicht in een ' + locatieElement)
                    succes = False
                else:
                    basisgeo_id = basisgeo_id.text
                    if basisgeo_id in bekende_id:
                        foutmeldingen.add ('Basisgeometrie-id "' + basisgeo_id + '"komt meerdere keren voor')
                        succes = False
                    else:
                        bekende_id.add (basisgeo_id)
            if geometrie is None:
                foutmeldingen.add ('Geometrie ontbreekt in een ' + locatieElement)
                succes = False
                continue
            geometrie = list(geometrie)
            if len(geometrie) == 0:
                foutmeldingen.add ('Geometrie ontbreekt in een ' + locatieElement)
                succes = False
                continue
            try:
                geoLocatie = pygml.parse (ElementTree.tostring(geometrie[0], encoding='unicode'))
            except Exception as e:
                foutmeldingen.add ('GML-geometrie kan niet gebruikt worden: ' + str(e))
                succes = False
                continue

            isRD = False
            prop = geoLocatie.geometry.get ('crs')
            if not prop is None:
                prop = prop.get ('properties')
                if not prop is None:
                    prop = prop.get ('name')
                    isRD = (prop == 'urn:ogc:def:crs:EPSG::28992') or (prop == 'EPSG:28992')
                geoLocatie.geometry.pop ('crs') # Wordt later op feature collectie niveau toegevoegd
            if not isRD:
                foutmeldingen.add ('Alleen RD coördinaten (urn:ogc:def:crs:EPSG::28992 of EPSG:28992) zijn toegestaan')
                succes = False

            geoLocatie = {
                    'type': 'Feature',
                    'geometry': geoLocatie.geometry,
                    'properties': { 'id' : basisgeo_id }
                }
            data.Locaties.append (geoLocatie)

            # Kijk naar het type geometrie
            if geoLocatie['geometry']['type'] == 'MultiGeometry':
                dimensie = None
                for geom in geoLocatie['geometry']['geometries']:
                    geomDimensie = GeoManipulatie._GeometryDimension.get (geom['type'])
                    if geomDimensie is None:
                        foutmeldingen.add ('Deze geo-tools kunnen niet omgaan met een geometrie van type ' + geoLocatie['geometry']['type'] + ' in een MultiGeometry')
                        succes = False
                        continue
                    elif dimensie is None:
                        dimensie = geomDimensie
                    elif dimensie != geomDimensie:
                        foutmeldingen.add ('Deze geo-tools kunnen niet omgaan met een mengsel van punten, lijnen en vlakken')
                        succes = False
                        continue
            else:
                dimensie = GeoManipulatie._GeometryDimension.get (geoLocatie['geometry']['type'])
                if dimensie is None:
                    foutmeldingen.add ('Deze geo-tools kunnen niet omgaan met een geometrie van type ' + geoLocatie['geometry']['type'])
                    succes = False
                    continue

            if data.Dimensie is None:
                data.Dimensie = dimensie
            elif data.Dimensie != dimensie:
                foutmeldingen.add ('Deze geo-tools kunnen niet omgaan met een mengsel van punten, lijnen en vlakken')
                succes = False

            # Kijk welke attributen er bij de locatie aanwezig zijn
            elt = locatie.find (GeoManipulatie._GeoNS + labelNaam)
            if not elt is None:
                geoLocatie['properties'][labelNaam] = elt.text
                data.LabelNaam = labelNaam
            elt = locatie.find (GeoManipulatie._GeoNS + labelNaam)
            if not elt is None:
                geoLocatie['properties'][labelNaam] = elt.text
                data.LabelNaam = labelNaam
            if heeftAttribuut is None:
                heeftAttribuut = False
                for naam in attribuutNamen:
                    elt = locatie.find (GeoManipulatie._GeoNS + naam)
                    if not elt is None:
                        geoLocatie['properties'][naam] = elt.text
                        data.AttribuutNaam = naam
                        heeftAttribuut = True
            elif heeftAttribuut:
                elt = locatie.find (GeoManipulatie._GeoNS + data.AttribuutNaam)
                if elt is None:
                    foutmeldingen.add ('Alle locaties moeten een waarde voor "' + data.AttribuutNaam + '" hebben')
                    succes = False
                else:
                    geoLocatie['properties'][data.AttribuutNaam] = elt.text
            else:
                for naam in attribuutNamen:
                    elt = locatie.find (GeoManipulatie._GeoNS + naam)
                    if not elt is None:
                        foutmeldingen.add ('Alle locaties moeten een waarde voor "' + naam + '" hebben')
                        succes = False
                        break

        for foutmelding in foutmeldingen:
            self.Log.Fout (foutmelding)
        return succes

    _GeoNS = '{https://standaarden.overheid.nl/stop/imop/geo/}'
    _BasisgeoNS = '{http://www.geostandaarden.nl/basisgeometrie/1.0}'
    _GeometryDimension = {
            'Point': 0, 'MultiPoint': 0, 
            'LineString': 1, 'MultiLineString': 1,
            'Polygon': 2, 'MultiPolygon': 2
        }

#----------------------------------------------------------------------
#
# Conversie naar Shapely objecten om mee te rekenen
#
#----------------------------------------------------------------------
    @staticmethod
    def MaakShapelyShape (locatie):
        """Maak een Shapely shape voor de locatie (als dat niet eerder gebeurd is) en geef die terug.

        Argumenten:

        locatie {}  Een locatie voals die eerder is ingelezen
        """
        if not '_shape' in locatie:
            locatie['_shape'] = shape (locatie['geometry'])
        return locatie['_shape']

#----------------------------------------------------------------------
#
# Wegschrijven als JSON voor kaart in de webpagina
#
#----------------------------------------------------------------------
    def VoegGeoDataToe (self, geoData : GeoData):
        """Voeg de geo-gegevens uit een GIO of gebied toe aan de data beschikbaar in de resultaatpagina;

        Argumenten:

        geoData GeoData  Een geo-data object waarvan de locaties op de kaart weergegeven moeten worden

        Geeft de naam terug die gebruikt moet worden om de gegevens aan een kaart te koppelen
        """
        if geoData is None:
            self.Log.Detail ('Geen geo-data beschikbaar dus niet toegevoegd aan de kaartgegevens')
            return
        collectie = {
            'type' : 'FeatureCollection',
            'crs': { 'type': 'name', 'properties': { 'name': 'urn:ogc:def:crs:EPSG::28992' } },
            'features' : geoData.Locaties
        }
        # Bepaal de bounding box van de hele collectie
        bbox = False
        for locatie in geoData.Locaties:
            locatieShape = GeoManipulatie.MaakShapelyShape (locatie)
            if not locatieShape.is_empty:
                locatieBBox = locatieShape.bounds
                if bbox:
                    bbox = [
                            bbox[0] if bbox[0] < locatieBBox[0] else locatieBBox[0],
                            bbox[1] if bbox[1] < locatieBBox[1] else locatieBBox[1],
                            bbox[2] if bbox[2] > locatieBBox[2] else locatieBBox[2],
                            bbox[3] if bbox[3] > locatieBBox[3] else locatieBBox[3]
                        ]
                else:
                    bbox = list (locatieBBox)
        if bbox:
            collectie['bbox'] = bbox

        # Bepaal de properties die op de kaart getoond kan worden
        if len (geoData.Attributen) > 0:
            collectie['properties'] = {a.Tag : [a.Label, '' if a.Eenheid is None else a.Eenheid] for a in geoData.Attributen.values ()} 

        # Voeg toe aan de scripts van de pagina
        self._InitialiseerWebpagina ()
        self._NaamIndex += 1
        naam = 'data' + str(self._NaamIndex)
        self.Generator.VoegSlotScriptToe ('\nKaartgegevens.Instantie.VoegDataToe ("' + naam + '",\n' + json.dumps (collectie, cls=GeoManipulatie._JsonGeoEncoder, ensure_ascii=False) + '\n);\n')
        return naam

    class _JsonGeoEncoder (json.JSONEncoder):
        def default(self, o):
            """Objecten worden niet meegenomen"""
            return None

#======================================================================
#
# Weergave op de kaart
#
#======================================================================

#----------------------------------------------------------------------
#
# Symbolisatie
#
#----------------------------------------------------------------------
    def VoegDefaultSymbolisatieToe (self, geoData : GeoData) -> str:
        """Voeg de default symbolisatie toe voor de geodata
        
        Argumenten:

        geoData GeoData  Eerdef ingelezen data

        Geeft de naam terug die gebruikt moet worden om de symbolisatie aan geodata voor een kaart te koppelen
        """
        naam = self._DefaultSymbolenToegevoegd.get (geoData.Dimensie)
        if naam is None:
            self._DefaultSymbolenToegevoegd[geoData.Dimensie] = naam = self.VoegUniformeSymbolisatieToe (geoData.Dimensie, "#0000FF", "#0000CD")
        return naam


    def VoegUniformeSymbolisatieToe (self, dimensie : int, vulkleur: str, randkleur: str, opacity : str = '1') -> str:
        """Voeg een STOP symbolisatie toe voor gebruik in kaarten.

        Argumenten:

        dimensie int  De dimensie van de geodata
        vulkleur str  De #hexcode van de te gebruiken kleur voor de opvulling van een symbool.
        randkleur str  De #hexcode van de te gebruiken kleur voor de rand van een symbool.

        Geeft de naam terug die gebruikt moet worden om de symbolisatie aan geodata voor een kaart te koppelen
        """
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
                <SvgParameter name="stroke">''' + vulkleur + '''</SvgParameter>
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
                <SvgParameter name="fill-opacity">0.8</SvgParameter>
            </Fill>
            <Stroke>
                <SvgParameter name="stroke">''' + randkleur + '''</SvgParameter>
                <SvgParameter name="stroke-opacity">1</SvgParameter>
                <SvgParameter name="stroke-width">3</SvgParameter>
                <SvgParameter name="stroke-linejoin">round</SvgParameter>
            </Stroke>
        </PolygonSymbolizer>
    </Rule>'''
        return self.VoegSymbolisatieToe (GeoManipulatie._MaakFeatureTypeStyle ([rule]))


    def VoegSymbolisatieToe (self, symbolisatie : str):
        """Voeg een STOP symbolisatie toe voor gebruik in kaarten.

        Argumenten:

        naam str  De naam die gebruikt moet worden om de symbolisatie toe te passen
        symbolisatie str  De XML van een STOP symbolisatie module.

        Geeft de naam terug die gebruikt moet worden om de symbolisatie aan geodata voor een kaart te koppelen
        """
        # Verwijder <?xml ?> regel indien aanwezig
        if symbolisatie is None:
            self.Log.Detail ('Geen symbolisatie beschikbaar dus niet toegevoegd aan de kaartgegevens')
            return
        symbolisatie = GeoManipulatie._StripHeader.sub ('', symbolisatie)

        # Voeg toe aan de scripts van de pagina
        self._InitialiseerWebpagina ()
        self._NaamIndex += 1
        naam = 'sym' + str(self._NaamIndex)
        self.Generator.VoegSlotScriptToe ('\nKaartgegevens.Instantie.VoegSymbolisatieToe ("' + naam + '",`' + symbolisatie + '`);\n')
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

    def VoegWijzigMarkeringToe (self):
        """Voeg de symbolisatie voor de speciale wijzigmarkeringen toe en geef de naam terug"""
        naam = self._DefaultSymbolenToegevoegd.get ('WM')
        if naam is None:
            self._DefaultSymbolenToegevoegd['WM'] = naam = self.VoegSymbolisatieToe (GeoManipulatie.WijzigMarkeringSymbolisatie ())
        return naam

    @staticmethod
    def WijzigMarkeringSymbolisatie ():
        """Geef de symbolisatie voor de speciale wijzigmarkeringen"""
        return GeoManipulatie._MaakFeatureTypeStyle ([GeoManipulatie._WijzigMarkeringSymbolisatie])

    _WijzigMarkeringSymbolisatie = '''
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
                        <SvgParameter name="fill">#F8CECC</SvgParameter><!--#B85450-->
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
                        <SvgParameter name="fill">#82B366</SvgParameter><!--#D5E8D4-->
                        <SvgParameter name="fill-opacity">1</SvgParameter>
                    </Fill>
                </Mark>
                <Size>10</Size>
                <Rotation>0</Rotation>
            </Graphic>
        </PointSymbolizer>
    </Rule>'''

#----------------------------------------------------------------------
#
# Kaart in webpagina
#
#----------------------------------------------------------------------
    def ToonKaart (self, jsInitialisatie : str, kaartElementId : str = None):
        """Toon een kaart op de huidige plaats in de webpagina

        Argumenten:

        jsInitialisatie str  Javascript om de kaartlagen aan de kaart toe te voegen. De kaart is beschikbaar als 'kaart' variabele,
        kaartElementId str  Naam van het (in dese methode te maken) HTML element waarin de kaart getoond wordt  Geef None door om een elementnaam te genereren.

        Geeft kaartElementId terug.
        """
        self._InitialiseerWebpagina ()
        if kaartElementId is None:
            self._NaamIndex += 1
            kaartElementId = 'kaart_' + str(self._NaamIndex)
        self.Generator.VoegHtmlToe (self.Generator.LeesHtmlTemplate ("kaart", False).replace ('<!--ID-->', kaartElementId))
        self.Generator.VoegSlotScriptToe ('\nwindow.addEventListener("load", function () {\nvar kaart = new Kaart ();\n' + jsInitialisatie + '\nkaart.Toon ("' + kaartElementId + '", "900", "600");\n});')
        return kaartElementId

    def _InitialiseerWebpagina (self):
        """Voeg de bestanden toe nodig om OpenLayers kaarten op te nemen in de webpagina
        """
        if not hasattr (self, '_WebpaginaKanKaartTonen'):
            setattr (self, '_WebpaginaKanKaartTonen', True)
            self.Generator.LeesCssTemplate ('ol')
            self.Generator.LeesJSTemplate ("ol", True, True)
            self.Generator.LeesJSTemplate ("sldreader", True, True)
            self.Generator.LeesCssTemplate ("juxtapose")
            self.Generator.LeesJSTemplate ("juxtapose", True, True)
            self.Generator.LeesCssTemplate ("kaart")
            self.Generator.LeesJSTemplate ("kaart", True, True)

#======================================================================
#
# Ondersteuning GIO-wijziging
#
#======================================================================

    def NauwkeurigheidInMeter (self) -> float:
        """Haal de nauwkeurigheid als float uit de request parameters"""
        if self.Request.LeesString ("teken-nauwkeurigheid") is None:
            self.Log.Waarschuwing ("Geen teken-nauwkeurigheid doorgegeven - kan de GIO niet valideren")
            return None
        try:
            nauwkeurigheid = float (self.Request.LeesString ("teken-nauwkeurigheid"))
        except:
            self.Log.Fout ('De opgegeven teken-nauwkeurigheid is geen getal: "' + self.Request.LeesString ("teken-nauwkeurigheid") + '"')
            return None
        return nauwkeurigheid * 0.1


    class EnkeleGeometrie:
        def __init__ (self, locatie, geometrie, attribuutwaarde : str):
            """Een Point, LineString of Polygon geometrie die onderdeel is van de (multi-)geometrie van de locatie.
            
            Argumenten:

            locatie object  Locatie zoals ingelezen voor GeoData
            geometrie object  Een Point, LineString of Polygon
            attribuutwaarde str  Als het GIO normwaarden bevat: de normwaarde van de locatie.
                                 Als het GIO GIO-delen bevat: de groepID van de locatie.
            """
            self.ID = locatie['properties']['id']
            self.Locatie = locatie
            self.Geometrie = geometrie
            self.Attribuutwaarde = attribuutwaarde

    def MaakLijstVanGeometrieen (self, geoData : GeoData) -> Tuple[List[EnkeleGeometrie], bool]:
        """Zet de informatie in de locaties om in een lijst met objecten die elk slechts één geometrie (punt, lijn of vlak) hebben.

        Argumenten:

        geoData GeoData  Het ingelezen GIO

        Geeft de lijst terug, en een indicatie of er sprake is van multi-geometrie
        """
        lijst = []
        isMulti = False
        for locatie in geoData.Locaties:
            attribuutwaarde = None if geoData.AttribuutNaam is None else locatie['properties'][geoData.AttribuutNaam]
            opgesplitst = self.SplitsMultiGeometrie (locatie)
            if len (opgesplitst) > 0:
                isMulti = True
            lijst.extend (GeoManipulatie.EnkeleGeometrie(locatie, geom, attribuutwaarde) for geom in opgesplitst)
        return lijst, isMulti

    def SplitsMultiGeometrie (self, locatie):
        """Zet de geometrie om in een geometrieen die elk slechts één geometrie (punt, lijn of vlak) hebben
        en die te gebruiken zijn als een locatie in GeoData.Locaties

        Argumenten:

        locatie object Een locatie uit een GeoData.Locaties

        Geeft de lijst van geometrieën terug
        """
        locatieGeometrie = locatie['geometry']
        if locatieGeometrie['type'] == 'MultiPoint':
            return [{
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': coords
                        }
                    } for coords in locatieGeometrie['coordinates']]
        elif locatieGeometrie['type'] == 'MultiLineString':
            return [{
                        'type': 'Feature',
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': coords
                        }
                    } for coords in locatieGeometrie['coordinates']]
        elif locatieGeometrie['type'] == 'MultiPolygon':
            return [{
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': coords
                        }
                    } for coords in locatieGeometrie['coordinates']]
        elif locatieGeometrie['type'] == 'GeometryCollection':
            return [{
                        'type': 'Feature',
                        'geometry': geom
                    } for geom in locatieGeometrie['geometries']]
        else:
            return [{
                        'type': 'Feature',
                        'geometry': locatieGeometrie
                    }]
