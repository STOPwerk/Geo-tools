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
    "symbolisatie": [ "punt_style.xml", "lijn_style.xml", "vlak_style.xml" ],
    "juridische-nauwkeurigheid": 1,
    "toon-gio-schaalafhankelijk": true | false,
    "kwaliteitscontrole": false | true,
    "beschrijving": "Optionele beschrijving"
}
```
met:

| Parameter | Beschrijving |
| --------- | ------------ |
| `geometrie` | Het pad naar het bestand met de STOP module [Effectgebied](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_Effectgebied.html), [Gebiedsmarkering](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_Gebiedsmarkering.html), [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) |
| `symbolisatie` | Opsomming van de paden naar het bestand met de STOP module [FeatureTypeStyle](@@@STOP_Documentatie_Url@@@se_xsd_Element_se_FeatureTypeStyle.html) voor de weergave van een punt, lijn of vlak van de geometrie. Optioneel; als dit niet gegeven is (of niet gegeven voor een punt/lijn of vlak) worden de gebieden, lijnen en/of punten op een standaard-manier weergegeven. |
| `juridische-nauwkeurigheid` | Als de STOP-module een GIO-versie bevat: de [juridische nauwkeurigheid](Algoritme-controle) in decimeter van de geometrieën in het GIO. Deze waarde wordt alleen gebruikt als de juridische nauwkeurigheid niet (conform STOP 2) in de GIO-versie is opgenomen. Optioneel. |
| `toon-gio-schaalafhankelijk` |  Als de STOP-module een GIO-versie bevat en de juridische nauwkeurigheid bekend is: gebruik dit om de GIO-versie schaalafhankelijk weer te geven. Optioneel; default is true.|
| `kwaliteitscontrole` |  Als de STOP-module een GIO-versie bevat en de juridische nauwkeurigheid bekend is: controleer dat de GIO-versie aan de kwaliteitseisen voor een muteerbare GIO voldoet. Optioneel; default is false.|
| `beschrijving` | Optioneel: een beschrijving van het GIO die in de resultaatpagina wordt opgenomen |


## Maak GIO wijziging
Het specificatiebestand `maak_gio_wijziging.json` geeft de invoer voor de geo-tool die van twee geo-informatieobjecten een GIO-wijziging maakt.
```
{
    "was": "GIO_was_versie.gml",
    "wordt": "GIO_wordt_versie.gml",
    "juridische-nauwkeurigheid": 1,
    "symbolisatie": [ "style.xml" ],
    "toon-gio-wijziging": true | false,
    "wijziging": "GIO_wijziging.gml",
    "beschrijving": "Optionele beschrijving"
}
```
met:

| Parameter | Beschrijving |
| --------- | ------------ |
| `was` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) dat de oorspronkelijke (was-)versie van het GIO bevat.|
| `wordt` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) dat de nieuwe (wordt-)versie van het GIO bevat.|
| `juridische-nauwkeurigheid` | De (juridische) [juridische-nauwkeurigheid](Algoritme-controle) in decimeter van de geometrieën in de GIO. |
| `symbolisatie` | Opsomming van de paden naar het bestand met de STOP module [FeatureTypeStyle](@@@STOP_Documentatie_Url@@@se_xsd_Element_se_FeatureTypeStyle.html) voor de weergave van een punt, lijn of vlak voor zowel de was- als de wordt-versie van het GIO bevat. De symbolisatie wordt gebruuikt om (tussen-)resultaten van de bepaling te laten zien. Als dit niet gegeven is (voor een geometrietype) worden alle gebieden, lijnen en/of punten op een standaard-manier weergegeven. |
| `wijziging` | Optioneel. Als een pad wordt opgegeven plaatst de geo-tool daar een bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) met de GIO-wijziging. Dit bestand kan als invoer gebruikt worden voor de [Toon GIO wijziging](#toon-gio-wijziging) geo-tool. |
| `toon-gio-wijziging` |  Toon de GIO-wijziging op de manier zoals een viewer dat zou (moeten) doen. Optioneel; default is true.|
| `beschrijving` | Optioneel: een beschrijving van de GIO-wijziging die in de resultaatpagina wordt opgenomen |


## Toon GIO wijziging
Het specificatiebestand `toon_gio_wijziging.json` geeft de invoer voor de geo-tool die een een GIO-wijziging weergeeft.
```
{
    "was": "GIO_was_versie.gml",
    "wijziging": "GIO_wijziging.gml",
    "symbolisatie": [ "style.xml" ],
    "wordt": "GIO_wordt_versie.gml"
}
```
met:

| Parameter | Beschrijving |
| --------- | ------------ |
| `was` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) dat de oorspronkelijke (was-)versie van het GIO bevat.|
| `wijziging` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) dat de GIO-wijziging bevat.|
| `symbolisatie` | Opsomming van de paden naar het bestand met de STOP module [FeatureTypeStyle](@@@STOP_Documentatie_Url@@@se_xsd_Element_se_FeatureTypeStyle.html) voor de weergave van een punt, lijn of vlak voor zowel de was- als de wordt-versie van het GIO bevat. De symbolisatie wordt gebruuikt om (tussen-)resultaten van de bepaling te laten zien. Als dit niet gegeven is (voor een geometrietype) worden alle gebieden, lijnen en/of punten op een standaard-manier weergegeven. |
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
            "kwaliteitscontrole": false,
            "symbolisatie": [ "afwijkende_style.xml" ]
        },
        {"pad": "gio_2.gml" }
        {"pad": "gio_3.gml" }
    ]
    "symbolisatie": [ "punt_style.xml", "vlak_style.xml"],
    "juridische-nauwkeurigheid": 1,
    "kwaliteitscontrole": true,
    "wijziging": [
        {
            "was": "gio_1.gml", 
            "wordt": "gio_2.gml", 
            "juridische-nauwkeurigheid": 10,
            "beschrijving": "Optionele beschrijving van de GIO-wijziging",
            "toon-gio-wijziging": true | false,
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
| [toon_geo.json](#toon-geo): `juridische-nauwkeurigheid` | `geometrie`: `juridische-nauwkeurigheid` indien aanwezig, anders `juridische-nauwkeurigheid` |
| [toon_geo.json](#toon-geo): `kwaliteitscontrole` | `geometrie`: `kwaliteitscontrole` indien aanwezig, anders `kwaliteitscontrole` |
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
| toon-gio-wijziging niet uitvoeren | `wijziging`: `toon-gio-wijziging` = `false` (waarde van `toon-gio-wijziging` is `true` indien niet opgegeven) |
| [toon_gio_wijziging.json](#toon-gio-wijziging): `was` | `wijziging`: `was` |
| [toon_gio_wijziging.json](#toon-gio-wijziging): `symbolisatie` | `wijziging`: `symbolisatie` indien aanwezig, anders `symbolisatie` |
| [toon_gio_wijziging.json](#toon-gio-wijziging): `beschrijving` | `wijziging`: `beschrijving_toon` |

De GIO-wijziging uit de `maak_gio_wijziging` wordt in-memory doorgegeven aan de `toon_gio_wijziging` operatie.
