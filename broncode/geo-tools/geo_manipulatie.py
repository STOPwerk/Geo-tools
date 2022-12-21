#======================================================================
#
# Gemeenschappelijke code voor alle geo-gerelateerde operaties
# en weergave van geo-informatie.
#
#======================================================================

from typing import Dict, List, Tuple

import pygml
from pygml.v32 import encode_v32, GML32_ENCODER
GML32_ENCODER.id_required = False # Basisgeometrie gebruikt geen gml:id
from lxml import etree as lxml_etree
from shapely.geometry import shape, mapping

import json
import math
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
#region Maken van een webpagina

    class Cache:
        def __init__ (self, generator):
            """Instantie met gegevens die door opeenvolgende operaties gedeeld moeten worden"""
            # Generator om de resultaat-pagina te maken
            self.Generator = generator
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
        self._Cache = GeoManipulatie.Cache (self.Generator)

    def _GebruikCache (self, cache : Cache) -> 'GeoManipulatie':
        """Laat deze operatie de cache van een andere GeoManipulatie operatie gebruiken"""
        self._Cache = cache
        self.Generator = cache.Generator
        return self

    def VoerUit(self):
        """Maak de webpagina aan"""
        self.Log.Informatie ("Geo-tools (@@@GeoTools_Url@@@) versie @@@VERSIE@@@.")
        try:
            # _VoerUit moet in een afgeleide klasse worden geïmplementeerd
            if self._VoerUit ():
                self.Log.Informatie ("De verwerking is voltooid.")
                self.Generator.VoegHtmlToe ("<p>&nbsp;</p>")
                einde = self.Generator.StartSectie ("<h3>Verslag van de verwerking</h3>")
            else:
                self.Log.Fout ("De verwerking is afgebroken.")
                self.Generator.VoegHtmlToe ("<p><b>De verwerking is afgeboken!</b></p>")
                einde = self.Generator.StartSectie ("<h3>Verslag van de incomplete verwerking</h3>")

            self.Generator.VoegHtmlToe ("<p>&nbsp;</p>")
            self.Log.MaakHtml (self.Generator, None)
            self.Generator.VoegHtmlToe (einde)
            return self.Generator.Html ()
        except Exception as e:
            self.Log.Fout ("Oeps, deze fout is niet verwacht: " + str(e))
            generator = WebpaginaGenerator (self._TitelBijFout)
            self.Log.MaakHtml (generator, None, "De verwerking is afgebroken.")
            return generator.Html ()
#endregion

#----------------------------------------------------------------------
#
# Niet-kaartgerelateerde hulpfuncties
#
#----------------------------------------------------------------------
#region Niet-kaartgerelateerde hulpfuncties
    def _InitialiseerWebpagina (self):
        """Voeg de bestanden toe nodig om OpenLayers kaarten op te nemen in de webpagina
        """
        if not hasattr (self._Cache, '_WebpaginaKanKaartTonen'):
            setattr (self._Cache, '_WebpaginaKanKaartTonen', True)
            self.Generator.LeesCssTemplate ('ol')
            self.Generator.LeesJSTemplate ("ol", True, True)
            self.Generator.LeesJSTemplate ("sldreader", True, True)
            self.Generator.LeesCssTemplate ("juxtapose")
            self.Generator.LeesJSTemplate ("juxtapose", True, True)
            self.Generator.LeesCssTemplate ("kaart")
            self.Generator.LeesJSTemplate ("kaart", True, True)
            self.Generator.LeesCssTemplate ("resultaat")
            self.Generator.LeesJSTemplate ("resultaat")

    def _ToonResultaatInTekstvak (self, tekst, filenaam : str, dataType : str, elementNaam : str = None, toon : bool = True):
        self._Cache._NaamIndex += 1
        elementId = 'resultaat_' + str(self._Cache._NaamIndex)
        self.Generator.VoegHtmlToe ('<textarea id="' + elementId + '" class="resultaat"')
        if not elementNaam is None:
            self.Generator.VoegHtmlToe (' name="' + elementNaam + '"')
        if not toon:
            self.Generator.VoegHtmlToe (' style="display: none;"')
        self.Generator.VoegHtmlToe ('>\n' + tekst.replace ('<', '&lt;').replace ('>', '&gt;') + '\n</textarea>\n')
        if toon:
            self.Generator.VoegHtmlToe ('<div><a data-copy="' + elementId + '" href="#">Kopieer</a> of <a data-download_' + dataType + '="' + elementId + '" data-filenaam="' + filenaam + '" href="#">download</a></div>\n')
#endregion

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
            # Definitie van de GIO-delen
            self.GIODelen : Dict[str,GeoManipulatie.GIODeel] = None
            # Label voor de norm
            self.NormLabel = None
            # ID voor de norm
            self.NormID = None
            # Label voor de eenheid van de normwaarden
            self.EenheidLabel = None
            # ID voor de eenheid van de normwaarden
            self.EenheidID = None
            # Teken-nauwkeurigheid in decimeter
            self.Tekennauwkeurigheid : int = None
            #----------------------------------------------------------
            # Voor een GIO-versie
            #----------------------------------------------------------
            # De expression-identificatie van de GIO
            self.ExpressionId : str = None
            # De vaststellingscontext van de GIO (indien bekend)
            self.Vaststellingscontext : str = None
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
            # De wordt-locaties die uitsluitend als revisie voorkomen
            self.WordtRevisies : GeoManipulatie.GeoData = None 
            # De wijzig-markering indien aanwezig, uitgesplitst naar de dimensie van de geometrieën.
            self.WijzigMarkering : Dict[int,GeoManipulatie.GeoData] = None
            #----------------------------------------------------------
            # Voor weergave op de kaart
            #----------------------------------------------------------
            # De naam waaronder deze date via VoegGeoDataToe is geregistreerd voor kaartweergave
            self._KaartgegevensNaam : str = None
            # De vereenvoudige geomeotrieën voor deze geo-data, per zoom-level.
            # Key van de collectie is de teken-nauwkeurigheid in decimeters
            self._VereenvoudigdeGeometrie : Dict[int,List[GeoManipulatie.GeoData]] = None
            # Als dit een vereenvoudigde geometrie is, geeft het zoom-level waarvoor deze geo-data is gemaakt.
            # Zoom-level is zoals gebruikt in OpenLayers.
            self._VoorZoomLevel = None
            # Als dit een vereenvoudige geometrie is, dan geeft _InGridCel aan waar in een grid hoeveel gemetrieën
            # gelokaliseerd zijn die in verband met de resolutie niet meer getoond worden.
            # Dit zijn (X,Y) coordinaten in een grid met cellen:
            # - Lengte en breedte zijn ZoomLevelDetailPerMeter
            # - Centrum van de cel is _GridCenterX + X * ZoomLevelDetailPerMeter, _GridCenterY + Y * ZoomLevelDetailPerMeter
            self._AantalInGridCel : GeoManipulatie.GeoData = None

        def GeometrieNaam (self, meervoud: bool) -> str:
            """Geeft de gewone naam voor de geometrieën in de geo-data, in enkel- of meervoud."""
            if self.Dimensie == 0:
                return "punten" if meervoud else "punt"
            if self.Dimensie == 1:
                return "lijnen" if meervoud else "lijn"
            if self.Dimensie == 2:
                return "vlakken" if meervoud else "vlak"

    def MaximaalZoomLevel (self, nauwkeurigheidDecimeter : int = None):
        """Maximaal zoom level voor een GIO bij gegeven nauwkeurigheid.
        
        Argumenten:

        nauwkeurigheidDecimeter int  Teken-nauwkeurigheid van de GIO. Bij None wordt de teken-nauwkeurigheid uit de specs gebruikt
        """
        maxZoom = 22 - math.floor(math.log2(self._Operatie.NauwkeurigheidInDecimeter () if nauwkeurigheidDecimeter is None else nauwkeurigheidDecimeter))
        return 22 if maxZoom > 22 else maxZoom

    def ZoomLevelDetailPerMeter (self, zoomLevel : int):
        """Geef de kleinst zichtbare details voor een zoomlevel bij gegeven nauwkeurigheid
        
        Argumenten:

        zoomLevel int  Zoom level, kan niet groter zijn dan MaximaalZoomLevel
        """
        return 0.1 * math.pow (2, (22 - zoomLevel) if zoomLevel < 22 else 0)

    def _GridCelNaarRD (self, dpm : float, cel : Tuple[int,int]) -> List[float]:
        """Conversie van grid cellen naar de coördinaten van het centrum van de cellen:

        Argumenten:
        dpm float  Uitkomst van ZoomLevelDetailPerMeter
        cel (x,y) Index van de cel als gemaat door _GridCelVoorPunt

        Geeft terug: De coördinaten van het centrum van de cel
        """
        return [GeoManipulatie._GridCenterX + cel[0] * dpm, GeoManipulatie._GridCenterY + cel[1] * dpm]

    def _PastGeometrieInGridCel (self, dpm : float, locatie):
        """Bekijk of een locatie-geometrie zo klein is dat die in een grid cel past,
        en geef terug welke dat is (indien te groot: geeft None terug).

        Argumenten:
        dpm float  Uitkomst van ZoomLevelDetailPerMeter
        locatie object  Locatie van GeoData
        """
        locatieShape = GeoManipulatie.MaakShapelyShape (locatie)
        if locatieShape.bounds[2] - locatieShape.bounds[0] <= dpm and locatieShape.bounds[3] - locatieShape.bounds[1] <= dpm:
            return self._GridCelVoorPunt (dpm, [(locatieShape.bounds[2] + locatieShape.bounds[0]) / 2, (locatieShape.bounds[3] + locatieShape.bounds[1]) / 2])

    def _GridCelVoorPunt (self, dpm : float, coords : List[float]):
        """Geef terug in welke grid cel een punt ligt.

        Argumenten:
        dpm float  Uitkomst van ZoomLevelDetailPerMeter
        coords [.,.]  Coördinaten van het punt
        """
        x = round ((coords[0] - GeoManipulatie._GridCenterX) / dpm)
        y = round ((coords[1] - GeoManipulatie._GridCenterY) / dpm)
        return (x,y)

    _GridCenterX = 142735.75
    _GridCenterY = 470715.91

#endregion

#----------------------------------------------------------------------
#
# Inlezen van GML
#
#----------------------------------------------------------------------
#region Inlezen van GML

    def LeesGeoBestand (self, key : str, verplicht : bool, bewaarGml = None) -> GeoData:
        """Lees de inhoud van een GIO, effectgebied of gebiedsmarkering.
        Het bestand wordt gevonden aan de hand van de specificatie key / input type="file" control naam.

        Argumenten:

        key str        Key waarvoor de data opgehaald moet worden
        verplicht bool Geeft aan dat het bestand aanwezig moet zijn (dus niet optioneel is)
        bewaarGml lambda  Functie die aangeroepen wordt met de GML van het bestand

        Geeft de inhoud van het bestand als GeoData terug, of None als er geen bestand/data is of als er een fout optreedt
        """
        self.Log.Detail ("Lees het GIO, gebiedsmarkering of effectgebied")
        gml = self.Request.LeesBestand (self.Log, key, verplicht)
        if not bewaarGml is None:
            bewaarGml (gml)
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
                if not data.Vaststellingscontext is None:
                    data.Vaststellingscontext = ElementTree.tostring (data.Vaststellingscontext, encoding='unicode')
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
            elt = geoXml.find (GeoManipulatie._GeoNS + 'groepen')
            if not elt is None:
                data.AttribuutNaam = 'groepID'
                data.GIODelen = {}
                for groepXml in elt.findall (GeoManipulatie._GeoNS + 'Groep'):
                    groepId = groepXml.find (GeoManipulatie._GeoNS + 'groepID')
                    elt2 = groepXml.find (GeoManipulatie._GeoNS + 'label')
                    if groepId is None or elt2 is None:
                        self.Log.Fout ("Een GIO-deel/groep moet een groepID en label hebben")
                        succes = False
                    else:
                        data.GIODelen[groepId.text] = GeoManipulatie.GIODeel (groepId.text, elt2.text)
                        if mutatie:
                            # GIO-wijziging
                            elt2 = groepXml.find (GeoManipulatie._GeoNS + 'wijzigactie')
                            if not elt2 is None:
                                data.GIODelen[groepId.text] = elt2.text

            else:
                elt = geoXml.find (GeoManipulatie._GeoNS + 'normlabel')
                if not elt is None:
                    data.NormLabel = elt.text
                    elt = geoXml.find (GeoManipulatie._GeoNS + 'normID')
                    if not elt is None:
                        data.NormID = elt.text
                    elt = geoXml.find (GeoManipulatie._GeoNS + 'eenheidlabel')
                    if not elt is None:
                        data.EenheidLabel = elt.text
                    elt = geoXml.find (GeoManipulatie._GeoNS + 'eenheidID')
                    if not elt is None:
                        data.EenheidID = elt.text

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
                elif data.AttribuutNaam == 'groepID':
                    if data.GIODelen is None:
                        self.Log.Fout ("GIO bevat geen definities van GIO-delen")
                        succes = False
                    else:
                        meldingen = set ()
                        for locatie in data.Locaties:
                            groepId = locatie['properties']['groepID']
                            if not groepId in data.GIODelen:
                                meldingen.add ("Locatie heeft onbekende groepID = '" + groepId + "'")
                        if len (meldingen) > 0:
                            succes = False
                            for melding in meldingen:
                                self.Log.Fout (melding)
                elif not data.NormLabel is None:
                    if data.AttribuutNaam is None:
                        self.Log.Fout ("GIO bevat een norm maar de locaties hebben geen normwaarden")
                        succes = False
                elif not data.AttribuutNaam is None:
                    if data.NormLabel is None:
                        self.Log.Fout ("GIO heeft geen label voor de norm")
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
                    if geoXml is None:
                        self.Log.Fout ("wijzigmarkering moet aanwezig zijn")
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
                data.Attributen[data.AttribuutNaam] = GeoManipulatie.Attribuut (data.AttribuutNaam, 'groepID')
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
        heeftAttribuut = None if data.AttribuutNaam is None else True
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
#endregion

#----------------------------------------------------------------------
#
# Maken van GML
#
#----------------------------------------------------------------------
#region Maken van GML

    def SchrijfGIO (self, gio : GeoData) -> str:
        """Stel de XML op voor een GIO (als string)

        Argumenten:
        gio GeoData  Het GIO
        """
        gioGML = '''<geo:GeoInformatieObjectVersie schemaversie="@@@IMOP_Versie@@@" xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0" xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://standaarden.overheid.nl/stop/imop/geo/
  https://standaarden.overheid.nl/stop/@@@IMOP_Versie@@@/imop-geo.xsd">
    <geo:FRBRWork>''' + gio.WorkId + '''</geo:FRBRWork>
    <geo:FRBRExpression>''' + gio.ExpressionId + '''</geo:FRBRExpression>'''
        if hasattr (gio, 'Tekennauwkeurigheid'):
            gioGML += '''
    <geo:tekennauwkeurigheid>''' + str (gio.Tekennauwkeurigheid) + '''</geo:tekennauwkeurigheid>'''

        if not gio.GIODelen is None:
            gioGML += '''
    <geo:groepen>'''
            for gioDeel in gio.GIODelen.values ():
                gioGML += '''
        <geo:Groep>
            <geo:groepID>''' + gioDeel.GroepId + '''</geo:groepID>
            <geo:label>''' + gioDeel.Label + '''</geo:label>
            <geo:/Groep>'''
            gioGML += '''
    </geo:groepen>'''
        elif not gio.NormLabel is None:
            gioGML += '''
    <geo:normlabel>''' + gio.NormLabel + '''</geo:normlabel>'''
            if not gio.NormID is None:
                gioGML += '''
    <geo:normID>''' + gio.NormID + '''</geo:normID>'''
            if not gio.EenheidLabel is None:
                gioGML += '''
    <geo:eenheidlabel>''' + gio.EenheidLabel + '''</geo:eenheidlabel>'''
            if not gio.EenheidID is None:
                gioGML += '''
    <geo:eenheidID>''' + gio.EenheidID + '''</geo:eenheidID>'''


        gioGML += '''
    <geo:locaties>'''

        for locatie in gio.Locaties:
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
                        ''' + GeoManipulatie._GeometrieGML (locatie['geometry']) + '''
                    </basisgeo:geometrie>
                </basisgeo:Geometrie>
            </geo:geometrie>'''
            waarde = None if gio.AttribuutNaam is None else props.get(gio.AttribuutNaam)
            if not waarde is None:
                gioGML += '''
            <geo:''' + gio.AttribuutNaam + '>' + waarde + '</geo:' + gio.AttribuutNaam + '>'
            gioGML += '''
        </geo:Locatie>'''

        gioGML += '''
    </geo:locaties>
</geo:GeoInformatieObjectVersie>'''
        return gioGML

    def SchrijfGIOWijziging (self, gioWijziging : GeoData) -> str:
        """Stel de XML op voor een GIO-wijziging (als string)

        Argumenten:
        gioWijziging GeoData  De GIO-wijzifging
        """

        wijzigingGML = '''<geo:GeoInformatieObjectVaststelling schemaversie="@@@IMOP_Versie@@@" xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0" xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/" xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://standaarden.overheid.nl/stop/imop/geo/
  https://standaarden.overheid.nl/stop/@@@IMOP_Versie@@@/imop-geo.xsd">
''' + gioWijziging.Vaststellingscontext + '''
    <geo:vastgesteldeVersie>
        <geo:GeoInformatieObjectMutatie>
            <geo:FRBRWork>''' + gioWijziging.WorkId + '''</geo:FRBRWork>
            <geo:FRBRExpression>''' + gioWijziging.Wordt.ExpressionId + '''</geo:FRBRExpression>
            <geo:tekennauwkeurigheid>''' + str (gioWijziging.Tekennauwkeurigheid) + '''</geo:tekennauwkeurigheid>'''

        if not gioWijziging.GIODelen is None:
            wijzigingGML += '''
            <geo:groepen>'''
            for gioDeel in gioWijziging.GIODelen.values ():
                wijzigingGML += '''
                <geo:Groep>
                    <geo:groepID>''' + gioDeel.GroepId + '''</geo:groepID>
                    <geo:label>''' + gioDeel.Label + '''</geo:label>'''
                if not gioDeel.WijzigActie is None:
                    wijzigingGML += '''
                    <geo:wijzigactie>''' + gioDeel.WijzigActie + '''</geo:wijzigactie>'''
                wijzigingGML += '''
                <geo:/Groep>'''

            wijzigingGML += '''
            </geo:groepen>'''
        elif not gioWijziging.NormLabel is None:
            wijzigingGML += '''
                    <geo:normlabel>''' + gioWijziging.NormLabel + '''</geo:normlabel>'''
            if not gioWijziging.NormID is None:
                wijzigingGML += '''
                    <geo:normID>''' + gioWijziging.NormID + '''</geo:normID>'''
            if not gioWijziging.EenheidLabel is None:
                wijzigingGML += '''
                    <geo:eenheidlabel>''' + gioWijziging.EenheidLabel + '''</geo:eenheidlabel>'''
            if not gioWijziging.EenheidID is None:
                wijzigingGML += '''
                    <geo:eenheidID>''' + gioWijziging.EenheidID + '''</geo:eenheidID>'''


        wijzigingGML += '''
            <geo:mutaties>'''

        def __VoegLocatieToe (wijzigingGML, locatie, actie):
            wijzigingGML += '''
                <geo:LocatieMutatie>
                    <geo:wijzigactie>''' + actie + '''</wijzigactie>'''
            props = locatie.get ('properties')
            revisieVan = props.get ('isRevisieVan')
            if not revisieVan is None:
                for was_id in revisieVan:
                    wijzigingGML += '''
                    <geo:isRevisieVan>''' + was_id + '''</geo:isRevisieVan>'''

            waarde = props.get('naam')
            if not waarde is None:
                wijzigingGML += '''
                    <geo:naam>''' + waarde + '''</geo:naam>'''
            wijzigingGML += '''
                    <geo:geometrie>
                        <basisgeo:Geometrie>
                            <basisgeo:id>''' + props['id'] + '''</basisgeo:id>
                            <basisgeo:geometrie>
                                ''' + GeoManipulatie._GeometrieGML (locatie['geometry']) + '''
                            </basisgeo:geometrie>
                        </basisgeo:Geometrie>
                    </geo:geometrie>'''
            waarde = None if gioWijziging.AttribuutNaam is None else props.get(gioWijziging.AttribuutNaam)
            if not waarde is None:
                wijzigingGML += '''
                    <geo:''' + gioWijziging.AttribuutNaam + '>' + waarde + '</geo:' + gioWijziging.AttribuutNaam + '>'
            wijzigingGML += '''
                </geo:LocatieMutatie>'''
            return wijzigingGML

        for locatie in gioWijziging.Was.Locaties:
            wijzigingGML = __VoegLocatieToe (wijzigingGML, locatie, 'verwijder')
        for locatie in gioWijziging.Wordt.Locaties:
            wijzigingGML = __VoegLocatieToe (wijzigingGML, locatie, 'voegtoe')
        for locatie in gioWijziging.WordtRevisies.Locaties:
            wijzigingGML = __VoegLocatieToe (wijzigingGML, locatie, 'reviseer')

        wijzigingGML += '''
            </geo:mutaties>
            <geo:wijzigmarkering>'''

        for dimensie, markeringen in gioWijziging.WijzigMarkering.items ():
            markeringType = ('Punt' if dimensie == 0 else 'Lijn' if dimensie == 1 else 'Vlak')
            for markering in markeringen.Locaties:
                wijzigingGML += '''
                <geo:''' + markeringType + '''>
                    <basisgeo:Geometrie>
                        <basisgeo:id>''' + markering['properties']['id'] + '''</basisgeo:id>
                        <basisgeo:geometrie>
                                ''' + GeoManipulatie._GeometrieGML (markering['geometry']) + '''
                        </basisgeo:geometrie>
                    </basisgeo:Geometrie>
                </geo:''' + markeringType + '''>'''


        wijzigingGML += '''
            </geo:wijzigmarkering>
        </geo:GeoInformatieObjectMutatie>
    </geo:vastgesteldeVersie>
    <geo:wasID>''' + gioWijziging.Was.ExpressionId + '''</geo:wasID>
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
        if not '_shape' in locatie:
            locatie['_shape'] = shape (locatie['geometry'])
        return locatie['_shape']
#endregion

#----------------------------------------------------------------------
#
# Wegschrijven als JSON voor kaart in de webpagina
#
#----------------------------------------------------------------------
#region Wegschrijven als JSON voor kaart in de webpagina

    def VoegGeoDataToe (self, geoData : GeoData):
        """Voeg de geo-gegevens uit een GIO of gebied toe aan de data beschikbaar in de resultaatpagina;

        Argumenten:

        geoData GeoData  Een geo-data object waarvan de locaties op de kaart weergegeven moeten worden

        Geeft de naam terug die gebruikt moet worden om de gegevens aan een kaart te koppelen
        """
        if geoData is None:
            self.Log.Detail ('Geen geo-data beschikbaar dus niet toegevoegd aan de kaartgegevens')
            return
        if not geoData._KaartgegevensNaam is None:
            # Is al eerder geregistreerd
            return geoData._KaartgegevensNaam

        self._Cache._NaamIndex += 1
        geoData._KaartgegevensNaam = 'data' + str(self._Cache._NaamIndex)
        self._Cache._Dimensie[geoData._KaartgegevensNaam] = geoData.Dimensie

        collectie = {
            'type' : 'FeatureCollection',
            'crs': { 'type': 'name', 'properties': { 'name': 'urn:ogc:def:crs:EPSG::28992' } },
            'features' : geoData.Locaties
        }
        # Bepaal de properties die op de kaart getoond kan worden
        if len (geoData.Attributen) > 0:
            collectie['properties'] = {a.Tag : [a.Label, '' if a.Eenheid is None else a.Eenheid] for a in geoData.Attributen.values ()} 

        if not geoData.GIODelen is None:
            collectie['properties']['GIO-deel'] = ['GIO-deel', '']
            collectie['features'] = []
            for locatie in geoData.Locaties:
                toon = locatie.copy ()
                toon['properties'] = locatie['properties'].copy ()
                toon['properties']['GIO-deel'] = geoData.GIODelen[toon['properties']['groepID']].Label
                collectie['features'].append (toon)

        # Bepaal de bounding box van de hele collectie
        bbox = None
        for locatie in geoData.Locaties:
            locatieShape = GeoManipulatie.MaakShapelyShape (locatie)
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
            self._Cache._BoundingBox[geoData._KaartgegevensNaam] = bbox

        # Voeg toe aan de scripts van de pagina
        self._InitialiseerWebpagina ()
        self.Generator.VoegSlotScriptToe ('\nKaartgegevens.Instantie.VoegDataToe ("' + geoData._KaartgegevensNaam + '",\n' + json.dumps (collectie, cls=GeoManipulatie._JsonGeoEncoder, ensure_ascii=False) + '\n);\n')
        return geoData._KaartgegevensNaam

    class _JsonGeoEncoder (json.JSONEncoder):
        def default(self, o):
            """Objecten worden niet meegenomen"""
            return None
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
        def __init__ (self, operatie : 'GeoManipulatie'):
            """Maak een nieuwe kaart om dadelijk te tonen"""
            self._Operatie = operatie
            self._Operatie._InitialiseerWebpagina ()
            self._Operatie._Cache._NaamIndex += 1
            # Initialisatie van de kaartlagen (per dimensie)
            self._InitialisatieScripts = { 0 : '', 1: '', 2: '' }
            self._DimensieLaatsteWijzigingInitialisatieScripts = None
            # Bounding box van alle lagen tot nu toe
            self._BoundingBox = None
            # Opties om door te geven aan de kaart
            self._Opties = {
                'kaartelementId': 'kaart_' + str(self._Operatie._Cache._NaamIndex),
                'kaartelementWidth': 900,
                'kaartelementHeight': 600
            }
            nauwkeurigheid = self._Operatie.Request.LeesString ("teken-nauwkeurigheid");
            if not nauwkeurigheid is None:
                self._Opties['teken-nauwkeurigheid'] = int (nauwkeurigheid)


        def VoegLaagToe (self, naam : str, dataNaam : str, symbolisatieNaam : str, inControls : bool = False, toonInitieel : bool = True, negeerBBox : bool = False):
            """Voeg data met symbolisatie toe aan de kaart
            
            Argumenten:

            naam str  Naam van de kaart zoals gebruikt bij de weergave van properties en bij het aan/uit zetten van lagen
            dataNaam str  Naam van de geodata die getoond moet worden, zoals verkregen uit de VoegGeoDataToe
            symbolisatieNaam str  Naam van de symbolisatie, zoals verkregen uit een van de Voeg*Toe methoden
            inControls bool  Geeft aan dat de laag aan/uit gezet kan worden door de eindgebruiker
            toonInitieel bool  Geeft aan dat de kaart bij weergave ven de kaart zichtbaar moet zijn.
            negeerBBox bool  Negeer de uitgestrektheid van de laag voor de bepalong van de initiële kaartview
            """
            self._DimensieLaatsteWijzigingInitialisatieScripts= self._Operatie._Cache._Dimensie[dataNaam]
            self._InitialisatieScripts[self._DimensieLaatsteWijzigingInitialisatieScripts] += ';\nkaart.VoegLaagToe ("' + naam + '", "' + dataNaam + '", "' + symbolisatieNaam + '")'
            if inControls:
                self.LaatsteLaagInControls (toonInitieel)
            if not negeerBBox:
                bbox = self._Operatie._Cache._BoundingBox.get (dataNaam)
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
            """Geeft aan dat het maximale zoom level overen moet komen met de teken-nauwkeurigheid
            
            Argumenten:

            extraZoom bool  Geeft aan dat er extra zoom levels moeten zijn zodat het effect van de teken-nauwkeurigheid te zien is
            """
            nauwkeurigheid = self._Operatie.NauwkeurigheidInDecimeter (False)
            if nauwkeurigheid is None:
                self._Opties.pop ('maxZoom', None)
            else:
                maxZoom = 22 - math.floor(math.log2(nauwkeurigheid))
                self._Opties['maxZoom'] = (22 if maxZoom > 22 else maxZoom) + (4 if extraZoom else 0)

        def Toon (self):
            """Toon een kaart op de huidige plaats in de webpagina"""
            self._Operatie.Generator.VoegHtmlToe (self._Operatie.Generator.LeesHtmlTemplate ("kaart", False).replace ('<!--ID-->', self._Opties['kaartelementId']))
            if not self._BoundingBox is None:
                self._Opties['bbox'] = self._BoundingBox
            
            self._Operatie.Generator.VoegSlotScriptToe ('\nwindow.addEventListener("load", function () {\nvar kaart = new Kaart ()' + ''.join (self._InitialisatieScripts[d] for d in [2,1,0]) + ';\nkaart.Toon (' + json.dumps (self._Opties) + ');\n});')
#endregion

#----------------------------------------------------------------------
#
# Symbolisatie
#
#----------------------------------------------------------------------
#region Symbolisatie

    def VoegDefaultSymbolisatieToe (self, geoData : GeoData) -> str:
        """Voeg de default symbolisatie toe voor de geodata
        
        Argumenten:

        geoData GeoData  Eerdef ingelezen data

        Geeft de naam terug die gebruikt moet worden om de symbolisatie aan geodata voor een kaart te koppelen
        """
        return self.VoegUniformeSymbolisatieToe (geoData.Dimensie, "#0000FF", "#0000CD")

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
            self._Cache._DefaultSymbolenToegevoegd[key] = naam =  self.VoegSymbolisatieToe (GeoManipulatie._MaakFeatureTypeStyle ([rule]))
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
            self.Log.Detail ('Geen symbolisatie beschikbaar dus niet toegevoegd aan de kaartgegevens')
            return
        symbolisatie = GeoManipulatie._StripHeader.sub ('', symbolisatie)

        # Voeg toe aan de scripts van de pagina
        self._InitialiseerWebpagina ()
        self._Cache._NaamIndex += 1
        naam = 'sym' + str(self._Cache._NaamIndex)
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

    def VoegWijzigMarkeringToe (self, dimensie : int, revisie : bool = False):
        """Voeg de symbolisatie voor de speciale wijzigmarkeringen toe en geef de naam terug"""
        key  = 'WM' + str(dimensie) + str(revisie)
        naam = self._Cache._DefaultSymbolenToegevoegd.get (key)
        if naam is None:
            self._Cache._DefaultSymbolenToegevoegd[key] = naam = self.VoegSymbolisatieToe (GeoManipulatie.WijzigMarkeringSymbolisatie (dimensie, revisie))
        return naam

    @staticmethod
    def WijzigMarkeringSymbolisatie (dimensie : int, revisie : bool = False):
        """Geef de symbolisatie voor de speciale wijzigmarkeringen"""
        return GeoManipulatie._MaakFeatureTypeStyle ([GeoManipulatie._RevisieMarkeringSymbolisatie[dimensie] if revisie else GeoManipulatie._WijzigMarkeringSymbolisatie[dimensie]])

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
                <CssParameter name="stroke">#F8CECC</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
                <CssParameter name="stroke-dasharray">5 5</CssParameter>
            </Stroke>
        </LineSymbolizer>
        <LineSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#82B366</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
                <CssParameter name="stroke-dasharray">0 5 5</CssParameter>
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
                <CssParameter name="stroke">#F8CECC</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
                <CssParameter name="stroke-dasharray">5 5</CssParameter>
            </Stroke>
        </PolygonSymbolizer>
        <PolygonSymbolizer>
            <Stroke>
                <CssParameter name="stroke">#82B366</CssParameter>
                <CssParameter name="stroke-width">3</CssParameter>
                <CssParameter name="stroke-linecap">round</CssParameter>
                <CssParameter name="stroke-dasharray">0 5 5</CssParameter>
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
# Ondersteuning rekenen met geometrieën
#
#======================================================================

#----------------------------------------------------------------------
#
# Teken-nauwkeurigheid
#
#----------------------------------------------------------------------
#region Teken-nauwkeurigheid

    def NauwkeurigheidInDecimeter (self, verplicht: bool = True) -> int:
        """Haal de nauwkeurigheid in decimeters uit de request parameters
        
        Argumenten:

        verplicht bool  Geeft aan dat de teken-nauwkeurigheid een verplichte parameter is

        Geeft de waarde als int terug, of None als de teken-nauwkeurigheid niet is opgegeven
        """
        if self.Request.LeesString ("teken-nauwkeurigheid") is None:
            if verplicht:
                self.Log.Fout ("De teken-nauwkeurigheid is niet opgegeven in de specificatie")
            return None
        try:
            nauwkeurigheid = int (self.Request.LeesString ("teken-nauwkeurigheid"))
        except:
            self.Log.Fout ('De opgegeven teken-nauwkeurigheid is geen getal: "' + self.Request.LeesString ("teken-nauwkeurigheid") + '"')
            return None
        return nauwkeurigheid

    def NauwkeurigheidInMeter (self, verplicht: bool = True) -> float:
        """Haal de nauwkeurigheid in meters uit de request parameters
        
        Argumenten:

        verplicht bool  Geeft aan dat de teken-nauwkeurigheid een verplichte parameter is

        Geeft de waarde als int terug, of None als de teken-nauwkeurigheid niet is opgegeven
        """
        nauwkeurigheid = self.NauwkeurigheidInDecimeter (True)
        if not nauwkeurigheid is None:
            try:
                return 0.1 * float (nauwkeurigheid)
            except:
                self.Log.Fout ('De opgegeven teken-nauwkeurigheid is geen getal: "' + self.Request.LeesString ("teken-nauwkeurigheid") + '"')
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
#endregion

#----------------------------------------------------------------------
#
# Zoom-afhankelijke operaties
#
#----------------------------------------------------------------------
#region Zoom-afhankelijke operaties

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

    def MaakSchaalafhankelijkeGeometrie (self, geoData : GeoData):
        """Vereenvoudig de geometrieën in de locaties voor weergave, waarbij
        voor lagere zoom-levels (verder uitgezoomd) minder detail getoond wordt.
        Geeft de lijst met vereenvoudigde GeoData terug
        """
        nauwkeurigheid = self.NauwkeurigheidInDecimeter (False) if geoData.Tekennauwkeurigheid is None else geoData.Tekennauwkeurigheid
        nauwkeurigheid = 1 if nauwkeurigheid is None else nauwkeurigheid
        if geoData._VereenvoudigdeGeometrie is None:
            geoData._VereenvoudigdeGeometrie = {}
        resultaat = geoData._VereenvoudigdeGeometrie.get (nauwkeurigheid)
        if not resultaat is None:
            return resultaat
        geoData._VereenvoudigdeGeometrie[nauwkeurigheid] = resultaat = []

        # Ga uit van de enkelvoudige geometrieën
        locatiesVoorgaandNiveau = geoData.Locaties

        # Key = (x,y) van cel, value = aantal geometrieën, som van X, som van Y
        aantalVoorgaandeNiveau : Dict[Tuple[int,int], GeoManipulatie.CelData] = {}
        voorgaandeCelDeler = 1
        for zoomLevel in range (self.MaximaalZoomLevel (nauwkeurigheid), 0, -1):
            locatiesAndersDanVoorgaande = False
            cellenAndersDanVoorgaande = False
            voorgaandeCelDeler *= 2

            # Neem de grid cellen uit het voorgaande niveau over op dit niveau
            aantalDitNiveau : Dict[Tuple[int,int], GeoManipulatie.CelData]= {}
            for celVoorgaandNiveau, voorgaandeData in aantalVoorgaandeNiveau.items ():
                celDitNiveau = (celVoorgaandNiveau[0] // voorgaandeCelDeler, celVoorgaandNiveau[1] // voorgaandeCelDeler)
                data = aantalDitNiveau.get (celDitNiveau)
                if data is None:
                    aantalDitNiveau[celDitNiveau] = voorgaandeData
                else:
                    cellenAndersDanVoorgaande = True # Dit niveau beslaat minder cellen
                    data.Combineer (voorgaandeData)

            dpm = self.ZoomLevelDetailPerMeter (zoomLevel)
            locatiesDitNiveau : List[object] = []
            if geoData.Dimensie == 0:
                # Behandel punten niet meer als losse geometrie als er meerdere in een grid cel vallen
                puntCellen : Dict[Tuple[int,int], GeoManipulatie.EnkeleGeometrie] = {}
                for locatie in locatiesVoorgaandNiveau:
                    punt = locatie['geometry']['coordinates']
                    cel = self._GridCelVoorPunt (dpm, punt)
                    data = aantalDitNiveau.get (cel)
                    if not data is None:
                        # Er zijn al meer punten in deze cel
                        data.VoegToe (punt[0], punt[1])
                        locatiesAndersDanVoorgaande = cellenAndersDanVoorgaande = True # Dit niveau heeft minder punten
                    else:
                        anderPunt = puntCellen.get (cel)
                        if not anderPunt is None:
                            # Er is nog een punt op dit niveau dat in de cel valt
                            puntCellen.pop (cel)
                            data = GeoManipulatie.CelData (punt[0], punt[1])
                            data.VoegToe (anderPunt[0], anderPunt[1])
                            locatiesAndersDanVoorgaande = cellenAndersDanVoorgaande = True # Dit niveau heeft minder punten
                        else:
                            # Tot nu toe het enige punt
                            puntCellen[cel] = punt
                locatiesDitNiveau = list (puntCellen.values ())

            else:
                # Laat een lijn of vlak weg als het helemaal in een grid cel valt
                for locatie in locatiesVoorgaandNiveau:
                    cel = self._PastGeometrieInGridCel (dpm, locatie)
                    if not cel is None:
                        # Ja, laat de geometrie weg
                        data = aantalDitNiveau.get (cel)
                        shape = self.MaakShapelyShape (locatie)
                        if data is None:
                            aantalDitNiveau[cel] = GeoManipulatie.CelData ((shape.bounds[0] + shape.bounds[2])/2, (shape.bounds[1] + shape.bounds[3])/2)
                        else:
                            data.VoegToe ((shape.bounds[0] + shape.bounds[2])/2, (shape.bounds[1] + shape.bounds[3])/2)
                        locatiesAndersDanVoorgaande = cellenAndersDanVoorgaande = True # Dit niveau heeft minder geometrieën
                    else:
                        # Nee, simplificeer de geometrie
                        vorigeShape = self.MaakShapelyShape (locatie)
                        shape = vorigeShape.simplify (dpm)
                        if not shape.__eq__ (vorigeShape):
                            locatiesAndersDanVoorgaande = True # Andere geometrie
                            locatie = {
                                'type': 'Feature',
                                'properties': locatie.get ('properties'),
                                'geometry': mapping(shape),
                                '_shape': shape
                            }
                        locatiesDitNiveau.append (locatie)

            # Het is nu mogelijk dat twee nabije geometrieën in twee naburige cellen terecht
            # komen, bijv met x-index = 127 en x = 128. Het volgende zoomniveau zijn het nog
            # steeds twee cellen, met x-index 63 en 64. Combineer daarom steeds naburige cellen,
            # daardoor zal de versmelting van naburige geometrieën wel plaatsvinden. Bovendien
            # wordt de afstand tussen naburige markers daardoor groter
            for cel in list (aantalDitNiveau.keys ()):
                data = aantalDitNiveau.pop (cel, None)
                if not data is None:
                    for dx in range (0, 4): # Combineer 4x4 cellen
                        for dy in range (0, 4):
                            if dx == 9 and dy == 0:
                                continue
                            buur = (cel[0] + dx, cel[1] + dy)
                            if data.Combineer (aantalDitNiveau.pop (buur, None)):
                                cellenAndersDanVoorgaande = True

                    # Ken dat toe aan de juiste grid cel
                    cel = self._GridCelVoorPunt (dpm, [data.CelX (), data.CelY ()])
                    aantalDitNiveau[cel] = data

            if locatiesAndersDanVoorgaande or cellenAndersDanVoorgaande:
                # Maak een nieuw niveau aan
                ditNiveau = GeoManipulatie.GeoData ()
                ditNiveau.Attributen = geoData.Attributen
                ditNiveau.Dimensie = geoData.Dimensie
                ditNiveau._VoorZoomLevel = zoomLevel
                if locatiesAndersDanVoorgaande:
                    ditNiveau.Locaties = locatiesDitNiveau
                else:
                    ditNiveau.Locaties = None

                if cellenAndersDanVoorgaande:
                    ditNiveau._AantalInGridCel = GeoManipulatie.GeoData ()
                    ditNiveau._AantalInGridCel.Attributen = { 'n': GeoManipulatie.Attribuut ('n',  'Aantal niet-getoonde locaties') }
                    ditNiveau._AantalInGridCel.Dimensie = 0
                    ditNiveau._AantalInGridCel.Locaties = [{
                        'type': 'Feature',
                        'properties': { 'n': data.Aantal },
                        'geometry': {
                            'type': 'Point',
                            'coordinates': self._GridCelNaarRD (dpm, cel)
                        }
                    } for cel, data in aantalDitNiveau.items ()]

                resultaat.append (ditNiveau)

                aantalVoorgaandeNiveau = aantalDitNiveau
                voorgaandeCelDeler = 1
                locatiesVoorgaandNiveau = locatiesDitNiveau

        return resultaat

    def VoegSchaalafhankelijkeLagenToe (self, kaart : Kaart, naam: str, geoData : GeoData, geometrieSymbolisatieNaam: str, markeringSymbolisatieNaam: str, postLaag = None):
        """Voeg de schaalafhankelijke kaartlagen aan de kaart toe; ze moeten eerder zijn gemaakt via MaakSchaalafhankelijkeGeometrie.

        Argumenten:

        kaart Kaart  Kaart waaraan de lagen toegevoegd moeten worden
        naam str  Naam van de kaartlaag
        geoData GeoData  De geometrieën die aan de kaart toegevoegd moeten worden
        geometrieSymbolisatieNaam str  Naam van de symbolisatie (verkregen via een van de Voeg*Toe methoden) te gebruiken voor de locaties in geoData.
        markeringSymbolisatieNaam str  Naam van de symbolisatie (verkregen via een van de Voeg*Toe methoden) te gebruiken voor de punten die ontbrekende geometrieën aanduiden.
        postLaag lambda  Methode die aangeroepen wordt nadat een kaartlaag is toegevoegd
        """
        schaalafhankelijk = self.MaakSchaalafhankelijkeGeometrie (self._Geometrie)

        kaart.VoegLaagToe (naam, self.VoegGeoDataToe (geoData), geometrieSymbolisatieNaam)
        if not postLaag is None:
            postLaag ()
        voorgaandeZoom = None
        for geschaald in schaalafhankelijk:
            if not geschaald.Locaties is None:
                kaart.LaatsteLaagZoomLevel (geschaald._VoorZoomLevel, voorgaandeZoom)
                voorgaandeZoom = geschaald._VoorZoomLevel
                dataNaam = self.VoegGeoDataToe (geschaald)
                kaart.VoegLaagToe (naam, dataNaam, geometrieSymbolisatieNaam)
        if not voorgaandeZoom is None:
            kaart.LaatsteLaagZoomLevel (None, voorgaandeZoom)

        # Nu placeholders voor de ontbrekende geometrieën, indien noodzakelijk
        voorgaandeZoom = None
        for geschaald in schaalafhankelijk:
            if not geschaald._AantalInGridCel is None:
                if not voorgaandeZoom is None:
                    kaart.LaatsteLaagZoomLevel (geschaald._VoorZoomLevel, voorgaandeZoom)
                dataNaam = self.VoegGeoDataToe (geschaald._AantalInGridCel)
                kaart.VoegLaagToe (naam, dataNaam, markeringSymbolisatieNaam, False, False, True)
                voorgaandeZoom = geschaald._VoorZoomLevel
        if not voorgaandeZoom is None:
            kaart.LaatsteLaagZoomLevel (None, voorgaandeZoom)
#endregion
