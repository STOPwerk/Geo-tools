#======================================================================
#
# Helper om met request/test parameters om te gaan
#
#======================================================================
from typing import Dict, List

import json
import os
from applicatie_meldingen import Meldingen

class Parameters:

#region Inlezen van parameters
    @staticmethod
    def Lees (log : Meldingen, specificatiePad : str) -> 'Parameters':
        """Probeer een specificatie te lezen en maak daar parameters van

        Argumenten:

        log Meldingen  Verzameling meldingen van de uitvoerende applicatie
        specificatiePad str  Volledig pad naar het specificatiebestand

        Geeft parameters terug, of None als het bestand niet gelezen kan worden
        """
        try:
            with open (specificatiePad, 'r', encoding='utf-8') as json_file:
                specificatie = json.load (json_file)
        except Exception as e:
            log.Fout ('Bestand "' + specificatiePad + '" is geen JSON bestand: ' + str(e))
            return
        if not isinstance (specificatie, dict):
            log.Fout ('Bestand "' + specificatiePad + '" is geen specificatie want de inhoud is geen JSON object')
            return
        return Parameters (log, specificatie, None, os.path.dirname (specificatiePad))
#endregion

#region Initialisatie en algemene methoden
    def __init__ (self, log : Meldingen, formdata : Dict[str,str], filedata, directory_pad: str):
        """Maak een instantie van de parameters aan

        Argumenten:

        log Meldingen      Verzameling meldingen van de uitvoerende applicatie
        formdata {}        Key = value parameters die invoer zijn voor de operatie
        filedata           Bestanden die in een web request zijn meegegeven; None voor een test
        directory_pad str  Voor een test: pad waarin de bestanden staan; None voor een web request
        """
        self.Log : Meldingen = log
        self._FormData = formdata
        self._FileData = filedata
        self._Pad = directory_pad
        # Geeft aan of resultaatbestanden weggeschreven kunnen worden
        self.KanBestandenSchrijven = not directory_pad is None

    def LeesString (self, key : str, lowercase : bool = False):
        """Lees de waarde van een parameter aan de hand van de specificatie key / input control naam.

        Argumenten:

        key str  Key waarvoor de waarde opgehaald moet worden
        lowercase bool  Geeft aan dat de waarde als lowervase teruggegeven moet worden

        Geeft de waarde terug als string, of None als de waarde niet gegeven is
        """
        waarde = None if self._FormData is None else self._FormData.get (key)
        if not waarde is None:
            waarde = str(waarde)
            if len (waarde) > 0:
                return waarde.lower () if lowercase else waarde

    def IsOptie (self, naam: str, defaultWaarde: bool = False) -> bool:
        """Haal de waarde voor een boolean optie uit de request parameters
        
        Argumenten:

        naam str Naam van de optie
        defaultWaarde bool  Geeft de waarde voor de optie als de optie niet in de request parameters aanwezig is

        Geeft de waarde terug, of defaultWaarde als het optie niet is opgegeven
        """
        waarde = None if self._FormData is None else self._FormData.get (naam)
        if waarde is None:
            return defaultWaarde
        try:
            return bool (waarde)
        except:
            self.Log.Fout ('De opgegeven waarde voor optie "' + naam + '" is onbegrijpelijk: "' + str(waarde) + '"')
            return defaultWaarde
#endregion

#region Ondersteuning voor bestanden
    def LeesBestand (self, key: str, verplicht: bool) -> str:
        """Lees de inhoud van een bestand aan de hand van de specificatie key / input type="file" control naam.

        Argumenten:

        log Meldingen  Verzameling meldingen voor de uitvoering van dit request
        key str        Key waarvoor de data opgehaald moet worden
        verplicht bool Geeft aan dat het bestand aanwezig moet zijn (dus niet optioneel is)

        Geeft de inhoud van het bestand terug, of None als er geen bestand/data is
        """
        if not self._Pad is None:
            filenaam = self._FormData.get (key)
            if filenaam is None:
                if verplicht:
                    self.Log.Fout ('Geen bestand gespecificeerd voor "' + key + '"')
                else:
                    self.Log.Detail ('Geen bestand gespecificeerd voor "' + key + '"')
                return None
            pad = os.path.join (self._Pad, filenaam)
            if not os.path.isfile (pad):
                self.Log.Fout ('Bestand voor "' + key + '" niet gevonden: "' + filenaam + '"')
                return None
            try:
                with open (pad, 'r', encoding = 'utf-8') as dataFile:
                    data = dataFile.read ()
                self.Log.Detail ('Bestand "' + filenaam + '" voor "' + key + '" ingelezen')
                return data
            except Exception as e:
                self.Log.Fout ('Bestand voor "' + key + '" ("' + filenaam + '") kan niet gelezen worden: ' + str(e))
                return None

        else:
            files = None if self._FileData is None or not key in self._FileData else self._FileData.getlist (key)
            if files is None:
                self.Log.Detail ('Geen bestand doorgegeven voor "' + key + '"')
                return None
            for fileData in files:
                if fileData.filename != '':
                    try:
                        data = fileData.stream.read ().decode("utf-8").strip ()
                        if len(data) == 0:
                            self.Log.Waarschuwing ('Leeg bestand "' + fileData.filename + '" voor "' + key + '" genegeerd')
                        else:
                            self.Log.Detail ('Bestand "' + fileData.filename + '" voor "' + key + '" ingelezen')
                            return data
                    except Exception as e:
                        self.Log.Fout ('Bestand "' + fileData.filename + '" bevat geen valide (utf-8) data: ' + str(e))
                    break
            return None

    def LeesBestanden (self, key: str, verwerkBestand):
        """Lees de inhoud van een of meer bestanden aan de hand van de specificatie key / input type="file" control naam.

        Argumenten:

        log Meldingen  Verzameling meldingen voor de uitvoering van dit request
        key str        Key waarvoor de data opgehaald moet worden
        verwerkBestand lambda Methode die aangeroepen wordt met de naam en inhoud van elk gevonden bestand
        """
        if not self._Pad is None:
            filenamen = self._FormData.get (key)
            if filenamen is None:
                self.Log.Detail ('Geen bestand(en) gespecificeerd voor "' + key + '"')
                return
            if isinstance (filenamen, str):
                filenamen = [filenamen]
            for filenaam in filenamen:
                pad = os.path.join (self._Pad, filenaam)
                if not os.path.isfile (pad):
                    self.Log.Fout ('Bestand voor "' + key + '" niet gevonden: "' + filenaam + '"')
                    return
                try:
                    with open (pad, 'r', encoding = 'utf-8') as dataFile:
                        data = dataFile.read ()
                    self.Log.Detail ('Bestand "' + filenaam + '" voor "' + key + '" ingelezen')
                    verwerkBestand (filenaam, data)
                except Exception as e:
                    self.Log.Fout ('Bestand voor "' + key + '" ("' + filenaam + '") kan niet gelezen worden: ' + str(e))

        else:
            files = None if self._FileData is None or not key in self._FileData else self._FileData.getlist (key)
            if files is None:
                self.Log.Detail ('Geen bestand(en) doorgegeven voor "' + key + '"')
                return
            for fileData in files:
                if fileData.filename != '':
                    try:
                        data = fileData.stream.read ().decode("utf-8").strip ()
                        if len(data) == 0:
                            self.Log.Waarschuwing ('Leeg bestand "' + fileData.filename + '" voor "' + key + '" genegeerd')
                        else:
                            self.Log.Detail ('Bestand "' + fileData.filename + '" voor "' + key + '" ingelezen')
                            verwerkBestand (fileData.filename, data)
                    except Exception as e:
                        self.Log.Fout ('Bestand "' + fileData.filename + '" bevat geen valide (utf-8) data: ' + str(e))

    def Bestandsnaam (self, key: str, inclusiefExtensie : bool = True):
        """Geef de bestandnaam van een bestand aan de hand van de specificatie key / input type="file" control naam.  
        
        Argumenten:
        
        key str  Key waarmee het bestand wirdt/is gelezen.
        inclusiefExtensie bool  Geeft aan of de extensie behouden moet worden.
        """
        filenaam = None
        if not self._Pad is None:
            filenaam = self._FormData.get (key)
            filenaam = os.path.basename (filenaam)
        else:
            files = None if self._FileData is None or not key in self._FileData else self._FileData.getlist (key)
            if not files is None:
                for fileData in files:
                    if fileData.filename != '':
                        filenaam = fileData.filename
                        break
        if not filenaam is None:
            if inclusiefExtensie:
                return filenaam
            else:
                return os.path.splitext (filenaam)[0]
#endregion

#region Ondersteuning voor nauwkeurigheden
    def ToepassingsnauwkeurigheidInCentimeter (self, verplicht: bool = True) -> int:
        """Haal de nauwkeurigheid in centimeter uit de request parameters
        
        Argumenten:

        verplicht bool  Geeft aan dat de toepassingsnauwkeurigheid een verplichte parameter is

        Geeft de waarde als int terug, of None als de toepassingsnauwkeurigheid niet is opgegeven
        """
        if self.LeesString ("toepassingsnauwkeurigheid") is None:
            if verplicht:
                self.Log.Fout ("De toepassingsnauwkeurigheid is niet opgegeven in de specificatie")
            return None
        try:
            nauwkeurigheid = int (self.LeesString ("toepassingsnauwkeurigheid"))
        except:
            self.Log.Fout ('De opgegeven toepassingsnauwkeurigheid is geen getal: "' + self.LeesString ("toepassingsnauwkeurigheid") + '"')
            return None
        return nauwkeurigheid

    def ToepassingsnauwkeurigheidInMeter (self, verplicht: bool = True) -> float:
        """Haal de nauwkeurigheid in meters uit de request parameters
        
        Argumenten:

        verplicht bool  Geeft aan dat de toepassingsnauwkeurigheid een verplichte parameter is

        Geeft de waarde als float terug, of None als de toepassingsnauwkeurigheid niet is opgegeven
        """
        nauwkeurigheid = self.ToepassingsnauwkeurigheidInCentimeter (verplicht)
        if not nauwkeurigheid is None:
            try:
                return 0.01 * float (nauwkeurigheid)
            except:
                self.Log.Fout ('De opgegeven toepassingsnauwkeurigheid is geen getal: "' + self.LeesString ("toepassingsnauwkeurigheid") + '"')
#endregion
