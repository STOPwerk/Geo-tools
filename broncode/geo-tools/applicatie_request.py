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
        return Parameters (specificatie, None, os.path.dirname (specificatiePad))

    def __init__ (self, formdata : Dict[str,str], filedata, directory_pad: str):
        """Maak een instantie van de parameters aan

        Argumenten:

        formdata {}        Key = value parameters die invoer zijn voor de operatie
        filedata           Bestanden die in een web request zijn meegegeven; None voor een test
        directory_pad str  Voor een test: pad waarin de bestanden staan; None voor een web request
        """
        self._FormData = formdata
        self._FileData = filedata
        self._Pad = directory_pad
        # Geeft aan of resultaatbestanden weggeschreven kunnen worden
        self.KanBestandenSchrijven = not directory_pad is None
        # Geeft aan of het een online request betreft waar resultaten doorgegeven kunnen worden aan de volgeode operatie.
        self.IsOnlineOperatie = directory_pad is None

    def LeesString (self, key : str, lowercase : bool = False):
        """Lees de waarde van een parameter aan de hand van de specificatie key / input control naam.

        Argumenten:

        key str  Key waarvoor de waarde opgehaald moet worden
        lowercase bool  Geeft aan dat de waarde als lowervase teruggegeven moet worden

        Geeft de waarde terug als string, of None als de waarde niet gegeven is
        """
        waarde = None if self._FormData is None else self._FormData.get (key)
        if not waarde is None:
            return str(waarde).ower () if lowercase else str(waarde)

    def LeesBestand (self, log : Meldingen, key: str, verplicht: bool):
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
                    log.Fout ('Geen bestand gespecificeerd voor "' + key + '"')
                else:
                    log.Detail ('Geen bestand gespecificeerd voor "' + key + '"')
                return None
            pad = os.path.join (self._Pad, filenaam)
            if not os.path.isfile (pad):
                log.Fout ('Bestand voor "' + key + '" niet gevonden: "' + filenaam + '"')
                return None
            try:
                with open (pad, 'r', encoding = 'utf-8') as dataFile:
                    data = dataFile.read ()
                log.Detail ('Bestand "' + filenaam + '" voor "' + key + '" ingelezen')
                return data
            except Exception as e:
                log.Fout ('Bestand voor "' + key + '" ("' + filenaam + '") kan niet gelezen worden: ' + str(e))
                return None

        else:
            files = None if self._FileData is None or not key in self._FileData else self._FileData.getlist (key)
            if files is None:
                log.Detail ('Geen bestand doorgegeven voor "' + key + '"')
                return None
            for fileData in files:
                if fileData.filename != '':
                    try:
                        data = fileData.stream.read ().decode("utf-8").strip ()
                        if len(data) == 0:
                            log.Waarschuwing ('Leeg bestand "' + fileData.filename + '" voor "' + key + '" genegeerd')
                        else:
                            log.Detail ('Bestand "' + fileData.filename + '" voor "' + key + '" ingelezen')
                            return data
                    except Exception as e:
                        log.Fout ('Bestand "' + fileData.filename + '" bevat geen valide (utf-8) data: ' + str(e))
                    break
            return None

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
