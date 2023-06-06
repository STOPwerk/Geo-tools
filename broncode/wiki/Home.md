# Geo-tools
Gereedschap om met [geografische informatieobjecten](@@@STOP_Documentatie_Url@@@gio-intro.html) (GIO's) uit [STOP](@@@STOP_Documentatie_Url@@@) om te kunnen gaan. Laat ook zien hoe de randvoorwaarden voor het muteren van GIO's ingevuld kunnen worden.

## Online
De huidige versie is: `@@@VERSIE@@@`.

Deze documentatie betreft een aantal [Python scripts](../broncode/geo-tools) die aan software leveranciers demonstreren hoe een GIO-wijziging bepaald en getoond kan worden. De scripts zijn online uit te voeren:

- [Tonen/controleren van geo-informatie](@@@GeoTools_Online_Url@@@toon_geo) en uitvoeren van een kwaliteitscontrole voor geschiktheid voor een muteerbare GIO.(Met deze tool is ook een gebiedsmarkering of effectgebied te bekijken.).
- [Bepaling van een GIO-wijziging](@@@GeoTools_Online_Url@@@maak_gio_wijziging) uit twee versies van een GIO.
- [Tonen van een GIO-wijziging](@@@GeoTools_Online_Url@@@toon_gio_wijziging) die de geo-renvooi voor een GIO-wijziging toont.

De [demo en voorbeelden](../docs) met een demo en uitleg van de principes zijn ook [online](@@@GeoTools_Pages_Url@@@) te bekijken.

De scripts sluiten aan bij de [beschrijving in STOP](@@@STOP_Documentatie_Url@@@404.html).

## Offline / eigen computer
De scripts zijn te [downloaden](..) en op de eigen computer uit te voeren. De invoerbestanden moeten dan in een map op de eigen computer staan:

- [Invoerspecificatie](Invoerspecificatie) voor de scripts op de eigen computer.

In het downloadpakketje zit `voer_tools_uit_voor_mijn_voorbeelden.bat` om Python componenten te installeren en geo-tools te draaien op Windows.
Gebruik `voer_tools_uit_voor_mijn_voorbeelden.sh` op Unix en MacOS. Zie verder het overzicht van de [command line opties](Geo-tools-uitvoeren).

In het downloadpakketje zit ook `start_webserver.bat` / `start_webserver.sh` om de geo-tools in een lokale webserver te draaien en zo dezelfde functionaliteit te hebben als de online tools.

# Zelf programmeren
Voor inspiratie voor een eigen implementatie van het maken van een GIO-wijziging, zie de beschrijving van de structuur van de [Python code](structuur-code).
