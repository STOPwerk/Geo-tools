window.addEventListener('load', function () {

    // ======================================================================
    // Input en functie om de GFS te maken
    // ======================================================================
    function GFSMaker(type) {
        this.Bestandsnaam = false;
        this.Type = type;
        this.GIOWijzigingOnderdeel = '-';
        this.GeometrieType = '-';
        this.SRS = '-';
        this.HeeftNaam = true;
        this.AttribuutNaam = '-'

        this.MaakGFS = function () {
            var geometrieNaam = ' <!-- moet nog gekozen worden -->';
            if (this.GeometrieType === 'Point' || this.GeometrieType === 'MultiPoint') {
                geometrieNaam = ' - punten';
            }
            else if (this.GeometrieType === 'Line' || this.GeometrieType === 'MultiLine') {
                geometrieNaam = ' - lijnen';
            }
            else if (this.GeometrieType === 'Polygon' || this.GeometrieType === 'MultiPolygon') {
                geometrieNaam = ' - vlakken';
            }
            var gfs = `<GMLFeatureClassList>
    <!--
        Gebruik dit *.gfs bestand om de data uit ` + (this.Bestandsnaam ? this.Bestandsnaam : (this.Type === 'EG' ? 'een effectgebied/gebiedsmarkering' : 'een GIO')) + ` in te lezen
        in software die de OGR/GDAL specificatie ondersteunt.
        Gemaakt met @@@GeoTools_Online_Url@@@gfs_maker
    -->
    <GMLFeatureClass>`;

            if (this.Type === 'GIO') {
                gfs += `
        <Name>` + this._LaagNaam() + geometrieNaam + `</Name>
        <ElementPath>vastgesteldeVersie|GeoInformatieObjectVersie|locaties|Locatie</ElementPath>`;
            } else if (this.Type === 'CGIO') {
                gfs += `
        <Name>` + this._LaagNaam() + geometrieNaam + `</Name>
        <ElementPath>locaties|Locatie</ElementPath>`;
            } else if (this.Type === 'EG') {
                gfs += `
        <Name>` + this._LaagNaam() + geometrieNaam + `</Name>
        <ElementPath>Gebied</ElementPath>`;
            } else if (this.GIOWijzigingOnderdeel === 'was' || this.GIOWijzigingOnderdeel == 'wordt') {
                gfs += `
        <Name>` + this._LaagNaam() + ' (' + this.GIOWijzigingOnderdeel + ')' + geometrieNaam + `</Name>
        <ElementPath>vastgesteldeVersie|GeoInformatieObjectMutatie|` + this.GIOWijzigingOnderdeel + `|Locatie</ElementPath>`;
            } else if (this.GIOWijzigingOnderdeel === 'wijzigmarkering') {
                gfs += `
        <Name>` + this._LaagNaam() + ' (' + this.GIOWijzigingOnderdeel + `)</Name>
        <ElementPath>vastgesteldeVersie|GeoInformatieObjectMutatie|wijzigmarkering|Gebied</ElementPath>`;
            } else {
                gfs += `
        <Name>` + this._LaagNaam() + ` (welk onderdeel?)</Name>
        <ElementPath>vastgesteldeVersie|GeoInformatieObjectMutatie|<!-- moet nog gekozen worden --></ElementPath>`;
            }

            gfs += `
        <GeometryName>geometrie</GeometryName>
        <GeometryElementPath>geometrie|Geometrie|geometrie</GeometryElementPath>
        <GeometryType>` + (this.GeometrieType === '-' ? '<!-- Nog te kiezen -->' : this.GeometrieType) + `</GeometryType>
        <SRSName>` + (this.SRS === '-' ? '<!-- Nog te kiezen -->' : this.SRS) + `</SRSName>`;

            if (this.GIOWijzigingOnderdeel === 'wijzigmarkering') {
                if (this.HeeftNaam) {
                    gfs += `
        <PropertyDefn>
            <Name>label</Name>
            <ElementPath>label</ElementPath>
            <Type>String</Type>
        </PropertyDefn>`;
                }
            } else if (this.Type === 'EG') {
                if (this.HeeftNaam) {
                    gfs += `
        <PropertyDefn>
            <Name>label</Name>
            <ElementPath>label</ElementPath>
            <Type>String</Type>
        </PropertyDefn>`;
                }
            } else {
                if (this.HeeftNaam) {
                    gfs += `
        <PropertyDefn>
            <Name>naam</Name>
            <ElementPath>naam</ElementPath>
            <Type>String</Type>
        </PropertyDefn>`;
                }
                if (this.AttribuutNaam !== '-') {
                    gfs += `
        <PropertyDefn>
            <Name>` + this.AttribuutNaam + `</Name>
            <ElementPath>` + this.AttribuutNaam + `</ElementPath>
            <Type>` + (this.AttribuutNaam === 'kwantitatieveNormwaarde' ? 'Real' : 'String') + `</Type>
        </PropertyDefn>`;
                }
            }

            gfs += `
    </GMLFeatureClass>
</GMLFeatureClassList>`;
            return gfs;
        }

        this.GFSFileNaam = function () {
            if (this.Bestandsnaam) {
                return this.Bestandsnaam.replace(/\.[^/.]+$/, '.gfs');
            } else if (this.Type === 'EG') {
                return 'Gebied.gfs';
            } else {
                return 'GIO.gfs';
            }
        }
        this._LaagNaam = function () {
            if (this.Bestandsnaam) {
                return this.Bestandsnaam.replace(/\.[^/.]+$/, '');
            } else if (this.Type === 'GIO') {
                return 'Vastgestelde GIO-versie';
            } else if (this.Type === 'CGIO') {
                return 'GIO-versie';
            } else if (this.Type === 'EG') {
                return 'Gebiedsmarkering/effectgebied';
            } else {
                return 'GIO-wijziging';
            }
        }

        this.GFSAlsDownload = function (downloadLink, fileNaam) {
            if ((this.Type === 'GIOW' && this.GIOWijzigingOnderdeel === '-') || this.GeometrieType === '-' || this.SRS === '-') {
                return false;
            } else {
                var textFileAsBlob = new Blob([this.MaakGFS()], { type: 'text/xml' });
                downloadLink.download = this.GFSFileNaam(fileNaam);
                if (window.webkitURL !== null) {
                    downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
                }
                else {
                    downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
                }
                return true
            }
        }
    }

    // ======================================================================
    // Afhandeling van de handmatige invoer
    // ======================================================================
    function CheckedValue(name) {
        var elt = document.querySelector('#handmatig_form input[name="' + name + '"]:checked');
        if (elt) {
            return elt.value;
        }
        return '-';
    }

    function VerwerkInvoervelden() {

        var maker = new GFSMaker(CheckedValue('type'));
        maker.GIOWijzigingOnderdeel = (maker.Type === 'GIOW' ? CheckedValue('giow') : '-');
        maker.GeometrieType = (maker.GIOWijzigingOnderdeel !== 'wijzigmarkering' ? CheckedValue('geo') : 'Polygon');
        maker.SRS = CheckedValue('srs');
        maker.AttribuutNaam = (maker.Type !== 'EG' && maker.GIOWijzigingOnderdeel !== 'wijzigmarkering' ? CheckedValue('attr') : '-');

        document.querySelectorAll('tr[class]').forEach((elt) => {
            if (maker.Type === 'GIOW') {
                if (elt.classList.contains('geen_giow')) {
                    elt.classList.remove('geen_giow');
                    elt.classList.add('voor_giow');
                }
            } else {
                if (elt.classList.contains('voor_giow')) {
                    elt.classList.remove('voor_giow');
                    elt.classList.add('geen_giow');
                }
            }
            if (maker.GIOWijzigingOnderdeel === 'wijzigmarkering') {
                if (elt.classList.contains('niet_voor_wm')) {
                    elt.classList.remove('niet_voor_wm');
                    elt.classList.add('geen_niet_voor_wm');
                }
            } else {
                if (elt.classList.contains('geen_niet_voor_wm')) {
                    elt.classList.remove('geen_niet_voor_wm');
                    elt.classList.add('niet_voor_wm');
                }
            }
            if (maker.Type !== 'EG' && maker.GIOWijzigingOnderdeel !== 'wijzigmarkering') {
                if (elt.classList.contains('geen_gio')) {
                    elt.classList.remove('geen_gio');
                    elt.classList.add('voor_gio');
                }
            } else {
                if (elt.classList.contains('voor_gio')) {
                    elt.classList.remove('voor_gio');
                    elt.classList.add('geen_gio');
                }
            }
        });


        var gfs = maker.MaakGFS();
        document.getElementById('handmatig_gfs').value = gfs;

        var downloadLink = document.getElementById('handmatig_download');
        if (maker.GFSAlsDownload(downloadLink)) {
            downloadLink.style.visibility = 'visible';
        } else {
            downloadLink.style.visibility = 'hidden';
        }
    }
    VerwerkInvoervelden();

    document.querySelectorAll('#handmatig_form input[type=radio]').forEach((elt) => {
        elt.addEventListener('click', VerwerkInvoervelden);
    });

    // ======================================================================
    // Afhandeling van de automatische detectie
    // ======================================================================
    const fileInput = document.querySelector('#autodetect_form [name="files[]"');

    function FileLezer(file, line) {
        this._Line = line;
        this._File = file;

        this._InterpreteerGML = function (gml) {
            var maker = null;
            var fragmenten = [];
            if (gml.match(/\<([^:]+:){0,1}Gebiedsmarkering[\s>]/) || gml.match(/\<([^:]+:){0,1}Effectgebied[\s>]/)) {
                maker = new GFSMaker('EG');
                fragmenten.push({
                    onderdeel: '',
                    gml: gml,
                    update: function (m) { }
                });
                maker.HeeftNaam = gml.match(/\<([^:]+:){0,1}label[\s>]/);
            }
            else {
                if (gml.match(/\<([^:]+:){0,1}GeoInformatieObjectVaststelling[\s>]/)) {
                    if (gml.match(/\<([^:]+:){0,1}GeoInformatieObjectMutatie[\s>]/)) {
                        maker = new GFSMaker('GIOW');
                        var gmlFragment = gml.replace(/.*\<([^:]+:){0,1}was[\s>]/gs, '').replace(/\<\/([^:]+:){0,1}was[\s>].*$/gs, '')
                        var heeftNaam = gmlFragment.match(/\<([^:]+:){0,1}naam[\s>]/);
                        fragmenten.push({
                            onderdeel: 'was - ',
                            gml: gmlFragment,
                            update: function (m) { m.GIOWijzigingOnderdeel = 'was'; m.HeeftNaam = heeftNaam; }
                        });
                        gmlFragment = gml.replace(/.*\<([^:]+:){0,1}wordt[\s>]/gs, '').replace(/\<\/([^:]+:){0,1}wordt[\s>].*$/gs, '')
                        heeftNaam = gmlFragment.match(/\<([^:]+:){0,1}naam[\s>]/);
                        fragmenten.push({
                            onderdeel: 'wordt - ',
                            gml: gmlFragment,
                            update: function (m) { m.GIOWijzigingOnderdeel = 'wordt'; m.HeeftNaam = heeftNaam; }
                        });
                        gmlFragment = gml.replace(/.*\<([^:]+:){0,1}wijzigmarkering[\s>]/gs, '').replace(/\<\/([^:]+:){0,1}wijzigmarkering[\s>].*$/gs, '')
                        heeftNaam = gmlFragment.match(/\<([^:]+:){0,1}label[\s>]/);
                        fragmenten.push({
                            onderdeel: 'wijzigmarkering - ',
                            gml: gmlFragment,
                            update: function (m) { m.GIOWijzigingOnderdeel = 'wijzigmarkering'; m.HeeftNaam = heeftNaam; }
                        });
                    } else {
                        maker = new GFSMaker('GIO');
                        maker.HeeftNaam = gml.match(/\<([^:]+:){0,1}naam[\s>]/);
                        fragmenten.push({
                            onderdeel: '',
                            gml: gml,
                            update: function (m) { }
                        });
                    }
                }
                else if (gml.match(/\<([^:]+:){0,1}GeoInformatieObjectVersie[\s>]/)) {
                    maker = new GFSMaker('CGIO');
                    maker.HeeftNaam = gml.match(/\<([^:]+:){0,1}naam[\s>]/);
                    fragmenten.push({
                        onderdeel: '',
                        gml: gml,
                        update: function (m) { }
                    });
                }
                else {
                    this._Line.innerText = file.name + ' is niet herkend als STOP GML module.';
                    return;
                }
                if (gml.match(/\<([^:]+:){0,1}kwantitatieveNormwaarde[\s>]/)) {
                    maker.AttribuutNaam = 'kwantitatieveNormwaarde';
                }
                else if (gml.match(/\<([^:]+:){0,1}kwalitatieveNormwaarde[\s>]/)) {
                    maker.AttribuutNaam = 'kwalitatieveNormwaarde';
                } else if (gml.match(/\<([^:]+:){0,1}groepID[\s>]/)) {
                    maker.AttribuutNaam = 'groepID';
                }
            }
            if (gml.match(/"urn:ogc:def:crs:EPSG::4258"/)) {
                maker.SRS = 'urn:ogc:def:crs:EPSG::4258';
            }
            else if (gml.match(/"urn:ogc:def:crs:EPSG::28992"/) || gml.match(/"EPSG:28992"/)) {
                maker.SRS = 'urn:ogc:def:crs:EPSG::28992';
            }
            else {
                this._Line.innerText = file.name + ': srsName niet herkend.';
                return;
            }
            maker.Bestandsnaam = file.name;
            this._Line.innerText = file.name + ': ';
            this._Eerste = true;
            for (var i = 0; i < fragmenten.length; i++) {
                fragmenten[i].update(maker);
                var gml = fragmenten[i].gml;
                if (maker.GIOWijzigingOnderdeel != 'wijzigmarkering') {
                    if (gml.match(/\<([^:]+:){0,1}MultiPoint[\s>]/)) {
                        maker.GeometrieType = 'MultiPoint';
                        this._MaakDownloadLink(maker, fragmenten[i].onderdeel + 'punten');
                    }
                    else if (gml.match(/\<([^:]+:){0,1}Point[\s>]/)) {
                        maker.GeometrieType = 'Point';
                        this._MaakDownloadLink(maker, fragmenten[i].onderdeel + 'punten');
                    }
                    if (gml.match(/\<([^:]+:){0,1}MultiLine[\s>]/)) {
                        maker.GeometrieType = 'MultiLine';
                        this._MaakDownloadLink(maker, fragmenten[i].onderdeel + 'lijnen');
                    }
                    else if (gml.match(/\<([^:]+:){0,1}LineString[\s>]/)) {
                        maker.GeometrieType = 'Line';
                        this._MaakDownloadLink(maker, fragmenten[i].onderdeel + 'lijnen');
                    }
                }
                if (gml.match(/\<([^:]+:){0,1}MultiSurface[\s>]/) || gml.match(/\<([^:]+:){0,1}MultiPolygon[\s>]/)) {
                    maker.GeometrieType = 'MultiPolygon';
                    this._MaakDownloadLink(maker, fragmenten[i].onderdeel + 'vlakken');
                }
                else if (gml.match(/\<([^:]+:){0,1}Polygon[\s>]/)) {
                    maker.GeometrieType = 'Polygon';
                    this._MaakDownloadLink(maker, fragmenten[i].onderdeel + 'vlakken');
                }
            }

        }
        this._MaakDownloadLink = function (maker, onderdeel) {
            var downloadLink = document.createElement('a');
            downloadLink.href = '#';
            var fileNaam = maker.GFSFileNaam();
            downloadLink.innerText = fileNaam + ' (' + onderdeel + ')';
            if (maker.GFSAlsDownload(downloadLink, fileNaam)) {
                if (this._Eerste) {
                    this._Eerste = false;
                } else {
                    var span = document.createElement('span')
                    span.innerText = ', ';
                    this._Line.appendChild(span);
                }
                this._Line.appendChild(downloadLink);
            }
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

    function DetecteerGMLType() {
        var container = document.getElementById('autodetect_links');
        container.innerHTML = '';

        for (var i = 0; i < fileInput.files.length; i++) {
            var file = fileInput.files[i];
            var line = document.createElement('div');
            container.appendChild(line);

            if (!file.name.toLowerCase().endsWith('.gml')) {
                line.innerText = file.name + ' is geen GML bestand';
            } else {
                line.innerText = 'Analyseer ' + file.name + '...';

                new FileLezer(file, line).VoerUit();
            }
        }
    }


    const box = document.querySelector('#autodetect_form .box');
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
        DetecteerGMLType();
    }, false);

    fileInput.addEventListener('click', function (e) {
        DetecteerGMLType();
    });

});
