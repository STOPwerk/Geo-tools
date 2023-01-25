# Maak een GIO-wijziging

## Doel van de operatie

Bepaalt hoe een originele (was)-versie van een GIO wijzigt naar een nieuwe (wordt)-versie van dezelfde GIO. Het resultaat is een GIO-wijziging, een GML-bestand dat (na aanvulling met de vaststellingscontext) gebruikt kan worden in een besluit in de plaats van de nieuwe GIO-versie. De GIO-wijziging kan in [geo-renvooi](Toon-gio-wijziging) worden weergegeven; dat is een vervolgoperatie.

Online: [Tonen/controleren van geo-informatie](@@@GeoTools_Online_Url@@@maak_gio_wijziging).

Python script: [toon_geo.py](../blob/main/broncode/geo-tools/maak_gio_wijziging.py) met gebruik making van [geo_manipulatie.py](../blob/main/broncode/geo-tools/geo_manipulatie.py).


## Algoritme

De uitgangspunten voor dit algeoritme zijn:
* De geo-tools werken alleen als een GIO uitsluitend punten, lijnen of vlakken hebben. Dit is een implementatiebeperking. Het algoritme kan uitgebreid worden naar GIO's waarin een mix van punten, lijnen en vlakken voorkomen.
* Beide GIO-versies zijn [geschikt bevonden](Toon-controleer-gio) voor dezelfde juridische nauwkeurigheid die gebruikt wordt bij deze operatie.
* Als het een GIO betreft met GIO-delen, dan zijn de groepID en bijbehorende naam onveranderlijk in de tijd en onderanderlijk aan elkaar gekoppeld. Als in de was- en wordt-versie van de GIO dezelfde groepID voorkomt, dan hoort daar dezelfde naam bij. Als dezelfde naam voorkomt, dan heeft die dezelfde groepID. 

De bepaling van de GIO-wijziging kan opgesplitst worden in:

* Een vergelijking van de locaties met een manifest ongewijzigde geometrie, d.w.z. locaties met een geometrie met een basisgeometrie-ID die zowel in de was- als wordt-versie voorkomt. Deze locaties nemen geen deel aan geo-operaties.
* Een vergelijking van de overige locaties. Hierbij moeten geo-operaties uitgevoerd worden om te bepalen of (en in hoeverre) geometriën gewijzigd zijn.

Het algoritme blijft werken als de basisgeometrie_IDs van de locaties voor elke GIO-versie opnieuw bepaald worden. Maar zeker als er eigenlijk weinig verschil zit tussen de was- en wordt-versie neemt de bepaling van GIO-wijziging in dat geval veel meer rekentijd in beslag.

De uitkomst van het algoritme is een GIO-wijziging die bestaat uit:

* GIO-Locaties uit de was-versie waarvan ofwel de geometrie, ofwel het groepID, ofwel de normwaarde is gewijzigd in de wordt-versie van de GIO.
* GIO-Locaties uit de wordt-versie waarvan ofwel de geometrie, ofwel het groepID, ofwel de normwaarde is gewijzigd ten opzichte van de was-versie van de GIO.
* GIO-Locaties uit de wordt-versie die juridisch niet zijn gewijzigd ten opzichte van de was-versie van de GIO maar die wel een andere naam hebben (revisies).
* Wijzigmarkeringen die geografisch aangeven waar de wijzigingen in de GIO-versies optreden. Dit zijn enkelvoudige (geen multi-)geometrieën zonder verdere eigenschappen:
    * Als de GIO uit punten bestaat, dan zijn de wijzigmarkeringen ook punten.
    * Als de GIO uit lijnen bestaat, dan zijn de wijzigmarkeringen lijnen (overeenkomend met manifest ongewijzigde geometrieën) en/of vlakken. 
    * Als de GIO uit lijnen bestaat, dan zijn de wijzigmarkeringen vlakken. 

### GIO-locaties met een manifest ongewijzigde geometrie
Als dezelfde basisgeometrie-ID zowel in de was- als wordt-versie bij een GIO-Locatie voorkomt, dan:

* is de geometrie ongewijzigd, want dat is de eis om dezelfde basisgeometrie-ID te mogen gebruiken;
* zijn er binnen de wordt-versie geen andere locaties die (voor de opgegeven juridische nauwkeurigheid) op een juridisch significante manier met de geometrie overlappen (want anders zou de wordt-versie ongeschikt bevonden zijn);
* zijn er binnen de was-versie geen andere locaties die (voor de opgegeven juridische nauwkeurigheid) op een juridisch significante manier met de geometrie overlappen (want anders zou de was-versie ongeschikt bevonden zijn).

De bijbehorende GIO-locatie uit de was-versie muteert daarom naar de GIO-Locatie in wordt-versie en overlapt io geen enkele manier geometrisch met de overige locaties uit de GIO-versies. Voor deze locaties geldt:

* De locatie is ongewijzigd als:
    * De GIO alleen uit geometrie bestaat
    * De GIO bestaat uit GIO-delen en de groepID is voor was-versie gelijk aan die van de wordt-versie 
    * De GIO bevat normwaarden en de normwaarde is voor was-versie gelijk aan die van de wordt-versie (rekening houdend met afrondingsfouten voor kwantitatieve normwaarden).
* Als de locatie ongewijzigd is, dan:
    * Als de naam van de locatie in de wordt-versie afwijkt van de was-versie, dan is er sprake van een revisie. Alleen de GIO-locatie uit de wordt-versie wordt dan als revisie opgenomen in de GIO-wijziging.
    * Zo niet, dan hoeft de locatie niet opgenomen te worden in de GIO-wijziging.
* Als de locatie niet ongewijzigd is, dan:
    * wordt zowel de GIO-locatie uit de was- en de wordt-versie opgenomen in de GIO-wijziging;
    * wordt de geometrie daarnaast opgenomen in de wijzigingmarkeringen van de GIO-wijziging.

