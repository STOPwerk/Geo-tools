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
from datetime import date
import json
import os;
from uuid import uuid4

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from geo_manipulatie import GeoManipulatie
from weergave_webpagina import WebpaginaGenerator

class GIOWijzigingMaker (GeoManipulatie):
#======================================================================
#
# Webpagina's
#
#======================================================================
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("Bepaling van een GIO-wijziging")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters, log: Meldingen = None):
        return GIOWijzigingMaker (request, log).VoerUit ()

#======================================================================
#
# Implementatie
#
#======================================================================
    def __init__(self, request : Parameters, log: Meldingen):
        super ().__init__ ("GIO-wijziging", "GIO-wijziging - geen resultaat", request, log)
        # Was-versie van de GIO
        self._Was : GeoManipulatie.GeoData = None
        # Wordt-versie van de GIO
        self._Wordt : GeoManipulatie.GeoData = None
        # Naam waaronder de te gebruiken symbolisatie voor zowel de was- als wordt-versie is geregistreerd
        self._SymbolisatieNaam : str = None
        # Gegevens waaruit de GIO-wijziging wordt samengesteld
        self._Wijzigingen = None
        # Was-versie van de GIO minus de manifest ongewijzigde locaties
        self._ResterendWas : GeoManipulatie.GeoData = None
        # Naam om de resterend-was-data in de kaart te tonen
        self._ResterendWasDataNaam : str = None
        # Wordt-versie van de GIO minus de manifest ongewijzigde locaties
        self._ResterendWordt : GeoManipulatie.GeoData = None
        # Naam om de resterend-wordt-data in de kaart te tonen
        self._ResterendWordtDataNaam : str = None
        # De resulterende GIO-wijziging
        self._Wijziging : GeoManipulatie.GeoData = None

    def _VoerUit (self, titelOperatie = "Bepaling GIO wijziging"):
        """Voer het request uit"""
        if not self._LeesBestandenEnSpecificatie  ():
            return False

        self._InitialiseerWebpagina ()
        self.Generator.LeesCssTemplate ('resultaat')
        self.Generator.LeesJSTemplate ('resultaat')
        einde = self.Generator.StartSectie ("<h3>" + titelOperatie + "</h3>", True)
        if self.Request.LeesString ("beschrijving"):
            self.Generator.VoegHtmlToe ('<p>' + self.Request.LeesString ("beschrijving") + '</p>') 

        self._BepaalWijzigingen ()

        self.Generator.VoegHtmlToe (einde)

        teHernoemen = { wordt_id: list(was_id) for wordt_id, was_id in  self._Wijzigingen.WordtRevisieLocaties.items () if not wordt_id in was_id }
        if len (teHernoemen) > 0:
            einde = self.Generator.StartSectie ("Overeenkomstige basisgeometrie-IDs", True)
            self._ToonOvereenkomstigeLocaties (teHernoemen)
            self.Generator.VoegHtmlToe (einde)
            
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
            def __BewaarGML (gml):
                if self.Request.IsOnlineOperatie:
                    self._WasGML = gml
            self._Was = self.LeesGeoBestand ('was', True, __BewaarGML)
            if self._Was is None:
                return False
            if self._Was.Soort != 'GIO':
                self.Log.Fout ("Het bestand bevat geen GIO maar: " + self._Was.Soort)
                succes = False
                valideerGIOs = False

        if self._Wordt is None:
            self.Log.Informatie ("Lees de wordt-versie van de GIO")
            self._Wordt = self.LeesGeoBestand ('wordt', True)
            if self._Wordt is None:
                return False
            if self._Wordt.Soort != 'GIO':
                self.Log.Fout ("Het bestand bevat geen GIO maar: " + self._Wordt.Soort)
                succes = False
                valideerGIOs = False

        if valideerGIOs:
            if self._Was.Dimensie != self._Wordt.Dimensie:
                self.Log.Fout ("De was- en wordt-versie moeten allebei uitsluitend vlakken, lijnen of punten hebben")
                succes = False
            if self._Was.AttribuutNaam != self._Wordt.AttribuutNaam:
                self.Log.Fout ("De was- en wordt-versie moeten allebei uitsluitend geometrie, GIO-delen of normwaarden hebben")
                succes = False
            elif not self._Was.GIODelen is None:
                for groepId, gioDeel in self._Was.GIODelen.items ():
                    nieuw = self._Wordt.GIODelen.get (groepId)
                    if not nieuw is None and nieuw.Label != gioDeel.Label:
                        self.Log.Fout ("Label van GIO-deel verschilt: groepID '" + groepID + "' had label '" + gioDeel.Label + "' en dat wordt '" + nieuw.Label + "'")
                        succes = False

        if self._SymbolisatieNaam is None:
            self.Log.Informatie ("Lees de symbolisatie (indien aanwezig)")
            symbolisatie = self.Request.LeesBestand (self.Log, "symbolisatie", False)
            if self.Request.IsOnlineOperatie:
                self._SymbolisatieXML = symbolisatie
            self._SymbolisatieNaam = self.VoegDefaultSymbolisatieToe (self._Was) if symbolisatie is None else self.VoegSymbolisatieToe (symbolisatie)

        if self.NauwkeurigheidInDecimeter (True) is None:
            succes = False

        return succes

#======================================================================
#
# Bepaling van wijzigingen tussen twee GIO's
#
#======================================================================
    class Wijzigingen:

        def __init__ (self, wasVersie : GeoManipulatie.GeoData):
            # De basisgeo-ID van de locaties uit de was-versie die in de GIO-wijziging opgenomen moet worden
            self.WasLocaties : Set[str] = set ()
            # De basisgeo-ID van de locaties uit de wordt-versie die in de GIO-wijziging opgenomen moet worden
            self.WordtLocaties : Set[str] = set ()
            # De gebieden waar de was-/wordt-locaties van elkaar verschillen.
            # Dit kunnen zowel geometrieën uit de GIO-versie zijn als gebieden.
            # Key: dimensie van de geometrie in de markering, value: lijst van enkelvoudige geometrieën (geo-interface)
            self.Markering : Dict[int,List[object]] = {}
            self.Markering[wasVersie.Dimensie] = [] # Geometrie uit de GIO
            if wasVersie.Dimensie == 1: # Ook gebieden
                self.Markering[2] = []

            # De juridisch ongewijzigde locaties in de wordt-versie die een revisie 
            # zijn van de locaties in de was-versie, d.w.z. alleen van naam verschillen
            # of waarvan de geometrie binnen de juridische nauwkeurigheid is gewijzigd.
            # Relatie tussen de wordt-revisie-locatie en de was-locatie waar het een revisie van is
            # Key is de basisgeometrie-ID wordt-locatie, value de basisgeo-ID van de was-versie.
            self.WordtRevisieLocaties : Dict[str,List[str]] = {}
            # Alleen voor de weergave: de gebieden waar de was- en wordt-revisies van elkaar verschillen.
            # Dit kunnen zowel geometrieën uit de GIO-versie zijn als gebieden.
            # Key: dimensie van de geometrie in de markering, value: lijst van enkelvoudige geometrieën
            self.RevisieMarkering : Dict[int,List[object]] = {}
            self.RevisieMarkering[wasVersie.Dimensie] = [] # Geometrie uit de GIO
            if wasVersie.Dimensie == 1: # Ook gebieden
                self.RevisieMarkering[2] = []

            # Alleen voor weergave: de locaties die voor zowel de was- als wordt-versie dezelfde 
            # basisgeo-ID hebben, en waarvan bovendien de naam en eventuele attribuutwaarde gelijk zijn
            self.ManifestOngewijzigdeLocaties : Set[str] = set ()
            # Alleen voor weergave: buffergebieden
            self.VerdikteGeometrie = []
            self.VerkleindeGeometrie = []

    def _BepaalWijzigingen (self) :
        """Bepaal de wijzigingen tussen twee versies van een GIO"""
        self.Generator.VoegHtmlToe ('''<p>Voor de bepaling van een GIO-wijziging wordt de elders beschreven <a href="@@@GeoTools_Url@@@wiki/Maak-gio-wijziging" target="_blank">procedure</a> gevolgd.
In onderstaande kaart wordt het startpunt getoond: links de originele (was)-versie van de GIO met ''' + str(len (self._Was.Locaties)) + ''' locaties, rechts de nieuwe (wordt)-versie met ''' + str(len (self._Wordt.Locaties)) + ''' locaties.
Beweeg de schuif om meer of minder van elke versie te zien. Klik op een ''' + self._Was.GeometrieNaam (False) + ' voor aanvullende details</p>\n')
        kaart = GeoManipulatie.Kaart (self)
        dataNaam = self.VoegGeoDataToe (self._Was)
        kaart.VoegOudLaagToe ("Was-versie", dataNaam, self._SymbolisatieNaam)
        dataNaam = self.VoegGeoDataToe (self._Wordt)
        kaart.VoegNieuwLaagToe ("Wordt-versie", dataNaam, self._SymbolisatieNaam)
        kaart.ZoomTotNauwkeurigheid (False)
        kaart.Toon ()

        self.Generator.VoegHtmlToe ('''<p>De bepaling van een GIO-wijziging bestaat uit de volgende stappen:</p>
<ol>''')
        self._Wijzigingen = GIOWijzigingMaker.Wijzigingen (self._Was)
        self._WasLocaties = { locatie['properties']['id'] : locatie for locatie in self._Was.Locaties}
        self._WordtLocaties = { locatie['properties']['id'] : locatie for locatie in self._Wordt.Locaties}

        # De locaties voor de geo-operaties worden bijgehouden in:
        self._ManifestOngewijzigdeGeometrieen ()

        tijd = None
        if len (self._ResterendWas.Locaties) == 0:
            if len (self._ResterendWordt.Locaties) == 0:
                # Speciaal geval: alleen locaties met ongewijzigde geometrieën
                self.Generator.VoegHtmlToe ('<li>Er zijn geen locaties over die via geometrische vergelijking op wijzigingen geanalyseerd hoeven te worden</li>')
            else:
                # Speciaal geval: alle locaties uit de was-versie hebben een ongewijzigde geometrie
                self.Generator.VoegHtmlToe ('<li>Er zijn geen locaties uit de was-versie over die via geometrische vergelijking op wijzigingen geanalyseerd hoeven te worden. De overgebleven locaties in de wordt-versie zijn nieuw.</li>')
                self._Wijzigingen.WordtLocaties.update (self._ResterendWordt.Locaties)
                wordtGeometrieen, isMulti2 = self.MaakLijstVanGeometrieen (self._ResterendWordt)
                self._Wijzigingen.Markering[self._Was.Dimensie].extend (wordtGeometrieen)

        elif len (self._ResterendWordt.Locaties) == 0:
            # Speciaal geval: alle locaties uit de wordt-versie hebben een ongewijzigde geometrie
            self.Generator.VoegHtmlToe ('<li>Er zijn geen locaties uit de wordt-versie over die via geometrische vergelijking op wijzigingen geanalyseerd hoeven te worden. De overgebleven locaties in de was-versie komen te vervallen.</li>')
            self._Wijzigingen.WasLocaties.update (self._ResterendWordt.Locaties)
            wasGeometrieen, isMulti = self.MaakLijstVanGeometrieen (self._ResterendWas)
            self._Wijzigingen.Markering[self._Was.Dimensie].extend (wasGeometrieen)

        else:
            # Voer de geometrische analyse uit
            wasGeometrieen, isMulti = self.MaakLijstVanGeometrieen (self._ResterendWas)
            wordtGeometrieen, isMulti2 = self.MaakLijstVanGeometrieen (self._ResterendWordt)
            if self._Was.Dimensie == 0:
                self._AnalyseerPunten (wasGeometrieen, wordtGeometrieen, isMulti or isMulti2)

        self.Generator.VoegHtmlToe ('</ol>')

        self._VerwerkTotGIOWijziging ()
        self._ToonGeoAnalyseResultaat ()

    #------------------------------------------------------------------
    #
    # Verwerk locaties met een basisgeo-ID die zowel in de was-
    # als wordt-versie voorkomen.
    #
    #------------------------------------------------------------------
    def _ManifestOngewijzigdeGeometrieen (self):
        self.Log.Informatie ('Onderzoek de locaties met manifest ongewijzigde geometrieën')
        self.Generator.VoegHtmlToe ('<li>Als dezelfde basisgeometrie-ID zowel in de was- als wordt-versie voorkomt, dan is de geometrie per definitie ongewijzigd. ')
        if not self._Was.AttribuutNaam is None:
            self.Generator.VoegHtmlToe ('Als de ' + self._Was.AttribuutNaam + ' van de bijbehorende locatie verschilt in beide versies, dan wijzigt de locatie en moet de hele geometrie in de wijzigmarkeringen opgenomen worden. ')
        self.Generator.VoegHtmlToe ('Als alleen de naam van de locatie verschilt, dan wordt dat niet als een wijziging maar als een revisie beschouwd. ')

        tijd = self.Log.Tijd ()

        # Bepaal of en hoe de locaties met manifest ongewijzigde geometrie muteren
        manifestOngewijzigdId = set ()
        for wasId, wasLocatie in self._WasLocaties.items ():
            wordtLocatie = self._WordtLocaties.get (wasId)
            if not wordtLocatie is None:
                manifestOngewijzigdId.add (wasId)

                isGewijzigd = False if self._Was.AttribuutNaam is None else bool (wasLocatie['properties'][self._Was.AttribuutNaam] != wordtLocatie['properties'][self._Was.AttribuutNaam])
                if isGewijzigd:
                    self._Wijzigingen.WasLocaties.add (wasId)
                    self._Wijzigingen.WordtLocaties.add (wasId)
                    self._Wijzigingen.Markering[self._Was.Dimensie].extend (self.SplitsMultiGeometrie (wasLocatie))

                elif wasLocatie['properties'].get ('naam') != wordtLocatie['properties'].get ('naam'):
                    self._Wijzigingen.WordtRevisieLocaties[wasId] = [wasId]
                    self._Wijzigingen.RevisieMarkering[self._Was.Dimensie].extend (self.SplitsMultiGeometrie (wasLocatie))
                else:
                    self._Wijzigingen.ManifestOngewijzigdeLocaties.add (wasId)

        # De overgebleven locaties zijn:
        self._ResterendWas = GeoManipulatie.GeoData () 
        self._ResterendWas.Attributen = self._Was.Attributen
        self._ResterendWas.AttribuutNaam = self._Was.AttribuutNaam
        self._ResterendWas.Locaties = [l for l in self._Was.Locaties if not l['properties']['id'] in manifestOngewijzigdId]
        self._ResterendWordt = GeoManipulatie.GeoData () 
        self._ResterendWordt.Attributen = self._Was.Attributen
        self._ResterendWordt.AttribuutNaam = self._Was.AttribuutNaam
        self._ResterendWordt.Locaties = [l for l in self._Wordt.Locaties if not l['properties']['id'] in manifestOngewijzigdId]

        if not tijd is None:
            tijd = self.Log.Tijd () - tijd

        num = len (manifestOngewijzigdId)
        self.Generator.VoegHtmlToe ('Er zijn ' + str(num) + ' locatie(s) met manifest ongewijzigde geometrie, ')
        self.Generator.VoegHtmlToe ('waarvan ' + str(len (self._Wijzigingen.WordtLocaties)) + ' gewijzigd, ')
        self.Generator.VoegHtmlToe (str(len (self._Wijzigingen.WordtRevisieLocaties)) + ' gereviseerd en ')
        self.Generator.VoegHtmlToe (str(len (self._Wijzigingen.ManifestOngewijzigdeLocaties)) + ' ongewijzigd.')
        if not tijd is None:
            self.Generator.VoegHtmlToe (' Het analyseren van deze locaties duurde ' + '{:.3f}'.format (tijd) + 's.')
        self.Generator.VoegHtmlToe ('</li>')

    #------------------------------------------------------------------
    #
    # Verwerk de punten voor locaties zonder manifest ongewijzigde
    # geometrie.
    #
    #------------------------------------------------------------------
    def _AnalyseerPunten (self, wasGeometrieen : List[GeoManipulatie.EnkeleGeometrie], wordtGeometrieen : List[GeoManipulatie.EnkeleGeometrie], heeftMultiGeometrie : bool):
        self.Log.Informatie ('Onderzoek de overige punt-locaties')
        drempel = self.NauwkeurigheidInMeter ()
        self.Generator.VoegHtmlToe ('<li>Vergelijk ' + str(len (self._ResterendWas.Locaties)) + ' locaties met ' + str(len(wasGeometrieen)) + ' punten uit de was-versie en ' + str(len (self._ResterendWordt.Locaties)) + ''''
met ''' + str(len(wordtGeometrieen)) + ''' punten uit de wordt-versie paarsgewijs met elkaar.<ul>
<li>Als de twee punten uit een paar op een afstand kleiner dan de juridische nauwkeurigheid (''' + '{:.1f}'.format (drempel) + ''''m) staan, dan
worden ze geacht dezelfde plaats te betreffen. ''')
        if not self._Was.AttribuutNaam is None:
            self.Generator.VoegHtmlToe ('Er is dan sprake van een wijziging als de bijbehorende locaties verschillen in ' + self._Was.AttribuutNaam + '''; 
beide locaties worden dan als gewijzigd beschouwd, en het wordt-punt wordt aan de wijzigmarkering toegevoegd.''')
        self.Generator.VoegHtmlToe ('''Zo niet, dan worden de punten als revisie van elkaar gezien - de geo-tools doen niet aan het vergelijken van geomeotrieën om te zien of ze gelijk zijn.</li>
<li>Punten uit de was-versie die geen corresponderend punt in de wordt-versie hebben worden als vervallen beschouwd. De 
locatie wordt aan de gewijzigde locaties toegevoegd, en het punt aan de wijzigmarkeringen.
<li>Punten uit de wordt-versie die geen corresponderend punt in de was-versie hebben worden als nieuw beschouwd. De 
locatie wordt aan de gewijzigde locaties toegevoegd, en het punt aan de wijzigmarkeringen.</li>
</ul>
''')
        drempel *= drempel

        # Met was-locaties worden de hier self._ResterendWas.Locaties bedoeld, niet de self._Was.Locaties. Idem voor wordt.

        # Meet de doorlooptijd van de geo-operatie (indien tijd wordt bijgehouden)
        tijd = self.Log.Tijd ()

        # Verzamel eerst gegevens over de punten, verdeel ze over de groepen:
        # Punten van een gewijzigde wordt-locatie of die nieuw zijn
        wijzigingPunten : Set[GeoManipulatie.EnkeleGeometrie] = set ()
        # Punten uit de wordt-versie die onderdeel zijn van een revisie of die niet wijzigen voor een gewijzigde wordt-locatie.
        revisieWordtPunten : Set[GeoManipulatie.EnkeleGeometrie] = set ()
        # Paren was-wordt punten die een revisie kunnen vormen
        revisieParen : List[Tuple[GeoManipulatie.EnkeleGeometrie,GeoManipulatie.EnkeleGeometrie]] = []
        # Hou op locatie-ID niveau bij:
        # Was-locaties die gewijzigd zijn
        gewijzigdeWasLocaties : Set[str] = set ()
        # Wordt-locaties die gewijzigd zijn
        gewijzigdeWordtLocaties : Set[str] = set ()
        # Statistieken
        numWasVervallen = 0

        for i in range (0, len (wasGeometrieen)):
            was_geom = wasGeometrieen[i]
            was_coord = was_geom.Geometrie['geometry']['coordinates']

            wasIsVervallen = None
            revisieWordtParen = []
            for j in range (0, len (wordtGeometrieen)):
                wordt_geom = wordtGeometrieen[j]
                wordt_coord = wordt_geom.Geometrie['geometry']['coordinates']
                afstand = (was_coord[0] - wordt_coord[0]) * (was_coord[0] - wordt_coord[0]) + (was_coord[1] - wordt_coord[1]) * (was_coord[1] - wordt_coord[1])

                if afstand < drempel:
                    # Dit moeten corresponderende geometrieën zijn
                    if was_geom.Attribuutwaarde != wordt_geom.Attribuutwaarde:
                        # Nooit een revisie maar een wijziging
                        wasIsVervallen = True
                        wijzigingPunten.add (wordt_geom)
                        gewijzigdeWordtLocaties.add (wordt_geom.Locatie['properties']['id'])
                    else:
                        # Kan onderdeel zijn van een revisie
                        revisieWordtParen.append (wordt_geom)
                        # Alleen de weergave: dit punt wordt altijd gemarkeerd als een revisie
                        # Deze markering is geen onderdeel van de GIO-wijziging
                        revisieWordtPunten.add (wordt_geom)

            if len (revisieWordtParen) > 0:
                # revisie-kandidaat
                if wasIsVervallen is None:
                    # Vooralsnog lijken dit revisies
                    revisieParen.extend ((was_geom, wordt_geom) for wordt_geom in revisieWordtParen)
                    wasIsVervallen = False
            elif wasIsVervallen is None:
                # Locatie is vervallen
                wijzigingPunten.add (was_geom)
                numWasVervallen += 1
                wasIsVervallen = True

            if wasIsVervallen:
                gewijzigdeWasLocaties.add (was_geom.Locatie['properties']['id'])

        # Het kan zijn dat een wordt-punt voor het ene was-punt als revisie gezien wordt, en voor het andere als gewijzigd.
        # Dat kan voorkomen als een van de GIO-versies punten heeft die te dicht bij elkaar staan
        revisieWordtPunten.difference_update (wijzigingPunten)

        # Bepaal de nieuwe geometrieën
        numWordtGewijzigd = len (wijzigingPunten) - numWasVervallen
        for wordt_geom in wordtGeometrieen:
            if not wordt_geom in wijzigingPunten and not wordt_geom in revisieWordtPunten:
                # Deze wordt heeft geen matching was en is dus een nieuw punt
                wijzigingPunten.add (wordt_geom)
                gewijzigdeWordtLocaties.add (wordt_geom.Locatie['properties']['id'])
        numWordtNieuw = len (wijzigingPunten) - numWordtGewijzigd - numWasVervallen

        # Bewaar de wijzigmarkeringen
        self._Wijzigingen.Markering[0].extend (p.Geometrie for p in wijzigingPunten)
        self._Wijzigingen.RevisieMarkering[0].extend (p.Geometrie for p in revisieWordtPunten)

        if not tijd is None:
            tijd = self.Log.Tijd () - tijd

        self.Generator.VoegHtmlToe ('Zo blijken ' + str(numWasVervallen) + ' punten uit de was-versie vervallen, en in de wordt-versie ' + str(numWordtNieuw) + ' punten nieuw en ' + str(numWordtGewijzigd) + ' gewijzigd te zijn. ')
        self.Generator.VoegHtmlToe ('En er zijn ' + str(len(revisieParen)) + ' paren van een punt uit de was-versie en een uit de wordt-versie gevonden die revisies van elkaar zijn.')
        if not tijd is None:
            self.Generator.VoegHtmlToe (' De bepaling hiervan duurde ' + '{:.3f}'.format (tijd) + 's.')
        self.Generator.VoegHtmlToe ('</li>')

        # Bepaal welke wordt-locaties een revisie zijn, en van welke was-locaties.
        self._VerwerkAnalyseUitkomst (gewijzigdeWasLocaties, gewijzigdeWordtLocaties, revisieParen, heeftMultiGeometrie)

    #------------------------------------------------------------------
    #
    # Verwerk de analyseresultaten tot de gegevens voor de GIO-wijzigjng
    #
    #------------------------------------------------------------------
    def _VerwerkAnalyseUitkomst (self, gewijzigdeWasLocaties : Set[str], gewijzigdeWordtLocaties : Set[str], revisieParen : List[Tuple[GeoManipulatie.EnkeleGeometrie,GeoManipulatie.EnkeleGeometrie]], heeftMultiGeometrie : bool):
        """Gebruik de gegevens om de wijzigingen volgens spec aan te vullen"""

        self.Generator.VoegHtmlToe ('''<li>Voer eventuele correcties door:
<ul>
<li>Als een of beide GIO-versies geometrieën bevat die minder dan de juridische nauwkeurigheid zijn gescheiden, dan kan dezelfde geometrie 
uit de ene versie zowel als revisie van de ene als wijziging van de andere geometrie uit de andere GIO-versie gezien worden. Voer hiervoor een ontdubbeling uit.</li>''')
        if heeftMultiGeometrie:
            self.Generator.VoegHtmlToe ('''<li>Een of beide GIO-versies hebben locaties die multi-geometrieën bevatte. Het kan voorkomen dat van dezelfde locatie de ene geometrie 
als wijziging gezien wordt en de andere als revisie. In de geo-renvooi van STOP kan alleen de hele locatie als gewijzigd of revisie aangemerkt worden. 
Doordat de revisie-geometrie als gewijzigd opgenomen wordt, moet de locatie van de corresponderende geometrie uit de andere GIO-versie ook als wijziging opgenomen worden,
anders zou de revisie-geometrie bij de geo-renvooiweergave niet bij zowel de was als de wordt-versie zichtbaar zijn.</li>''')
        self.Generator.VoegHtmlToe ('</ul>')

        # Meet de doorlooptijd van de verwerking (indien tijd wordt bijgehouden)
        tijd = self.Log.Tijd ()

        # De revisieParen bevat relaties tussen was- en wordt-locaties op puntniveau
        # Als de locaties multi-geometrieën hebben, dan kan een revisie-punt een relatie 
        # leggen tussen twee locaties die wijzigen. Haal die uit de revisieParen zodat
        # alleen de echte revisieparen overblijven,
        # Overigens: elke was-locatie is nu ofwel gewijzigd, ofwel deel van een revisieParen
        # relatie omdat er geen ongewijzigde locaties zijn (geo-tools vergelijken geen geometrieën).
        # Iden voor wordt-locaties.
        revisiePaarId = [(was_geom.Locatie['properties']['id'], wordt_geom.Locatie['properties']['id']) for was_geom, wordt_geom in revisieParen]
        while True:
            echteRevisiePaarId = []
            for was_id, wordt_id in revisiePaarId:
                if was_id in gewijzigdeWasLocaties:
                    gewijzigdeWordtLocaties.add (wordt_id)
                elif wordt_id in gewijzigdeWordtLocaties:
                    gewijzigdeWasLocaties.add (was_id)
                else:
                    echteRevisiePaarId.append ((was_id, wordt_id))
            if len (echteRevisiePaarId) == len (revisiePaarId):
                break;
            revisiePaarId = echteRevisiePaarId

        # Vul hiermee de wijzigingen specificaties
        self._Wijzigingen.WasLocaties.update (gewijzigdeWasLocaties)
        self._Wijzigingen.WordtLocaties.update (gewijzigdeWordtLocaties)
        was_revisies = set ()
        for was_id, wordt_id in revisiePaarId:
            lijst = self._Wijzigingen.WordtRevisieLocaties.get (wordt_id)
            if lijst is None:
                self._Wijzigingen.WordtRevisieLocaties[wordt_id] = lijst = set ()
            lijst.add (was_id)
            was_revisies.add (was_id)

        if not tijd is None:
            tijd = self.Log.Tijd () - tijd

        self.Generator.VoegHtmlToe ('Uiteindelijk blijken ' + str(len(gewijzigdeWasLocaties)) + ' locaties uit de was-versie en ' + str(len(gewijzigdeWordtLocaties)) + ' locaties uit de wordt-versie gewijzigd.')
        self.Generator.VoegHtmlToe (str(len(self._Wijzigingen.WordtRevisieLocaties)) + ' Locaties uit de wordt-versie blijken revisies van ' + str(len(was_revisies)) + ' locaties uit de was-versie.')
        if not tijd is None:
            self.Generator.VoegHtmlToe (' Het onderzoek naar en doorvoeren van correcties duurde ' + '{:.3f}'.format (tijd) + 's.')
        self.Generator.VoegHtmlToe ('</li>')

    #------------------------------------------------------------------
    #
    # Verwerk de gegevens voor de GIO-wijzigjng tot een GeoData structuur
    #
    #------------------------------------------------------------------
    def _VerwerkTotGIOWijziging (self):
        self._Wijziging = GeoManipulatie.GeoData ()
        self._Wijziging.Attributen = self._Was.Attributen
        self._Wijziging.AttribuutNaam = self._Was.AttribuutNaam
        self._Wijziging.Dimensie = self._Was.Dimensie
        self._Wijziging.Soort = 'GIO-wijziging'
        self._Wijziging.JuridischeNauwkeurigheid = self.NauwkeurigheidInDecimeter ()
        if self._Wordt.Vaststellingscontext is None:
            nu = date.today().strftime ("%Y-%m-%d")
            self._Wijziging.Vaststellingscontext = '''    <geo:context>
        <gio:GeografischeContext>
            <gio:achtergrondVerwijzing>brt</gio:achtergrondVerwijzing>
            <gio:achtergrondActualiteit>''' + nu + '''</gio:achtergrondActualiteit>
        </gio:GeografischeContext>
    </geo:context>'''
        else:
            self._Wijziging.Vaststellingscontext = self._Wordt.Vaststellingscontext
        self._Wijziging.WorkId = self._Was.WorkId
        if not self._Was.GIODelen is None:
            self._Wijziging.GIODelen = {}
            for groepId, gioDeel in self._Was.GIODelen.items ():
                nieuw = self._Wordt.GIODelen.get (groepId)
                if nieuw is None:
                    kloon = GeoManipulatie.GIODeel (groepId, gioDeel.Label)
                    kloon.WijzigActie = 'verwijder'
                else:
                    kloon = gioDeel
                self._Wijziging.GIODelen[groepId] = kloon

            for groepId, gioDeel in self._Wordt.GIODelen.items ():
                if not groepId in self._Was.GIODelen:
                    kloon = GeoManipulatie.GIODeel (groepId, gioDeel.Label)
                    kloon.WijzigActie = 'voegtoe'
                    self._Wijziging.GIODelen[groepId] = kloon
        else:
            self._Wijziging.NormLabel = self._Wordt.NormLabel
            self._Wijziging.NormID = self._Wordt.NormID
            self._Wijziging.EenheidLabel = self._Wordt.EenheidLabel
            self._Wijziging.EenheidID = self._Wordt.EenheidID

        self._Wijziging.Was = GeoManipulatie.GeoData ()
        self._Wijziging.Was.Attributen = self._Was.Attributen
        self._Wijziging.Was.AttribuutNaam = self._Was.AttribuutNaam
        self._Wijziging.Was.Dimensie = self._Was.Dimensie
        self._Wijziging.Was.GIODelen = self._Was.GIODelen
        self._Wijziging.Was.ExpressionId = self._Was.ExpressionId
        self._Wijziging.Was.Locaties = [self._WasLocaties[locatie_id] for locatie_id in self._Wijzigingen.WasLocaties]

        self._Wijziging.Wordt = GeoManipulatie.GeoData ()
        self._Wijziging.Wordt.Attributen = self._Wordt.Attributen
        self._Wijziging.Wordt.AttribuutNaam = self._Was.AttribuutNaam
        self._Wijziging.Wordt.Dimensie = self._Was.Dimensie
        self._Wijziging.Wordt.GIODelen = self._Wordt.GIODelen
        self._Wijziging.Wordt.ExpressionId = self._Wordt.ExpressionId
        self._Wijziging.Wordt.Locaties = [self._WordtLocaties[locatie_id] for locatie_id in self._Wijzigingen.WordtLocaties]

        self._Wijziging.WordtRevisies = GeoManipulatie.GeoData ()
        self._Wijziging.WordtRevisies.Dimensie = self._Was.Dimensie
        self._Wijziging.WordtRevisies.Locaties = []
        for locatie_id, was_id in self._Wijzigingen.WordtRevisieLocaties.items ():
            locatie = self._WordtLocaties[locatie_id].copy ()
            locatie['properties']['isRevisieVan'] = was_id
            self._Wijziging.WordtRevisies.Locaties.append (locatie)

        self._Wijziging.WijzigMarkering = {}
        for dimensie, markeringen in self._Wijzigingen.Markering.items ():
            if len (markeringen) > 0:
                self._Wijziging.WijzigMarkering[dimensie] = GeoManipulatie.GeoData ()
                self._Wijziging.WijzigMarkering[dimensie].Dimensie = dimensie
                for markering in markeringen:
                    markering['properties'] = { 'id': str(uuid4()) }
                    self._Wijziging.WijzigMarkering[dimensie].Locaties.append (markering)

    #------------------------------------------------------------------
    #
    # Toon de uitkomst van de geo-analyses op de kaart
    #
    #------------------------------------------------------------------
    def _ToonGeoAnalyseResultaat (self):
        """Maak een kaart met de uitkomsten van de analyse, waarbij alle locaties/geometrieën naar hun rol in GIO-wijziging zijn opgedeeld"""
        self.Generator.VoegHtmlToe ('''<p>De resultaten van de bepaling zijn in de kaart weergegeven.</p>''')

        kaart = GeoManipulatie.Kaart (self)
        kaart.ZoomTotNauwkeurigheid (True)
        dataSet = GeoManipulatie.GeoData ()
        dataSet.Dimensie = self._Was.Dimensie
        dataSet.Attributen = self._Was.Attributen

        if len (self._Wijzigingen.VerdikteGeometrie) > 0:
            # Buffers om geometrieën heen
            bufferSet = GeoManipulatie.GeoData ()
            bufferSet.Dimensie = 2
            bufferSet.Locaties = [{ 'type': 'Feature', 'geometry': mapping (b) } for b in self._Wijzigingen.VerdikteGeometrie]
            symNaam = self.VoegUniformeSymbolisatieToe (2, "#D80073", "#A50040")
            kaart.VoegLaagToe ("Buffers voor de geometrieën", self.VoegGeoDataToe (bufferSet), symNaam, True, True)

        if len (self._Wijzigingen.ManifestOngewijzigdeLocaties) > 0:
            # Manifest ongewijzigde geometrieën
            dataSet.Locaties = [self._WasLocaties[i] for i in self._Wijzigingen.ManifestOngewijzigdeLocaties]
            symNaam = self.VoegUniformeSymbolisatieToe (dataSet.Dimensie, "#cccccc", "#000000", '0' if dataSet.Dimensie == 2 else '1')
            kaart.VoegLaagToe ("Manifest ongewijzigde locaties", self.VoegGeoDataToe (dataSet), symNaam, True, True)

        if len (self._Wijzigingen.WordtRevisieLocaties) > 0:
            # Revisies
            symNaam = self.VoegDefaultSymbolisatieToe (dataSet)
            wasRevisieLocaties = set ()
            for was_id in self._Wijzigingen.WordtRevisieLocaties.values ():
                wasRevisieLocaties.update (was_id)
            dataSet.Locaties = [self._WasLocaties[i] for i in wasRevisieLocaties]
            kaart.VoegOudLaagToe ("Locaties met revisies", self.VoegGeoDataToe (dataSet), symNaam, True, True)
            dataSet.Locaties = [self._WordtLocaties[i] for i in self._Wijzigingen.WordtRevisieLocaties.keys ()]
            kaart.VoegNieuwLaagToe ("Locaties met revisies", self.VoegGeoDataToe (dataSet), symNaam, True, True)

        if len (self._Wijzigingen.WasLocaties) > 0:
            # Wijzigingen
            symNaam = self.VoegUniformeSymbolisatieToe (dataSet.Dimensie, "#F8CECC", "#B85450", '0' if dataSet.Dimensie == 2 else '1')
            dataSet.Locaties = [self._WasLocaties[i] for i in self._Wijzigingen.WasLocaties]
            kaart.VoegOudLaagToe ("Gewijzigde locaties", self.VoegGeoDataToe (dataSet), symNaam, True, True)
        if len (self._Wijzigingen.WordtLocaties) > 0:
            # Wijzigingen
            symNaam = self.VoegUniformeSymbolisatieToe (dataSet.Dimensie, "#F8CECC", "#B85450", '0' if dataSet.Dimensie == 2 else '1')
            dataSet.Locaties = [self._WordtLocaties[i] for i in self._Wijzigingen.WordtLocaties]
            kaart.VoegNieuwLaagToe ("Gewijzigde locaties", self.VoegGeoDataToe (dataSet), symNaam, True, True)

        if len (self._Wijzigingen.VerkleindeGeometrie) > 0:
            # Buffers om geometrieën heen
            bufferSet = GeoManipulatie.GeoData ()
            bufferSet.Dimensie = 2
            bufferSet.Locaties = [{ 'type': 'Feature', 'geometry': mapping (b) } for b in self._Wijzigingen.VerkleindeGeometrie]
            symNaam = self.VoegUniformeSymbolisatieToe (2, "#D80073", "#A50040")
            kaart.VoegLaagToe ("Buffers voor de geometrieën", self.VoegGeoDataToe (bufferSet), symNaam, True, True)

        for dimensie, markeringen in self._Wijzigingen.RevisieMarkering.items ():
            # Markeringen voor de revisies
            if len (markeringen) > 0:
                bufferSet = GeoManipulatie.GeoData ()
                bufferSet.Dimensie = dimensie
                bufferSet.Locaties = markeringen
                symNaam = self.VoegWijzigMarkeringToe (dimensie, True)
                kaart.VoegLaagToe ("Markering waar revisies gevonden zijn", self.VoegGeoDataToe (bufferSet), symNaam, True, True)

        for dimensie, markeringen in self._Wijzigingen.Markering.items ():
            # Markeringen voor de wijzigingen
            if len (markeringen) > 0:
                bufferSet = GeoManipulatie.GeoData ()
                bufferSet.Dimensie = dimensie
                bufferSet.Locaties = markeringen
                symNaam = self.VoegWijzigMarkeringToe (dimensie)
                kaart.VoegLaagToe ("Markering waar wijzigingen gevonden zijn", self.VoegGeoDataToe (bufferSet), symNaam, True, True)

        kaart.Toon ()

#======================================================================
#
# Toon d eresultaten
#
#======================================================================

    #------------------------------------------------------------------
    #
    # Toon de was/wordt locaties die hernoemd zouden moeten/kunnen worden
    #
    #------------------------------------------------------------------
    def _ToonOvereenkomstigeLocaties (self, wasIdvoorwordtId : Dict[str,List[str]]):
        self.Log.Informatie ('Presenteer overeenkomstige basisgeometrie-IDs van locaties')
        self.Generator.VoegHtmlToe ('''<p>Er zijn locaties in de was- en wordt-versie van het GIO waarvan de geometrieën
binnen de juridische nauwkeurigheid met elkaar overeenkomen. Omdat de basisgeometrie-ID van de locaties niet met elkaar overeenkomen,
moet aangenomen worden dat de geometrieën toch van elkaar verschillen (want de geo-tools voeren geen vergelijking van
geometrieën uit). Het advies is om de locaties in de wordt-versie te vervangen door de locaties uit de was-versie,
zodat deze revisie niet meer nodig is. Of om, als de naam van de locatie wel moet wijzigen, dezelfde basisgeometrie-IDs
te gebruiken in beide versies.</p>
<p>In onderstaand tekstvak staat per basisgeometrie-ID van de locaties in de wordt-versie
aangegeven de basisgeometrie-ID van dw corresponderende locatie(s) uit de was-versie.</p>''')
        self._ToonResultaatInTekstvak (json.dumps (wasIdvoorwordtId, indent=4), 'Te_vervangen_locaties.json', 'json')
        self.Generator.VoegHtmlToe ('''
<p>Deze locaties zijn opgenomen in GIO-wijziging als revisies.</p>''')

    #------------------------------------------------------------------
    #
    # Maak en toon de GIO-wijziging
    #
    #------------------------------------------------------------------
    def _ToonGIOWijziging (self):
        self.Log.Detail ("Maak en presenteer de GIO-wijziging")
        if self.Request.IsOnlineOperatie:
            self.Generator.VoegHtmlToe ('<form id="upload_form" action="toon_gio_wijziging" method="post" enctype="multipart/form-data">')
        self.Generator.VoegHtmlToe ('''
<p>De GIO-wijziging is een GML bestand waarin de vaststellingscontext nog aangepast moet worden:</p>''')

        wijzigingGML = self.SchrijfGIOWijziging (self._Wijziging)

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

        if self.Request.IsOnlineOperatie:
            self.Log.Detail ("Neem was-GML en smbolisatie op in form")
            self._ToonResultaatInTekstvak (self._WasGML, None, None, "was", False)
            if self._SymbolisatieXML is None:
                self._ToonResultaatInTekstvak (self._SymbolisatieXML, None, None, "symbolisatie", False)
            self.Generator.VoegHtmlToe ('''
<p>Het tonen van de GIO-wijziging wordt door een andere webpagina verzorgd:</p>
<input type="submit" value ="Toon gio-wijziging"/>
</form>''')
