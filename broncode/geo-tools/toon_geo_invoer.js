window.addEventListener('load', function () {

    // ======================================================================
    // Afhandeling van de automatische detectie
    // ======================================================================
    const geometrieFile = document.getElementById('geometrie');
    const symbolisatieFile = document.getElementById('symbolisatie');
    const symbolisatieInvoer = document.getElementById('symbolisatie_invoer');
    const startknop = this.document.getElementById("startknop");

    var geoFileType = '';
    var symbolisatieNodig = false;
    var teveelFiles = false;
    var geometrieOk = false;

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
                if (gml.match(/\<([^:]+:){0,1}kwantitatieveNormwaarde[\s>]/)
                    || gml.match(/\<([^:]+:){0,1}kwalitatieveNormwaarde[\s>]/)
                    || gml.match(/\<([^:]+:){0,1}groepID[\s>]/)) {
                    symbolisatieNodig = true;
                }
                if (gml.match(/\<([^:]+:){0,1}GeoInformatieObjectVaststelling[\s>]/)) {
                    if (gml.match(/\<([^:]+:){0,1}GeoInformatieObjectMutatie[\s>]/)) {
                        geoFileType = 'GIO-wijziging (wordt niet ondersteund!)';
                        symbolisatieNodig = false;
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
                    symbolisatieNodig = false;
                }
            }
            line.innerText = geoFileType + ': ' + file.name;
            symbolisatieInvoer.style.display = (symbolisatieNodig ? '' : 'none');
            startknop.disabled = (teveelFiles || !geometrieOk);
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
        for (var i = 0; i < symbolisatieFile.files.length; i++) {
            var file = symbolisatieFile.files[i];
            var line = document.createElement('div');
            container.appendChild(line);
            if (i > 0) {
                teveelFiles = true;
                line.innerText = 'Extra bestand geselecteerd! ' + file.name;
            } else {
                line.innerText = 'Symbolisatie: ' + file.name;
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

});
