window.addEventListener('load', function () {

    // ======================================================================
    // Basale validatie
    // ======================================================================
    const wasFile = document.getElementById('was');
    const wordtFile = document.getElementById('wordt');
    const startknop = this.document.getElementById("startknop");

    function UpdateControlStatus() {

        var heeftWas = 0;
        var heeftWordt = 0;

        var container = document.getElementById('bestanden');
        container.innerHTML = '';

        for (var i = 0; i < wasFile.files.length; i++) {
            var file = wasFile.files[i];
            var line = document.createElement('div');
            container.appendChild(line);
            line.innerText = 'Was-versie: ' + file.name;
            heeftWas++;
        }
        for (var i = 0; i < wordtFile.files.length; i++) {
            var file = wordtFile.files[i];
            var line = document.createElement('div');
            container.appendChild(line);
            line.innerText = 'Wordt-versie: ' + file.name;
            heeftWordt++;
        }
        if (heeftWas > 1 || heeftWordt > 1) {
            var line = document.createElement('div');
            container.appendChild(line);
            line.innerText = 'Er mag maar 1 was-versie en 1 wordt-versie geselecteerd zijn!';
        }
        startknop.disabled = heeftWas != 1 || heeftWordt != 1;
    }
    UpdateControlStatus();

    // Event handlers
    wasFile.addEventListener('click', function (e) {
        UpdateControlStatus();
    });
    wordtFile.addEventListener('click', function (e) {
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
    InitBox(document.getElementById('wordt_box'), wordtFile);

});
