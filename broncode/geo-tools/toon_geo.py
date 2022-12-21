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

from typing import List, Tuple

from shapely.geometry import mapping
import math

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from geo_manipulatie import GeoManipulatie
from weergave_webpagina import WebpaginaGenerator

class GeoViewer (GeoManipulatie):
#======================================================================
#
# Webpagina's
#
#======================================================================
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("Tonen van een GIO-versie of gebieden")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters, log: Meldingen = None):
        return GeoViewer (request, log).VoerUit ()

#======================================================================
#
# Implementatie
#
#======================================================================
    def __init__(self, request : Parameters, log: Meldingen):
        super ().__init__ ("Geo-informatie in beeld", "Geo-informatie - geen beeld", request, log)
        # Geometrie specificatie
        self._Geometrie : GeoManipulatie.GeoData = None
        # Naam van de geometrische data voor kaartweergave
        self._DataNaam : str = None
        # Naam waaronder de te gebruiken symbolisatie is geregistreerd
        self._SymbolisatieNaam : str = None

    def _VoerUit (self):
        """Voer het request uit"""
        if self.Request.LeesString ("beschrijving"):
            self.Generator.VoegHtmlToe ('<p>' + self.Request.LeesString ("beschrijving") + '</p>') 

        if self._Geometrie is None:
            self.Log.Informatie ("Lees het GIO, gebiedsmarkering of effectgebied")
            self._Geometrie = self.LeesGeoBestand ('geometrie', True)
            if self._Geometrie is None:
                return False
            if self._Geometrie.Soort == 'GIO-wijziging':
                self.Log.Fout ("Kan deze geo-informatie niet weergeven: " + self._Geometrie.Soort)
                return False

        symbolisatieVereist = False
        if self._Geometrie.Soort == 'GIO' and not self._Geometrie.AttribuutNaam is None:
            self.Log.Informatie ('GIO heeft per locatie een ' + self._Geometrie.AttribuutNaam + ' - een symbolisatie is nodig om dat weer te geven')
            symbolisatieVereist = True

        if self._SymbolisatieNaam is None:
            self.Log.Informatie ("Lees de symbolisatie (indien aanwezig)")
            symbolisatie = self.Request.LeesBestand (self.Log, "symbolisatie", False)
            if symbolisatie is None:
                if symbolisatieVereist:
                    self.Log.Waarschuwing ('Geen symbolisatie beschikbaar - gebruik de standaard symbolisatie voor geometrieën')
                else:
                    self.Log.Informatie ('Geen symbolisatie beschikbaar - gebruik de standaard symbolisatie voor geometrieën')
            else:
                self.Log.Informatie ("Symbolisatie ingelezen uit '" + self.Request.Bestandsnaam ("symbolisatie")+ "'")
            self._SymbolisatieNaam = self.VoegDefaultSymbolisatieToe (self._Geometrie) if symbolisatie is None else self.VoegSymbolisatieToe (symbolisatie)

        self.Generator.VoegHtmlToe ('Bestand: ' + self.Request.Bestandsnaam ('geometrie'))

        self.Log.Informatie ('Maak de kaartweergave')
        self._DataNaam = self.VoegGeoDataToe (self._Geometrie)
        kaart = GeoManipulatie.Kaart (self)
        kaart.ZoomTotNauwkeurigheid (True)
        kaart.VoegLaagToe (self._Geometrie.Soort, self._DataNaam, self._SymbolisatieNaam)
        kaart.Toon ()

        if self._Geometrie.Soort == 'GIO' and not self.NauwkeurigheidInDecimeter (False) is None:
            self.Log.Informatie ('Toon GIO met schaalafhankelijkheid')
            self.Generator.VoegHtmlToe ('<p>De GIO zou met een teken-nauwkeurigheid van ' + str(self.NauwkeurigheidInDecimeter ()) +  ''' decimeter zijn opgesteld.
            Een GIO-viewer zou dat kunnen gebruiken om het maximale zoom-niveau in te perken. Een viewer kan ook andere schaal-afhankelijke vereenvoudigingen doorvoeren,
            zoals in deze kaart gedaan is:.</p>''')

            kaart = GeoManipulatie.Kaart (self)
            kaart.ZoomTotNauwkeurigheid (False)
            self.VoegSchaalafhankelijkeLagenToe (kaart, self._Geometrie.Soort, self._Geometrie, self._SymbolisatieNaam, self.VoegWijzigMarkeringToe (0, True))
            kaart.Toon ()

            self.Log.Informatie ('Valideer de GIO op teken-nauwkeurigheid')
            self.Generator.VoegHtmlToe ('''<p>Het opgeven van een teken-nauwkeurigheid voor een GIO suggereert dat twee <a href="@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_Locatie.html" target="_blank">GIO-Locaties</a>
            elkaar niet overlappen binnen de teken-nauwkeurigheid. Om te zien of dat klopt wordt de elders beschreven <a href="@@@GeoTools_Url@@@wiki/Toon-controleer-gio" target="_blank">procedure</a> gevolgd.</p>''')
            lijst = self.MaakLijstVanGeometrieen (self._Geometrie)[0]
            heeftProblemen, tekennauwkeurigheid = self.ValideerGIO (lijst, self._Geometrie.Dimensie)
            if not heeftProblemen:
                self.Generator.VoegHtmlToe ('<p>Het GIO past inderdaad bij een teken-nauwkeurigheid van ' + str(self.NauwkeurigheidInDecimeter ()) + ' decimeter</p>')
            else:
                self.Generator.VoegHtmlToe ('<p>Het GIO past <b>niet</b> bij een teken-nauwkeurigheid van ' + str(self.NauwkeurigheidInDecimeter ()) + ''' decimeter.
                Tenzij de verkeerde teken-nauwkeurigheid opgegeven is zouden eerst de geometrieën in de GIO gecorrigeerd moeten worden. ''')
                if not tekennauwkeurigheid is None:
                    if tekennauwkeurigheid <= 0:
                        self.Generator.VoegHtmlToe ('Er is sprake van verschillende locaties waarvan de geometrieën samenvallen.')
                    else:
                        self.Generator.VoegHtmlToe ('Het GIO lijkt gemaakt voor een teken-nauwkeurigheid van ' + str(tekennauwkeurigheid) + ' decimeter of kleiner')
                self.Generator.VoegHtmlToe ('</p>')
        self.Log.Detail ('Maak de pagina af')
        self.Generator.LeesCssTemplate ('resultaat')
        return True

#======================================================================
#
# Controleren of een GIO geschikt is voor bepaling van GIO-wijziging
#
#======================================================================
    def ValideerGIO (self, geometrie: List[GeoManipulatie.EnkeleGeometrie], dimensie : int) -> Tuple[bool,float]:
        """Valideer dat de enkele locaties binnen een GIO onderling disjunct zijn

        Argumenten:

        geometrie EnkeleGeometrie[]  De geometrieën uit de GIO, gemaakt via MaakLijstVanGeometrieen
        dimensie int  Dimensie van de geometrieën in de GIO

        Geeft een of de GIO valide is. Geeft daarnaast (indien mogelijk) terug bij 
        welke tekennauwkeurigheid (in decimeter) de GIO wel valide is.
        """
        if self.NauwkeurigheidInMeter () is None:
            return (None, None)
        if dimensie == 0:
            return self._ValideerGIOPunten (geometrie)
        elif dimensie == 1:
            return self._ValideerGIOLijnen (geometrie)
        elif dimensie == 2:
            return (self._ValideerGIOVlakken (geometrie), None)
        raise 'dimensie = ' + str(dimensie)

    #------------------------------------------------------------------
    # Punten
    #------------------------------------------------------------------
    def _ValideerGIOPunten (self, punten: List[GeoManipulatie.EnkeleGeometrie]) -> Tuple[bool,float]:
        """Implementatie van ValideerGIO voor punt-geometrieën"""
        self.Generator.VoegHtmlToe ('''<p>Voor een GIO met punten als geometrie wordt gecontroleerd dat de afstand tussen de punten groter is dan de teken-nauwkeurigheid.''')
        nauwkeurigheid = self.NauwkeurigheidInMeter ()
        drempel = nauwkeurigheid * nauwkeurigheid
        minimaleAfstand = None
        afstanden = {}
        aantal = {}
        def __Afstand (i, afstand):
            afstand_i = afstanden.get (i)
            if afstand_i is None or afstand < afstand_i:
                afstanden[i] = afstand
            aantal_i = aantal.get (i)
            aantal[i] = (0 if aantal_i is None else aantal_i) + 1


        # Vind alle punten die te dicht bij een ander punt liggen
        for i in range (0, len (punten)):
            locatie_id_i = punten[i].Locatie['properties']['id']
            coord_i = punten[i].Geometrie['geometry']['coordinates']
            for j in range (i+1, len (punten)):
                if punten[j].Locatie['properties']['id'] != locatie_id_i:
                    coord_j = punten[j].Geometrie['geometry']['coordinates']
                    afstand = (coord_i[0] - coord_j[0]) * (coord_i[0] - coord_j[0]) + (coord_i[1] - coord_j[1]) * (coord_i[1] - coord_j[1])
                    if afstand < drempel:
                        __Afstand (i, afstand)
                        __Afstand (j, afstand)
                        if minimaleAfstand is None or afstand < minimaleAfstand:
                            minimaleAfstand  = afstand

        # Alleen voor weergave: teken een buffer om de punten
        dikkePunten = GeoManipulatie.GeoData ()
        dikkePunten.Dimensie = 2
        for i in range (0, len (punten)):
            dikkePunt = self.MaakShapelyShape (punten[i].Geometrie).buffer (0.5*nauwkeurigheid)
            dikkePunten.Locaties.append ({ 
                'type': 'Feature', 
                'geometry': mapping (dikkePunt)
            })

        kaart = GeoManipulatie.Kaart (self)
        kaart.ZoomTotNauwkeurigheid (True)
        dataNaam = self.VoegGeoDataToe (dikkePunten)
        symNaam = self.VoegUniformeSymbolisatieToe (2, "#DAE8FC", "#6C8EBF", '0.5')
        kaart.VoegLaagToe ("Getekende punt (diameter is teken-afstand)", dataNaam, symNaam, True, True)

        symNaam = self.VoegUniformeSymbolisatieToe (0, "#DAE8FC", "#6C8EBF", '0.5')
        kaart.VoegLaagToe ("Geo-informatieobject", self._DataNaam, symNaam, True, True)

        # Is er een probleem?
        if minimaleAfstand is None:
            self.Generator.VoegHtmlToe ('Dat is het geval.</p>')
            self.Log.Informatie ('Alle punten liggen tenminste ' + str(self.NauwkeurigheidInDecimeter ()) + ' decimeter van elkaar af')
        else:
            self.Log.Waarschuwing ('Er zijn ' + str(len (afstanden)) + ' punten die minder dan ' + str(self.NauwkeurigheidInDecimeter ()) + ' decimeter van elkaar af liggen, met een minimum van ' + str(minimaleAfstand) + ' decimeter')
            self.Generator.VoegHtmlToe ('Dat is niet het geval; er zijn ' + str(len (afstanden)) + ' punten die te dicht bij elkaar staan.</p>')

            problemen = GeoManipulatie.GeoData ()
            problemen.Attributen['d'] = GeoManipulatie.Attribuut ('d', 'Minimale afstand', 'decimeter')
            problemen.Attributen['n'] = GeoManipulatie.Attribuut ('n', 'Te nabije buren')
            problemen.AttribuutNaam = 'afstand'
            problemen.Dimensie = 1
            for i, afstand in afstanden.items ():
                punt = punten[i].Geometrie
                punt['properties'] = { 'd': round (math.sqrt (100*afstand), 2), 'n': aantal[i] }
                problemen.Locaties.append (punt);

            dataNaam = self.VoegGeoDataToe (problemen)
            symNaam = self.VoegWijzigMarkeringToe (1)
            kaart.VoegLaagToe ("Problematische geometrie", dataNaam , symNaam, True, True)

        kaart.Toon ()

        if minimaleAfstand is None:
            return (False, None)
        else:
            return (True, round(math.sqrt (100 * minimaleAfstand), 2))

    #------------------------------------------------------------------
    # Lijnen
    #------------------------------------------------------------------
    def _ValideerGIOLijnen (self, lijnen: List[GeoManipulatie.EnkeleGeometrie]) -> Tuple[bool,float]:
        """Implementatie van ValideerGIO voor lijn-geometrieën"""
        nauwkeurigheid = self.NauwkeurigheidInMeter ();
        self.Generator.VoegHtmlToe ('''<p>Voor een GIO met lijnen:
<ol>
    <li>Locaties waarvan de uitgestrektheid kleiner is dan de teken-nauwkeurigheid worden genegeerd, als: bounding_box.width &lt; ''' + '{:2f}'.format (nauwkeurigheid) + ''' en bounding_box.height &lt; ''' + '{:2f}'.format (nauwkeurigheid) + '''</li>
    <li>Geef de lijnen als dikte de teken-nauwkeurigheid: buffer (''' + '{:2f}'.format (nauwkeurigheid) + ''')</li>
    <li>Van de dikke lijnen wordt paarsgewijs de overlap (intersection) bepaald. Als er overlap is, dan komen de originele lijnen te dicht bij elkaar.
    <li>Van dikke lijnen die tot dezelfde locatie behoren wordt geen intersectie bepaald - de lijnen mogen dicht bij elkaar liggen of elkaar zelfs snijden.
</ol>
Klik op een lijn in de kaart om de uitkomst van de procedure te zien voor een locatie.</p>''')

        # Kopie van de GIO, met uitkomst van de analyse
        uitkomstData = GeoManipulatie.GeoData () # Voor weergave op een kaart
        uitkomstData.Dimensie = self._Geometrie.Dimensie
        uitkomstData.Attributen = self._Geometrie.Attributen.copy ()
        uitkomstData.Attributen['p'] = GeoManipulatie.Attribuut ('p', 'In orde')
        uitkomstLocaties = {}
        for locatie in self._Geometrie.Locaties:
            uitkomstLocatie = { 
                'type': 'Feature', 
                'properties' : locatie['properties'].copy (), 
                'geometry': locatie['geometry'], 
                '_shape' : self.MaakShapelyShape (locatie)
            }
            uitkomstData.Locaties.append (uitkomstLocatie)
            uitkomstLocaties[locatie['properties']['id']] = uitkomstLocatie

        # Verzamel alle intersecties in:
        problemen = GeoManipulatie.GeoData ()
        problemen.Dimensie = 2

        # Zoek eerst uit of er te kleine lijnen zijn
        teKlein = set ()
        for locatie in uitkomstData.Locaties:
            bbox = self.MaakShapelyShape (locatie).bounds
            if bbox[2] - bbox[0] < nauwkeurigheid and bbox[3] - bbox[1] < nauwkeurigheid:
                teKlein.add (locatie['properties']['id'])
                locatie['properties']['p'] = 'nee; te klein'
            else:
                locatie['properties']['p'] = 'ja'

        # Maak de gebieden met een buffer van de nauwkeurigheid
        dikkeLijnen = []
        dikkeLijnenData = GeoManipulatie.GeoData () # Voor weergave op een kaart
        dikkeLijnenData.Dimensie = 2
        for lijn in lijnen:
            locatie_id = lijn.Locatie['properties']['id']
            if not locatie_id in teKlein:
                lijn_shape = self.MaakShapelyShape (lijn.Geometrie)
                dikkeLijn = (locatie_id, lijn_shape, lijn_shape.buffer (nauwkeurigheid))
                dikkeLijnen.append (dikkeLijn)
                dikkeLijnenData.Locaties.append ({ 
                    'type': 'Feature', 
                    'geometry': mapping (dikkeLijn[2]), 
                    '_shape' : dikkeLijn[2]
                })

        # Bepaal de onderlinge overlap en afstand
        minimaleAfstand = None
        for i in range (0, len (dikkeLijnen)):
            locatie_id_i, lijn_i, dikkeLijn_i = dikkeLijnen[i]
            for j in range (i+1, len (dikkeLijnen)):
                locatie_id_j, lijn_j, dikkeLijn_j = dikkeLijnen[j]
                if locatie_id_i != locatie_id_j:
                    afstand = lijn_i.distance (lijn_j)
                    if afstand < nauwkeurigheid:
                        if minimaleAfstand is None or afstand < minimaleAfstand:
                            minimaleAfstand = afstand

                        # Bereken de intersectie; dit is alleen nodig voor de weergave in het kaartje
                        # Alleen nodig zijn als de afstand kleiner is dan de nauwkeurigheid,
                        # anders weten we al dat er niets uit komt
                        intersectie = dikkeLijn_j.intersection (dikkeLijn_i)
                        if not intersectie is None and not intersectie.is_empty:
                            uitkomstLocaties[locatie_id_i]['properties']['p'] = 'nee; te dicht bij buur-lijn'
                            uitkomstLocaties[locatie_id_j]['properties']['p'] = 'nee; te dicht bij buur-lijn'
                            problemen.Locaties.append ({ 
                                'type': 'Feature', 
                                'geometry': mapping (intersectie), 
                                '_shape' : intersectie
                            })


        # Toon de vlakken in een kaart
        kaart = GeoManipulatie.Kaart (self)
        kaart.ZoomTotNauwkeurigheid (True)
        dataNaam = self.VoegGeoDataToe (dikkeLijnenData)
        symNaam = self.VoegUniformeSymbolisatieToe (2, "#DAE8FC", "#6C8EBF", '0.5')
        kaart.VoegLaagToe ("Verdikte lijnen", dataNaam, symNaam, True, True)

        if len (problemen.Locaties) > 0:
            dataNaam = self.VoegGeoDataToe (problemen)
            symNaam = self.VoegUniformeSymbolisatieToe (2, "#D80073", "#A50040")
            kaart.VoegLaagToe ("Gebieden waar afstanden kleiner zijn dan de teken-nauwkeurigheid", dataNaam, symNaam, True, True)

        dataNaam = self.VoegGeoDataToe (uitkomstData)
        symNaam = self.VoegUniformeSymbolisatieToe (1, "#0000ff", "#0000ff")
        kaart.VoegLaagToe ("Lijnen uit het GIO", dataNaam, symNaam, True, True)

        if len (problemen.Locaties) > 0:
            uitkomstData.Locaties = [l for l in uitkomstData.Locaties if l['properties']['p'] != 'ja']
            uitkomstData.Attributen = {}
            dataNaam = self.VoegGeoDataToe (uitkomstData)
            symNaam = self.VoegUniformeSymbolisatieToe (1, "#F8CECC", "#B85450", '0.5')
            kaart.VoegLaagToe ("Lijnen die niet passen bij de teken-nauwkeurigheid", dataNaam, symNaam, True, True)

        kaart.Toon ()

        return not minimaleAfstand is None, None if minimaleAfstand is None else round(10 * minimaleAfstand, 2)

    #------------------------------------------------------------------
    # Vlakken
    #------------------------------------------------------------------
    def _ValideerGIOVlakken (self, vlakken: List[GeoManipulatie.EnkeleGeometrie]) -> bool:
        """Implementatie van ValideerGIO voor vlak-geometrieën"""
        bufferafstand = - 0.5 * self.NauwkeurigheidInMeter ();
        self.Generator.VoegHtmlToe ('''<p>Voor een GIO met vlakken:
<ol>
    <li>Verklein de vlakken met de halve teken-nauwkeurigheid: buffer (''' + '{:2f}'.format (bufferafstand) + ''')</li>
    <li>Vlakken die te klein zijn verdwijnen daardoor. Als een locatie uit alleen van dat soort vlakken bestaat, dan past de locatie niet in de GIO voor de opgegeven teken-nauwkeurigheid.</li>
    <li>Van de verkleinde vlakken wordt paarsgewijs de overlap (intersection) bepaald. Als er overlap is, dan overlappen de originele vlakken teveel.
</ol>
Klik in een gebied in de kaart om de uitkomst van de procedure te zien voor een locatie.</p>''')

        # Kopie van de GIO, met uitkomst van de analyse
        uitkomstData = GeoManipulatie.GeoData () # Voor weergave op een kaart
        uitkomstData.Dimensie = self._Geometrie.Dimensie
        uitkomstData.Attributen = self._Geometrie.Attributen.copy ()
        uitkomstData.Attributen['p'] = GeoManipulatie.Attribuut ('p', 'In orde')
        uitkomstLocaties = {}
        for locatie in self._Geometrie.Locaties:
            uitkomstLocatie = { 
                'type': 'Feature', 
                'properties' : locatie['properties'].copy (), 
                'geometry': locatie['geometry'], 
                '_shape' : self.MaakShapelyShape (locatie),
                '_1ok': False
            }
            uitkomstData.Locaties.append (uitkomstLocatie)
            uitkomstLocaties[locatie['properties']['id']] = uitkomstLocatie

        # Verzamel alle intersecties/te kleine gebieden in:
        problemen = GeoManipulatie.GeoData ()
        problemen.Dimensie = 2

        # Maak de gebieden met een negatieve buffer van de helft van de nauwkeurigheid
        kleinereVlakken = []
        kleinereVlakkenData = GeoManipulatie.GeoData () # Voor weergave op een kaart
        kleinereVlakkenData.Dimensie = 2
        nauwkeurigheidTeGroot = False
        for vlak in vlakken:
            vlakkenDataLocatie = uitkomstLocaties[vlak.Locatie['properties']['id']]

            kleinerVlak = self.MaakShapelyShape (vlak.Geometrie).buffer (bufferafstand)
            if kleinerVlak is None or kleinerVlak.is_empty:
                if not nauwkeurigheidTeGroot:
                    self.Log.Waarschuwing ("De teken-nauwkeurigheid is zo'n groot getal dat het groter is dan sommige vlakken")
                    nauwkeurigheidTeGroot = True
                vlakkenDataLocatie['properties']['p'] = 'nee; kleiner dan de teken-nauwkeurigheid'
                problemen.Locaties.append ({ 
                    'type': 'Feature', 
                    'geometry': vlak.Locatie['geometry'], 
                    '_shape' :  self.MaakShapelyShape (vlak.Geometrie),
                    '_origineel': vlakkenDataLocatie
                })
            else:
                kleinereVlakken.append (kleinerVlak)
                kleinereVlakkenData.Locaties.append ({ 
                    'type': 'Feature', 
                    'geometry': mapping (kleinerVlak), 
                    '_shape' : kleinerVlak,
                    '_origineel': vlakkenDataLocatie
                })
                vlakkenDataLocatie['_1ok'] = True

        # Alle locaties met tenminste één groot vlak zijn in orde
        for locatie in uitkomstData.Locaties:
            if locatie['_1ok']:
                locatie['properties']['p'] = 'ja'
            locatie.pop ('_1ok')
        problemen.Locaties = [l for l in problemen.Locaties if l['_origineel']['properties']['p'] != 'ja']


        # Bepaal de onderlinge overlap
        for i in range (0, len (kleinereVlakken)):
            vlak_i = kleinereVlakken[i]
            for j in range (i+1, len (kleinereVlakken)):
                if kleinereVlakken[j].intersects (vlak_i):
                    kleinereVlakkenData.Locaties[i]['_origineel']['properties']['p'] = 'nee; overlap met buur-vlak(ken)'
                    kleinereVlakkenData.Locaties[j]['_origineel']['properties']['p'] = 'nee; overlap met buur-vlak(ken)'

                    # Bereken de intersectie; dit is alleen nodig voor de weergave in het kaartje
                    intersectie = kleinereVlakken[j].intersection (vlak_i)
                    problemen.Locaties.append ({ 
                        'type': 'Feature', 
                        'geometry': mapping (intersectie), 
                        '_shape' : intersectie
                    })


        # Toon de vlakken in een kaart
        kaart = GeoManipulatie.Kaart (self)
        kaart.ZoomTotNauwkeurigheid (True)
        dataNaam = self.VoegGeoDataToe (uitkomstData)
        symNaam = self.VoegUniformeSymbolisatieToe (2, "#ffffff", "#0000ff", '0')
        kaart.VoegLaagToe ("Vlakken uit het GIO", dataNaam, symNaam, True, True)
        if len (problemen.Locaties) > 0:
            uitkomstData.Locaties = [l for l in uitkomstData.Locaties if l['properties']['p'] != 'ja']
            uitkomstData.Attributen = {}
            dataNaam = self.VoegGeoDataToe (uitkomstData)
            symNaam = self.VoegUniformeSymbolisatieToe (2, "#F8CECC", "#B85450", '0.5')
            kaart.VoegLaagToe ("Vlakken die niet passen bij de teken-nauwkeurigheid", dataNaam, symNaam, True, True)

        dataNaam = self.VoegGeoDataToe (kleinereVlakkenData)
        symNaam = self.VoegUniformeSymbolisatieToe (2, "#DAE8FC", "#6C8EBF", '0.5')
        kaart.VoegLaagToe ("Verkleinde vlakken", dataNaam, symNaam, True, True)
        if len (problemen.Locaties) > 0:
            dataNaam = self.VoegGeoDataToe (problemen)
            symNaam = self.VoegUniformeSymbolisatieToe (2, "#D80073", "#A50040")
            kaart.VoegLaagToe ("Gebieden waar de vlakken niet passen bij de teken-nauwkeurigheid", dataNaam, symNaam, True, True)
        kaart.Toon ()

        return len (problemen.Locaties) > 0
