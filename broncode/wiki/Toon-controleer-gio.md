# Controle op geschiktheid van een GIO

## Doel van de operatie

Controleert dat het GIO geen details bevat die het geautomatiseerd bepalen van de wijzigingen tussen twee GIO-versies in de weg staat. De grens aan de toegestane mate van detaillering wordt gegeven door de teken-nauwkeurigheid. Als een GIO niet geschikt bevonden wordt hoeft dat niet aan de inhoud van het GIO te liggen, het kan ook zijn dat de teken-nauwkeurigheid verkeerd ingeschat is.

Deze geo-tool kan ook gebruikt worden om een STOP gebiedsmarkering of effectgebied te bekijken.

Online: [Tonen/controleren van geo-informatie](@@@GeoTools_Online_Url@@@toon_geo).

Python script: [toon_geo.py](../blob/main/broncode/geo-tools/toon_geo.py) met gebruik making van [geo_manipulatie.py](../blob/main/broncode/geo-tools/geo_manipulatie.py).


## Tekennauwkeurigheid
Een geo-informatieobject (GIO) legt vast waar juridische regels gelden, en geeft eventueel ook een normwaarde voor een locatie. Met de term *teken-nauwkeurigheid* wordt in deze geo-tools de geometrische nauwkeurigheid bedoeld waarmee de locatie door (of in overleg met) de juristen is "ingetekend", hoe "dik" de punten en lijnen zijn. Het is het antwoord op de vraag: hoe ver van de exacte locatie zoals in het GIO is opgenomen zijn nog steeds dezelfde regels van toepassing? Dat zal van de context afhangen. Voor regels over bouwen op een perceel is 1 meter veel en zal een locatie in het GIO de perceelgrenzen tot op een decimeter nauwkeurig volgen. De locaties voor bouwhoogtebeperkingen rond Schiphol zullen niet op een decimeter nauwkeurig bepaald hoven te worden; de teken-nauwkeurigheid kan daar best meters of meer zijn.

In een GIO moet ondubbelzinnig vastgelegd zijn waar de regels en/of normwaarde gelden. Dan verwacht een "lezer" van de geo-informatie dat er geen relevante details zijn die kleiner zijn dan de teken-nauwkeurigheid. Maar ook dat details die kleiner zijn dan de teken-nauwkeurigheid er niet toe doen. De teken-nauwkeurigheid is geen "hard" getal dat onderdeel is van de geo-informatie, meer een leiddraad voor het bevoegd gezag bij het opstellen van het GIO. Het is het geo-equivalent van een schrijfstijl. Als een regeling globale regels bevat dan zullen die niet tot in de kleinste details zijn uitgewerkt. 

Voor het bepalen van de wijzigingen die in de ene versie van het GIO ten opzichte van de voorgaande versie zijn aangebracht kunnen details kleiner den de teken-nauwkeurigheid genegeerd worden. Om dit geautomatiseerd te kunnen doen mogen dergelijke details niet in het GIO voorkomen - de automatisering kan wijzigingen daarin niet detecteren. In onderstaande figuur staat aangegeven wat wel en niet in een GIO mag voorkomen.

![(On)mogelijkheden](Tekennauwkeurigheid.svg)

In woorden:
* Punt-locaties moeten verder dan de teken-nauwkeurigheid uit elkaar liggen (bovenste rij). Punten met een onderlinge afstand kleiner dan de teken-nauwkeurigheid (onderste rij) zijn niet toegestaan.
* Lijn-locaties waarvan de onderlinge afstand groter is dan de teken-nauwkeurigheid (bovenste rij) zijn toegestaan.
* Lijn-locaties mogen geen onderlinge afstand hebben die kleiner is dan de teken-nauwkeurigheid (onderste rij). Lijn-locaties mogen elkaar ook niet snijden.
* Vlak-locaties zijn toegestaan als de onderlinge afstand tussen de locaties groter is dan de teken-nauwkeurigheid (bovenste rij).
* Vlak-locaties die overlappen of naast elkaar liggen waarbij zowel de afmetingen van de overlap als de onderlinge afstand kleiner is dan de teken-nauwkeurigheid (bovenste rij) worden geacht elkaar te raken en elkaar niet te overlappen. Dit is toegestaan.
* Vlak-locaties die elkaar overlappen waarbij zowel de hoogte als breedte van de overlap groter is dan de teken-nauwkeurigheid (onderste rij) zijn niet toegestaan.
* Vlak-locaties die kleiner zijn dan de teken-nauwkeurigheid (onderste rij) zijn niet toegestaan.

Als een GIO voor een gegeven teken-nauwkeurigheid niet voldoet aan deze voorwaarden, kan dat ook liggen aan een verkeerde inschatting van de teken-nauwkeurigheid:

* Als punten, lijnen of vlakken op onvoldoende afstand van elkaar staan, dan is het GIO in groter detail getekend dan verwacht. Het GIO kan wel geschikt zijn bij een kleinere waarde voor de teken-nauwkeurigheid.
* Als vlakken een te grote mate van overlap kennen, dan is het GIO minder geteailleerd getekend dan verwacht. Bij een grotere waarde van de teken-nauwkeurigheid kan het GIO wel geschikt zijn.

Hieruit zijn randvoorwaarden voor een GIO af te leiden:
* Als twee punten dezelfde positie hebben zal een GIO nooit geschikt zijn.
* Als twee lijnen elkaar snijden zal de GIO nooit geschikt zijn.
* Als de vlakken in het GIO een overlap kennen die groter is dan de kleinste afstand tussen niet-overlappende vlakken, dan bestaat er geen teken-nauwkeurigheid waarvoor het GIO geschikt is.

## Algoritme

De geo-tools werken alleen als een GIO uitsluitend punten, lijnen of vlakken hebben.

De ondersteunde geometrieën zijn _Point_, _LineString_ en _Polygon_ en de meervoudige _MultiGeometry_, _MultiPoint_, _MultiCurve_ en _MultiSurface_ (via [pygml](https://github.com/geopython/pygml)). De eerste stap is om de _Multi_-varianten om te vormen naar enkele geometrieën. Zo ontstaat een reeks met paren (basisgeometrie-id, _Point_ of _LineString_ of _Polygon_).

### Punten
In het geval van punten wordt van elk paar punten de afstand berekend. Punten die een onderlinge afstand kleiner dan de _teken-nauwkeurigheid_ hebben, worden gerapporteerd en leiden tot ongeschiktheid van het GIO. Het kan dus gaan om punten van dezelfde _MultiPoint_ geometrie. Voor een ongeschikte GIO wordt daarne de minimale afstand van de puntparen bepaald. Mits groter dan nul is dit de teken-nauwkeurigheid waarbij het GIO wel geldig is.

### Lijnen
In geval van lijnen wordt vppr elk paar lijnstukken in de GIO de onderlinge afstand bepaald. Als die kleiner is dan de _teken-nauwkeurigheid_ hebben, dan worden de lijnen gerapporteerd en leidt dat tot ongeschiktheid van het GIO. Voor een ongeschikte GIO wordt daarne de minimale afstand van de lijnparen bepaald. Mits groter dan nul is dit de teken-nauwkeurigheid waarbij het GIO wel geldig is.

Om inzicht te krijgen waar de afstand te klein is wordt om elke lijn een buffer gelegd met als afstand de halve _teken-nauwkeurigheid_. Daarna wordt voor elk paar gebufferde lijnen de intersectie bepaald. Waar de intersectie een resultaatgebied oplevert bevinden de lijnen zich niet ver genoeg van elkaar.

![Controle lijnen](DetectieOverlappendeLijnen.svg)

### Vlakken
In geval van vlakken is het niet relevant om te weten of twee vlakken elkaar een beetje overlappen. Elk vlak wordt verkleind met als afstand een halve  _teken-nauwkeurigheid_ - er wordt dus een buffer om het vlak gelegd van (-_teken-nauwkeurigheid_/2). Als er geen vlak overblijft is het vlak te klein en is de GIO ongeschikt.

Vervolgens wordt van elk paar van de verkleinde vlakken bepaald of er een intersectie bestaat. Dat zal zo zijn als de oorspronkelijke vlakken meer dan de _teken-nauwkeurigheid_ overlappen. In dat geval is de GIO ongeschikt. Om inzicht te krijgen waar dat het geval is, wordt ook de intersectie berekend en weergegeven.

![Controle vlakken](DetectieOverlappendeVlakken.svg)
