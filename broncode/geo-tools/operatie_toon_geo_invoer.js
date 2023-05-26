window.addEventListener('load', function () {

    // ======================================================================
    // Afhandeling van de automatische detectie
    // ======================================================================
    const geometrieFile = document.getElementById('geometrie');
    const symbolisatieFile = document.getElementById('symbolisatie');
    const symbolisatieInvoer = document.getElementById('symbolisatie_invoer');
    const toepassingsnauwkeurigheidInvoer = document.getElementById('nauwkeurigheid_invoer');
    const toepassingsnauwkeurigheidWaarde = document.getElementById('toepassingsnauwkeurigheid');
    const kwaliteitscontroleInvoer = document.getElementById('kwaliteitscontrole_invoer');
    const kwaliteitscontroleWaarde = document.getElementById('kwaliteitscontrole');
    const startknop = this.document.getElementById("startknop");

    var geoFileType = '';
    var symbolisatieNodig = false;
    var toepassingsnauwkeurigheidNodig = false;
    var kwaliteitscontroleMogelijk = false;
    var teveelFiles = false;
    var geometrieOk = false;

    function InvoerControlsStatus() {
        toepassingsnauwkeurigheidInvoer.style.display = (toepassingsnauwkeurigheidNodig ? '' : 'none');
        kwaliteitscontroleInvoer.style.display = (kwaliteitscontroleMogelijk ? '' : 'none');
        if (kwaliteitscontroleMogelijk && toepassingsnauwkeurigheidNodig) {
            kwaliteitscontroleWaarde.disabled = (toepassingsnauwkeurigheidWaarde.value == "");
        } else {
            kwaliteitscontroleWaarde.disabled = false;
        }
        symbolisatieInvoer.style.display = (symbolisatieNodig ? '' : 'none');
        startknop.disabled = (teveelFiles || !geometrieOk);
    }
    InvoerControlsStatus();

    function FileLezer(file, line) {
        this._Line = line;
        this._File = file;

        this._InterpreteerGML = function (gml) {
            symbolisatieNodig = false;
            geometrieOk = false;
            startknop.disabled = true;
            if (gml.match(/\<([^:]+:){0,1}Gebiedsmarkering[\s>]/)) {
                geoFileType = 'Gebiedsmarkering';
                geometrieOk = true;
            }
            else if (gml.match(/\<([^:]+:){0,1}Effectgebied[\s>]/)) {
                geoFileType = 'Effectgebied';
                geometrieOk = true;
            }
            else {
                if (gml.match(/\<([^:]+:){0,1}GeoInformatieObjectVaststelling[\s>]/)) {
                    if (gml.match(/\<([^:]+:){0,1}GeoInformatieObjectMutatie[\s>]/)) {
                        geoFileType = 'GIO-wijziging (wordt niet ondersteund!)';
                    } else {
                        geoFileType = 'GIO (vaststelling)';
                        geometrieOk = true;
                    }
                }
                else if (gml.match(/\<([^:]+:){0,1}GeoInformatieObjectVersie[\s>]/)) {
                    geoFileType = 'GIO (versie)';
                    geometrieOk = true;
                }
                else {
                    geoFileType = 'Onbekend dataformaat';
                }
                if (geometrieOk) {
                    if (gml.match(/\<([^:]+:){0,1}kwantitatieveNormwaarde[\s>]/)
                        || gml.match(/\<([^:]+:){0,1}kwalitatieveNormwaarde[\s>]/)
                        || gml.match(/\<([^:]+:){0,1}groepID[\s>]/)) {
                        symbolisatieNodig = true;
                    }
                    toepassingsnauwkeurigheidNodig = true;
                    if (gml.match(/\<([^:]+:){0,1}toepassingsnauwkeurigheid[\s>]/)) {
                        toepassingsnauwkeurigheidNodig = false;
                    }
                    kwaliteitscontroleMogelijk = true;
                }
            }
            line.innerText = geoFileType + ': ' + file.name;
            InvoerControlsStatus();
        }

        const This = this;
        const reader = new FileReader();
        this.VoerUit = function () {
            reader.addEventListener("load", () => {
                This._InterpreteerGML(reader.result);
            }, false);
            reader.readAsText(file);
        }
    }
    symbolisatieInvoer.style.display = 'none';
    startknop.disabled = true;

    function UpdateControlStatus(geometrieGewijzigd) {

        const container = document.getElementById('bestanden');
        container.innerHTML = '';
        const titel = document.getElementById('titel');
        titel.value = '';

        if (geometrieGewijzigd) {
            geoFileType = '';
            symbolisatieNodig = false;
        }

        var heeftGeometrie = false;
        var analyseline = false;
        teveelFiles = false;
        for (var i = 0; i < geometrieFile.files.length; i++) {
            var file = geometrieFile.files[i];
            var line = document.createElement('div');
            container.appendChild(line);

            if (i > 0) {
                teveelFiles = true;
                line.innerText = 'Extra bestand geselecteerd! ' + file.name;
                titel.value = '';
            } else {
                line.innerText = geoFileType + ': ' + file.name;
                analyseline = line;
                titel.value = file.name;
            }
            heeftGeometrie = file;
        }
        if (heeftGeometrie && geometrieGewijzigd) {
            geometrieOk = false;
            analyseline.innerText = 'Analyseer ' + heeftGeometrie.name + '...';
            new FileLezer(heeftGeometrie, analyseline).VoerUit();
        }
        if (symbolisatieFile.files.length > 0) {
            var line = document.createElement('div');
            container.appendChild(line);
            line.innerText = 'Symbolisatie';
            var sep = ': '
            for (var i = 0; i < symbolisatieFile.files.length; i++) {
                var file = symbolisatieFile.files[i];
                if (i == 3) {
                    teveelFiles = true;
                    line = document.createElement('div');
                    container.appendChild(line);
                    line.innerText = 'Extra symbolisatie bestand';
                    sep = ': '
                }
                line.innerText += sep + file.name;
                sep = ', ';
            }
        }
        startknop.disabled = (teveelFiles || !geometrieOk);
    }

    // Event handlers
    geometrieFile.addEventListener('click', function (e) {
        UpdateControlStatus(true);
    });
    symbolisatieFile.addEventListener('click', function (e) {
        UpdateControlStatus(false);
    });
    function InitBox(box, fileInput, isGemetrie) {
        ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach(event => box.addEventListener(event, function (e) {
            e.preventDefault();
            e.stopPropagation();
        }), false);

        ['dragover', 'dragenter'].forEach(event => box.addEventListener(event, function (e) {
            box.classList.add('is-dragover');
        }), false);

        ['dragleave', 'dragend', 'drop'].forEach(event => box.addEventListener(event, function (e) {
            box.classList.remove('is-dragover');
        }), false);

        box.addEventListener('drop', function (e) {
            fileInput.files = e.dataTransfer.files;
            UpdateControlStatus(isGemetrie);
        }, false);
    }
    InitBox(document.getElementById('geometrie_box'), geometrieFile, true);
    InitBox(document.getElementById('symbolisatie_box'), symbolisatieFile, false);
    toepassingsnauwkeurigheidWaarde.addEventListener('click', InvoerControlsStatus);
    toepassingsnauwkeurigheidWaarde.addEventListener('change', InvoerControlsStatus);
});
