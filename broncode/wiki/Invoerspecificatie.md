_**Moet nog afgesplitst en bijgewerkt worden**_

## Invoerbestanden staan in een map
Als de geo-tools [uitgevoerd](Geo-tools-uitvoeren) worden als Python script, dan moeten alle invoerbestanden in een enkele map staan. De bestanden zijn:

* Specificatie voor een van de operaties in de geo-tools:
    * [toon_geo.json](#toon-geo)
    * [maak_gio_wijziging.json](#maak-gio-wijziging)
    * [toon_gio_wijziging.json](#toon-gio-wijziging)
    * [gio_wijziging.json](#gio_wijziging) combineert meerdere van de bovenstaande tot één operatie.

    De specificaties worden in deze volgorde ingelezen en door de bijbehorende geo-tool uitgvoerd. De geo-tools herkennen een map als een map met invoerbestanden als een van de specificaties gevonden wordt.

* GML en symbolisatiebestanden die in de specificatie genoemd zijn, gecodeerd volgens de voorschriften van de STOP modules:
    * [Effectgebied](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_Effectgebied.html)
    * [Gebiedsmarkering](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_Gebiedsmarkering.html)
    * GIO in de vorm van een [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html)
    * GIO in de vorm van een [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html)
    * [FeatureTypeStyle](@@@STOP_Documentatie_Url@@@se_xsd_Element_se_FeatureTypeStyle.html)

    Zo'n bestand mag ook in een andere map dan de specificatiemap staan, als in de specificatie maar het relatieve pad naar het bestand is aangegeven. Als scheidingsteken voor directories moet daarbij `/` gebruikt worden, bijvoorbeeld `../data/gio.gml`.

    De geo-tools ondersteunen alleen RD coördinaten (urn:ogc:def:crs:EPSG::28992). In een GIO mogen uitsluitend geometrieën van dezelfde soort (punten, lijnen of vlakken) voorkomen.

* Als de invoerbestanden voor een test bedoeld zijn, dan moeten ook de verwachte uitkomsten aangegeven worden:
    * ***_specificatie_zonder_json*_log_verwacht.json** bevat de verwachte foutmeldingen en waarschuwingen die uit de test komen. Als het bestand leeg is wordt niet gecontroleerd of de actuele meldingen aan de verwachtingen voldoen. Als de inhoud `[]` is worden geen foutmeldingen of waarschuwingen verwacht.
    * ***_specificatie_zonder_json*_verwacht.html** bevat de verwachte resultaatpagina van de geo-tool. Als het bestand leeg is wordt niet gecontroleerd of het actuele resultaat aan de verwachtingen voldoen. Het bestand kan weggelaten worden als er foutmeldingen zijn.

## Toon Geo
Het specificatiebestand `toon_geo.json` geeft de invoer voor de geo-tool die een geo-informatieobject, effectgebied of gebiedsmarkering toont.
```
{
    "geometrie": "geometrische_data.gml",
    "symbolisatie": "style.xml",
    "juridische-nauwkeurigheid": 1,
    "beschrijving": "Optionele beschrijving"
}
```
met:

| Parameter | Beschrijving |
| --------- | ------------ |
| `geometrie` | Het pad naar het bestand met de STOP module [Effectgebied](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_Effectgebied.html), [Gebiedsmarkering](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_Gebiedsmarkering.html), [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) |
| `symbolisatie` | Pad naar het bestand met de STOP module [FeatureTypeStyle](@@@STOP_Documentatie_Url@@@se_xsd_Element_se_FeatureTypeStyle.html). Optioneel; als dit niet gegeven is worden alle gebieden/lijnen/punten op een standaard manier weergegeven. |
| `juridische-nauwkeurigheid` | De [juridische nauwkeurigheid](Algoritme-controle) in decimeter van de geometrieën in de GIO. Als dit aanwezig is voor een GIO-versie dan wordt de geschikt |
| `beschrijving` | Optioneel: een beschrijving van het GIO die in de resultaatpagina wordt opgenomen |


## Maak GIO wijziging
Het specificatiebestand `maak_gio_wijziging.json` geeft de invoer voor de geo-tool die van twee geo-informatieobjecten een GIO-wijziging maakt.
```
{
    "was": "GIO_was_versie.gml",
    "wordt": "GIO_wordt_versie.gml",
    "juridische-nauwkeurigheid": 1,
    "symbolisatie": "style.xml",
    "wijziging": "GIO_wijziging.gml",
    "beschrijving": "Optionele beschrijving"
}
```
met:

| Parameter | Beschrijving |
| --------- | ------------ |
| `was` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) dat de oorspronkelijke (was-)versie van de GIO bevat.|
| `wordt` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) dat de nieuwe (wordt-)versie van de GIO bevat.|
| `juridische-nauwkeurigheid` | De (juridische) [juridische-nauwkeurigheid](Algoritme-controle) in decimeter van de geometrieën in de GIO. |
| `symbolisatie` | Pad naar het bestand met de STOP module [FeatureTypeStyle](@@@STOP_Documentatie_Url@@@se_xsd_Element_se_FeatureTypeStyle.html) dat de symbolisatie voor zowel de was- als de wordt-versie van de GIO bevat. De symbolisatie wordt gebruuikt om (tussen-)resultaten van de bepaling te laten zien. Als dit niet gegeven is worden alle gebieden/lijnen/punten op dezelfde manier weergegeven. |
| `wijziging` | Optioneel. Als een pad wordt opgegeven plaatst de geo-tool daar een bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) met de GIO-wijziging. Dit bestand kan als invoer gebruikt worden voor de [Toon GIO wijziging](#toon-gio-wijziging) geo-tool. |
| `beschrijving` | Optioneel: een beschrijving van de GIO-wijziging die in de resultaatpagina wordt opgenomen |


## Toon GIO wijziging
Het specificatiebestand `toon_gio_wijziging.json` geeft de invoer voor de geo-tool die een een GIO-wijziging weergeeft.
```
{
    "was": "GIO_was_versie.gml",
    "wijziging": "GIO_wijziging.gml",
    "symbolisatie": "style.xml",
    "wordt": "GIO_wordt_versie.gml"
}
```
met:

| Parameter | Beschrijving |
| --------- | ------------ |
| `was` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) dat de oorspronkelijke (was-)versie van de GIO bevat.|
| `wijziging` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) dat de GIO-wijziging bevat.|
| `symbolisatie` | Pad naar het bestand met de STOP module [FeatureTypeStyle](@@@STOP_Documentatie_Url@@@se_xsd_Element_se_FeatureTypeStyle.html) dat de symbolisatie voor zowel de was- als de wordt-versie van de GIO bevat. Verplicht voor een GIO met GIO-delen of normwaarden. Optioneel voor een GIO  met alleen geometrie; als dit niet gegeven is worden alle gebieden/lijnen/punten op dezelfde manier weergegeven. |
| `wordt` | Optioneel. Als een pad wordt opgegeven plaatst de geo-tool daar een bestand met de STOP module [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) met de wordt-versie van de GIO. |


## GIO wijziging
Het specificatiebestand `gio_wijziging.json` is een specificatie voor een gecombineerde operatie die eerst de GIO's toont, daarna de GIO-wijzigingen bepaalt en deze vervolgens laat zien:.
```
{
    "beschrijving": "Optionele beschrijving van de reden om deze operatie uit te voeren",
    "geometrie": [ 
        {
            "pad": "gio_1.gml", 
            "beschrijving": "Optionele beschrijving van de GIO",
            "juridische-nauwkeurigheid": 10,
            "symbolisatie": "afwijkende_style.xml"
        },
        {"pad": "gio_2.gml" }
        {"pad": "gio_3.gml" }
    ]
    "symbolisatie": "style.xml",
    "juridische-nauwkeurigheid": 1,
    "optimalisatie": false,
    "wijziging": [
        {
            "was": "gio_1.gml", 
            "wordt": "gio_2.gml", 
            "juridische-nauwkeurigheid": 10,
            "beschrijving": "Optionele beschrijving van de GIO-wijziging",
            "toon": true | false,
            "beschrijving_toon": "Optionele beschrijving van het tonen van de GIO-wijziging"
        },
        { "was": "gio_2.gml", "wordt": "gio_3.gml"},
        { "was": "gio_1.gml", "wordt": "gio_3.gml"}
    ]
}
```
Elk `geometrie` element wordt omgevormd naar een [toon_geo.json](#toon-geo) specificatie en uitgevoerd:

| Parameter van operatie | In deze specificatie: |
| ---------------------- | --------------------- |
| [toon_geo.json](#toon-geo): `geometrie` | `geometrie`: `pad` |
| [toon_geo.json](#toon-geo): `symbolisatie` | `geometrie`: `symbolisatie` indien aanwezig, anders `symbolisatie` |
| [toon_geo.json](#toon-geo): `juridische-nauwkeurigheid` | `geometrie`: `juridische-nauwkeurigheid` indien aanwezig, anderd `juridische-nauwkeurigheid` |
| [toon_geo.json](#toon-geo): `beschrijving` | `geometrie`: `beschrijving` |

Elk `wijziging` element wordt omgevormd naar een [maak_gio_wijziging.json](#maak-gio-wijziging) en uitgevoerd:

| Parameter van operatie | In deze specificatie: |
| ---------------------- | --------------------- |
| [maak_gio_wijziging.json](#maak-gio-wijziging): `was` | `wijziging`: `was` |
| [maak_gio_wijziging.json](#maak-gio-wijziging): `wordt` | `wijziging`: `wordt` |
| [maak_gio_wijziging.json](#maak-gio-wijziging): `juridische-nauwkeurigheid` | `wijziging`: `juridische-nauwkeurigheid` indien aanwezig, anders `juridische-nauwkeurigheid` |
| [maak_gio_wijziging.json](#maak-gio-wijziging): `symbolisatie` | `wijziging`: `symbolisatie` indien aanwezig, anders `symbolisatie` |
| [maak_gio_wijziging.json](#maak-gio-wijziging): `beschrijving` | `wijziging`: `beschrijving` |

Vervolgens wordt elk `wijziging` element omgevormd naar een [toon_gio_wijziging.json](#toon-gio-wijziging) specificatie en uitgevoerd:

| Parameter van operatie | In deze specificatie: |
| ---------------------- | --------------------- |
| toon-gio-wijziging niet uitvoeren | `wijziging`: `toon` = `false` (waarde van `toon` is `true` indien niet opgegeven) |
| [toon_gio_wijziging.json](#toon-gio-wijziging): `was` | `wijziging`: `was` |
| [toon_gio_wijziging.json](#toon-gio-wijziging): `symbolisatie` | `wijziging`: `symbolisatie` indien aanwezig, anders `symbolisatie` |
| [toon_gio_wijziging.json](#toon-gio-wijziging): `beschrijving` | `wijziging`: `beschrijving_toon` |

De GIO-wijziging uit de `maak_gio_wijziging` wordt in-memory doorgegeven aan de `toon_gio_wijziging` operatie.
