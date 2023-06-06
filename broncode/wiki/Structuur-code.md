# Structuur van de code

De [Python scripts](../blob/main/broncode/geo-tools) bestaan uit een aantal modules. Aan de naam is te zien wat de functie van de code in de module is:

| Naam | Functie |
| ---- | ------- |
| applicatie*.py | Modules die de offline versie van de Python scripts aansturen. |
| index*.py | Modules die de online versie van de Python scripts aansturen. |
| operatie*.py | Modules die de eigenlijke functionaliteit (tonen van GIO, maken en tonen van GIO-wijziging) implementeren. |
| data*.py | Module met hulpfuncties die door de operatie*.py modules gebruikt worden. |
| weergave*.py | Modules die helpen bij het maken van de webpagina met de resultaten van de tool. |

Naast de Python modules zijn er *.html, *.css en *.js bestanden met dezelfde (begin)naam als een Python module. Dat zijn losse onderdelen
van de resultaat-webpagina die door de Python module ingelezen en toegevoegd worden.

Om inspiratie op te doen voor een eigen implementatie van het maken/tonen van een GIO-wijziging:

- [operatie_toon_geo.py](../blob/main/broncode/geo-tools/operatie_toon_geo.py) bevat de code om een webpagina samen te stellen die een GIO toont. De code controleert tevens de kwaliteitseisen van het GIO.
- [operatie_maak_gio_wijziging.py](../blob/main/broncode/geo-tools/operatie_maak_gio_wijziging.py) bevat de code om een GIO-wijziging te maken.
- [operatie_toon_gio_wijziging.py](../blob/main/broncode/geo-tools/operatie_toon_gio_wijziging.py) bevat de code om een webpagina samen te stellen die een GIO-wijziging toont.
- [weergave_kaart_kaart.html](../blob/main/broncode/geo-tools/weergave_kaart_kaart.html), [weergave_kaart_kaart.css](../blob/main/broncode/geo-tools/weergave_kaart_kaart.css) en [weergave_kaart_kaart.js](../blob/main/broncode/geo-tools/weergave_kaart_kaart.js) bevatten de code om een kaart van een GIO of GIO-wijziging op te bouwen op basis van Openlayers (weergave_kaart_ol.*) en een [SLD lezer](../blob/main/broncode/geo-tools/weergave_kaart_sldreader.js)
