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

from typing import List, Dict, Tuple

import json
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
        # Naam om de was-data in de kaart te tonen
        self._WasDataNaam : str = None
        # Wordt-versie van de GIO
        self._Wordt : GeoManipulatie.GeoData = None
        # Naam om de wordt-data in de kaart te tonen
        self._WordtDataNaam : str = None
        # Naam waaronder de te gebruiken symbolisatie voor zowel de was- als wordt-versie is geregistreerd
        self._SymbolisatieNaam : str = None
        # Gegevens waaruit de GIO-wijziging wordt samengesteld
        self._Wijzigingen = GIOWijzigingMaker.Wijzigingen ()
        # Executietijd voor de analyse van manifest ongewijzigde geometrie-locaties
        self._Tijd_ViaID = None
        # Executietijd voor de analyse van de overige locaties
        self._Tijd_GeoAnalyse = None
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

    def _VoerUit (self, titelBepaling = "Bepaling GIO wijziging"):
        """Voer het request uit"""
        if not self._LeesBestandenEnSpecificatie  ():
            return False

        einde = self.Generator.StartSectie ("<h3>" + titelBepaling + "</h3>", True)
        if self.Request.LeesString ("beschrijving"):
            self.Generator.VoegHtmlToe ('<p>' + self.Request.LeesString ("beschrijving") + '</p>') 

        self._InitialiseerWebpagina ()
        self.Generator.LeesCssTemplate ('resultaat')
        symbolisatie = self.Request.LeesBestand (self.Log, "symbolisatie", False)
        self._SymbolisatieNaam = self.VoegDefaultSymbolisatieToe (self._Was) if symbolisatie is None else self.VoegSymbolisatieToe (symbolisatie)

        self._BepaalWijzigingen ()

        self.Generator.VoegHtmlToe (einde)

        if len (self._Wijzigingen.OngewijzigdeGeometrie) > 0:
            einde = self.Generator.StartSectie ("Basisgeometrie-IDs", True)
            self._ToonOngewijzigdeGeometrie ()
            self.Generator.VoegHtmlToe (einde)
            
        einde = self.Generator.StartSectie ("GIO-Wijziging", True)
        self.Generator.VoegHtmlToe ("... GML nog maken...")
        self.Generator.VoegHtmlToe (einde)

        return True


    def _LeesBestandenEnSpecificatie (self):
        """Lees de specificatie en GIO's en valideeer de invoer"""
        succes = True

        valideerGIOs = True
        if self._Was is None:
            self.Log.Informatie ("Lees de was-versie van de GIO")
            self._Was = self.LeesGeoBestand ('was', True)
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

        if self._Symbolisatie is None:
            self.Log.Informatie ("Lees de symbolisatie (indien aanwezig)")
            self._Symbolisatie = self.Request.LeesBestand (self.Log, "symbolisatie", False)
            if not self._Symbolisatie is None:
                self.Log.Detail ('Symbolisatie ingelezen')

        if self.Request.LeesString ('nauwkeurigheid') is None:
            self.Log.Fout ("De nauwkeurigheid is niet opgegeven in de specificatie")
            succes = False

        return succes

#======================================================================
#
# Bepaling van wijzigingen tussen twee GIO's
#
#======================================================================
    class Wijzigingen:

        def __init__ (self):
            # De locaties uit de was-versie die in de GIO-wijziging opgenomen moet worden
            self.WasLocaties = []
            # De locaties uit de wordt-versie die in de GIO-wijziging opgenomen moet worden
            self.WordtLocaties = []
            # De basisgeometrie-ID van een locatie uit de wordt-versie (key) waarvan alle geometrieën met bijbehorende
            # attribuutwaarde corresponderen met een onveranderde (binnen de nauwkeurigheid) geometrie van de 
            # was-versie. De value zijn de basisgeometrie-ID van de locatie(s) uit de was-versie.
            # De manifest ongewijzigde geometrieën zijn hierin niet opgenomen
            self.OngewijzigdeGeometrie : Dict[str,List[str]] = {}
            # De juridisch ongewijzigde locaties in de wordt-versie die een revisie 
            # zijn van de locaties in de was-versie, d.w.z. alleen van naam verschillen.
            self.WordtRevisies = []
            # De gedetecteerde wijzigingen. Dit zijn ofwel gebieden ofwel punten.
            self.Markering = GeoManipulatie.GeoData ()

    def _BepaalWijzigingen (self) -> Wijzigingen:
        """Bepaal de wijzigingen tussen twee versies van een GIO"""
        self.Generator.VoegHtmlToe ('''<p>Voor de bepaling van een GIO-wijziging wordt de elders beschreven <a href="@@@GeoTools_Url@@@wiki/Maak-gio-wijziging" target="_blank">procedure</a> gevolgd.
In onderstaande kaart wordt links de was-versie, rechts de wordt-versie van de GIO getoond.
Beweeg de schuif om meer of minder van elke versie te zien. Klik op een ''' + self._Was.GeometrieNaam (False) + ' voor aanvullende details</p>\n')
        self._WasDataNaam = self.VoegGeoDataToe (self._Was)
        self._WordtDataNaam = self.VoegGeoDataToe (self._Wordt)
        self.ToonKaart ('kaart.VoegOudLaagToe ("Was-versie", "' + self._WasDataNaam + '", "' + self._SymbolisatieNaam + '").VoegNieuwLaagToe ("Wordt-versie", "' + self._WordtDataNaam + '", "' + self._SymbolisatieNaam + '");')

        self._WasLocaties = { locatie['properties']['id'] : locatie for locatie in self._Was.Locaties}
        self._WordtLocaties = { locatie['properties']['id'] : locatie for locatie in self._Wordt.Locaties}
        numLocaties = len (self._WasLocaties) + len (self._WordtLocaties)
        self._ManifestOngewijzigdeGeometrieen ()

        analyseLocaties = len (self._ResterendWas.Locaties) + len (self._ResterendWordt.Locaties)
        if analyseLocaties > 0:
            wasGeometrieen, isMulti = self.MaakLijstVanGeometrieen (self._ResterendWas)
            wordtGeometrieen, isMulti2 = self.MaakLijstVanGeometrieen (self._ResterendWordt)
            if self._Was.Dimensie == 0:
                self._AnalyseerPunten (wasGeometrieen, wordtGeometrieen, isMulti or isMulti2)

        self.Generator.VoegHtmlToe ('<p>Alle (' + str(numLocaties) + ') locaties zijn hiermee verwerkt. ')
        if not self._Tijd_ViaID is None:
            self.Generator.VoegHtmlToe ('Het bepalen van de wijzigingen op basis van de basisgeometrie-IDs die in beide GIO-versies voorkomen nam ' + '{.3f}'.format (self._Tijd_ViaID) + 's voor ' + str(numLocaties - analyseLocaties) + ' locaties. ')
        if not self._Tijd_GeoAnalyse is None:
            self.Generator.VoegHtmlToe ('Het bepalen van de wijzigingen op basis van een geo-analyse nam ' + '{.3f}'.format (self._Tijd_GeoAnalyse) + 's voor ' + str(analyseLocaties) + ' locaties.')
        self.Generator.VoegHtmlToe ('</p>\n')

    #------------------------------------------------------------------
    #
    # Verwerk persistente ID: basisgeo-ID die zowel in de was-
    # als wordt-versie voorkomen.
    #
    #------------------------------------------------------------------
    def _ManifestOngewijzigdeGeometrieen (self):
        self.Log.Informatie ('Onderzoek de locaties met manifest ongewijzigde geometrieën')

        tijd_start = self.Log.Tijd ()

        # Bepaal of en hoe de locaties met manifest ongewijzigde geometrie muteren
        manifestOngewijzigdId = set ()
        ongewijzigd = []
        for wasId, wasLocatie in self._WasLocaties.items ():
            wordtLocatie = self._WordtLocaties.get (wasId)
            if not wordtLocatie is None:
                manifestOngewijzigdId.add (wasId)

                isGewijzigd = False if self._Was.AttribuutNaam is None else bool (wasLocatie['properties'][self._Was.AttribuutNaam] != wordtLocatie['properties'][self._Was.AttribuutNaam])
                if isGewijzigd:
                    self._Wijzigingen.WasLocaties.append (wasLocatie)
                    self._Wijzigingen.WordtLocaties.append (wordtLocatie)
                    self._Wijzigingen.Markering.Locaties.extend (self.SplitsMultiGeometrie (wasLocatie))

                elif wasLocatie['properties'].get ('naam') != wordtLocatie['properties'].get ('naam'):
                    self._Wijzigingen.WordtRevisies.append (wordtLocatie)
                else:
                    ongewijzigd.append (wasLocatie)

        # De overgebleven locaties zijn:
        self._ResterendWas = GeoManipulatie.GeoData () 
        self._ResterendWas.Attributen = self._Was.Attributen
        self._ResterendWas.Locaties = [l for l in self._Was.Locaties if not l['properties']['id'] in manifestOngewijzigdId]

        self_ResterendWordt = GeoManipulatie.GeoData () 
        self_ResterendWordt.Attributen = self._Was.Attributen
        self_ResterendWordt.Locaties = [l for l in self._Wordt.Locaties if not l['properties']['id'] in manifestOngewijzigdId]

        if not tijd_start is None:
            self._Tijd_ViaID = self.Log.Tijd () - tijd_start

        # Neem de resultaten van deze stap in de resultaatpagina
        self.Log.Informatie ('Presenteer de resultaten')
        if len (manifestOngewijzigdId) == 0:
            self.Generator.VoegHtmlToe ('''<p>Er zijn geen locaties gevonden met een manifest ongewijzigde geometrie, dus locaties die in de was- en wordt-versie dezelfde basisgeometrie-ID hebben.</p>''')
        else:
            self.Generator.VoegHtmlToe ('<p> Er ' + ('is één locatie' if len(manifestOngewijzigdId) == 1 else 'zijn ' + str(len(manifestOngewijzigdId)) + ' locaties') + '''gevonden 
met een manifest ongewijzigde geometrie, dus locaties die in de was- en wordt-versie dezelfde basisgeometrie-ID hebben:
<ul>''')
            if not self._Was.AttribuutNaam is None:
                self.Generator.VoegHtmlToe ('<li>' + str(len(self._Wijzigingen.WasLocaties)) + ' met een gewijzigde ' + self._Was.AttribuutNaam + ';</li>')
            self.Generator.VoegHtmlToe ('<li>' + str(len(self._Wijzigingen.WordtRevisies)) + ''' met een gewijzigde naam;</li>
<li>''' + str(len (ongewijzigd)) + ''' ongewijzigd</li></ul>
In onderstaande kaart zijn deze locaties opgenomen.
</p>\n''')
            kaartScript = ''
            if len (ongewijzigd) > 0:
                dataSet = GeoManipulatie.GeoData () 
                dataSet.Attributen = self._Was.Attributen
                dataSet.Locaties = ongewijzigd
                kaartScript += 'kaart.VoegOnderlaagToe ("Juridisch ongewijzigd", "' + self.VoegGeoDataToe (dataSet) + '", "' + self._SymbolisatieNaam + '", true, true);'

            if len (self._Wijzigingen.Markering.Locaties) > 0:
                kvSym = self.VoegUniformeSymbolisatieToe (self._Was.Dimensie, "#D80073", "#A50040")
                kaartScript += 'kaart.VoegOnderlaagToe ("Gewijzigd (exclusief revisies)", "' + self.VoegGeoDataToe (self._Wijzigingen.Markering) + '", "' + kvSym + '", true, true);'

            if len (self._Wijzigingen.WordtRevisies) > 0:
                dataSet.Attributen = {}
                dataSet.Locaties = self._Wijzigingen.WordtRevisies
                kvSym = self.VoegUniformeSymbolisatieToe (self._Was.Dimensie, "#DAE8FC", "#6C8EBF")
                kaartScript += 'kaart.VoegOnderlaagToe ("Revisies", "' + self.VoegGeoDataToe (dataSet) + '", "' + kvSym + '", true, true);'

            if len (self._ResterendWas.Locaties) > 0 or len (self_ResterendWordt.Locaties) > 0:
                self._ResterendWas = self.VoegGeoDataToe (self._ResterendWas)
                self._ResterendWordtNaam = self.VoegGeoDataToe (self_ResterendWordt)
                kaartScript += 'kaart.VoegOudLaagToe ("Nog te analyseren geometrieën", "' + self._ResterendWas + '", "' + self._SymbolisatieNaam + '", true, true).VoegNieuwLaagToe ("Nog te analyseren geometrieën", "' + self._ResterendWordtNaam + '", "' + self._SymbolisatieNaam + '", true, true);'

            self.ToonKaart (kaartScript)

    #------------------------------------------------------------------
    #
    # Verwerk de punten voor locaties zonder manifest ongewijzigde
    # geometrie.
    #
    #------------------------------------------------------------------
    def _AnalyseerPunten (self, wasGeometrieen : List[GeoManipulatie.EnkeleGeometrie], wordtGeometrieen : List[GeoManipulatie.EnkeleGeometrie], heeftMultiGeometrie : bool):
        self.Log.Informatie ('Onderzoek de overige punt-locaties')
        drempel = self.NauwkeurigheidInMeter ()
        drempel *= drempel

        tijd_start = self.Log.Tijd ()

        # Vind alle punten die te dicht bij een ander punt liggen
        gewijzigdeWasId = set () # ID van was-locaties waarvan tenminste een punt wordt gemuteerd
        gewijzigdeWordtId = set () # ID van was-locaties waarvan tenminste een punt wordt gemuteerd
        wijzigmarkeringen = [] # Apart houden voor weergave later
        for i in range (0, len (wasGeometrieen)):
            was_geom = wasGeometrieen[i]
            was_coord = was_geom.Geometrie['geometry']['coordinates']

            wasIsGemuteerd = True
            for j in range (0, len (wordtGeometrieen)):
                wordt_geom = wordtGeometrieen[j]
                if wordt_geom is None:
                    continue

                wordt_coord = wordt_geom.Geometrie['geometry']['coordinates']
                afstand = (was_coord[0] - wordt_coord[0]) * (was_coord[0] - wordt_coord[0]) + (was_coord[1] - wordt_coord[1]) * (was_coord[1] - wordt_coord[1])

                if afstand < drempel:
                    # Dit moeten corresponderende geometrieën zijn
                    if was_geom.Attribuutwaarde == wordt_geom.Attribuutwaarde and was_geom.Locatie['properties'].get('naam') == wordt_geom.Locatie['properties'].get('naam'):
                        # Ook de naam en de groepID/normwaarde komen overeen
                        lijst = self._Wijzigingen.OngewijzigdeGeometrie.get (wordt_geom.ID)
                        if lijst is None:
                            self._Wijzigingen.OngewijzigdeGeometrie[wordt_geom.ID] = lijst = [was_geom.ID]
                        else:
                            lijst.append (was_geom.ID)
                        # Niet nodig om verder te kijken; er kan er maar 1 zijn anders waren de GIO-versies ongeschikt
                        wasIsGemuteerd = False
                    else:
                        # De groepID/normwaarde komen niet overeen, dus er is toch sprake van een mutatie
                        # Omdat we niet zeker weten of de geometrieën exact hetzelfde zijn, kan alleen een verandering van de naam niet tot een revisie leiden.
                        gewijzigdeWordtId.add (wordt_geom.ID)
                        wijzigmarkeringen.append (wordt_geom.Geometrie)

                    wordtGeometrieen[j] = None # Deze geometrie is uitgeanalyseerd.
                    break # De was-geometrie ook

                if wasIsGemuteerd:
                    # Deze was heeft geen matching wordt
                    gewijzigdeWasId.add (was_geom.ID)
                    wijzigmarkeringen.append (was_geom.Geometrie)

        for wordt_geom in wordtGeometrieen:
            if not wordt_geom is None:
                # Deze wordt heeft geen matching was
                gewijzigdeWordtId.add (wordt_geom.ID)
                wijzigmarkeringen.append (wordt_geom.Geometrie)
        if heeftMultiGeometrie:
            self._VerifieerOngewijzigdeGeometrie (gewijzigdeWasId, gewijzigdeWordtId)

        # Werk de wijzigingen bij
        self._Wijzigingen.WasLocaties.extend (self._WasLocaties[i] for i in gewijzigdeWasId)
        self._Wijzigingen.WordtLocaties.extend (self._WordtLocaties[i] for i in gewijzigdeWordtId)
        self._Wijzigingen.Markering.Locaties.extend (wijzigmarkeringen)

        if not tijd_start is None:
            self._Tijd_GeoAnalyse = self.Log.Tijd () - tijd_start

        # Toon het resultaat
        self._ToonGeoAnalyseResultaat (wijzigmarkeringen, 0)

    #------------------------------------------------------------------
    #
    # Kijk voor revisies in corresponderende geometrieën, als tenmiste
    # alle geometrieën van een multi-geometrie ongewijzigd zijn
    #
    #------------------------------------------------------------------
    def _VerifieerOngewijzigdeGeometrie (self, gewijzigdeWasId : set, gewijzigdeWordtId : set):
        # Bij gebruik van multi-geometrieën kan het voorkomen dat er was-wordt paren in OngewijzigdeGeometrie
        # staan (corresponderende geometrieën) terwijl andere geometrieën wel gewijzigd zijn
        while True:
            verwijderWordtId = set ()
            for wordtId, wasIds in self._Wijzigingen.OngewijzigdeGeometrie.items ():
                if wordtId in gewijzigdeWordtId:
                    verwijderWordtId.add (wordtId)
                    for wasId in wasIds:
                        gewijzigdeWasId.add (wasId)
                else:
                    for wasId in wasIds:
                        if wasId in gewijzigdeWasId:
                            gewijzigdeWordtId.add (wordtId)
                            for w in wasIds:
                                gewijzigdeWasId.add (w)
                            verwijderWordtId.add (wordtId)
                            break
            if len (verwijderWordtId) == 0:
                break
            for wordtId in verwijderWordtId:
                self._Wijzigingen.OngewijzigdeGeometrie.pop (wordtId)

    #------------------------------------------------------------------
    #
    # Toon de uitkomst van de geo-analyses op de kaart
    #
    #------------------------------------------------------------------
    def _ToonGeoAnalyseResultaat (self, wijzigmarkeringen, dimensieMarkeringen):
        self.Log.Informatie ('Presenteer de resultaten')
        if len (wijzigmarkeringen) == 0:
            self.Generator.VoegHtmlToe ('''<p>Er zijn geen locaties gevonden met een gewijzigde geometrie, groepID, normwaarde en/of naam.</p>''')
        else:
            self.Generator.VoegHtmlToe ('<p> Er ' + ('is één plaats' if len(wijzigmarkeringen) == 1 else 'zijn ' + str(len(wijzigmarkeringen)) + ' plaatsen') + '''gevonden 
waar er iets is gewijzigd (geometrie, groepID, normwaarde en/of naam).
In onderstaande kaart worden deze plaatsen getoond.</p>\n''')
            kaartScript = ''
            dataSet = GeoManipulatie.GeoData ()
            dataSet.Locaties = wijzigmarkeringen
            kvSym = self.VoegUniformeSymbolisatieToe (dimensieMarkeringen, "#D80073", "#A50040")
            kaartScript = 'kaart.VoegToplaagToe ("Posities van wijzigingen", "' + self.VoegGeoDataToe (dataSet) + '", "' + kvSym + '", true, true);'
            kaartScript += 'kaart.VoegOudLaagToe ("Geanalyseerde geometrieën", "' + self._ResterendWasDataNaam + '", "' + self._SymbolisatieNaam + '", true, true).VoegNieuwLaagToe ("Geanalyseerde geometrieën", "' + self._ResterendWordtDataNaam + '", "' + self._SymbolisatieNaam + '", true, true);'

            self.ToonKaart (kaartScript)

    #------------------------------------------------------------------
    #
    # Toon de OngewijzigdeGeometrie
    #
    #------------------------------------------------------------------
    def _ToonOngewijzigdeGeometrie (self):
        self.Log.Informatie ('Presenteer de basisgeometrie-ID bevindingen')
        self.Generator.VoegHtmlToe ('''<p>De was-versie bevat geometrieën die binnen de marge van de teken-nauwkeurigheid overeenkomen
met geometrieën in de wordt-versie. Het is bovendien zo dat alle geometrieën uit de was-versie overeenkomen met locaties die verder
geen mutaties bevat, idem voor de geometrieën uit de wordt-versie. In onderstaand tekstvak staat per basisgeometrie-ID van de locaties in de wordt-versie
aangegeven de basisgeometrie-ID van dw corresponderende locatie(s) uit de was-versie.</p>\n<textarea>\n''')
        self.Generator.VoegHtmlToe (json.dumps (self._Wijzigingen.OngewijzigdeGeometrie, indent=4))
        self.Generator.VoegHtmlToe ('''\n</textarea>
<p>Deze locaties zijn niet opgenomen in GIO-wijziging.</p>''')

