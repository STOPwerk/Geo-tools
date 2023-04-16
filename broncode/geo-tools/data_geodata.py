#======================================================================
#
# Code om een GIO-versie of GIO-wijziging in te lezen of 
# weg te schrijven.
#
#======================================================================
from typing import Dict, List, Set, Tuple

import pygml
from pygml.v32 import encode_v32, GML32_ENCODER
GML32_ENCODER.id_required = False # Basisgeometrie gebruikt geen gml:id
from lxml import etree as lxml_etree
from shapely.geometry import shape

from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters


#----------------------------------------------------------------------
#
# GeoData: interne representatie van een GIO/gebied/GIO-wijziging
#
#----------------------------------------------------------------------
#region Interne representatie van een GIO/gebied

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

class GIODeel:
    def __init__ (self, groepId : str, label : str):
        """Maak een instantie van de informatie over een GIO-deel
            
        Argumenten:

        groepId str  ID voor het GIO-deel
        label str  Naam van het GIO-deel
        """
        self.GroepId = groepId
        self.Label = label
        # Als onderdeel van de GIO-Wijziging: wat moet er mee gebeuren?
        self.WijzigActie = None

    _WIJZIGACTIE_VOEGTOE = "voegtoe"
    _WIJZIGACTIE_VERWIJDER = "verwijder"

class GeoData:
    def __init__(self):
        # Geeft de bron aan: Gebiedsmarkering, Effectgebied, GIO-versie of GIO-wijziging
        self.Soort : str = None
        #----------------------------------------------------------
        # Voor een GIO-versie of GIO-wijziging
        #----------------------------------------------------------
        # De work-identificatie van het GIO
        self.WorkId : str = None
        # Geeft aan of er een waarde met de locatie geassocieerd is (groepID, normwaarde).
        # Zo nee, dan is dit None. Zo ja, dan staat er de naam van het waarde-element
        self.AttribuutNaam : str = None
        # Definitie van de GIO-delen
        self.GIODelen : Dict[str,GIODeel] = None
        # Label voor de norm
        self.NormLabel = None
        # ID voor de norm
        self.NormID = None
        # Label voor de eenheid van de normwaarden
        self.EenheidLabel = None
        # ID voor de eenheid van de normwaarden
        self.EenheidID = None
        # Juridische nauwkeurigheid in decimeter
        self.JuridischeNauwkeurigheid : int = None
        #----------------------------------------------------------
        # Voor een GIO-versie
        #----------------------------------------------------------
        # De expression-identificatie van het GIO
        self.ExpressionId : str = None
        # De vaststellingscontext van het GIO (indien bekend)
        self.Vaststellingscontext : str = None
        #----------------------------------------------------------
        # Voor een GIO-versie, effectgebied, gebiedsmarkering
        #----------------------------------------------------------
        # Geeft aan of er Locaties/Gebieden zijn met een naam.
        # Zo nee, dan is dit None. Zo ja, dan staat er de naam van het element met het label/naam
        self.LabelNaam : str = None
        # De locaties/gebieden in in-memory format
        # Key is dimensie van de geometrie: 0 = punt, 1 = lijn, 2 = vlak
        self.Locaties : Dict[int,GeoData] = {}
        # De attributen voor de data; key = tag naam
        self.Attributen : Dict[str,Attribuut] = {}
        #----------------------------------------------------------
        # Voor een GIO-wijziging
        #----------------------------------------------------------
        # De was-locaties
        self.Was : GeoData = None 
        # De wordt-locaties
        self.Wordt : GeoData = None 
        # De wordt-locaties die uitsluitend als revisie voorkomen
        self.WordtRevisies : GeoData = None 
        # De wijzig-markering indien aanwezig.
        self.WijzigMarkering : GeoData = None
        #----------------------------------------------------------
        # Voor weergave op de kaart
        #----------------------------------------------------------
        # De namen waaronder deze data via KaartGenerator.VoegGeoDataToe is geregistreerd voor kaartweergave
        # Key is dimensie van de geometrie: 0 = punt, 1 = lijn, 2 = vlak
        self._KaartgegevensNamen : Dict[int,str] = None

    @staticmethod
    def GeometrieNaam (dimensie : int, meervoud: bool) -> str:
        """Geeft de gewone naam voor de geometrieën in de geo-data, in enkel- of meervoud.
        
        Argumenten:
        
        dimensie int  Dimensie van de geometrie: 0 = punt, 1 = lijn, 2 = vlak
        meervoud bool  Geef de meervoudsvorm van de geometrie
        """
        if dimensie == 0:
            return "punten" if meervoud else "punt"
        if dimensie == 1:
            return "lijnen" if meervoud else "lijn"
        if dimensie == 2:
            return "vlakken" if meervoud else "vlak"

    SOORT_Gebiedsmarkering = 'Gebiedsmarkering'
    SOORT_Effectgebied = 'Effectgebied'
    SOORT_GIOVersie = 'GIO-versie'
    SOORT_GIOWijziging = 'GIO-Wijziging'

    _GeoNS = '{https://standaarden.overheid.nl/stop/imop/geo/}'
    _BasisgeoNS = '{http://www.geostandaarden.nl/basisgeometrie/1.0}'
    _GeometryDimension = {
            'Point': 0, 'MultiPoint': 0, 
            'LineString': 1, 'MultiLineString': 1,
            'Polygon': 2, 'MultiPolygon': 2
        }
    _Wijzigactie_Was = 'verwijder'
    _Wijzigactie_Wordt = 'voegtoe'
    _Wijzigactie_Revisie = 'reviseer'
#endregion

#----------------------------------------------------------------------
#
# Inlezen van GML
#
#----------------------------------------------------------------------
#region Inlezen van GML

    @staticmethod
    def LeesGeoBestand (request : Parameters, key : str, verplicht : bool, bewaarGml = None) -> 'GeoData':
        """Lees de inhoud van een GIO, effectgebied of gebiedsmarkering.
        Het bestand wordt gevonden aan de hand van de specificatie key / input type="file" control naam.

        Argumenten:

        request Parameters  Parameters voor het request
        key str             Key (in request parameters) waarvoor de data opgehaald moet worden
        verplicht bool      Geeft aan dat het bestand aanwezig moet zijn (dus niet optioneel is)
        bewaarGml lambda    Functie die aangeroepen wordt met de GML van het bestand; mag None zijn

        Geeft de inhoud van het bestand als GeoData terug, of None als er geen bestand/data is of als er een fout optreedt
        """
        request.Log.Detail ("Lees het GIO, gebiedsmarkering of effectgebied")
        gml = request.LeesBestand (key, verplicht)
        if not bewaarGml is None:
            bewaarGml (gml)
        if not gml is None:
            data = GeoData._LeesGeoData (request.Log, gml)
            if data is None:
                request.Log.Fout ("Het GIO, gebiedsmarkering of effectgebied '" + request.Bestandsnaam (key) + "' kan niet ingelezen worden")
            else:
                request.Log.Informatie (data.Soort + " ingelezen uit '" + request.Bestandsnaam (key) + "'")
                if data.JuridischeNauwkeurigheid is None:
                    data.JuridischeNauwkeurigheid = request.JuridischeNauwkeurigheidInDecimeter (False)
                return data

    @staticmethod
    def _LeesGeoData (log : Meldingen, gml) -> 'GeoData':
        """Lees de GML van een GIO of GIO-wijziging in"""
        # Lees de XML
        try:
            geoXml = ElementTree.fromstring (gml)
        except Exception as e:
            log.Fout ("GML is geen valide XML: " + str(e))
            return
        data = GeoData ()
        data.Attributen['id'] = Attribuut ('id', "ID")
        succes = True

        # Vertaal naar GeoData afhankelijk van het bronformaat
        if geoXml.tag == GeoData._GeoNS + 'Gebiedsmarkering' or geoXml.tag == GeoData._GeoNS + 'Effectgebied':
            # Gebiedsmarkering of effectgebied: alleen geometrie met optioneel een label
            data.Soort = GeoData.SOORT_Gebiedsmarkering if geoXml.tag == GeoData._GeoNS + 'Gebiedsmarkering' else GeoData.SOORT_Effectgebied
            if not data._LeesLocaties (log, geoXml, GeoData._GeoNS + 'Gebied', 'label'):
                succes = False
            elif len (data.Locaties.keys ()) == 0:
                log.Waarschuwing ("Gebiedsmarkering/effectgebied bevat geen gebieden")
                succes = False
            elif len (data.Locaties.keys ()) > 1 or not 2 in data.Locaties:
                log.Fout ("Gebiedsmarkering/effectgebied mag alleen vlakken bevatten")
                succes = False
        else:
            # GIO-versie, vastgestelde GIO-versie of GIO-wijziging
            gioMutatie = None
            wasID = None
            if geoXml.tag == GeoData._GeoNS + 'GeoInformatieObjectVaststelling':
                # Vastgestelde GIO-versie of GIO-wijziging
                wasID = geoXml.find (GeoData._GeoNS + 'wasID')
                data.Vaststellingscontext = geoXml.find (GeoData._GeoNS + 'context')
                if not data.Vaststellingscontext is None:
                    data.Vaststellingscontext = ElementTree.tostring (data.Vaststellingscontext, encoding='unicode')
                geoXml = geoXml.find (GeoData._GeoNS + 'vastgesteldeVersie')
                if not geoXml is None:
                    gioMutatie = geoXml.find (GeoData._GeoNS + 'GeoInformatieObjectMutatie')
                    geoXml = geoXml.find (GeoData._GeoNS + 'GeoInformatieObjectVersie') if gioMutatie is None else gioMutatie
            elif geoXml.tag != GeoData._GeoNS + 'GeoInformatieObjectVersie':
                geoXml = None
            if geoXml is None:
                log.Fout ("GML wordt niet herkend als een GIO, gebiedsmarkering of effectgebied")
                return

            # Voor GIO-versie en GIO-wijziging
            elt = geoXml.find (GeoData._GeoNS + 'FRBRWork')
            if not elt is None:
                data.WorkId = elt.text
            else:
                log.Fout ("GIO-versie bevat geen FRBRWork")
                succes = False
            elt = geoXml.find (GeoData._GeoNS + 'juridischeNauwkeurigheid')
            if not elt is None:
                data.JuridischeNauwkeurigheid = elt.text

            elt = geoXml.find (GeoData._GeoNS + 'groepen')
            if not elt is None:
                data.AttribuutNaam = 'groepID'
                data.GIODelen = {}
                for groepXml in elt.findall (GeoData._GeoNS + 'Groep'):
                    groepId = groepXml.find (GeoData._GeoNS + 'groepID')
                    elt2 = groepXml.find (GeoData._GeoNS + 'label')
                    if groepId is None or elt2 is None:
                        log.Fout ("Een GIO-deel/groep moet een groepID en label hebben")
                        succes = False
                    elif groepId.text in data.GIODelen:
                        log.Fout ("Elk GIO-deel/groep moet een unieke groepID hebben")
                        succes = False
                    else:
                        data.GIODelen[groepId.text] = GIODeel (groepId.text, elt2.text)
                        if not gioMutatie is None:
                            # Voor GIO-wijziging
                            elt2 = groepXml.find (GeoData._GeoNS + 'wijzigactie')
                            if not elt2 is None:
                                data.GIODelen[groepId.text].WijzigActie = elt2.text

            else:
                elt = geoXml.find (GeoData._GeoNS + 'normlabel')
                if not elt is None:
                    data.NormLabel = elt.text
                    elt = geoXml.find (GeoData._GeoNS + 'normID')
                    if not elt is None:
                        data.NormID = elt.text
                    elt = geoXml.find (GeoData._GeoNS + 'eenheidlabel')
                    if not elt is None:
                        data.EenheidLabel = elt.text
                    elt = geoXml.find (GeoData._GeoNS + 'eenheidID')
                    if not elt is None:
                        data.EenheidID = elt.text

            if gioMutatie is None:
                # Het is een GIO-versie
                data.Soort = GeoData.SOORT_GIOVersie
                elt = geoXml.find (GeoData._GeoNS + 'FRBRExpression')
                if not elt is None:
                    data.ExpressionId = elt.text
                else:
                    log.Fout ("GIO-versie bevat geen FRBRExpression")
                    succes = False
                if not data._LeesLocaties (log, geoXml.find (GeoData._GeoNS + 'locaties'), GeoData._GeoNS + 'Locatie', 'naam', ['groepID', 'kwalitatieveNormwaarde', 'kwantitatieveNormwaarde']):
                    succes = False
                elif len (data.Locaties) == 0:
                    log.Fout ("GIO bevat geen locaties")
                    succes = False
                elif data.AttribuutNaam is None:
                    if not data.NormLabel is None:
                        log.Fout ("GIO bevat een norm maar de locaties hebben geen normwaarden")
                        succes = False
                elif data.AttribuutNaam == 'groepID':
                    if data.GIODelen is None:
                        log.Fout ("GIO bevat geen definities van GIO-delen")
                        succes = False
                    else:
                        meldingen = set ()
                        for locaties in data.Locaties.values ():
                            for locatie in locaties:
                                groepId = locatie['properties']['groepID']
                                if not groepId in data.GIODelen:
                                    meldingen.add ("Locatie heeft onbekende groepID = '" + groepId + "'")
                        if len (meldingen) > 0:
                            succes = False
                            for melding in meldingen:
                                log.Fout (melding)
                elif not data.AttribuutNaam is None:
                    if data.NormLabel is None:
                        log.Fout ("GIO heeft geen label voor de norm")
                        succes = False
            else:
                # Het is een GIO-wijziging
                data.Soort = GeoData.SOORT_GIOWijziging

                data.Was = GeoData ()
                data.Was.WorkId = data.WorkId
                if wasID is None:
                    log.Fout ("GIO-wijziging bevat geen wasID")
                    succes = False
                else:
                    data.Was.ExpressionId = wasID.text
                data.Was.Attributen = data.Attributen

                data.Wordt = GeoData ()
                data.Wordt.WorkId = data.WorkId 
                data.WordtRevisies = GeoData ()
                data.WordtRevisies.WorkId = data.WorkId 
                elt = geoXml.find (GeoData._GeoNS + 'FRBRExpression')
                if not elt is None:
                    data.ExpressionId = data.Wordt.ExpressionId = data.WordtRevisies.ExpressionId = elt.text
                else:
                    log.Fout ("GIO-wijziging bevat geen FRBRExpression van de wordt-versie")
                    succes = False
                data.Wordt.Attributen = data.Attributen
                data.WordtRevisies.Attributen = data.Attributen

                mutaties = GeoData ()
                mutaties.AttribuutNaam = data.AttribuutNaam
                if not mutaties._LeesLocaties (log, geoXml.find (GeoData._GeoNS + 'locatieMutaties'), GeoData._GeoNS + 'LocatieMutatie', 'naam', ['groepID', 'kwalitatieveNormwaarde', 'kwantitatieveNormwaarde'], True):
                    succes = False
                elif len (mutaties.Locaties) == 0:
                    log.Fout ("GIO-wijziging bevat geen mutaties")
                    succes = False
                else:
                    data.AttribuutNaam = mutaties.AttribuutNaam

                    def _KopieerLocaties (wijzigactie):
                        kopie = {}
                        for dimensie, locaties in mutaties.Locaties:
                            selectie = [l for l in locaties if l['properties']['wijzigactie'] == wijzigactie]
                            if len (selectie) > 0:
                                kopie[dimensie] = selectie
                        return kopie

                    data.Was.AttribuutNaam = mutaties.AttribuutNaam
                    data.Was.Locaties = _KopieerLocaties (GeoData._Wijzigactie_Was)

                    data.Wordt.AttribuutNaam = gioMutatie.AttribuutNaam
                    data.Wordt.Locaties = _KopieerLocaties (GeoData._Wijzigactie_Wordt)

                    data.WordtRevisies.AttribuutNaam = gioMutatie.AttribuutNaam
                    data.WordtRevisies.Locaties = _KopieerLocaties (GeoData._Wijzigactie_Revisie)

                    # Lees de wijzigmarkering in
                    geoXml = gioMutatie.find (GeoData._GeoNS + 'wijzigmarkeringen')
                    data.WijzigMarkering = GeoData ()
                    if not geoXml is None:
                        for geometrietype in ['Punt', 'Lijn', 'Vlak']:
                            if not data.WijzigMarkering._LeesLocaties (log, geoXml, GeoData._GeoNS + geometrietype):
                                succes = False

            if data.AttribuutNaam == 'groepID':
                data.Attributen[data.AttribuutNaam] = Attribuut (data.AttribuutNaam, 'groepID')
            elif not data.AttribuutNaam  is None:
                data.Attributen[data.AttribuutNaam] = Attribuut (data.AttribuutNaam, 'Normwaarde' if data.NormLabel is None else data.NormLabel, data.EenheidLabel)

        if not data.LabelNaam is None:
            data.Attributen[data.LabelNaam] = Attribuut (data.LabelNaam, 'Naam')

        if succes:
            return data

    def _LeesLocaties (self, log : Meldingen, geoXml: Element, locatieElement, labelNaam, attribuutNamen : List[str] = [], alsMutatie : bool = False):
        succes = True
        # Foutmeldigen worden maar één keer gedaan
        foutmeldingen = set ()
        heeftAttribuut = None if self.AttribuutNaam is None else True
        bekende_id = set ()
        for locatie in [] if geoXml is None else geoXml.findall (locatieElement):
            # Lees de geometrie van een locatie
            geometrie = locatie.find (GeoData._GeoNS + 'geometrie')
            basisgeo_id = None
            if not geometrie is None:
                geometrie = geometrie.find (GeoData._BasisgeoNS + 'Geometrie')
            if not geometrie is None:
                basisgeo_id = geometrie.find (GeoData._BasisgeoNS + 'id')
                geometrie = geometrie.find (GeoData._BasisgeoNS + 'geometrie')
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

            # Kijk naar het type geometrie
            if geoLocatie.geometry['type'] == 'MultiGeometry':
                dimensie = set ()
                for geom in geoLocatie.geometry['geometries']:
                    geomDimensie = GeoData._GeometryDimension.get (geom['type'])
                    if geomDimensie is None:
                        foutmeldingen.add ('Deze geo-tools kunnen niet omgaan met een geometrie van type ' + geoLocatie.geometry['type'] + ' in een MultiGeometry')
                        succes = False
                        continue
                    else:
                        dimensie.add (geomDimensie)
                if len (dimensie) == 0:
                    foutmeldingen.add ('Een MultiGeometry moet tenminste één geometrie bevatten')
                    succes = False
                    continue
                elif len (dimensie) > 1:
                    foutmeldingen.add ('Deze geo-tools kunnen niet omgaan met een mengsel van punten, lijnen en vlakken in een MultiGeometry')
                    succes = False
                    continue
                else:
                    dimensie = dimensie[0]
            else:
                dimensie = GeoData._GeometryDimension.get (geoLocatie.geometry['type'])
                if dimensie is None:
                    foutmeldingen.add ('Deze geo-tools kunnen niet omgaan met een geometrie van type ' + geoLocatie.geometry['type'])
                    succes = False
                    continue

            geoLocatie = {
                    'type': 'Feature',
                    'geometry': geoLocatie.geometry,
                    'properties': { 'id' : basisgeo_id }
                }
            if not dimensie in self.Locaties:
                self.Locaties[dimensie] = []
            self.Locaties[dimensie].append (geoLocatie)

            # Kijk welke attributen er bij de locatie aanwezig zijn
            elt = locatie.find (GeoData._GeoNS + labelNaam)
            if not elt is None:
                geoLocatie['properties'][labelNaam] = elt.text
                self.LabelNaam = labelNaam
            elt = locatie.find (GeoData._GeoNS + labelNaam)
            if not elt is None:
                geoLocatie['properties'][labelNaam] = elt.text
                self.LabelNaam = labelNaam
            if heeftAttribuut is None:
                heeftAttribuut = False
                for naam in attribuutNamen:
                    elt = locatie.find (GeoData._GeoNS + naam)
                    if not elt is None:
                        geoLocatie['properties'][naam] = float (elt.text) if naam == 'kwantitatieveNormwaarde' else elt.text
                        self.AttribuutNaam = naam
                        heeftAttribuut = True
            elif heeftAttribuut:
                elt = locatie.find (GeoData._GeoNS + self.AttribuutNaam)
                if elt is None:
                    foutmeldingen.add ('Alle locaties moeten een waarde voor "' + self.AttribuutNaam + '" hebben')
                    succes = False
                else:
                    geoLocatie['properties'][self.AttribuutNaam] = float (elt.text) if self.AttribuutNaam == 'kwantitatieveNormwaarde' else elt.text
            else:
                for naam in attribuutNamen:
                    elt = locatie.find (GeoData._GeoNS + naam)
                    if not elt is None:
                        foutmeldingen.add ('Alle locaties moeten een waarde voor "' + naam + '" hebben')
                        succes = False
                        break
            if alsMutatie:
                elt = locatie.find (GeoData._GeoNS + 'wijzigactie')
                if not elt is None:
                    geoLocatie['properties']['wijzigactie'] = elt.text
                else:
                    foutmeldingen.add ('Alle mutaties moeten een waarde voor "wijzigactie" hebben')
                    succes = False

        for foutmelding in foutmeldingen:
            log.Fout (foutmelding)
        return succes
#endregion

#----------------------------------------------------------------------
#
# Maken van GML
#
#----------------------------------------------------------------------
#region Maken van GML

    def SchrijfGIO (self) -> str:
        """Stel de XML op voor een GIO (als string). Deze GeoData moet een GIO-versie zijn!"""

        gioGML = '''<geo:GeoInformatieObjectVersie schemaversie="@@@IMOP_Versie@@@" xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0" xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://standaarden.overheid.nl/stop/imop/geo/
  https://standaarden.overheid.nl/stop/@@@IMOP_Versie@@@/imop-geo.xsd">
    <geo:FRBRWork>''' + self.WorkId + '''</geo:FRBRWork>
    <geo:FRBRExpression>''' + self.ExpressionId + '''</geo:FRBRExpression>'''
        if hasattr (self, 'JuridischeNauwkeurigheid'):
            gioGML += '''
    <geo:juridischeNauwkeurigheid>''' + str (self.JuridischeNauwkeurigheid) + '''</geo:juridischeNauwkeurigheid>'''

        if not self.GIODelen is None:
            gioGML += '''
    <geo:groepen>'''
            for gioDeel in self.GIODelen.values ():
                gioGML += '''
        <geo:Groep>
            <geo:groepID>''' + gioDeel.GroepId + '''</geo:groepID>
            <geo:label>''' + gioDeel.Label + '''</geo:label>
            <geo:/Groep>'''
            gioGML += '''
    </geo:groepen>'''
        elif not self.NormLabel is None:
            gioGML += '''
    <geo:normlabel>''' + self.NormLabel + '''</geo:normlabel>'''
            if not self.NormID is None:
                gioGML += '''
    <geo:normID>''' + self.NormID + '''</geo:normID>'''
            if not self.EenheidLabel is None:
                gioGML += '''
    <geo:eenheidlabel>''' + self.EenheidLabel + '''</geo:eenheidlabel>'''
            if not self.EenheidID is None:
                gioGML += '''
    <geo:eenheidID>''' + self.EenheidID + '''</geo:eenheidID>'''


        gioGML += '''
    <geo:locaties>'''

        for locaties in self.Locaties.values ():
            for locatie in locaties:
                gioGML += '''
            <geo:Locatie>'''
                props = locatie.get ('properties')
                waarde = props.get('naam')
                if not waarde is None:
                    gioGML += '''
                <geo:naam>''' + waarde + '''</geo:naam>'''
                gioGML += '''
                <geo:geometrie>
                    <basisgeo:Geometrie>
                        <basisgeo:id>''' + props['id'] + '''</basisgeo:id>
                        <basisgeo:geometrie>
                            ''' + GeoData._GeometrieGML (locatie['geometry']) + '''
                        </basisgeo:geometrie>
                    </basisgeo:Geometrie>
                </geo:geometrie>'''
                waarde = None if self.AttribuutNaam is None else props.get(self.AttribuutNaam)
                if not waarde is None:
                    gioGML += '''
                <geo:''' + self.AttribuutNaam + '>' + str(waarde) + '</geo:' + self.AttribuutNaam + '>'
                gioGML += '''
            </geo:Locatie>'''

        gioGML += '''
    </geo:locaties>
</geo:GeoInformatieObjectVersie>'''
        return gioGML

    def SchrijfGIOWijziging (self) -> str:
        """Stel de XML op voor een GIO-wijziging (als string). Deze GeoData moet een GIO-wijziging zijn!"""

        wijzigingGML = '''<geo:GeoInformatieObjectVaststelling schemaversie="@@@IMOP_Versie@@@" xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0" xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/" xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://standaarden.overheid.nl/stop/imop/geo/
  https://standaarden.overheid.nl/stop/@@@IMOP_Versie@@@/imop-geo.xsd">
''' + ('' if self.Vaststellingscontext is None else self.Vaststellingscontext) + '''
    <geo:vastgesteldeVersie>
        <geo:GeoInformatieObjectMutatie>
            <geo:FRBRWork>''' + self.WorkId + '''</geo:FRBRWork>
            <geo:FRBRExpression>''' + self.Wordt.ExpressionId + '''</geo:FRBRExpression>
            <geo:juridischeNauwkeurigheid>''' + str (self.JuridischeNauwkeurigheid) + '''</geo:juridischeNauwkeurigheid>'''

        if not self.GIODelen is None:
            wijzigingGML += '''
            <geo:groepen>'''
            for gioDeel in self.GIODelen.values ():
                wijzigingGML += '''
                <geo:GroepMutatie>
                    <geo:groepID>''' + gioDeel.GroepId + '''</geo:groepID>
                    <geo:label>''' + gioDeel.Label + '''</geo:label>'''
                if not gioDeel.WijzigActie is None:
                    wijzigingGML += '''
                    <geo:wijzigactie>''' + gioDeel.WijzigActie + '''</geo:wijzigactie>'''
                wijzigingGML += '''
                </geo:GroepMutatie>'''

            wijzigingGML += '''
            </geo:groepen>'''
        elif not self.NormLabel is None:
            wijzigingGML += '''
                    <geo:normlabel>''' + self.NormLabel + '''</geo:normlabel>'''
            if not self.NormID is None:
                wijzigingGML += '''
                    <geo:normID>''' + self.NormID + '''</geo:normID>'''
            if not self.EenheidLabel is None:
                wijzigingGML += '''
                    <geo:eenheidlabel>''' + self.EenheidLabel + '''</geo:eenheidlabel>'''
            if not self.EenheidID is None:
                wijzigingGML += '''
                    <geo:eenheidID>''' + self.EenheidID + '''</geo:eenheidID>'''


        wijzigingGML += '''
            <geo:locatieMutaties>'''

        def __VoegLocatieToe (wijzigingGML, locatie, actie):
            wijzigingGML += '''
                <geo:LocatieMutatie>'''
            props = locatie.get ('properties')
            waarde = props.get('naam')
            if not waarde is None:
                wijzigingGML += '''
                    <geo:naam>''' + waarde + '''</geo:naam>'''
            wijzigingGML += '''
                    <geo:geometrie>
                        <basisgeo:Geometrie>
                            <basisgeo:id>''' + props['id'] + '''</basisgeo:id>
                            <basisgeo:geometrie>
                                ''' + GeoData._GeometrieGML (locatie['geometry']) + '''
                            </basisgeo:geometrie>
                        </basisgeo:Geometrie>
                    </geo:geometrie>'''
            waarde = None if self.AttribuutNaam is None else props.get(self.AttribuutNaam)
            if not waarde is None:
                wijzigingGML += '''
                    <geo:''' + self.AttribuutNaam + '>' + str(waarde) + '</geo:' + self.AttribuutNaam + '>'
            wijzigingGML += '''
                    <geo:wijzigactie>''' + actie + '''</geo:wijzigactie>'''
            wijzigingGML += '''
                </geo:LocatieMutatie>'''
            return wijzigingGML

        for locaties in self.Was.Locaties.values ():
            for locatie in locaties:
                wijzigingGML = __VoegLocatieToe (wijzigingGML, locatie, GeoData._Wijzigactie_Was)
        for locaties in self.Wordt.Locaties.values ():
            for locatie in locaties:
                wijzigingGML = __VoegLocatieToe (wijzigingGML, locatie, GeoData._Wijzigactie_Wordt)
        for locaties in self.WordtRevisies.Locaties.values ():
            for locatie in locaties:
                wijzigingGML = __VoegLocatieToe (wijzigingGML, locatie, GeoData._Wijzigactie_Revisie)

        wijzigingGML += '''
            </geo:locatieMutaties>'''

        if not self.WijzigMarkering is None and len (self.WijzigMarkering.Locaties) > 0:
            wijzigingGML += '''
                <geo:wijzigmarkeringen>'''

            for dimensie, markeringen in self.WijzigMarkering.Locaties.items ():
                markeringType = ('Punt' if dimensie == 0 else 'Lijn' if dimensie == 1 else 'Vlak')
                for markering in markeringen:
                    wijzigingGML += '''
                    <geo:''' + markeringType + '''>
                        <geo:geometrie>
                            <basisgeo:Geometrie>
                                <basisgeo:id>''' + markering['properties']['id'] + '''</basisgeo:id>
                                <basisgeo:geometrie>
                                    ''' + GeoData._GeometrieGML (markering['geometry']) + '''
                                </basisgeo:geometrie>
                            </basisgeo:Geometrie>
                        </geo:geometrie>
                    </geo:''' + markeringType + '''>'''

            wijzigingGML += '''
            </geo:wijzigmarkeringen>'''
        wijzigingGML += '''
        </geo:GeoInformatieObjectMutatie>
    </geo:vastgesteldeVersie>
    <geo:wasID>''' + self.Was.ExpressionId + '''</geo:wasID>
</geo:GeoInformatieObjectVaststelling>'''
        return wijzigingGML

    @staticmethod
    def _GeometrieGML(geom):
        geom['crs'] = {'properties' : { 'name': "urn:ogc:def:crs:EPSG::28992" } }
        gml = encode_v32 (geom, None)
        for withId in gml.xpath ('//*[@gml:id]', namespaces={'gml' : 'http://www.opengis.net/gml/3.2'}):
            withId.attrib.pop ('{http://www.opengis.net/gml/3.2}id')
        gml = lxml_etree.tostring (gml, encoding='unicode')
        gml = gml.replace (' xmlns:gml="http://www.opengis.net/gml/3.2"', '')
        return gml
#endregion

#======================================================================
#
# Manipulatie van geometrieën
#
#======================================================================

#----------------------------------------------------------------------
#
# Conversie naar Shapely objecten om mee te rekenen
#
#----------------------------------------------------------------------
#region Conversie naar Shapely objecten om mee te rekenen

    @staticmethod
    def MaakShapelyShape (locatie):
        """Maak een Shapely shape voor de locatie (als dat niet eerder gebeurd is) en geef die terug.

        Argumenten:

        locatie {}  Een locatie voals die eerder is ingelezen
        """
        if not '_shape' in locatie or locatie['_shape'] is None:
            locatie['_shape'] = shape (locatie['geometry'])
        return locatie['_shape']
#endregion

#----------------------------------------------------------------------
#
# Omzetten multi-geometrie naar enkele geometrieën
#
#----------------------------------------------------------------------
#region Omzetten multi-geometrie naar enkele geometrieën

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

    def MaakLijstVanGeometrieen (self, dimensies : Set[int] = { 0, 1, 2 }) -> Tuple[Dict[int,List[EnkeleGeometrie]], bool]:
        """Zet de informatie in de locaties om in een lijst met objecten die elk slechts één geometrie (punt, lijn of vlak) hebben.

        Argumenten:

        dimensies int[] De dimensies waarvoor de enkele geometrieën gemaakt moeten worden. Voor andere dimensies worden de geometrieën
                        van de locaties as-is overgenomen.

        Geeft de lijst (per dimensie) terug, en een indicatie of er sprake is van multi-geometrie
        """
        lijsten = {}
        isMulti = False
        for dimensie, locaties in self.Locaties.items ():
            if len (locaties) > 0:
                lijsten[dimensie] = lijst = []
                if dimensie in dimensies:
                    for locatie in locaties:
                        attribuutwaarde = None if self.AttribuutNaam is None else locatie['properties'][self.AttribuutNaam]
                        opgesplitst = GeoData.SplitsMultiGeometrie (locatie)
                        if len (opgesplitst) > 1:
                            isMulti = True
                        lijst.extend (GeoData.EnkeleGeometrie(locatie, geom, attribuutwaarde) for geom in opgesplitst)
                else:
                    for locatie in locaties:
                        attribuutwaarde = None if self.AttribuutNaam is None else locatie['properties'][self.AttribuutNaam]
                        lijst.append (GeoData.EnkeleGeometrie(locatie, locatie, attribuutwaarde))
        return lijsten, isMulti

    @staticmethod
    def SplitsMultiGeometrie (locatie):
        """Zet de geometrie om in een geometrieen die elk slechts één geometrie (punt, lijn of vlak) hebben
        en die te gebruiken zijn als een locatie in GeoData.Locaties

        Argumenten:

        locatie object Een locatie uit een GeoData.Locaties
        index int  index van de locatie in de GeoData

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
#endregion
