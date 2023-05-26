#GIO met alleen geometrie

Dit is een technisch voorbeeld om geo-renvooi te demonstreren voor een GIO met alleen geometrie bestaande uit punten.
Het laat zien dat als een GIO zorgvuldig opgesteld wordt (geen overlappende geometrieën binnen de toepassingsnauwkeurigheid)
en als de basisgeometrie-ID van ongewijzigde geometrieën behouden blijft in verschillende versies van de GIO,
het bepalen van de geo-renvooi sneller verloopt omdat de ongewijzigde geometrieën niet meegenomen hoeven te worden
in de geo-operaties.

De geometrieën bestaan uit punten. Elk punt is een aparte GIO-Locatie.
Als de positie van een punt niet wijzigt in een volgende versie, dan heeft dat punt nog dezelfde basisgeometrie-ID.
