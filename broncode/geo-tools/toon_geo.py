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

    def _VoerUit (self):
        """Voer het request uit"""
        self.Log.Informatie ("Lees het GIO, gebiedsmarkering of effectgebied")
        gio = self.LeesGeoBestand ('geometrie', True)
        if gio is None:
            return False
        if gio.Soort == 'GIO-wijziging':
            self.Log.Fout ("Kan deze geo-informatie niet weergeven: " + gio.Soort)
            return False
        self.Log.Informatie (gio.Soort + ' ingelezen')

        symbolisatieVereist = False
        if gio.Soort == 'GIO' and not gio.AttribuutNaam is None:
            self.Log.Informatie ('GIO heeft per locatie een ' + gio.AttribuutNaam + ' - een symbolisatie is nodig om dat weer te geven')
            symbolisatieVereist = True

        self.Log.Informatie ("Lees de symbolisatie (indien aanwezig)")
        symbolisatie = self.Request.LeesBestand (self.Log, "symbolisatie", False)
        if symbolisatie is None:
            if symbolisatieVereist:
                self.Log.Waarschuwing ('Geen symbolisatie beschikbaar - gebruik de standaard symbolisatie voor geometrieën')
            else:
                self.Log.Informatie ('Geen symbolisatie beschikbaar - gebruik de standaard symbolisatie voor geometrieën')
        else:
            self.Log.Detail ('Symbolisatie ingelezen')

        self.Generator.VoegHtmlToe ('Bestand: ' + self.Request.Bestandsnaam ('geometrie'))

        self.Log.Informatie ('Maak de kaartweergave')
        self._DataNaam = self.VoegGeoDataToe (gio)
        symbolisatieNaam = self.VoegDefaultSymbolisatieToe (gio) if symbolisatie is None else self.VoegSymbolisatieToe (symbolisatie)
        self.ToonKaart ('kaart.VoegOnderlaagToe ("' + gio.Soort + '", "' + self._DataNaam + '", "' + symbolisatieNaam + '");')

        if gio.Soort == 'GIO' and not self.NauwkeurigheidInMeter () is None:
            self.Log.Informatie ('Valideer de GIO')
            self.Generator.VoegHtmlToe ('<p>Om te zien of het GIO geschikt is om te gebruiken voor een GIO-wijziging wordt de elders beschreven <a href="@@@GeoTools_Url@@@wiki/Toon-controleer-gio" target="_blank">procedure</a> gevolgd.</p>')
            lijst = self.MaakLijstVanGeometrieen (gio)[0]
            heeftProblemen, tekennauwkeurigheid = self.ValideerGIO (lijst, gio.Dimensie)
            if not heeftProblemen:
                self.Generator.VoegHtmlToe ('<p>Het GIO kan gebruikt worden voor de bepaling van een GIO-wijziging bij een teken-nauwkeurigheid van ' + self.Request.LeesString ("nauwkeurigheid") + ' decimeter</p>')
            else:
                self.Generator.VoegHtmlToe ('<p>Het GIO kan <b>niet</b> gebruikt worden voor de bepaling van een GIO-wijziging bij een teken-nauwkeurigheid van ' + self.Request.LeesString ("nauwkeurigheid") + " decimeter. ")
                if not tekennauwkeurigheid is None:
                    if tekennauwkeurigheid <= 0:
                        self.Generator.VoegHtmlToe ('Het GIO kan nooit gebruikt worden omdat er sprake is van samenvallende geometrieën')
                    else:
                        self.Generator.VoegHtmlToe ('Het GIO kan wel gebruikt worden met een teken-nauwkeurigheid van ' + str(tekennauwkeurigheid) + ' decimeter')
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
        self.Generator.VoegHtmlToe ('''Voor een GIO met punten als geometrie wordt gecontroleerd dat de afstand tussen de punten groter is dan de teken-nauwkeurigheid.''')
        drempel = self.NauwkeurigheidInMeter ()
        drempel *= drempel
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
            coord_i = punten[i].Geometrie['geometry']['coordinates']
            for j in range (i+1, len (punten)):
                coord_j = punten[j].Geometrie['geometry']['coordinates']
                afstand = (coord_i[0] - coord_j[0]) * (coord_i[0] - coord_j[0]) + (coord_i[1] - coord_j[1]) * (coord_i[1] - coord_j[1])
                if afstand < drempel:
                    __Afstand (i, afstand)
                    __Afstand (j, afstand)
                    if minimaleAfstand is None or afstand < minimaleAfstand:
                        minimaleAfstand  = afstand
        # Is er een probleem?
        if minimaleAfstand is None:
            self.Generator.VoegHtmlToe ('Dat is het geval.')
            self.Log.Informatie ('Alle punten liggen tenminste ' + self.Request.LeesString ("nauwkeurigheid") + ' decimeter van elkaar af')
            return (False, None)
        else:
            self.Log.Waarschuwing ('Er zijn ' + str(len (afstanden)) + ' punten die minder dan ' + self.Request.LeesString ("nauwkeurigheid") + ' decimeter van elkaar af liggen, met een minimum van ' + str(minimaleAfstand) + ' decimeter')
            problemen = GeoManipulatie.GeoData ()
            problemen.Attributen['d'] = GeoManipulatie.Attribuut ('d', 'Minimale afstand', 'decimeter')
            problemen.Attributen['n'] = GeoManipulatie.Attribuut ('n', 'Te nabije buren')
            problemen.AttribuutNaam = 'afstand'
            problemen.Dimensie = 1
            for i, afstand in afstanden.items ():
                punt = punten[i].Geometrie
                punt['properties'] = { 'd': round (math.sqrt (100*afstand), 2), 'n': aantal[i] }
                problemen.Locaties.append (punt);

            self.Generator.VoegHtmlToe ('Dat is niet het geval. De plaatsen waar punten te dicht bij elkaar staan:')
            gioSym = self.VoegUniformeSymbolisatieToe (0, "#DAE8FC", "#6C8EBF", '0.5')
            geomNaam = self.VoegGeoDataToe (problemen)
            geomSym = self.VoegWijzigMarkeringToe ()
            self.ToonKaart ('kaart.VoegOnderlaagToe ("Geo-informatieobject", "' + self._DataNaam + '", "' + gioSym + '", true, true);kaart.VoegOnderlaagToe ("Problematische geometrie", "' + geomNaam + '", "' + geomSym + '", true, true);')

            return (True, round(math.sqrt (100 * minimaleAfstand), 2))

    #------------------------------------------------------------------
    # Lijnen
    #------------------------------------------------------------------
    def _ValideerGIOLijnen (self, lijnen: List[GeoManipulatie.EnkeleGeometrie]) -> Tuple[bool,float]:
        """Implementatie van ValideerGIO voor lijn-geometrieën"""
        self.Generator.VoegHtmlToe ('''<p>Voor een GIO met lijnen wordt nagegaan of lijnen niet te dicht bij elkaar komen.
Dat kan op verschillende manieren. Bijvoorbeeld door de onderlinge afstanden van de lijnen te vergeleken met de teken-nauwkeurigheid - dat 
levert ook een inschatting op wat de teken-nauwkeurigheid maximaal kan zijn. Of door de lijnen te verdikken tot de teken-nauwkeurigheid
en dan de overlap te bepalen - dat levert een beeld op waar de problemen zitten. Beide methodes worden hier toegepast.</p>''')
        nauwkeurigheid = self.NauwkeurigheidInMeter ();
        problemen = GeoManipulatie.GeoData ()
        problemen.Dimensie = 2
        problemen.Attributen['p'] = GeoManipulatie.Attribuut ('p', 'Geschiktheid voor GIO-wijziging')

        # Maak de gebieden met een buffer van de nauwkeurigheid
        dikkeLijnen = []
        dikkeLijnenData = GeoManipulatie.GeoData () # Voor weergave op een kaart
        dikkeLijnenData.Dimensie = 2
        dikkeLijnenData.Attributen['p'] = GeoManipulatie.Attribuut ('p', 'Geschiktheid voor GIO-wijziging')
        for lijn in lijnen:
            dikkeLijn = self.MaakShapelyShape (lijn.Geometrie).buffer (0.5 * nauwkeurigheid)
            dikkeLijnen.append (dikkeLijn)
            dikkeLijnenData.Locaties.append ({ 
                'type': 'Feature', 
                'properties' : {
                    'p': 'ja'
                }, 
                'geometry': mapping (dikkeLijn), 
                '_shape' : dikkeLijn
            })

        # Bepaal de onderlinge overlap en afstand
        minimaleAfstand = None
        for i in range (0, len (dikkeLijnen)):
            lijn_i = self.MaakShapelyShape (lijnen[i].Geometrie)
            dikkeLijn_i = dikkeLijnen[i]
            for j in range (i+1, len (dikkeLijnen)):
                afstand = lijn_i.distance (self.MaakShapelyShape (lijnen[j].Geometrie))
                if afstand < nauwkeurigheid:
                    if minimaleAfstand is None or afstand < minimaleAfstand:
                        minimaleAfstand = afstand

                    # Bereken de intersectie; dit is alleen nodig voor de weergave in het kaartje
                    # Alleen nodig zijn als de afstand kleiner is dan de nauwkeurigheid,
                    # anders weten we al dat er niets uit komt
                    intersectie = dikkeLijnen[j].intersection (dikkeLijn_i)
                    if not intersectie is None and not intersectie.is_empty:
                        dikkeLijnenData.Locaties[i]['properties']['p'] = 'nee'
                        dikkeLijnenData.Locaties[j]['properties']['p'] = 'nee'
                        problemen.Locaties.append ({ 
                            'type': 'Feature', 
                            'geometry': mapping (intersectie), 
                            '_shape' : intersectie
                        })


        # Toon de vlakken in een kaart
        kvNaam = self.VoegGeoDataToe (dikkeLijnenData)
        kvSym = self.VoegUniformeSymbolisatieToe (2, "#DAE8FC", "#6C8EBF", '0.5')
        kaartScript = 'kaart.VoegOnderlaagToe ("Verdikte lijnen", "' + kvNaam + '", "' + kvSym + '", true, true);'
        if len (problemen.Locaties) > 0:
            dikkeLijnenData.Locaties = [l for l in dikkeLijnenData.Locaties if l['properties']['p'] != 'ja']
            kvNaam = self.VoegGeoDataToe (dikkeLijnenData)
            kvSym = self.VoegUniformeSymbolisatieToe (2, "#F8CECC", "#B85450", '0.5')
            kaartScript += 'kaart.VoegOnderlaagToe ("(Verdikte) lijnen ongeschikt voor GIO-wijziging", "' + kvNaam + '", "' + kvSym + '", true, true);'

            kvNaam = self.VoegGeoDataToe (problemen)
            kvSym = self.VoegUniformeSymbolisatieToe (2, "#D80073", "#A50040")
            kaartScript += 'kaart.VoegOnderlaagToe ("Probleemgebieden", "' + kvNaam + '", "' + kvSym + '", true, true);'
        gioSym = self.VoegUniformeSymbolisatieToe (1, "#0000ff", "#0000ff")
        kaartScript += 'kaart.VoegOnderlaagToe ("Lijnen uit het GIO", "' + self._DataNaam + '", "' + gioSym + '", true, true);'
        self.ToonKaart (kaartScript)

        return not minimaleAfstand is None, None if minimaleAfstand is None else round(10 * minimaleAfstand, 2)

    #------------------------------------------------------------------
    # Vlakken
    #------------------------------------------------------------------
    def _ValideerGIOVlakken (self, vlakken: List[GeoManipulatie.EnkeleGeometrie]) -> bool:
        """Implementatie van ValideerGIO voor vlak-geometrieën"""
        self.Generator.VoegHtmlToe ('''<p>Voor een GIO met vlakken wordt nagegaan of vlakken niet teveel overlappen.
Daartoe worden de vlakken verkleind met de halve teken-nauwkeurigheid en wordt bepaald of de verkleinde vlakken elkaar overlappen.</p>''')
        nauwkeurigheid = self.NauwkeurigheidInMeter ();
        problemen = GeoManipulatie.GeoData ()
        problemen.Dimensie = 2
        problemen.Attributen['p'] = GeoManipulatie.Attribuut ('p', 'Geschiktheid voor GIO-wijziging')

        # Maak de gebieden met een negatieve buffer van de helft van de nauwkeurigheid
        kleinereVlakken = []
        kleinereVlakkenData = GeoManipulatie.GeoData () # Voor weergave op een kaart
        kleinereVlakkenData.Dimensie = 2
        kleinereVlakkenData.Attributen['p'] = GeoManipulatie.Attribuut ('p', 'Geschiktheid voor GIO-wijziging')
        nauwkeurigheidTeGroot = False
        for vlak in vlakken:
            kleinerVlak = self.MaakShapelyShape (vlak.Geometrie).buffer (-0.5*nauwkeurigheid)
            if kleinerVlak is None or kleinerVlak.is_empty:
                if not nauwkeurigheidTeGroot:
                    self.Log.Waarschuwing ("De teken-nauwkeurigheid is zo'n groot getal dat het groter is dan sommige vlakken")
                    nauwkeurigheidTeGroot = True
                kleinereVlakkenData.Locaties.append ({ 
                    'type': 'Feature', 
                    'properties' : {
                        'p': 'nee; kleiner dan de teken-nauwkeurigheid'
                    }, 
                    'geometry': mapping (kleinerVlak), 
                    '_shape' : kleinerVlak
                })
                problemen.Locaties.append ({ 
                    'type': 'Feature', 
                    'properties' : {
                        'p': 'nee; kleiner dan de teken-nauwkeurigheid'
                    }, 
                    'geometry': vlak.Locatie['geometry'], 
                    '_shape' :  self.MaakShapelyShape (vlak.Geometrie)
                })
            else:
                kleinereVlakken.append (kleinerVlak)
                kleinereVlakkenData.Locaties.append ({ 
                    'type': 'Feature', 
                    'properties' : {
                        'p': 'ja'
                    }, 
                    'geometry': mapping (kleinerVlak), 
                    '_shape' : kleinerVlak})

        # Bepaal de onderlinge overlap
        for i in range (0, len (kleinereVlakken)):
            vlak_i = kleinereVlakken[i]
            for j in range (i+1, len (kleinereVlakken)):
                if kleinereVlakken[j].intersects (vlak_i):
                    kleinereVlakkenData.Locaties[i]['properties']['p'] = 'nee; overlap met buur-vlak(ken)'
                    kleinereVlakkenData.Locaties[j]['properties']['p'] = 'nee; overlap met buur-vlak(ken)'

                    # Bereken de intersectie; dit is alleen nodig voor de weergave in het kaartje
                    intersectie = kleinereVlakken[j].intersection (vlak_i)
                    problemen.Locaties.append ({ 
                        'type': 'Feature', 
                        'geometry': mapping (intersectie), 
                        '_shape' : intersectie
                    })


        # Toon de vlakken in een kaart
        gioSym = self.VoegUniformeSymbolisatieToe (2, "#ffffff", "#0000ff", '0')
        kvNaam = self.VoegGeoDataToe (kleinereVlakkenData)
        kvSym = self.VoegUniformeSymbolisatieToe (2, "#DAE8FC", "#6C8EBF", '0.5')
        kaartScript = 'kaart.VoegOnderlaagToe ("Vlakken uit het GIO", "' + self._DataNaam + '", "' + gioSym + '", true, true);kaart.VoegOnderlaagToe ("Verkleinde vlakken", "' + kvNaam + '", "' + kvSym + '", true, true);'
        if len (problemen.Locaties) > 0:
            kleinereVlakkenData.Locaties = [l for l in kleinereVlakkenData.Locaties if l['properties']['p'] != 'ja']
            kvNaam = self.VoegGeoDataToe (kleinereVlakkenData)
            kvSym = self.VoegUniformeSymbolisatieToe (2, "#F8CECC", "#B85450", '0.5')
            kaartScript += 'kaart.VoegOnderlaagToe ("Vlakken ongeschikt voor GIO-wijziging", "' + kvNaam + '", "' + kvSym + '", true, true);'

            kvNaam = self.VoegGeoDataToe (problemen)
            kvSym = self.VoegUniformeSymbolisatieToe (2, "#D80073", "#A50040")
            kaartScript += 'kaart.VoegOnderlaagToe ("Probleemgebieden", "' + kvNaam + '", "' + kvSym + '", true, true);'
        self.ToonKaart (kaartScript)

        return len (problemen.Locaties) > 0
