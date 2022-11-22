# Geo-tools

[Geo-tools online](https://geo-tools.vercel.app/) - huidige versie: `2022-11-22 23:58:15`.

## Wat is het?
Gereedschap om met [geografische informatieobjecten](https://koop.gitlab.io/STOP/voorinzage/standaard-preview-b/gio-intro.html) (GIO's) uit [STOP](https://koop.gitlab.io/STOP/voorinzage/standaard-preview-b/) om te kunnen gaan. Laat ook zien hoe de randvoorwaarden voor het muteren van GIO's ingevuld kunnen worden.

## Wat zit er in?

Twee webpagina's om aanvullende bestanden te maken die kunnen helpen om een GIO in GIS software (onder andere [QGIS](https://www.qgis.org/)) te tonen:
- [GFS bestand voor een GIO](https://geo-tools.vercel.app/gfs_maker)
- [SLD bestand voor een symbolisatie](https://geo-tools.vercel.app/sld_maker)

Een aantal [Python scripts](broncode/geo-tools) die aan software leveranciers demonstreren hoe een GIO-wijziging bepaald en getoond kan worden. De scripts zijn online uit te voeren:

- [Bepaling van een GIO-wijziging](https://geo-tools.vercel.app/gio_wijziging) uit twee versies van een GIO.
- [Tonen van een GIO-wijziging](https://geo-tools.vercel.app/toon_gio_wijziging) die de geo-renvooi voor een GIO-wijziging toont.

De scripts sluiten aan bij de [beschrijving in STOP](https://koop.gitlab.io/STOP/voorinzage/standaard-preview-b/404.html).

### Offline / eigen computer

De twee webpsagina's kunnen op de eigen computer opgeslagen worden en van daaruit gestart worden. Ze gebruiken geen andere bestanden van het internet en zijn offline uit te voeren.

De Python scripts kunnen gedownload worden en op de eigen computer uitgevoerd worden:

- Zorg dat Python geïnstalleerd is. Dat is op Unix en MacOS meestal het geval. Voor Windows kan de laatste versie van Python [hier](https://www.python.org/downloads/) gedownload worden.

- [Download](download.zip) de tools en pak het zip bestand uit.

- Lees de [documentatie](../../wiki) waarin staat hoe de invoerbestanden gemaakt moeten worden.

- Maak eigen voorbeelden in de `mijn voorbeelden` map en voer `voer_tools_uit_voor_mijn_voorbeelden` uit om de resultaat-webpagina te maken.

- Bekijk de [voorbeelden](voorbeelden) om inspiratie op te doen. De tools zijn ook gebruikt voor de [STOP voorbeelden](https://gitlab.com/koop/STOP/voorinzage/standaard-preview-b/-/tree/master/voorbeeldenCoderingen/GIO/GIO-wijziging).
