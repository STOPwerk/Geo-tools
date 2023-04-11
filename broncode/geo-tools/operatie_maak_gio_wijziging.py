#======================================================================
#
# /maak_gio_wijziging
#
#======================================================================
#
# Script om een GIO-wijziging samen te stellen uit een was- en 
# een wordt-versie van een GIO.
#
#======================================================================

from typing import List, Dict, Set, Tuple

from shapely.geometry import mapping
import os;
from uuid import uuid4

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from data_geodata import GeoData, GIODeel, Attribuut
from operatie_toon_gio_wijziging import ToonGIOWijziging
from weergave_kaart import KaartGenerator
from weergave_webpagina import WebpaginaGenerator

class MaakGIOWijziging (ToonGIOWijziging):
#======================================================================
#
# Webpagina's
#
#======================================================================
#region Webpagina's
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("Bepaling van een GIO-wijziging")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters, log: Meldingen = None):
        return MaakGIOWijziging (request, log).VoerUit ()
#endregion

#======================================================================
#
# Implementatie
#
#======================================================================
#region Implementatie
    def __init__(self, request : Parameters, log: Meldingen, defaultTitel = None, titelBijFout = None):
        super ().__init__ (request, log, "GIO-wijziging" if defaultTitel is None else defaultTitel, "GIO-wijziging - geen resultaat" if titelBijFout is None else titelBijFout)
        # Locaties uit was- en wordt-versie
        # key = id, value = dimensie, locatie
        self._WasLocaties : Dict[str,Tuple[int,object]] = None
        self._WordtLocaties : Dict[str,Tuple[int,object]] = None

    def _VoerUit (self, titelOperatie = "Bepaling GIO wijziging"):
        """Voer het request uit"""
        if not self._LeesBestandenEnSpecificatie  ():
            return False

        einde = self.Generator.StartSectie ("<h3>" + titelOperatie + "</h3>", True)
        if self.Request.LeesString ("beschrijving"):
            self.Generator.VoegHtmlToe ('<p>' + self.Request.LeesString ("beschrijving") + '</p>') 

        eindeToelichting = self.Generator.StartToelichting ("Bepaling GIO-Wijziging", False)
        self._BepaalWijzigingen ()
        self.Generator.VoegHtmlToe (eindeToelichting)

        self._ToonGIOWijzigingOnderdelen ();
        
        eindeToelichting = self.Generator.StartToelichting ("GML voor GIO-Wijziging", False)
        self._ToonGIOWinzigingGML ()
        self.Generator.VoegHtmlToe (eindeToelichting)

        self.Generator.VoegHtmlToe (einde)

        if self.Request.IsOptie ("toon-gio-wijziging", True):
            einde = self.Generator.StartSectie ("GIO-Wijziging", True)
            self._ToonGIOWijziging ()
            self.Generator.VoegHtmlToe (einde)

        return True


    def _LeesBestandenEnSpecificatie (self):
        """Lees de specificatie en GIO's en valideeer de invoer"""
        succes = True

        valideerGIOs = True
        if self._Was is None:
            self.Log.Informatie ("Lees de was-versie van de GIO")
            self._Was = GeoData.LeesGeoBestand (self.Request, 'was', True)
            if self._Was is None:
                return False
            if self._Was.Soort != GeoData.SOORT_GIOVersie:
                self.Log.Fout ("Het bestand bevat geen GIO maar: " + self._Was.Soort)
                succes = False
                valideerGIOs = False

        if self._Wordt is None:
            self.Log.Informatie ("Lees de wordt-versie van de GIO")
            self._Wordt = GeoData.LeesGeoBestand (self.Request, 'wordt', True)
            if self._Wordt is None:
                return False
            if self._Wordt.Soort != GeoData.SOORT_GIOVersie:
                self.Log.Fout ("Het bestand bevat geen GIO maar: " + self._Wordt.Soort)
                succes = False
                valideerGIOs = False

        if valideerGIOs:
            if self._Was.AttribuutNaam != self._Wordt.AttribuutNaam:
                self.Log.Fout ("De was- en wordt-versie moeten allebei uitsluitend geometrie, GIO-delen of normwaarden hebben")
                succes = False
            elif not self._Was.GIODelen is None:
                for groepId, gioDeel in self._Was.GIODelen.items ():
                    nieuw = self._Wordt.GIODelen.get (groepId)
                    if not nieuw is None and nieuw.Label != gioDeel.Label:
                        self.Log.Fout ("Label van GIO-deel verschilt: groepID '" + groepId + "' had label '" + gioDeel.Label + "' en dat wordt '" + nieuw.Label + "'")
                        succes = False

            nauwkeurigheid = self.Request.JuridischeNauwkeurigheidInDecimeter (False)
            if self._Wordt.JuridischeNauwkeurigheid is None and self._Was.JuridischeNauwkeurigheid is None:
                self.Log.Fout ("De juridische nauwkeurigheid van de was- en wordt-versie is onbekend en moet opgegeven worden")
                succes = False
            elif nauwkeurigheid is None and self._Wordt.JuridischeNauwkeurigheid != self._Was.JuridischeNauwkeurigheid:
                self.Log.Fout ("De juridische nauwkeurigheid van de was- en wordt-versie is verschillend en moet daarom opgegeven worden")
                succes = False
            elif not nauwkeurigheid is None:
                if self._Wordt.JuridischeNauwkeurigheid != nauwkeurigheid:
                    self.Log.Informatie ("Als juridische nauwkeurigheid van de wordt-versie wordt " + str(nauwkeurigheid) + " decimeter gebruikt in plaats van " + str (self._Wordt.JuridischeNauwkeurigheid))
                    self._Wordt.JuridischeNauwkeurigheid = nauwkeurigheid
                if self._Was.JuridischeNauwkeurigheid != nauwkeurigheid:
                    self.Log.Informatie ("Als juridische nauwkeurigheid van de was-versie wordt " + str(nauwkeurigheid) + " decimeter gebruikt in plaats van " + str (self._Was.JuridischeNauwkeurigheid))
                    self._Was.JuridischeNauwkeurigheid = nauwkeurigheid

            self._InitSymbolisatieNamen ([self._Was, self._Wordt])

        return succes
#endregion

#======================================================================
#
# Bepaling van wijzigingen tussen twee GIO's
#
#======================================================================
#region Bepaling van wijzigingen tussen twee GIO's
    def _BepaalWijzigingen (self) :
        """Bepaal de wijzigingen tussen twee versies van een GIO"""

#region Initialisatie GIO-wijziging als GeoData
        self.Log.Detail ("Maak GIO-wijziging aan")
        self._Wijziging = GeoData ()
        self._Wijziging.WorkId = self._Wordt.WorkId
        self._Wijziging.ExpressionId = self._Wordt.ExpressionId
        self._Wijziging.Attributen = self._Was.Attributen | self._Wordt.Attributen
        self._Wijziging.AttribuutNaam = self._Was.AttribuutNaam
        self._Wijziging.LabelNaam = self._Wordt.LabelNaam
        self._Wijziging.JuridischeNauwkeurigheid = self._Wordt.JuridischeNauwkeurigheid
        self._Wijziging.Was = GeoData ()
        self._Wijziging.Was.WorkId = self._Wordt.WorkId
        self._Wijziging.Was.ExpressionId = self._Was.ExpressionId
        self._Wijziging.Was.Attributen = self._Was.Attributen
        self._Wijziging.Was.AttribuutNaam = self._Was.AttribuutNaam
        self._Wijziging.Wordt = GeoData ()
        self._Wijziging.Wordt.WorkId = self._Wordt.WorkId
        self._Wijziging.Wordt.ExpressionId = self._Wordt.ExpressionId
        self._Wijziging.Wordt.Attributen = self._Wordt.Attributen
        self._Wijziging.Wordt.AttribuutNaam = self._Wordt.AttribuutNaam
        self._Wijziging.WordtRevisies = GeoData ()
        self._Wijziging.WordtRevisies.WorkId = self._Wordt.WorkId
        self._Wijziging.WordtRevisies.ExpressionId = self._Wordt.ExpressionId
        self._Wijziging.WordtRevisies.Attributen = self._Wordt.Attributen
        self._Wijziging.WordtRevisies.AttribuutNaam = self._Wordt.AttribuutNaam
        self._Wijziging.WijzigMarkering = GeoData ()
#endregion

#region Toevoegen locaties aan Was, Wordt en WordtRevisies
        self.Log.Detail ("Voeg de locaties aan de was, wordt en wordt-revisies toe; locaties met dezelfde basisgeo-id moeten gelijke geometrie hebben.")
        def _VoegLocatieToe (locaties, dimensie, locatie):
            if not dimensie in locaties:
                locaties[dimensie] = [locatie]
            else:
                locaties[dimensie].append (locatie)

        self.Generator.VoegHtmlToe ('''<p>Bij de bepaling van de GIO-wijziging wordt ervan uitgegaan dat de beide GIO-versies aan de kwaliteitseisen voldoen. 
        Deze kunnen gecontroleerd worden als onderdeel van het <a href="@@@GeoTools_Url@@@/toon_geo" target="_blank">tonen van een GIO-versie</a>.
        De bepaling bestaat uit de volgende stappen:</p>
        <p><ol><li>Bepaal de te verwijderen en toe te voegen locaties waarvan de geometrie is gewijzigd.
        Dit zijn alle locaties met een basisgeometrie-id die alleen in de was- of wordt-versie terugkomt.''')
        self._WasLocaties = { locatie["properties"]["id"] : (dimensie, locatie) for dimensie, locaties in self._Was.Locaties.items () for locatie in locaties }
        self._WordtLocaties = { locatie["properties"]["id"] : (dimensie, locatie) for dimensie, locaties in self._Wordt.Locaties.items () for locatie in locaties }
        numWas = 0
        numWordt = 0
        for id, (dimensie, locatie) in self._WasLocaties.items ():
            if not id in self._WordtLocaties:
                _VoegLocatieToe (self._Wijziging.Was.Locaties, dimensie, locatie)
                numWas += 1
        for id, (dimensie, locatie) in self._WordtLocaties.items ():
            if not id in self._WasLocaties:
                _VoegLocatieToe (self._Wijziging.Wordt.Locaties, dimensie, locatie)
                numWordt += 1
        self.Generator.VoegHtmlToe (' Het gaat om ' + str(numWas) + ' locatie' + ('' if numWas == 1 else 's') + ' uit de was-versie en ' + str(numWordt) + ' locatie' + ('' if numWordt == 1 else 's') + ' uit de wordt-versie</li>')

        numWaarde = 0
        numLabel = 0
        for id, (dimensie, locatie) in self._WordtLocaties.items ():
            wasLocatie = self._WasLocaties.get (id)
            if not wasLocatie is None:
                wasLocatie = wasLocatie[1]
                if not self._Wijziging.AttribuutNaam is None:
                    if locatie["properties"][self._Wijziging.AttribuutNaam] != wasLocatie["properties"][self._Wijziging.AttribuutNaam]:
                        _VoegLocatieToe (self._Wijziging.Was.Locaties, dimensie, wasLocatie)
                        _VoegLocatieToe (self._Wijziging.Wordt.Locaties, dimensie, locatie)
                        numWaarde += 1
                        continue
                if locatie["properties"].get (self._Wijziging.LabelNaam) != wasLocatie["properties"].get (self._Wijziging.LabelNaam):
                    numLabel += 1
                    _VoegLocatieToe (self._Wijziging.WordtRevisies.Locaties, dimensie, locatie)
                    continue
        if not self._Wijziging.AttribuutNaam is None:
            self.Generator.VoegHtmlToe ('''<li>Van de locaties met een manifest ongewijzigde geometrie (basisgeometrie-id komt in zowel de was- als wordt-versie voor) 
            die in beide versies een verschillende waarde voor ''' + self._Wijziging.AttribuutNaam + ''' hebben moet de oude verwijderd en de nieuwe toegevoegd worden.
            Het betreft ''' + str(numWaarde) + ' locatie' + ('' if numWaarde == 1 else 's') + '.</li>')
        self.Generator.VoegHtmlToe ('''<li>De locaties met een manifest ongewijzigde geometrie die in beide versies een verschillende waarde voor het label hebben 
        moet als revisie toegevoegd worden. Het betreft ''' + str(numLabel) + ' locatie' + ('' if numLabel == 1 else 's') + '.</li>')
#endregion

#region Overnemen GIO-delen en norm-eigenschappen
        if not self._Wijziging.AttribuutNaam is None:

            if self._Wijziging.AttribuutNaam == 'groepID':
                self.Log.Detail ("Neem gebruikte GIO-delen over")
                self.Generator.VoegHtmlToe ('''<li>Maak een lijst van alle GIO-delen die in de opgenomen locaties voorkomen en geef aan welke oud of nieuw zijn.''')
                wasGroepID = set (locatie["properties"]["groepID"] for locaties in self._Wijziging.Was.Locaties.values () for locatie in locaties)
                wordtGroepID = set (locatie["properties"]["groepID"] for locaties in self._Wijziging.Wordt.Locaties.values () for locatie in locaties)
                wordtGroepID = wordtGroepID.union (set (locatie["properties"]["groepID"] for locaties in self._Wijziging.WordtRevisies.Locaties.values () for locatie in locaties))
                self._Wijziging.GIODelen = {}
                numWas = 0
                numWordt = 0
                for groepID in wasGroepID:
                    gioDeel = self._Was.GIODelen[groepID]
                    if not groepID in self._Wordt.GIODelen:
                        gioDeel = GIODeel (groepID, gioDeel.Label)
                        gioDeel.WijzigActie = GIODeel._WIJZIGACTIE_VERWIJDER
                        numWas += 1
                    self._Wijziging.GIODelen[groepID] = gioDeel
                for groepID in wordtGroepID:
                    if not gioDeel in wasGroepID:
                        gioDeel = self._Wordt.GIODelen[groepID]
                        if not groepID in  self._Was.GIODelen:
                            gioDeel = GIODeel (groepID, gioDeel.Label)
                            gioDeel.WijzigActie = GIODeel._WIJZIGACTIE_VOEGTOE
                            numWordt += 1
                        self._Wijziging.GIODelen[groepID] = gioDeel
                self.Generator.VoegHtmlToe (' Er ' + ('wordt' if numWas == 1 and numWordt == 1 else 'worden') + ' ' + str(numWas) + ' GIO-de' + ('el' if numWas == 1 else 'len') + ' verwijderd en ' + str(numWordt) + ' toegevoegd.</li>')

            else:
                self.Log.Detail ("Neem norm-eigenschappen over")
                self.Generator.VoegHtmlToe ('''<li>Neem de eigenschappen van de norm en eenheid over uit de wordt-versie.</li>''')
                self._Wijziging.EenheidID = self._Wordt.EenheidID
                self._Wijziging.EenheidLabel = self._Wordt.EenheidLabel
                self._Wijziging.NormID = self._Wordt.NormID
                self._Wijziging.NormLabel = self._Wordt.NormLabel
#endregion

#region Bepaling GIO-wijzigingen
        self.Generator.VoegHtmlToe ('''<li>Bepaal de wijzigmarkeringen. Hierbij wordt bedoeld met:<ul>
        <li>De "buitenrand": de buitenste rand van de geometrie van een locatie getekend met een "dikke pen":<br/>
        <code>buitenrand = locatie.geometrie.<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.buffer.html#shapely.buffer" target="_blank">buffer</a> (juridische nauwkeurigheid / 2)</code></li>
        <li>Het "binnengebied": de binnenste rand van de geometrie getekend met een "dikke pen":<br/>
        <code>binnengebied = locatie.geometrie</code> voor een punt of lijn,<br/>
        <code>binnengebied = locatie.geometrie.<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.buffer.html#shapely.buffer" target="_blank">buffer</a> (- juridische nauwkeurigheid / 2)</code> voor vlakken.</li></ul>
        De wijzigmarkeringen worden opgesplitst in enkelvoudige geometrieën (punt, lijn, vlak) om bij weergave clustering te vereenvoudigen. Ze worden in meerdere stappen bepaald:
        <ol>''')

        # De verschillende stappen gebruiken steeds hetzelfde patroon:
        # Voeg de buitenranden van alle te vergelijken locaties samen
        def _VoegBuitenrandToe (gebied, locatie):
            buitenrand = GeoData.MaakShapelyShape (locatie).buffer (0.05 * self._Wijziging.JuridischeNauwkeurigheid)
            if gebied is None:
                return buitenrand
            else:
                return gebied.union (buitenrand)

        # Voeg de geometrieën per type samen voor alle locaties waarvoor de wijziging bepaald moet worden
        def _VoegGeometrieToe (gebieden : Dict[int,object], dimensie : int, locatie):
            if dimensie in gebieden:
                gebieden[dimensie] = gebieden[dimensie].union (GeoData.MaakShapelyShape (locatie))
            else:
                gebieden[dimensie] = GeoData.MaakShapelyShape (locatie)

        # De wijzigmarkeringen zijn het binnengebied van de samengevoegde geometrieën per type geometrie minus de buitenranden
        def _BepaalWijzigmarkeringen (gebieden : Dict[int,object], buitenranden) -> int:
            binnengebieden = None
            for dimensie, gebied in gebieden.items ():
                if dimensie == 2:
                    binnengebied = gebied.buffer (- 0.05 * self._Wijziging.JuridischeNauwkeurigheid)
                    if binnengebied.is_empty:
                        continue
                else:
                    binnengebied = gebied
                if binnengebieden is None:
                    binnengebieden = binnengebied
                else:
                    binnengebieden = binnengebieden.union (binnengebied)
            if not binnengebieden is None:
                markeringen = binnengebieden if buitenranden is None else binnengebieden.difference (buitenranden)
                if not markeringen.is_empty:
                    # Ga over naar de enkele geometrieën
                    if hasattr (markeringen, 'geoms'):
                        markeringen = list (markeringen.geoms)
                    else:
                        markeringen = [markeringen]
                    for markering in markeringen:
                        # Omzetting naar een Punt, Lijn, Vlak conform STOP
                        if markering.type == 'Point':
                            dimensie = 0
                        elif markering.type == 'Polygon':
                            dimensie = 2
                        else:
                            dimensie = 1
                        if not dimensie in self._Wijziging.WijzigMarkering.Locaties:
                            self._Wijziging.WijzigMarkering.Locaties[dimensie] = []
                        self._Wijziging.WijzigMarkering.Locaties[dimensie].append ({
                            'type': 'Feature',
                            'properties': {
                                'id': str(uuid4()) 
                            },
                            'geometry': mapping (markering)
                        })

                    return len (markeringen)
            return 0

        self.Generator.VoegHtmlToe ('''<li>De delen van de locaties uit de was-versie waar geen enkele juridische regel meer geldt.
        Oftewel: het deel van de binnengebieden van locaties uit de was-versie dat niet binnen de buitenranden ligt van de locaties uit de wordt-versie:<br/>
        <code>was_geometrie = <a href="https://shapely.readthedocs.io/en/stable/reference/shapely.union.html#shapely.union" target="_blank">union</a> (elke geometrie uit was-versie)</code><br/>
        <code>buitenranden = <a href="https://shapely.readthedocs.io/en/stable/reference/shapely.union.html#shapely.union" target="_blank">union</a> (elke buitenrand uit wordt-versie)</code><br/>
        <code>wijzigmarkering = (binnengebied van was_geometrie).<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.difference.html#shapely.difference" target="_blank">difference</a> (buitenranden)</code><br/>
        ''')
        self.Log.Detail ("Bepaal de wijzigmarkering voor de verwijderde gebieden")

        buitenranden = None
        for (_, locatie) in self._WordtLocaties.values ():
            buitenranden = _VoegBuitenrandToe (buitenranden, locatie)

        binnengebieden : Dict[int,object] = {}
        for (dimensie, locatie) in self._WasLocaties.values ():
            _VoegGeometrieToe (binnengebieden, dimensie, locatie)
        numMarkeringen = _BepaalWijzigmarkeringen (binnengebieden, buitenranden)
        self.Generator.VoegHtmlToe ('Dit levert ' + str(numMarkeringen) + ' markering' + ('' if numMarkeringen == 1 else 'en') + ' op.</li>')

        if self._Wijziging.AttribuutNaam is None:
            self.Generator.VoegHtmlToe ('''<li>De delen van de locaties uit de wordt-versie waar de juridische regel voor het eerst gaan gelden.
            Oftewel: het deel van de binnengebieden van locaties uit de wordt-versie dat niet binnen de buitenranden ligt van de locaties uit de was-versie:<br/>
            <code>wordt_geometrie = <a href="https://shapely.readthedocs.io/en/stable/reference/shapely.union.html#shapely.union" target="_blank">union</a> (elke geometrie uit wordt-versie)</code><br/>
            <code>buitenranden = <a href="https://shapely.readthedocs.io/en/stable/reference/shapely.union.html#shapely.union" target="_blank">union</a> (elke buitenrand uit was-versie)</code><br/>
            <code>wijzigmarkering = (binnengebied van wordt_geometrie).<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.difference.html#shapely.difference" target="_blank">difference</a> (buitenranden)</code><br/>
            ''')
            self.Log.Detail ("Bepaal de wijzigmarkering voor de toegevoegde gebieden")

            buitenranden = None
            for (_, locatie) in self._WasLocaties.values ():
                buitenranden = _VoegBuitenrandToe (buitenranden, locatie)

            binnengebieden : Dict[int,object] = {}
            for (dimensie, locatie) in self._WordtLocaties.values ():
                _VoegGeometrieToe (binnengebieden, dimensie, locatie)
            numMarkeringen = _BepaalWijzigmarkeringen (binnengebieden, buitenranden)
            self.Generator.VoegHtmlToe ('Dit levert ' + str(numMarkeringen) + ' markering' + ('' if numMarkeringen == 1 else 'en') + ' op.</li>')

        else:
            waarde = ('GIO-deel naam' if self._Wijziging.AttribuutNaam == 'groepID' else 'normwaarde')
            self.Generator.VoegHtmlToe ('''<li>Per voorkomende ''' + waarde + ''' in de wordt-versie:
            de delen van de locaties uit de wordt-versie met die ''' + waarde + ''' waar de juridische regels voor het eerst gelden.
            Oftewel: het deel van de binnengebieden van locaties uit de wordt-versie met een specifieke ''' + waarde + ''' dat niet binnen de buitenranden ligt van de locaties 
            uit de was-versie met dezelfde ''' + waarde + ''':<br/>
            <code>wordt_geometrie = <a href="https://shapely.readthedocs.io/en/stable/reference/shapely.union.html#shapely.union" target="_blank">union</a> (elke geometrie uit wordt-versie voor een specifieke ''' + waarde + ''')</code><br/>
            <code>buitenranden = <a href="https://shapely.readthedocs.io/en/stable/reference/shapely.union.html#shapely.union" target="_blank">union</a> (elke buitenrand uit was-versie met dezelfde specifieke ''' + waarde + ''')</code><br/>
            <code>wijzigmarkering = (binnengebied van wordt_geometrie).<a href="https://shapely.readthedocs.io/en/stable/reference/shapely.difference.html#shapely.difference" target="_blank">difference</a> (buitenranden)</code><br/>
            ''')
            sep = 'Dit levert als wijzigmarkeringen op: '

            waarden = set (locatie['properties'][self._Wijziging.AttribuutNaam] for _, locatie in self._WordtLocaties.values ())
            for waarde in waarden:
                self.Log.Detail ("Bepaal de wijzigmarkering voor de toegevoegde gebieden voor " + self._Wijziging.AttribuutNaam + " = '" + str(waarde) + "'")

                buitenranden = None
                for (_, locatie) in self._WasLocaties.values ():
                    if locatie['properties'][self._Wijziging.AttribuutNaam] == waarde:
                        buitenranden = _VoegBuitenrandToe (buitenranden, locatie)

                binnengebieden : Dict[int,object] = {}
                for (dimensie, locatie) in self._WordtLocaties.values ():
                    if locatie['properties'][self._Wijziging.AttribuutNaam] == waarde:
                        _VoegGeometrieToe (binnengebieden, dimensie, locatie)
                numMarkeringen = _BepaalWijzigmarkeringen (binnengebieden, buitenranden)
                if numMarkeringen > 0:
                    self.Generator.VoegHtmlToe (sep + str(numMarkeringen) + ' voor "' + str(waarde)  + '"')
                    sep = ', '
            if sep != ', ':
                self.Generator.VoegHtmlToe ('Dit levert geen wijzigmarkeringen op')
            self.Generator.VoegHtmlToe ('.</li>')

        self.Generator.VoegHtmlToe ('</ol></li></ol>')
#endregion

#endregion

#======================================================================
#
# Tonen van GIO-wijziging
#
#======================================================================
#region Toon GIO-wijziging op de kaart
    def _ToonGIOWijzigingOnderdelen (self):
        self.Log.Detail ("Toon de onderdelen van de GIO-wijziging in een kaart")
        kaart = KaartGenerator.Kaart (self.Kaartgenerator)

        # Voeg de juridische nauwkeurigheid toe
#region Maak de binnen- en buitenranden voor de was- en wordt-locaties
        juridischeNauwkeurigheid_was = GeoData ()
        juridischeNauwkeurigheid_was.Locaties = { 2:[] }
        juridischeNauwkeurigheid_wordt = GeoData ()
        juridischeNauwkeurigheid_wordt.Locaties = { 2:[] }
        for id, (dimensie, locatie) in self._WasLocaties.items ():
            buitenrand = GeoData.MaakShapelyShape (locatie).buffer (0.05 * self._Wijziging.JuridischeNauwkeurigheid)
            if dimensie == 2:
                buitenrand = buitenrand.difference (GeoData.MaakShapelyShape(locatie).buffer (-0.05 * self._Wijziging.JuridischeNauwkeurigheid))
            buitenrand = {
                    'type': 'Feature',
                    'geometry': mapping (buitenrand)
                }
            juridischeNauwkeurigheid_was.Locaties[2].append (buitenrand)
            if id in self._WordtLocaties:
                juridischeNauwkeurigheid_wordt.Locaties[2].append (buitenrand)
        for id, (dimensie, locatie) in self._WordtLocaties.items ():
            if not id in self._WasLocaties:
                buitenrand = GeoData.MaakShapelyShape (locatie).buffer (0.05 * self._Wijziging.JuridischeNauwkeurigheid)
                if dimensie == 2:
                    buitenrand = buitenrand.difference (GeoData.MaakShapelyShape(locatie).buffer (-0.05 * self._Wijziging.JuridischeNauwkeurigheid))
                buitenrand = {
                        'type': 'Feature',
                        'geometry': mapping (buitenrand)
                    }
                juridischeNauwkeurigheid_wordt.Locaties[2].append (buitenrand)
        namen_was = self.Kaartgenerator.VoegGeoDataToe (juridischeNauwkeurigheid_was)[2]
        namen_wordt = self.Kaartgenerator.VoegGeoDataToe (juridischeNauwkeurigheid_wordt)[2]
        symbolisatie = self.Kaartgenerator.VoegUniformeSymbolisatieToe (2, '#CCCCCC', '#000000', '0.5')
#endregion
        kaart.VoegLaagToe ('Juridische nauwkeurigheid', namen_was, symbolisatie, True, False)
        kaart.LaatsteLaagAlsOud ()
        kaart.VoegLaagToe ('Juridische nauwkeurigheid', namen_wordt, symbolisatie, True, False)
        kaart.LaatsteLaagAlsNieuw ()

        # Voeg de originelen toe
        namen_was = self.Kaartgenerator.VoegGeoDataToe (self._Was)
        namen_wordt = self.Kaartgenerator.VoegGeoDataToe (self._Wordt)
        kaart.VoegLagenToe ('Originelen', namen_was, self._SymbolisatieNamen, True, False, postLaag = lambda _: kaart.LaatsteLaagAlsOud ())
        kaart.VoegLagenToe ('Originelen', namen_wordt, self._SymbolisatieNamen, True, False, postLaag = lambda _: kaart.LaatsteLaagAlsNieuw ())

        # Voeg de niet-revisie-mutaties toe
#region Maak de mutaties met wijzigactie als attribuut
        mutaties = GeoData ()
        mutaties.Attributen = { 'w' : Attribuut ('w', 'wijzigactie') }
        mutaties.Locaties = { dimensie: [{ 'type': 'Feature', 'geometry': locatie['geometry'], 'properties': { 'w': 'verwijder' } } for locatie in locaties] for dimensie, locaties in self._Wijziging.Was.Locaties.items () }
        namen_was = self.Kaartgenerator.VoegGeoDataToe (mutaties)
        mutaties = GeoData ()
        mutaties.Attributen = { 'w' : Attribuut ('w', 'wijzigactie') }
        mutaties.Locaties = { dimensie: [{ 'type': 'Feature', 'geometry': locatie['geometry'], 'properties': { 'w': 'voegtoe' } } for locatie in locaties] for dimensie, locaties in self._Wijziging.Wordt.Locaties.items () }
        namen_wordt = self.Kaartgenerator.VoegGeoDataToe (mutaties)
#endregion
        symbolisatie = {d: self.Kaartgenerator.VoegUniformeSymbolisatieToe (d, '#F8CECC', '#B85450') for d in [0,1,2]}
        kaart.VoegLagenToe ('LocatieMutaties (geen revisie)', namen_was, symbolisatie, True, True, postLaag = lambda _: kaart.LaatsteLaagAlsOud ())
        symbolisatie = {d: self.Kaartgenerator.VoegUniformeSymbolisatieToe (d, '#D5E8D4', '#82B366') for d in [0,1,2]}
        kaart.VoegLagenToe ('LocatieMutaties (geen revisie)', namen_wordt, symbolisatie, True, True, postLaag = lambda _: kaart.LaatsteLaagAlsNieuw ())

        # Voeg de revisie-mutaties toe
#region Maak de mutaties met wijzigactie als attribuut
        mutaties = GeoData ()
        mutaties.Attributen = { 'w' : Attribuut ('w', 'wijzigactie') }
        mutaties.Locaties = { dimensie: [{ 'type': 'Feature', 'geometry': locatie['geometry'], 'properties': { 'w': 'reviseer' } } for locatie in locaties] for dimensie, locaties in self._Wijziging.WordtRevisies.Locaties.items () }
        namen_wordt = self.Kaartgenerator.VoegGeoDataToe (mutaties)
        symbolisatie = {d: self.Kaartgenerator.VoegUniformeSymbolisatieToe (d, '#FFF2CC', '#D6B656') for d in [0,1,2]}
#endregion
        kaart.VoegLagenToe ('LocatieMutaties (revisie)', namen_wordt, symbolisatie, True, True)

        # Voeg de wijzigmarkeringen toe
        namen_wordt = self.Kaartgenerator.VoegGeoDataToe (self._Wijziging.WijzigMarkering)
        symbolisatie = {d: self.Kaartgenerator.VoegUniformeSymbolisatieToe (d, '#E1D5E7', '#9673A6') for d in [0,1,2]}
        kaart.VoegLagenToe ("Wijzigmarkeringen", namen_wordt, symbolisatie, True, True)
        kaart.Toon ()
#endregion

#region Toon GIO-wijziging als GML
    def _ToonGIOWinzigingGML (self):
        self.Log.Detail ("Maak en presenteer de GIO-wijziging als GML")
        self.Generator.VoegHtmlToe ('''
<p>De GIO-wijziging is een GML bestand waarin de vaststellingscontext nog aangepast moet worden:</p>''')

        wijzigingGML = self._Wijziging.SchrijfGIOWijziging ()

        if self.Request.KanBestandenSchrijven:
            fileNaam = self.Request.LeesString ("wijziging")
            if not fileNaam is None:
                self.Log.Detail ("Bewaar GIO-wijzjging in bestand '" + fileNaam + "'")
                filePad = os.path.join (self.Request._Pad, fileNaam)
                try:
                    os.makedirs (os.path.dirname (filePad))
                    with open (filePad, 'w', encoding='utf-8') as gml_file:
                        gml_file.write (wijzigingGML)
                except Exception as e:
                    self.Log.Fout ("Kan GIO-wijzjging niet opslaan in bestand '" + filePad + "': " + str(e))

        self.Log.Detail ("Neem GIO-wijziging op in resultaatpagina")
        self._ToonResultaatInTekstvak (wijzigingGML, "GIO-wijziging.gml", "xml", "wijziging")
#endregion

