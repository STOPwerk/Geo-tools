_**Moet nog afgesplitst en bijgewerkt worden**_

## Invoerbestanden staan in een map
Als de geo-tools [uitgevoerd](Geo-tools-uitvoeren) worden als Python script, dan moeten alle invoerbestanden in een enkele map staan. De bestanden zijn:

* Specificatie voor een van de operaties in de geo-tools:
    * [toon_geo.json](#toon-geo)
    * [maak_gio_wijziging.json](#maak-gio-wijziging)
    * [toon_gio_wijziging.json](#toon-gio-wijziging)

    De specificaties worden in deze volgorde ingelezen en door de bibehorende geo-tool uitgvoerd. De geo-tools herkennen een map als een map met invoerbestanden als een van de specificaties gevonden wordt.

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
    "symbolisatie": "style.xml"
}
```
met:

| Parameter | Beschrijving |
| --------- | ------------ |
| `geometrie` | Het pad naar het bestand met de STOP module [Effectgebied](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_Effectgebied.html), [Gebiedsmarkering](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_Gebiedsmarkering.html), [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) |
| `symbolisatie` | Pad naar het bestand met de STOP module [FeatureTypeStyle](@@@STOP_Documentatie_Url@@@se_xsd_Element_se_FeatureTypeStyle.html). Optioneel; als dit niet gegeven is worden alle gebieden/lijnen/punten op een standaard manier weergegeven. |

## Maak GIO wijziging
Het specificatiebestand `maak_gio_wijziging.json` geeft de invoer voor de geo-tool die van twee geo-informatieobjecten een GIO-wijziging maakt.
```
{
    "was": "GIO_was_versie.gml",
    "wordt": "GIO_wordt_versie.gml",
    "persistente_id": true | false,
    "nauwkeurigheid": 1,
    "wijziging": "GIO_wijziging.gml"
}
```
met:

| Parameter | Beschrijving |
| --------- | ------------ |
| `was` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) dat de oorspronkelijke (was-)versie van de GIO bevat.|
| `wordt` | Het pad naar het bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) of [GeoInformatieObjectVersie](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVersie.html) dat de nieuwe (wordt-)versie van de GIO bevat.|
| `persistente_id` | Geeft aan of een ongewijzigde geometrie in de was- en wordt-versie met dezelfde [basisgeometrie-id](@@@Basisgeometrie_Url@@@) heeft. Als hiervoor `true` wordt ingevuld, dan ziet de geo-tool een verandering van basisgeometrie-id automatisch als een verandering van geometrie. Als hiervoor `false` wordt ingevuld, dan zal de geo-tool aan de hand van de `nauwkeurigheid` bepalen of er sprake is van een verandering in geometrie. Optioneel, `true` wordt gebruikt als `persistente_id` niet is opgegeven. |
| `nauwkeurigheid` | De juridische nauwkeurigheid in decimeter van de geometrieën in de GIO. Een geometrie in de was-versie en een geometrie in de wordt-versie worden juridisch als dezelfde geometrie gezien als ze minder dan `nauwkeurigheid` van elkaar af liggen. De `nauwkeurigheid` mag weggelaten worden als de GIO punten bevat en `persistente_id` is `true`. |
| `wijziging` | Optioneel. Als een pad wordt opgegeven plaatst de geo-tool daar een bestand met de STOP module [GeoInformatieObjectVaststelling](@@@STOP_Documentatie_Url@@@geo_xsd_Element_geo_GeoInformatieObjectVaststelling.html) met de GIO-wijziging. Dit bestand kan als invoer gebruikt worden voor de [Toon GIO wijziging](#toon-gio-wijziging) geo-tool. |


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
