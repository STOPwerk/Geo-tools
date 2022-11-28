## Uitvoeren van Python script

Ga naar de map waarin de Python scripts staan: de `geo-tools` map.

**Windows:**
```
voer_tools_uit [--help|-h] [--alle|-a] [--meldingen|-m meldingen_pad] [--testen|-t] directory_pad [directory_pad ..]
```

**Unix/MacOS en Windows:**
```
python applicatie.py [--help|-h] [--alle|-a] [--meldingen|-m meldingen_pad] [--testen|-t] directory_pad [directory_pad ..]
```

Voer de geo-tools uit voor één of meer mappen met invoerbestanden. In zo'n map moet tenminste een van de [specificatiebestanden](Invoerspecificatie) staan. De tools maken per specificatiebestand een resultaatbestand `*_resultaat.html` aan en eventueel aanvullende uitvoerbestanen en plaatst de bestanden in de map met het specificatiebestand. Daarnaast wordt een webpagina getoond met een verslag van de uitvoering van de applicatie. Deze webpagina wordt in de systeem-map voor tijdelijke bestanden geplaatst.

| Command line | Beschrijving |
| ----- | ----- |
| `voer_tools_uit` | Een script dat niet alleen het Python script start maar ook een virtuele omgeving maakt (als die nog niet bestaat) met de benodigde bibliotheken. |
| `python` | Het programma om een Python script mee uit te voeren. Op Windows is dat `py.exe` of `python.exe`, op MacOS/Unix `python3`. Voor Windows kan de laatste versie van Python [hier](https://www.python.org/downloads/) gedownload worden. |
| `applicatie.py` | Het pad van het Python script dat uitgevoerd moet worden. Het script is te vinden in de `geo-tools` map in [download.zip](../blob/master/download.zip). De overige bestanden in de `geo-tools` map worden bij het uitvoeren van de Python code ingelezen. |
| `directory_pad` | Pad naar een map met een specificatiebestanden waarvoor de geo-tools uitgevoerd moet worden |
| `-a` of `--alle` | Kijk ook in subdirectories van `directory_pad` voor specificatiebestanden. Met deze optie kunnen de tools tegelijk voor een hele collectie van specificaties uitgevoerd worden. |
| `-m meldingen_pad` of `--meldingen meldingen_pad` | Bewaar het verslag van de uitvoering van de applicatie in de `meldingen_pad` map, in plaats van in de systeem-map voor tijdelijke bestanden. |
| `-h` of `--help` | Toon de mogelijke command line opties, dus de informatie die op deze pagina staat. |
| `-t` of `--testen` | Deze optie is bedoeld voor gebruik bij de (door)ontwikkeling van de geo-tools. Zie de gebruikte [testen](../blob/master/broncode/tests/). De applicatie vergelijkt het resultaatbestand `*_actueel.html` met het aanwezige `*_verwacht.html`   en vergelijkt de tywee bestanden met elkaar. |

## Voorbereiden van Python

Als het `voer_tools_uit` script gebruikt wordt, dan wordt gecontroleerd of er een virtuele Python omgeving bestaat waarin alle benodigde bibliotheken zijn geladen.

Voor Unix/MacOS moeten de bibliotheken eerst geladen worden. Dat kan door zelf een virtuele Python omgeving te maken of door de bibliotheken in de standaard versie van Python op te nemen:
```
python3 -m pip install -r requirements.txt
```
