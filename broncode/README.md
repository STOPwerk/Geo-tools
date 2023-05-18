# Ontwikkeling van geo-tools

## Indeling
Dit is de root directory voor de ontwikkeling van de STOPwerk Geo-tools. Hierin staat de Python code en alle testen.

De ondersteunende scripts (en deze readme) gaan ervan uit dat:

* Deze `broncode` directory onderdeel is van een kloon van de public repository [Geo-tools](@@@GeoTools_Url@@@) met de code voor de geo-tools.

* Voor de doorontwikkeling van de geo-tools gebruik wordt gemaakt van de branch `development`.

* Vanuit deze branch wordt een uitlevering gedaan die op de `main` branch van deze kloon terecht komt en uiteindelijk gepusht wordt naar de public repository.

* Dat een online versie van de geo-tools gehost wordt pp [vercel.com](https://vercel.com/).

## Werkwijze

* Gebruik dit deel van de repository om de Geo-tools door te ontwikkelen of te onderhouden. Doe dat op de _development_ branch (of een feature branch).

* De documentatie wordt bijgehouden in [wiki](wiki); deze wordt naar de wiki van de publieke repository uitgeleverd. 

* Er zijn geen unit tests in code. Wel zijn er testen in [tests](tests) die controleren of de scripts voor gegeven invoerbestanden nog steeds dezelfde HTML output maakt. Voor het maken van invoerbestanden en het uitvoeren van de applicatie: zie de [documentatie](wiki).

* Sommige testen gebruiken voorbeelden uit [voorbeelden](..\voorbeelden). De brondata voor de voorbeelden staat in de [tests](tests) directories.

^ Om codewijzigingen uit te leveren: ga naar [uitleveren](uitleveren) en volg de instructies in de README.md..

* Zowel in de wiki als in de broncode kunnen parameters `@@@naam@@@` opgenomen worden die bij uitlevering worden vervangen door de waarde in [configuratie.json](uitleveren/configuratie.json) voordat de uitlevering naar de `main` branch wordt gecommit.

## Ontwikkelomgeving
De code is ontwikkeld met Python 3.9 en Visual Studio 2022 met extensies `Markdown Editor v2` en `Smart Command Line Arguments for 2022`. De .bat scripts zijn getest met Python 3.8.10.

Voor het uitvoeren van de scripts moet git en python in het PATH staan. Als dat niet zo is voor Windows, zet dan de environment variabelen:

* `STOP_PYTHON` : directory waar python.exe te vinden is

Hernoemen van grote aantallen bestanden gaat goed met [PowerRename](https://learn.microsoft.com/en-us/windows/powertoys/powerrename).
