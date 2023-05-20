# Geo-tools

[Geo-tools online](@@@GeoTools_Online_Url@@@) - huidige versie: `@@@VERSIE@@@`.

## Wat is het?

Het voornaamste doel is om te laten zien hoe het muteren van [geografische informatieobjecten](@@@STOP_Documentatie_Url@@@gio-intro.html) (GIO's) in [STOP](@@@STOP_Documentatie_Url@@@) werkt, waarom bepaalde keuzes zijn gemaakt. Het gaat hierbij om het maken van de GIO-wijziging die het verschil tussen twee GIO-versies beschrijft. Het versiebeheer dat nodig is voor de consolidatie van GIO's kan gesimuleerd worden met de [versiebeheer-simulator](@@@VersiebeheerSimulator_Url@@@).

- Er is een [demo en uitleg](@@@GeoTools_Online_Url@@@voorbeeld) beschikbaar van het maken en tonen van een GIO-wijziging.

De [brondata](broncode/geo-tools/voorbeelden) daarvan staat in deze repository. 

## Wat zit er in?

Minstens zo belangrijk is dat het mogelijk is software te maken die een GIO-wijziging kan maken en tonen, en dat GIO's te valideren zijn op de interne consistentie die daarvoor nodig is.De demo en uitleg zijn daarom gebaseerd op een aantal [Python scripts](broncode/geo-tools) die aan software leveranciers demonstreren hoe een GIO-wijziging bepaald en getoond kan worden. De scripts zijn online uit te voeren:

- [Tonen van een GIO-versie, gebiedsmarkering of effectgebied](@@@GeoTools_Online_Url@@@toon_geo) die geo-informatie toont en controleert of het GIO overeenkomt met de (in het GIO of expliciet) opgegeven teken-nauwkeurigheid.
- [Bepaling van een GIO-wijziging](@@@GeoTools_Online_Url@@@maak_gio_wijziging) uit twee versies van een GIO.
- [Tonen van een GIO-wijziging](@@@GeoTools_Online_Url@@@toon_gio_wijziging) die de geo-renvooi voor een GIO-wijziging toont.

De scripts sluiten aan bij de [beschrijving in STOP](@@@STOP_Documentatie_Url@@@404.html).

Verder twee webpagina's om aanvullende bestanden te maken die kunnen helpen om een GIO in GIS software (onder andere [QGIS](https://www.qgis.org/)) te tonen:
- [GFS bestand voor een GIO](@@@GeoTools_Online_Url@@@gfs_maker)
- [SLD bestand voor een symbolisatie](@@@GeoTools_Online_Url@@@sld_maker)

### Offline / eigen computer

De Python scripts kunnen gedownload worden en op de eigen computer uitgevoerd worden:

- Zorg dat Python geïnstalleerd is. Dat is op Unix en MacOS meestal het geval. Voor Windows kan de laatste versie van Python [hier](https://www.python.org/downloads/) gedownload worden.

- [Download](download.zip) de tools en pak het zip bestand uit.

Nu is er de keuze hoe verder te gaan. Om de [online versie](@@@GeoTools_Online_Url@@@) lokaal te draaien:

- Voer `start_webserver` uit om de webserver te starten. De online versie is daarna beschikbaar via [http://localhost:5555/](http://localhost:5555/).

De script kunnen ook op voorbeeldbestanden toegepast worden:

- Lees de [documentatie](../../wiki) waarin staat hoe de invoerbestanden gemaakt moeten worden.

- Maak eigen voorbeelden in de `mijn voorbeelden` map en voer `voer_tools_uit_voor_mijn_voorbeelden` uit om de resultaat-webpagina te maken.

- Bekijk de [voorbeelden](broncode/geo-tools/voorbeelden) om inspiratie op te doen. De tools zijn ook gebruikt voor de [STOP voorbeelden](@@@STOP_Voorbeelden_Url@@@Coderingen/GIO/GIO-wijziging).

De twee webpagina's kunnen op de eigen computer opgeslagen worden en van daaruit gestart worden. Ze gebruiken geen andere bestanden van het internet en zijn offline uit te voeren.

