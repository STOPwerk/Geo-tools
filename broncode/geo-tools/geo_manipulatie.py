#======================================================================
#
# Gemeenschappelijke code voor alle geo-gerelateerde operaties
# en weergave van geo-informatie.
#
#======================================================================

from typing import List

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
	def __init__ (self, titel, titelBijFout, request : Parameters, log: Meldingen = None):
		"""Maak een instantie van de geo-operatie aan

		Argumenten:

		titel str  Titel van de webpagina
		titelBijFout str  Titel van de webpagina als er een fout optreedt en alleen de log getoond wordt
		request Parameters  De parameters vor het web request
		"""
		self._TitelBijFout = titelBijFout
		self.Request = request
		# Meldingen voor de uitvoering van het request
		self.Log = Meldingen (False) if log is None else log
		# Generator om de resultaat-pagina te maken
		self.Generator = WebpaginaGenerator (titel)
		# Status attribuut voor het opnemen van de nodige scripts/css
		# self._WebpaginaKanKaartTonen
		# Status van het toevoegen van de default symbolen
		self._DefaultSymbolenToegevoegd = set ()

	def VoerUit(self):
		"""Maak de webpagina aan"""
		self.Log.Informatie ("Geo-tools (https://github.com/STOPwerk/Geo-tools/) versie 2022-11-28 22:22:02.")
		try:
			# _VoerUit moet in een afgeleide klasse worden geïmplementeerd
			if self._VoerUit ():
				self.Log.Informatie ("De verwerking is voltooid.")
			else:
				self.Log.Fout ("De verwerking is afgebroken.")

			self.Generator.VoegHtmlToe ("<h2>Verslag van de verwerking</h2>")
			self.Log.MaakHtml (self.Generator, None)
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
	class GeoData:
		def __init__(self):
			# Geeft de bron aan: Gebied, GIO of GIO-wijziging
			self.Soort : str = None
			#----------------------------------------------------------
			# Voor een GIO-versie of GIO-wijziging
			#----------------------------------------------------------
			# De work-identificatie van de GIO
			self.WorkId : str = None
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
			# Geeft aan of er een waarde met de locatie geassocieerd is (groepID, normwaarde).
			# Zo nee, dan is dit None. Zo ja, dan staat er de naam van het waarde-element
			self.AttribuutNaam : str = None
			# De locaties/gebieden in in-memory format
			self.Locaties = []
			# De dimensie van de geometrie: 0 = punt, 1 = lijn, 2  = vlak
			self.Dimensie : int = None
			#----------------------------------------------------------
			# Voor een GIO-wijziging
			#----------------------------------------------------------
			# De was-locaties
			self.Was : GeoManipulatie.GeoData = None 
			# De wordt-locaties
			self.Wordt : GeoManipulatie.GeoData = None 
			# De wijzig-markering indien aanwezig
			self.WijzigMarkering : GeoManipulatie.GeoData = None

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
			return self._LeesGeoData (gml)


	def _LeesGeoData (self, gml) -> GeoData:
		"""Lees de GML in als een GIO"""
		# Lees de XML
		try:
			geoXml = ElementTree.fromstring (gml)
		except Exception as e:
			self.Log.Fout ("GML is geen valide XML: " + str(e))
			return
		data = GeoManipulatie.GeoData ()
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

		if succes:
			return data

	def _LeesLocaties (self, data : GeoData, geoXml: Element, locatieElement, labelNamm, attribuutNamen : List[str] = []):
		succes = True
		# Vlaggen om meldingen over geometrie maar 1 keer te doen
		meldID = True
		meldRD = True
		meldGeomeetrie = set ()
		meldDimensie = True
		basisgeo_id = None
		for locatie in [] if geoXml is None else geoXml.findall (locatieElement):
			# Lees de geometrie van een locatie
			geometrie = locatie.find (GeoManipulatie._GeoNS + 'geometrie')
			if not geometrie is None:
				geometrie = geometrie.find (GeoManipulatie._BasisgeoNS + 'Geometrie')
			if not geometrie is None:
				basisgeo_id = geometrie.find (GeoManipulatie._BasisgeoNS + 'id')
				geometrie = geometrie.find (GeoManipulatie._BasisgeoNS + 'geometrie')
				if basisgeo_id is None:
					if meldID:
						meldID = False
						self.Log.Fout ('Basisgeometrie-id is verplicht in een ' + locatieElement)
						succes = False
				else:
					basisgeo_id = basisgeo_id.text
			if geometrie is None:
				self.Log.Fout ('Geometrie ontbreekt in een ' + locatieElement)
				succes = False
				continue
			geometrie = list(geometrie)
			if len(geometrie) == 0:
				self.Log.Fout ('Geometrie ontbreekt in een ' + locatieElement)
				succes = False
				continue
			try:
				geoLocatie = pygml.parse (ElementTree.tostring(geometrie[0]))
			except Exception as e:
				self.Log.Fout ('GML-geometrie kan niet gebruikt worden: ' + str(e))
				succes = False
				continue

			if meldRD:
				isRD = False
				prop = geoLocatie.geometry.get ('crs')
				if not prop is None:
					prop = prop.get ('properties')
					if not prop is None:
						prop = prop.get ('name')
						isRD = prop == 'urn:ogc:def:crs:EPSG::28992'
					geoLocatie.geometry.pop ('crs') # Wordt later op feature collectie niveau toegevoegd
				if not isRD:
					meldRD = False
					self.Log.Fout ('Alleen RD coördinaten (urn:ogc:def:crs:EPSG::28992) zijn toegestaan')
					succes = False

			geoLocatie = {
					'type': 'Feature',
					'geometry': geoLocatie.geometry,
					'properties': { 'id' : basisgeo_id }
				}
			data.Locaties.append (geoLocatie)

			# Kijk naar het type geometrie
			if meldDimensie:
				if geoLocatie['geometry']['type'] in ['Polygon', 'MultiPolygon']:
					dimensie = 2
				elif geoLocatie['geometry']['type'] in ['Point', 'MultiPoint']:
					dimensie = 0
				elif geoLocatie['geometry']['type'] in ['LineString', 'MultiLineString']:
					dimensie = 1
				else:
					if geoLocatie['geometry']['type'] in meldGeomeetrie:
						meldGeomeetrie.add (geoLocatie['geometry']['type'])
						self.Log.Fout ('STOP staat geen geometrie van type ' + geoLocatie['geometry']['type'] + ' toe')
						succes = False
						continue

				if data.Dimensie is None:
					data.Dimensie = dimensie
				elif meldDimensie and data.Dimensie != dimensie:
					meldDimensie = False
					self.Log.Fout ('Deze geo-tools kunnen niet omgaan met een mengsel van punten, lijnen en vlakken')
					succes = False

			# Kijk welke attributen er bij de locatie aanwezig zijn
			elt = locatie.find (GeoManipulatie._GeoNS + labelNamm)
			if not elt is None:
				geoLocatie['properties'][labelNamm] = elt.text
				data.LabelNaam = labelNamm
			elt = locatie.find (GeoManipulatie._GeoNS + labelNamm)
			if not elt is None:
				geoLocatie['properties'][labelNamm] = elt.text
				data.LabelNaam = labelNamm
			for naam in attribuutNamen:
				elt = locatie.find (GeoManipulatie._GeoNS + naam)
				if not elt is None:
					geoLocatie['properties'][naam] = elt.text
					data.AttribuutNaam = naam
					attribuutNamen = [naam]
		return succes

	_GeoNS = '{https://standaarden.overheid.nl/stop/imop/geo/}'
	_BasisgeoNS = '{http://www.geostandaarden.nl/basisgeometrie/1.0}'

	@staticmethod
	def MaakShapelyShape (locatie):
		"""Maak een Shapely shape voor de locatie (als dat niet eerder gebeurd is) en geef die terug.

		Argumenten:

		locatie {}  Een locatie voals die eerder is ingelezen
		"""
		if not '_shape' in locatie:
			locatie['_shape'] = shape (locatie['geometry'])
		return locatie['_shape']

	def VoegGeoDataToe (self, naam: str, locaties):
		"""Voeg de geo-gegevens uit een GIO of gebied toe aan de data beschikbaar in de resultaatpagina;

		Argumenten:

		naam str  De naam can de gegevens die gebruikt wordt om de gegevens aan een kaart te koppelen
		locaties []  Een array van locaties zoals die zijn ingelezen
		"""
		collectie = {
			'type' : 'FeatureCollection',
			'crs': { 'type': 'name', 'properties': { 'name': 'urn:ogc:def:crs:EPSG::28992' } },
			'features' : locaties
		}
		# Bepaal de bounding box van de hele collectie
		bbox = False
		for locatie in locaties:
			locatieBBox = GeoManipulatie.MaakShapelyShape (locatie).bounds
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

		# Voeg toe aan de scripts van de pagina
		self._InitialiseerWebpagina ()
		self.Generator.VoegSlotScriptToe ('\nKaartgegevens.Instantie.VoegDataToe ("' + naam + '",\n' + json.dumps (collectie, cls=_JsonGeoEncoder, ensure_ascii=False) + '\n);\n')

#======================================================================
#
# Symbolisatie
#
#======================================================================
	def VoegDefaultSymbolisatieToe (self, geoData : GeoData) -> str:
		"""Voeg de default symbolisatie toe voor de geodata en geef de naam ervan terug
		
		Argumenten:

		geoData GeoData  Eerdef ingelezen data
		"""
		naam = '@dimensie=' + str(geoData.Dimensie)
		if not naam in self._DefaultSymbolenToegevoegd:
			self._DefaultSymbolenToegevoegd.add (naam)
			if geoData.Dimensie == 0:
				rule = '''
	<Rule>
		<Name>Punt</Name>
		<PointSymbolizer>
			<Name>pv221</Name>
			<Graphic>
				<Mark>
					<WellKnownName>square</WellKnownName>
					<Fill>
						<SvgParameter name="fill">#0000ff</SvgParameter>
						<SvgParameter name="fill-opacity">1</SvgParameter>
					</Fill>
					<Stroke>
						<SvgParameter name="stroke">#999999</SvgParameter>
						<SvgParameter name="stroke-opacity">0</SvgParameter>
						<SvgParameter name="stroke-width">1</SvgParameter>
					</Stroke>
				</Mark>
				<Size>12</Size>
				<Rotation>0</Rotation>
			</Graphic>
		</PointSymbolizer>
	</Rule>'''
			elif geoData.Dimensie == 1:
				rule = '''
	<Rule>
		<Name>Lijn</Name>
		<LineSymbolizer>
			<Name>lm021</Name>
			<Stroke>
				<SvgParameter name="stroke">#0000ff</SvgParameter>
				<SvgParameter name="stroke-opacity">1</SvgParameter>
				<SvgParameter name="stroke-width">3</SvgParameter>
				<SvgParameter name="stroke-linecap">butt</SvgParameter>
			</Stroke>
		</LineSymbolizer>
	</Rule>'''
			elif geoData.Dimensie == 2:
				rule = '''
	<Rule>
		<Name>Vlak</Name>
		<PolygonSymbolizer>
			<Name>vsg120</Name>
			<Fill>
				<SvgParameter name="fill">#0000ff</SvgParameter>
				<SvgParameter name="fill-opacity">0.8</SvgParameter>
			</Fill>
			<Stroke>
				<SvgParameter name="stroke">#0000cd</SvgParameter>
				<SvgParameter name="stroke-opacity">1</SvgParameter>
				<SvgParameter name="stroke-width">3</SvgParameter>
				<SvgParameter name="stroke-linejoin">round</SvgParameter>
			</Stroke>
		</PolygonSymbolizer>
	</Rule>'''

			self.VoegSymbolisatieToe (naam, '''<FeatureTypeStyle version="1.1.0"
	xmlns="http://www.opengis.net/se"
	xmlns:ogc="http://www.opengis.net/ogc">
	<FeatureTypeName>geo:Locatie</FeatureTypeName>
	<SemanticTypeIdentifier>geo:geometrie</SemanticTypeIdentifier>''' + rule + '''
</FeatureTypeStyle>''')
		return naam


	def VoegSymbolisatieToe (self, naam : str, symbolisatie : str):

		# Verwijder <?xml ?> regel indien aanwezig
		symbolisatie = GeoManipulatie._StripHeader.sub ('', symbolisatie)

		# Voeg toe aan de scripts van de pagina
		self._InitialiseerWebpagina ()
		self.Generator.VoegSlotScriptToe ('\nKaartgegevens.Instantie.VoegSymbolisatieToe ("' + naam + '",`' + symbolisatie + '`);\n')

	_StripHeader = re.compile ("^\s*<\?\s*[^>]+>\s*\n")


#======================================================================
#
# Weergave op een kaart
#
#======================================================================
	def ToonKaart (self, kaartElementId : str, kaartClass : str, jsInitialisatie : str):
		"""Toon een kaart op de huidige plaats in de webpagina

		Argumenten:

		kaartElementId str  Naam van het (in dese methode te maken) HTML element waarin de kaart getoond wordt 
		kaartClass str De naam van de klasse van de kaart. Zorg er in de style voor dat het element een breedte en hoogte heeft.
		jsInitialisatie str  Javascript om de kaartlagen aan de kaart toe te voegen. De kaart is beschikbaar als 'kaart' variabele,
		"""
		self._InitialiseerWebpagina ()
		self.Generator.VoegHtmlToe ('<div id="' + kaartElementId + '"')
		if kaartClass:
			self.Generator.VoegHtmlToe (' class="' + kaartClass + '"')
		self.Generator.VoegHtmlToe ('></div>')
		self.Generator.VoegSlotScriptToe ('\nwindow.addEventListener("load", function () {\nvar kaart = new Kaart ();\n' + jsInitialisatie + '\nkaart.Toon ("' + kaartElementId + '");\n});')

	def _InitialiseerWebpagina (self):
		"""Voeg de bestanden toe nodig om OpenLayers kaarten op te nemen in de webpagina
		"""
		if not hasattr (self, '_WebpaginaKanKaartTonen'):
			setattr (self, '_WebpaginaKanKaartTonen', True)
			self.Generator.LeesCssTemplate ('ol')
			self.Generator.LeesJSTemplate ("ol", True, True)
			self.Generator.LeesJSTemplate ("sldreader", True, True)
			self.Generator.LeesJSTemplate ("kaart", True, True)

class _JsonGeoEncoder (json.JSONEncoder):
	def default(self, o):
		"""Objecten worden niet meegenomen"""
		return None

