#======================================================================
#
# /toon_geo
#
#======================================================================
#
# Script om een GIO of gebiedmarkering/effectgebied te tonen in een 
# viewer.
#
#======================================================================

from typing import Dict, List, Tuple

from shapely.geometry import mapping

from applicatie_meldingen import Meldingen
from applicatie_operatie import Operatie
from applicatie_request import Parameters
from data_geodata import GeoData, Attribuut
from weergave_kaart import KaartGenerator
from weergave_webpagina import WebpaginaGenerator

class ToonGeo (Operatie):
#======================================================================
#
# Webpagina's
#
#======================================================================
#region Webpagina's
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("Tonen van een GIO-versie of gebieden")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters, log: Meldingen = None):
        return ToonGeo (request, log).VoerUit ()
#endregion

#======================================================================
#
# Implementatie
#
#======================================================================
#region Implementatie
    def __init__(self, request : Parameters, log: Meldingen, defaultTitel = None, titelBijFout = None):
        super ().__init__ (request, log, "Geo-informatie in beeld" if defaultTitel is None else defaultTitel, "Geo-informatie - geen beeld" if titelBijFout is None else titelBijFout)
        # Geometrie specificatie
        self._Geometrie : GeoData = None
        # Namen van de geometrische data voor kaartweergave
        self._DataNamen : Dict[int,str] = None
        # Naam van de "dikke pen"-randen afgeleid van de geometrische data
        self._RandDataNaam : str = None
        # Naam van de symbolisatie voor de "dikke pen"-randen afgeleid van de geometrische data
        self._RandSymbolisatieNaam : str = None
        # Naam van de geometrische data met de analyseresultaten
        self._AnalyseResultaat : GeoData = None

    def _VoerUit (self):
        """Voer het request uit"""
        if self.Request.LeesString ("beschrijving"):
            self.Generator.VoegHtmlToe ('<p>' + self.Request.LeesString ("beschrijving") + '</p>') 

        if self._Geometrie is None:
            self.Log.Informatie ("Lees het GIO, gebiedsmarkering of effectgebied")
            self._Geometrie = GeoData.LeesGeoBestand (self.Request, 'geometrie', True)
            if self._Geometrie is None:
                return False
            if self._Geometrie.Soort == 'GIO-wijziging':
                self.Log.Fout ("Kan deze geo-informatie niet weergeven: " + self._Geometrie.Soort)
                return False

        if self._Geometrie.Soort == GeoData.SOORT_GIOVersie and not self._Geometrie.AttribuutNaam is None:
            self.Log.Informatie ('GIO heeft per locatie een ' + self._Geometrie.AttribuutNaam + ' - een symbolisatie is nodig om dat weer te geven')
        self._InitSymbolisatieNamen ([self._Geometrie])

        self.Generator.VoegHtmlToe ('Bestand: ' + self.Request.Bestandsnaam ('geometrie'))


        if self._Geometrie.Soort == GeoData.SOORT_GIOVersie and not self._Geometrie.JuridischeNauwkeurigheid is None:
            self._MaakRanden ()

        self.Log.Informatie ('Maak de kaartweergave')
        self._DataNamen = self.Kaartgenerator.VoegGeoDataToe (self._Geometrie)
        kaart = KaartGenerator.Kaart (self.Kaartgenerator)
        kaart.ZoomTotNauwkeurigheid (True)
        if not self._RandDataNaam is None:
            kaart.VoegLaagToe ('Juridische nauwkeurigheid', self._RandDataNaam, self._RandSymbolisatieNaam, True, False)
        kaart.VoegLagenToe (self._Geometrie.Soort, self._DataNamen, self._SymbolisatieNamen)
        kaart.Toon ()

        if self._Geometrie.Soort == GeoData.SOORT_GIOVersie and not self._Geometrie.JuridischeNauwkeurigheid is None:
            if self.Request.IsOptie ("toon-gio-schaalafhankelijk", True):
                self.Log.Informatie ('Toon GIO met schaalafhankelijkheid')
                self.Generator.VoegHtmlToe ('<p>De GIO-versie is met een juridische nauwkeurigheid van ' + str(self._Geometrie.JuridischeNauwkeurigheid) +  ''' decimeter opgesteld.
                Een GIO-viewer zou dat kunnen laten zien en/of gebruiken om het maximale zoom-niveau in te perken. Een viewer kan ook andere schaal-afhankelijke vereenvoudigingen doorvoeren,
                bijvoorbeeld vereenvoudiging van geometrieën en/of het clusteren van vrijwel onzichtbare geometrieën, zoals in deze kaart gedaan is:.</p>''')

                kaart = KaartGenerator.Kaart (self.Kaartgenerator)
                kaart.ZoomTotNauwkeurigheid (False)
                schaalafhankelijk = self.Kaartgenerator.MaakSchaalafhankelijkeGeometrie (self._Geometrie, self._Geometrie.Soort)
                self.Kaartgenerator.VoegSchaalafhankelijkeLocatiesToe (kaart, schaalafhankelijk, self._SymbolisatieNamen)
                self.Kaartgenerator.VoegSchaalafhankelijkeMarkeringenToe (kaart, schaalafhankelijk, self.Kaartgenerator.VoegWijzigMarkeringToe (0, True))
                kaart.Toon ()

            if self.Request.IsOptie ("kwaliteitscontrole", False):
                self.Log.Informatie ('Onderzoek de kwaliteit van de GIO-versie')
                self.Generator.VoegHtmlToe ('''<p>De GIO-versie kan gebruikt worden als oude of nieuwe versie in een GIO-wijziging als de juridische nauwkeurigheid in
                overeenstemming is met de detaillering van de geometrieën en als de verschillende locaties voldoende van elkaar gescheiden zijn.</p>''')
                self._VoerKwaliteitscontroleUit ();

                if self._AnalyseResultaat is None:
                    self.Generator.VoegHtmlToe ('''<p>Bij de kwaliteitscontrole zijn geen aandachtspunten gevonden.</p>''')
                else:
                    self.Generator.VoegHtmlToe ('''<p>De geometrieën waar problemen gevonden zijn, zijn op de kaart weergegeven. Klik op een geometrie om de beschrijving te tonen.</p>''')
                    kaart = KaartGenerator.Kaart (self.Kaartgenerator)
                    if not self._RandDataNaam is None:
                        kaart.VoegLaagToe ('Juridische nauwkeurigheid', self._RandDataNaam, self._RandSymbolisatieNaam, True, False)
                    kaart.VoegLagenToe (self._Geometrie.Soort, self._DataNamen, {d: self.Kaartgenerator.VoegUniformeSymbolisatieToe (d, '#ffffff', '#888888', '0.5') for d in [0,1,2]})
                    analysenamen = self.Kaartgenerator.VoegGeoDataToe (self._AnalyseResultaat)
                    kaart.VoegLagenToe ('Resultaat kwaliteitscontrole', analysenamen, {d: self.Kaartgenerator.VoegUniformeSymbolisatieToe (d, '#F8CECC', '#B85450') for d in [0,1,2]}, True)
                    kaart.Toon ()

        self.Log.Detail ('Maak de pagina af')
        self.Generator.LeesCssTemplate ('resultaat')
        return True
#endregion

#======================================================================
#
# Rekenen met juridische nauwkeurigheid
#
#======================================================================
#region Rekenen met juridische nauwkeurigheid
    def _MaakRanden (self):
        if self._RandSymbolisatieNaam is None:
            self._RandSymbolisatieNaam = self.Kaartgenerator.VoegUniformeSymbolisatieToe (2, '#cccccc', '#000000', '0.5')
        if not self._RandDataNaam is None:
            return

        self.Log.Detail ('Bereken randen via buffers om locaties')
        randen = GeoData ()
        randen.Locaties = { 2: [] }
        for dimensie in sorted (self._Geometrie.Locaties.keys (), reverse=True):
            for locatie in self._Geometrie.Locaties[dimensie]:
                rand = GeoData.MaakShapelyShape (locatie).buffer (0.05 * self._Geometrie.JuridischeNauwkeurigheid)
                if dimensie == 2:
                    rand = rand.difference (GeoData.MaakShapelyShape (locatie).buffer (-0.05 * self._Geometrie.JuridischeNauwkeurigheid))
                randen.Locaties[2].append ({ 
                    'type': 'Feature', 
                    'geometry': mapping (rand)
                })
        self.Log.Detail ('Randen zijn bepaald')
        self._RandDataNaam = self.Kaartgenerator.VoegGeoDataToe (randen)[2]

    def _VoerKwaliteitscontroleUit (self):

        self.Generator.VoegHtmlToe ('''<p>Om de kwaliteit van de GIO-versie te bepalen worden de volgende stappen doorlopen:.</p>
        <p><ol><li>Bepaal voor elke losse geometrie de "buitenrand": de buitenste rand van de geometrie met een "dikke rand":<br/>
        <code>buitenrand = geometrie.<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.buffer.html#shapely.buffer" target="_blank">buffer</a> (juridische nauwkeurigheid / 2)</code></li>
        <li>Bepaal voor elke losse geometrie het "binnengebied": de binnenste rand van de geometrie met een "dikke rand":<br/>
        <code>binnengebied = geometrie</code> voor een punt of lijn,<br/>
        <code>binnengebied = geometrie.<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.buffer.html#shapely.buffer" target="_blank">buffer</a> (- juridische nauwkeurigheid / 2)</code> voor vlakken.<br/>''')

        self.Log.Detail ('Maak binnengebieden en buitenranden voor losse geometrieën')

        enkeleGeometrieen : List[GeoData.EnkeleGeometrie] = []
        buitenranden : List[GeoData.EnkeleGeometrie] = []
        binnengebieden : List[GeoData.EnkeleGeometrie] = []
        rapporteerGeometrieen : List[GeoData.EnkeleGeometrie] = []
        numGeometrieMetGebrek = 0
        geenProblemen = True
        # Vlakken per locatie; key is locatie ID, value is lijst met geometrieën
        locatieVlakken : Dict[str,List[GeoData.EnkeleGeometrie]] = {}
        for dimensie, geometrieen in self._Geometrie.MaakLijstVanGeometrieen ()[0].items ():
            for geometrie in geometrieen:
                geometrie._Analyse : List[str] = []
                geometrie._Dimensie = dimensie
                geometrie._Index = len (enkeleGeometrieen)
                enkeleGeometrieen.append (geometrie)

                buitenrand = GeoData.MaakShapelyShape (geometrie.Geometrie).buffer (0.05 * self._Geometrie.JuridischeNauwkeurigheid)
                buitenrand = GeoData.EnkeleGeometrie (geometrie.Locatie, buitenrand, geometrie.Attribuutwaarde) # Geometrie is hier een shape
                buitenrand._Bron = geometrie
                buitenranden.append (buitenrand)
                geometrie._Buitenrand = buitenrand

                geometrie._Binnengebied = None
                binnengebied = GeoData.MaakShapelyShape (geometrie.Geometrie)
                if dimensie == 2:
                    binnengebied = binnengebied.buffer (-0.05 * self._Geometrie.JuridischeNauwkeurigheid)
                    if binnengebied.is_empty:
                        geometrie._Analyse.append ('Vlak heeft geen binnengebied')
                        numGeometrieMetGebrek += 1
                        continue
                    lijst = locatieVlakken.get (geometrie.ID)
                    if lijst is None:
                        locatieVlakken[geometrie.ID] = [geometrie]
                    else:
                        lijst.append (geometrie)

                binnengebied = GeoData.EnkeleGeometrie (geometrie.Locatie, binnengebied, geometrie.Attribuutwaarde) # Geometrie is hier een shape
                binnengebieden.append (binnengebied)
                binnengebied._Bron = geometrie
                geometrie._Binnengebied = binnengebied

        if numGeometrieMetGebrek > 0:
            geenProblemen = False
            self.Generator.VoegHtmlToe ('Voor ' + str(numGeometrieMetGebrek) + ' vlak' + ('' if numGeometrieMetGebrek == 1 else 'ken') + '''  is er geen "binnengebied" omdat de geometrie 
            te smal of klein is in vergelijking met de juridische nauwkeurigheid. Het wijzigen van zo\'n vlak zal niet worden gedetecteerd.''')
        self.Generator.VoegHtmlToe ('</li>')

        if len (binnengebieden) == 0:
            self.Generator.VoegHtmlToe ('<li>Er zijn geen losse geometrieën die een "binnengebied" hebben. De overige stappen in de kwaliteitscontrole worden overgeslagen.</li>')
        else:
            if len (locatieVlakken) > 0:
                self.Generator.VoegHtmlToe ('''<li>Verifieer dat locaties met vlakken geen uitstulpingen hebben die dunner zijn dan de juridische nauwkeurigheid
                en significant uitsteken buiten het binnengebied:<br/>
                <code>locatie_geometrie.<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.difference.html#shapely.difference" target="_blank">difference</a> (locatie_binnengebied.<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.buffer.html#shapely.buffer" target="_blank">buffer</a> (2 * juridische nauwkeurigheid)) moet leeg zijn</code> 
                <br/>Het wijzigen van deze uitstulpingen zal niet worden gedetecteerd.''')
                
                self.Log.Detail ('Bepaal vergroot binnengebied per locatie-met-vlakken, en verifieer dat alle vlakken daar binnen liggen')
                numGeometrieMetGebrek = 0
                for vlakken in locatieVlakken.values ():
                    binnengebied = None
                    for geometrie in vlakken:
                        if not geometrie._Binnengebied is None:
                            if binnengebied is None:
                                binnengebied = geometrie._Binnengebied.Geometrie
                            else:
                                binnengebied = binnengebied.union (geometrie._Binnengebied.Geometrie)
                    if not binnengebied is None:
                        # Maak het binnengebied groter
                        binnengebied = binnengebied.buffer (0.2 * self._Geometrie.JuridischeNauwkeurigheid)
                        isOK = True
                        for geometrie in vlakken:
                            uitstulpingen = GeoData.MaakShapelyShape (geometrie.Geometrie).difference (binnengebied)
                            if not uitstulpingen.is_empty:
                                uitstulpingen = GeoData.EnkeleGeometrie (geometrie.Locatie, uitstulpingen, geometrie.Attribuutwaarde) # Geometrie is hier een shape
                                uitstulpingen._Dimensie = geometrie._Dimensie
                                uitstulpingen._Analyse = ['Locatie-geometrie heeft uitstulpingen']
                                rapporteerGeometrieen.append (uitstulpingen)
                        if not isOK:
                            numGeometrieMetGebrek += 1

                if numGeometrieMetGebrek > 0:
                    geenProblemen = False
                    self.Generator.VoegHtmlToe (' Bij ' + str(numGeometrieMetGebrek) + ' locatie' + ('' if numGeometrieMetGebrek == 1 else 's') + '  is dit het geval.')
                self.Generator.VoegHtmlToe ('</li>')

            self.Generator.VoegHtmlToe ('''<li>Verifieer dat er geen geometrieën zijn waarvan het binnengebied geheel binnen de buitenrand van een of meer andere geometrieën
            ligt.<br/>
            <code>gebied = binnengebied</code><br/>
            <code>gebied = gebied.<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.difference.html#shapely.difference" target="_blank">difference</a> (buitenrand)</code> voor alle buitenranden behalve die behorend bij het binnengebied <br/>
            <code>gebied mag niet leeg zijn</code><br/>
            Er zijn situaties dat het wijzigen van deze geometrieën niet gedetecteerd zal worden.''')
            self.Log.Detail ('Bepaal welke binnengebieden geheel binnen een buitenrand van een of meer andere geometrieën ligt')
            numGeometrieMetGebrek = 0
            for binnengebied in binnengebieden:
                nietInRand = binnengebied.Geometrie
                for buitenrand in buitenranden:
                    if buitenrand._Bron._Index != binnengebied._Bron._Index:
                        nietInRand = nietInRand.difference (buitenrand.Geometrie)
                        if nietInRand.is_empty:
                            break
                if nietInRand.is_empty:
                    binnengebied._Bron._Analyse.append ('Binnengebied geheel in buitenrand andere geometrieën')
                    numGeometrieMetGebrek += 1

            if numGeometrieMetGebrek > 0:
                geenProblemen = False
                self.Generator.VoegHtmlToe (' Bij ' + str(numGeometrieMetGebrek) + ' geometrie' + ('' if numGeometrieMetGebrek == 1 else 'ën') + ' is dit het geval.')
            self.Generator.VoegHtmlToe ('</li>')

            self.Generator.VoegHtmlToe ('''<li>Verifieer dat er geen overlap in de geometrieën bestaat, waarbij het binnengebied van twee geometrieën
            punten gemeen hebben. Snijdende lijnen binnen dezelfde locatie worden niet gerapporteerd.<br/>
            <code>binnengebied1.<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.intersection.html#shapely.intersection" target="_blank">intersection</a> (binnengebied2) moet leeg zijn</code> <br/>
            ''')
            self.Log.Detail ('Bepaal welke binnengebieden gedeeltelijk overlappen')
            numGeometrieMetGebrek = 0
            numGeometrieTegenstrijdig = 0
            indexVolgende = 0
            for binnengebied1 in binnengebieden:
                indexVolgende += 1
                binnengebiedShape = binnengebied1.Geometrie
                for binnengebied2 in [binnengebieden[i] for i in range (indexVolgende, len (binnengebieden))]:
                    if binnengebied1._Bron._Dimensie != 1 or binnengebied1.Locatie != binnengebied2.Locatie:
                        overlap = binnengebiedShape.intersection (binnengebied2.Geometrie)
                        if not overlap.is_empty:
                            numGeometrieMetGebrek += 1
                            binnengebied1._Bron._Analyse.append ('Binnengebied overlapt met binnengebied andere geometrie')
                            binnengebied2._Bron._Analyse.append ('Binnengebied overlapt met binnengebied andere geometrie')
                            if binnengebied1.Attribuutwaarde != binnengebied2.Attribuutwaarde:
                                binnengebied1._Bron._Analyse.append ('Overlappend binnengebied met verschillende warde voor ' + self._Geometrie.AttribuutNaam)
                                binnengebied2._Bron._Analyse.append ('Overlappend binnengebied met verschillende warde voor ' + self._Geometrie.AttribuutNaam)
                                numGeometrieTegenstrijdig += 1

            if numGeometrieMetGebrek > 0:
                geenProblemen = False
                self.Generator.VoegHtmlToe (' Bij ' + str(numGeometrieMetGebrek) + ' geometrie-' + ('paar' if numGeometrieMetGebrek == 1 else 'paren') + '  is dit het geval')
                if numGeometrieTegenstrijdig > 0:
                    self.Generator.VoegHtmlToe (', en bij ' + str(numGeometrieTegenstrijdig) + ' ervan verschilt zelfs de waarde voor ' + self._Geometrie.AttribuutNaam)
                self.Generator.VoegHtmlToe ('.')
            self.Generator.VoegHtmlToe ('</li>')

        self.Log.Detail ('Kwaliteitscontrole afgerond')
        self.Generator.VoegHtmlToe ('</ol></p>')

        if not geenProblemen:
            self.Log.Detail ('Maak overzicht van analyseresultaten')
            self._AnalyseResultaat = GeoData ()
            self._AnalyseResultaat.Attributen = { 'r' : Attribuut ('r', 'Bevindingen'), 'id' : Attribuut ('id', 'Locatie ID') }
            self._AnalyseResultaat.Locaties = { }
            for geometrie in enkeleGeometrieen:
                if len (geometrie._Analyse) > 0:
                    geometrie.Geometrie['properties'] = {
                            'r' : '<br/>' + '<br/>'.join (geometrie._Analyse),
                            'id': geometrie.ID
                        }
                    if not geometrie._Dimensie in self._AnalyseResultaat.Locaties:
                        self._AnalyseResultaat.Locaties[geometrie._Dimensie] = []
                    self._AnalyseResultaat.Locaties[geometrie._Dimensie].append (geometrie.Geometrie)
            for geometrie in rapporteerGeometrieen:
                geometrie.Geometrie = {
                        'type': 'Feature',
                        'geometry': mapping (geometrie.Geometrie),
                        'properties': {
                            'r' : '<br/>' + '<br/>'.join (geometrie._Analyse),
                            'id': geometrie.ID
                        }
                    }
                if not geometrie._Dimensie in self._AnalyseResultaat.Locaties:
                    self._AnalyseResultaat.Locaties[geometrie._Dimensie] = []
                self._AnalyseResultaat.Locaties[geometrie._Dimensie].append (geometrie.Geometrie)
#endregion
