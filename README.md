# Geo-tools

[Geo-tools online](@@@GeoTools_Online_Url@@@) - huidige versie: `@@@VERSIE@@@`.

## Wat is het?
Gereedschap om met [geografische informatieobjecten](@@@STOP_Documentatie_Url@@@gio-intro.html) (GIO's) uit [STOP](@@@STOP_Documentatie_Url@@@) om te kunnen gaan. De geo-tools zijn vooral bedoeld om te laten zien hoe de randvoorwaarden voor het muteren van GIO's ingevuld kunnen worden.

Het versiebeheer dat nodig is voor de consolidatie van GIO's kan gesimuleerd worden met de [versiebeheer-simulator](@@@VersiebeheerSimulator_Url@@@).

## Wat zit er in?

Een aantal [Python scripts](broncode/geo-tools) die aan software leveranciers demonstreren hoe een GIO-wijziging bepaald en getoond kan worden. De scripts zijn online uit te voeren:

- [Bepaling van een GIO-wijziging](@@@GeoTools_Online_Url@@@gio_wijziging) uit twee versies van een GIO.
- [Tonen van een GIO-wijziging](@@@GeoTools_Online_Url@@@toon_gio_wijziging) die de geo-renvooi voor een GIO-wijziging toont.
- Er zijn [voorbeelden](@@@GeoTools_Online_Url@@@voorbeeld) online beschikbaar om deze scripts uit te voeren. 

De scripts sluiten aan bij de [beschrijving in STOP](@@@STOP_Documentatie_Url@@@404.html).

Als bijvangst is beschikbaar:
- [Tonen van een GIO-versie, gebiedsmarkering of effectgebied](@@@GeoTools_Online_Url@@@toon_geo) die geo-informatie toont.

Verder twee webpagina's om aanvullende bestanden te maken die kunnen helpen om een GIO in GIS software (onder andere [QGIS](https://www.qgis.org/)) te tonen:
- [GFS bestand voor een GIO](@@@GeoTools_Online_Url@@@gfs_maker)
- [SLD bestand voor een symbolisatie](@@@GeoTools_Online_Url@@@sld_maker)

### Offline / eigen computer

De Python scripts kunnen gedownload worden en op de eigen computer uitgevoerd worden:

- Zorg dat Python geïnstalleerd is. Dat is op Unix en MacOS meestal het geval. Voor Windows kan de laatste versie van Python [hier](https://www.python.org/downloads/) gedownload worden.

- [Download](download.zip) de tools en pak het zip bestand uit.

- Lees de [documentatie](../../wiki) waarin staat hoe de invoerbestanden gemaakt moeten worden.

- Maak eigen voorbeelden in de `mijn voorbeelden` map en voer `voer_tools_uit_voor_mijn_voorbeelden` uit om de resultaat-webpagina te maken.

- Bekijk de [voorbeelden](broncode/geo-tools/voorbeelden) om inspiratie op te doen. De tools zijn ook gebruikt voor de [STOP voorbeelden](@@@STOP_Voorbeelden_Url@@@Coderingen/GIO/GIO-wijziging).

De twee webpsagina's kunnen op de eigen computer opgeslagen worden en van daaruit gestart worden. Ze gebruiken geen andere bestanden van het internet en zijn offline uit te voeren.

