window.addEventListener('load', function () {

    // ======================================================================
    // Basale validatie
    // ======================================================================
    const wasFile = document.getElementById('was');
    const wijzigingFile = document.getElementById('wijziging');
    const symbolisatieFile = document.getElementById('symbolisatie');
    const startknop = this.document.getElementById("startknop");

    function UpdateControlStatus() {

        var heeftWas = 0;
        var heeftWijziging = 0;
        var heeftSymbolisatie = 0;

        var container = document.getElementById('bestanden');
        container.innerHTML = '';
        const titel = document.getElementById('titel');
        titel.value = '';

        for (var i = 0; i < wasFile.files.length; i++) {
            var file = wasFile.files[i];
            var line = document.createElement('div');
            container.appendChild(line);
            line.innerText = 'Was-versie: ' + file.name;
            heeftWas++;
        }
        for (var i = 0; i < wijzigingFile.files.length; i++) {
            var file = wijzigingFile.files[i];
            var line = document.createElement('div');
            container.appendChild(line);
            line.innerText = 'GIO-wijziging: ' + file.name;
            heeftWijziging++;
            if (i == 0) {
                titel.value = file.name;
            }
        }
        for (var i = 0; i < symbolisatieFile.files.length; i++) {
            var file = symbolisatieFile.files[i];
            var line = document.createElement('div');
            container.appendChild(line);
            line.innerText = 'Symbolisatie: ' + file.name;
            heeftSymbolisatie++;
        }
        if (heeftWas > 1 || heeftWijziging > 1 || heeftSymbolisatie > 1) {
            var line = document.createElement('div');
            container.appendChild(line);
            line.innerText = 'Er mag maar 1 was-versie, 1 GIO-wijziging en hooguit 1 symbolisatie geselecteerd zijn!';
        }
        startknop.disabled = heeftWas != 1 || heeftWijziging != 1 || heeftSymbolisatie > 1;
    }
    UpdateControlStatus();

    // Event handlers
    wasFile.addEventListener('click', function (e) {
        UpdateControlStatus();
    });
    wijzigingFile.addEventListener('click', function (e) {
        UpdateControlStatus();
    });
    symbolisatieFile.addEventListener('click', function (e) {
        UpdateControlStatus();
    });
    function InitBox(box, fileInput) {
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
            UpdateControlStatus();
        }, false);
    }
    InitBox(document.getElementById('was_box'), wasFile);
    InitBox(document.getElementById('wijziging_box'), wijzigingFile);
    InitBox(document.getElementById('symbolisatie_box'), wijzigingFile);
});
