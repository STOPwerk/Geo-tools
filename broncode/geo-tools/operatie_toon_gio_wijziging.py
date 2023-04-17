#======================================================================
#
# /toon_gio_wijziging
#
#======================================================================
#
# Script om een GIO-wijziging samen met een was- en een wordt-versie 
# van het GIO te tonen in een viewer. De wordt-versie wordt afgeleid
# uit de wijziging en was-versie.
#
#======================================================================

from applicatie_meldingen import Meldingen
from applicatie_operatie import Operatie
from applicatie_request import Parameters
from data_geodata import GeoData, GIODeel
from weergave_kaart import KaartGenerator
from weergave_webpagina import WebpaginaGenerator

class ToonGIOWijziging (Operatie):
#======================================================================
#
# Webpagina's
#
#======================================================================
#region Webpagina's
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("Tonen van een GIO-wijziging")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters, log: Meldingen = None):
        return ToonGIOWijziging (request, log).VoerUit ()
#endregion

#======================================================================
#
# Implementatie
#
#======================================================================
#region Implementatie
    def __init__(self, request : Parameters, log: Meldingen, defaultTitel = None, titelBijFout = None):
        super ().__init__ (request, log, "GIO-wijziging in beeld" if defaultTitel is None else defaultTitel, "GIO-wijziging - geen beeld" if titelBijFout is None else titelBijFout)
        # Was-versie van de GIO
        self._Was : GeoData = None
        # De resulterende GIO-wijziging
        self._Wijziging : GeoData = None
        # Wordt-versie van de GIO, gereconstrueerd uit de was en de GIO-wijziging
        self._Wordt : GeoData = None

    def _VoerUit (self, titelOperatie : str = None):
        """Voer het request uit"""
        if not self._LeesBestandenEnSpecificatie  ():
            return False
        if not self._MaakWordtVersie ():
            return False

        eindeSectie = self.Generator.StartSectie ("Weergave van de GIO-wijziging" if titelOperatie is None else "<h3>" + titelOperatie + "</h3>", True)
        if self.Request.LeesString ("beschrijving"):
            self.Generator.VoegHtmlToe ('<p>' + self.Request.LeesString ("beschrijving") + '</p>') 
        self._ToonGIOWijziging ()

        einde = self.Generator.StartSectie ("Reconstructie van de wordt-versie", False)
        self._ToonWordtVersie ()
        self.Generator.VoegHtmlToe (einde);

        self.Generator.VoegHtmlToe (eindeSectie);

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
            if self._Was.Soort != GeoData.SOORT_GIOVersie:
                self.Log.Fout ("Het bestand bevat geen GIO maar: " + self._Was.Soort)
                succes = False
                valideerGIOs = False

        if self._Wijziging is None:
            self.Log.Informatie ("Lees de GIO-wijziging")
            self._Wijziging = self.LeesGeoBestand ('wijziging', True)
            if self._Wijziging is None:
                return False
            if self._Wijziging.Soort != 'GIO-wijziging':
                self.Log.Fout ("Het bestand bevat geen GIO-wijziging maar: " + self._Wordt.Soort)
                succes = False
                valideerGIOs = False

        if valideerGIOs:
            if self._Was.ExpressionId != self._Wijziging.Was.ExpressionId:
                self.Log.Fout ("De was-versie heeft een andere expression-identificatie dan het origineel van de GIO-wijziging")
                succes = False
            if self._Was.AttribuutNaam != self._Wijziging.AttribuutNaam:
                self.Log.Fout ("De was-versie en GIO-wijziging moeten allebei uitsluitend geometrie, GIO-delen of normwaarden hebben")
                succes = False
            self._InitSymbolisatieNamen ([self._Was, self._Wijziging.Wordt, self._Wijziging.WordtRevisies])

        return succes
#endregion

#======================================================================
#
# Reconstructie van de wordt-versie
#
#======================================================================
#region Reconstructie van de wordt-versie
    def _MaakWordtVersie (self):
        succes = True

        self._Wordt = GeoData ()
        self._Wordt.Soort = GeoData.SOORT_GIOVersie
        self._Wordt.WorkId = self._Wijziging.WorkId
        self._Wordt.ExpressionId = self._Wijziging.Wordt.ExpressionId
        self._Wordt.Attributen = self._Wijziging.Wordt.Attributen
        self._Wordt.AttribuutNaam = self._Wijziging.Wordt.AttribuutNaam
        self._Wordt.EenheidID = self._Wijziging.EenheidID
        self._Wordt.EenheidLabel = self._Wijziging.EenheidLabel
        self._Wordt.NormID = self._Wijziging.NormID
        self._Wordt.NormLabel = self._Wijziging.NormLabel
        if not self._Wijziging.GIODelen is None:
            self._Wordt.GIODelen = { i : GIODeel(i, g.Label) for i, g in self._Was.GIODelen.items () }
            for i, g in self._Wijziging.GIODelen.items ():
                if g.WijzigActie == GIODeel._WIJZIGACTIE_VERWIJDER:
                    del self._Wordt.GIODelen[i]
                elif g.WijzigActie == GIODeel._WIJZIGACTIE_VOEGTOE:
                    self._Wordt.GIODelen[i]= GIODeel(i, g.Label)
        self._Wordt.JuridischeNauwkeurigheid = self._Wijziging.JuridischeNauwkeurigheid

        wordtLocaties = {locatie['properties']['id'] : (dimensie, locatie) for dimensie, locaties in self._Was.Locaties.items () for locatie in locaties}

        for locaties in self._Wijziging.Was.Locaties.values ():
            for locatie in locaties:
                if wordtLocaties.pop (locatie['properties']['id'], None) is None:
                    self.Log.Fout ("GIO-wijziging verwijdert een locatie met basisgeometrie-ID '" + locatie['properties']['id'] + "' die niet voorkomt in de originele versie")
                    succes = False

        for locaties in self._Wijziging.WordtRevisies.Locaties.values ():
            for locatie in locaties:
                if wordtLocaties.pop (locatie['properties']['id'], None) is None:
                    self.Log.Fout ("GIO-wijziging reviseert een locatie met basisgeometrie-ID '" + locatie['properties']['id'] + "' die niet voorkomt in de originele versie")
                    succes = False

        toegevoegd = set ()
        for dimensie, locaties in self._Wijziging.Wordt.Locaties.items ():
            for locatie in locaties:
                wordt_id = locatie['properties']['id']
                if wordt_id in toegevoegd:
                    self.Log.Fout ("GIO-wijziging bevat twee toegevoegde locaties met basisgeometrie-ID '" + wordt_id + "'")
                    succes = False
                elif wordt_id in wordtLocaties:
                    self.Log.Fout ("GIO-wijziging voegt een locatie toe met basisgeometrie-ID '" + locatie['properties']['id'] + "' die al voorkomt in de originele versie en niet verwijderd is")
                    succes = False
                else:
                    toegevoegd.add (wordt_id)
                    wordtLocaties[wordt_id] = (dimensie, locatie)

        for dimensie, locaties in self._Wijziging.WordtRevisies.Locaties.items ():
            for locatie in locaties:
                wordt_id = locatie['properties']['id']
                if wordt_id in toegevoegd:
                    self.Log.Fout ("GIO-wijziging reviseert een locaties toe met basisgeometrie-ID '" + wordt_id + "' die dubbel in de GIO-wijziging voorkomt (als voegtoe en/of reviseer)")
                    succes = False
                else:
                    toegevoegd.add (wordt_id)
                    wordtLocaties[wordt_id] = (dimensie, locatie)

        for dimensie, locatie in wordtLocaties.values ():
            if dimensie in self._Wordt.Locaties:
                self._Wordt.Locaties[dimensie].append (locatie)
            else:
                self._Wordt.Locaties[dimensie] = [locatie]

        return succes

    def _ToonWordtVersie (self):
        self.Generator.VoegHtmlToe ('''<p>Door combinatie van de originele GIO-versie en de GIO-wijziging kan de nieuwe versie gereconstrueerd worden.
De volgorde van de Locaties in het GIO hoeft niet overeen te komen met de volgorde in de GIO-versie die voor de bepaling van de GIO-wijziging
is gebruikt, of (voor de behouden locaties) voor de locaties in de originele GIO-versie.</p>''')
        gml = self._Wordt.SchrijfGIO ()
        self._ToonResultaatInTekstvak (gml, 'Wordt_versie.gml', 'xml')
#endregion

#======================================================================
#
# Weergave van de GIO-wijziging
#
#======================================================================
    def _ToonGIOWijziging (self):
        self.Generator.VoegHtmlToe ('''<p>Net als bij tekst-renvooi geeft de geo-renvooi aan <i>waar</i> de verschillen te vinden zijn.
<i>Wat</i> de verschillen zijn blijkt uit de vergelijking van de originele en nieuwe versie. De aandacht wordt meteen op de verschillen
gevestigd door de niet-gewijzigde of gereviseerde kleinste eenheden van mutatie (GIO-locaties) weg te laten. Om de wijzigingen in hun context
te zien moeten ook de niet-gewijzigde locaties te zien zijn, als de eindgebruiker daarom vraagt.</p>
<p>De geometrieën die altijd in beeld zijn maar die geen geo-renvooi markering hebben zijn ofwel onderdeel van een GIO-locatie met een geometrie 
die wel een geo-renvooi markering heeft, of zijn gewijzigd op een manier die de geldigheid van de juridische regels niet verandert. Bijvoorbeeld 
omdat een grens tussen twee gebieden is aangepast.</p>
<p>Wat wel verschilt van de tekst-renvooi is dat de kaart zover uitgezoomd is dat sommige verschillen niet zichtbaar zijn.
Bij het tonen van de GIO-wijziging moet daarom via schaalafhankelijke markeringen ervoor gezorgd worden dat er geen wijzigingen buiten beeld raken.</p>''')

        self.Log.Detail ("Toon de onderdelen van de GIO-wijziging in een kaart")
        kaart = KaartGenerator.Kaart (self.Kaartgenerator)

        # Voeg de ongewijzigde locaties toe
        mutatie_id = set (locatie['properties']['id'] for locaties in self._Wijziging.Was.Locaties.values () for locatie in locaties)
        ongewijzigd = GeoData ()
        ongewijzigd.Attributen = self._Was.Attributen
        ongewijzigd.Locaties = { dimensie : [locatie for locatie in locaties if not locatie['properties']['id'] in mutatie_id] for dimensie, locaties in self._Was.Locaties.items () }
        namen_was = self.Kaartgenerator.VoegGeoDataToe (ongewijzigd)
        mutatie_id = set (locatie['properties']['id'] for locaties in self._Wijziging.Wordt.Locaties.values () for locatie in locaties)
        ongewijzigd = GeoData ()
        ongewijzigd.Attributen = self._Wordt.Attributen
        ongewijzigd.Locaties = { dimensie : [locatie for locatie in locaties if not locatie['properties']['id'] in mutatie_id] for dimensie, locaties in self._Wordt.Locaties.items () }
        namen_wordt = self.Kaartgenerator.VoegGeoDataToe (ongewijzigd)
        kaart.VoegLagenToe ('Ongewijzigd/gereviseerd', namen_was, self._SymbolisatieNamen, True, False, postLaag = lambda _: kaart.LaatsteLaagAlsOud ())
        kaart.VoegLagenToe ('Ongewijzigd/gereviseerd', namen_wordt, self._SymbolisatieNamen, True, False, postLaag = lambda _: kaart.LaatsteLaagAlsNieuw ())

        # Voeg de gewijzigde locaties toe
        namen_was = self.Kaartgenerator.VoegGeoDataToe (self._Wijziging.Was)
        namen_wordt = self.Kaartgenerator.VoegGeoDataToe (self._Wijziging.Wordt)
        kaart.VoegLagenToe ('GIO-wijziging', namen_was, self._SymbolisatieNamen, False, postLaag = lambda _: kaart.LaatsteLaagAlsOud ())
        kaart.VoegLagenToe ('GIO-wijziging', namen_wordt, self._SymbolisatieNamen, False, postLaag = lambda _: kaart.LaatsteLaagAlsNieuw ())

        # Voeg de wijzigmarkeringen toe
        if not self._Wijziging.WijzigMarkering is None:
            schaalafhankelijk = self.Kaartgenerator.MaakSchaalafhankelijkeGeometrie (self._Wijziging.WijzigMarkering, 'Wijzigmarkering', True)
            symbolisatie = {d: self.Kaartgenerator.VoegWijzigMarkeringToe (d, False) for d in [0,1,2]}
            self.Kaartgenerator.VoegSchaalafhankelijkeLocatiesToe (kaart, schaalafhankelijk, symbolisatie)
            self.Kaartgenerator.VoegSchaalafhankelijkeMarkeringenToe (kaart, schaalafhankelijk, symbolisatie[0])

        kaart.Toon ()
