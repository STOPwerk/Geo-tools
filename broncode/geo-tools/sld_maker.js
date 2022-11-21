window.addEventListener('load', function () {

    const fileInput = document.querySelector('#upload_form [name="files[]"');

    function FileLezer(file, line) {
        this._Line = line;
        this._File = file;

        this._InterpreteerXML = function (xml) {
            var start = /\<([^:]+:){0,1}FeatureTypeStyle[\s>]/s.exec(xml);

            if (start !== null) {
                var einde = /\<\/([^:]+:){0,1}FeatureTypeStyle[^>]*>/s.exec(xml);
                if (einde !== null) {
                    this._Line.innerText = file.name + ': ';

                    sld = `<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd"
	version="1.1.0">
    <!--
    Gemaakt met @@@GeoTools_Online_Url@@@sld_maker
    -->
	<NamedLayer>
		<Name>STOP symbolisatie</Name>
		<UserStyle>
			<Name>` + this._File.name + `</Name>
` + xml.substring(start.index, einde.index) + einde[0] + `
		</UserStyle>
	</NamedLayer>
</StyledLayerDescriptor>`;
                    var downloadLink = document.createElement('a');
                    downloadLink.href = '#';
                    var fileNaam = this._File.name.replace(/\.[^/.]+$/, '.sld');
                    downloadLink.innerText = fileNaam;
                    downloadLink.download = fileNaam;
                    var textFileAsBlob = new Blob([sld], { type: 'text/xml' });
                    if (window.webkitURL != null) {
                        downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
                    }
                    else {
                        downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
                    }
                    if (this._Eerste) {
                        this._Eerste = false;
                    } else {
                        var span = document.createElement('span')
                        span.innerText = ', ';
                        this._Line.appendChild(span);
                    }
                    this._Line.appendChild(downloadLink);
                    return;
                }
            }
            this._Line.innerText = file.name + ' bevat geen STOP symbolisatiemodule';

        }

        const This = this;
        const reader = new FileReader();
        this.VoerUit = function(){
            reader.addEventListener("load", () => {
                This._InterpreteerXML(reader.result);
            }, false);
            reader.readAsText(file);
        }
    }

    function MaakSLDBestanden() {
        var container = document.getElementById('upload_links');
        container.innerHTML = '';

        for (var i = 0; i < fileInput.files.length; i++) {
            var file = fileInput.files[i];
            var line = document.createElement('div');
            container.appendChild(line);

            line.innerText = 'Analyseer ' + file.name + '...';
            new FileLezer(file, line).VoerUit();
        }
    }


    const box = document.querySelector('#upload_form .box');
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
        MaakSLDBestanden();
    }, false);

    fileInput.addEventListener('click', function (e) {
        MaakSLDBestanden();
    });

});
