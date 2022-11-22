# Geo-tools
Gereedschap om met [geografische informatieobjecten](@@@STOP_Documentatie_Url@@@gio-intro.html) (GIO's) uit [STOP](@@@STOP_Documentatie_Url@@@) om te kunnen gaan. Laat ook zien hoe de randvoorwaarden voor het muteren van GIO's ingevuld kunnen worden.

## Online
De huidige versie is: `@@@VERSIE@@@`.

Deze documentatie betreft een aantal [Python scripts](../broncode/geo-tools) die aan software leveranciers demonstreren hoe een GIO-wijziging bepaald en getoond kan worden. De scripts zijn online uit te voeren:

- [Bepaling van een GIO-wijziging](@@@GeoTools_Online_Url@@@gio_wijziging) uit twee versies van een GIO.
- [Tonen van een GIO-wijziging](@@@GeoTools_Online_Url@@@toon_gio_wijziging) die de geo-renvooi voor een GIO-wijziging toont.

De scripts sluiten aan bij de [beschrijving in STOP](@@@STOP_Documentatie_Url@@@404.html).

## Offline / eigen computer
De scripts zijn ook te [downloaden](..) en op de eigen computer uit te voeren. De invoerbestanden moeten dan 
een map op de eigen computer staan:

- [Invoerspecificatie](Invoerspecificatie) voor de scripts op de eigen computer.

In het download pakketje zit `voer_tools_uit_voor_mijn_voorbeelden.bat` om Python compontenten te installeren en geo-tools te draaien op Windows.

Op Unix en MacOS moet dat handmatig gedaan worden. Eenmalig:
```
python3 -m venv %~dp0venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install geopandas
```
Daarna voor het draaien van de geo-tools:
```
source venv/bin/activate
python3 applicatie.py ... opties ...
```

Zie verder het overzicht van de [command line opties](Geo-tools-uitvoeren).