class Kaartgegevens {

    constructor() {
        this._GeoJSON = {};
        this._Symbolisaties = {};
    }

    VoegDataToe(naam, geoJSON) {
        this._GeoJSON[naam] = geoJSON;
        return this;
    }

    VoegSymbolisatieToe(naam, symbolisatie) {
        this._Symbolisaties[naam] = SLDReader.createOlStyleFunction(
            SLDReader.getStyle(
                SLDReader.getLayer(
                    SLDReader.Reader(`<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" version="1.1.0">
    <NamedLayer>
        <Name>Symbolisatie</Name>
        <UserStyle>
            <Name>Symbolisatie</Name>
` + symbolisatie + `
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>`)
                ), 'Symbolisatie'
            ).featuretypestyles[0]
        );
        return this;
    }

    static Instantie = new Kaartgegevens();
}


class Kaart {
    constructor() {
        this._Toplagen = [];
        this._OudLagen = [];
        this._NieuwLagen = [];
        this._Onderlagen = [];
        this._BBox = false;
        this._LagenMetProperties = 0;
    }
    static EPSG28992 = new ol.proj.Projection('urn:ogc:def:crs:EPSG::28992');

    VoegOnderlaagToe(naam, dataNaam, symbolisatieNaam, inControls = false, toonInitieel = true) {
        this._MaakKaartlaag(this._Onderlagen, naam, dataNaam, symbolisatieNaam, inControls, toonInitieel);
        return this;
    }

    VoegToplaagToe(naam, dataNaam, symbolisatieNaam, inControls = false, toonInitieel = true) {
        this._MaakKaartlaag(this._Toplagen, naam, dataNaam, symbolisatieNaam, inControls, toonInitieel);
        return this;
    }

    VoegOudLaagToe(naam, dataNaam, symbolisatieNaam, inControls = false, toonInitieel = true) {
        var layer = this._MaakKaartlaag(this._OudLagen, naam, dataNaam, symbolisatieNaam, inControls, toonInitieel);
        var self = this;
        layer.on('prerender', function (event) {
            var ctx = event.context;
            ctx.save();
            ctx.beginPath();
            ctx.rect(0, 0, self._SliderPositie, ctx.canvas.height);
            ctx.clip();
        });

        layer.on('postrender', function (event) {
            var ctx = event.context;
            ctx.restore();
        });
        return this;
    }
    VoegNieuwLaagToe(naam, dataNaam, symbolisatieNaam, inControls = false, toonInitieel = true) {
        var layer = this._MaakKaartlaag(this._NieuwLagen, naam, dataNaam, symbolisatieNaam, inControls, toonInitieel);
        var self = this;
        layer.on('prerender', function (event) {
            var ctx = event.context;
            ctx.save();
            ctx.beginPath();
            ctx.rect(self._SliderPositie, 0, ctx.canvas.width, ctx.canvas.height);
            ctx.clip();
        });

        layer.on('postrender', function (event) {
            var ctx = event.context;
            ctx.restore();
        });
        return this;
    }

    _MaakKaartlaag(collectie, naam, dataNaam, symbolisatieNaam, inControls, toonInitieel) {
        var geoJson = Kaartgegevens.Instantie._GeoJSON[dataNaam];
        if (this._BBox === false) {
            this._BBox = geoJson.bbox;
        } else {
            this._BBox = [
                (this._BBox[0] < geoJson.bbox[0] ? this._BBox[0] : geoJson.bbox[0]),
                (this._BBox[1] < geoJson.bbox[1] ? this._BBox[1] : geoJson.bbox[1]),
                (this._BBox[2] > geoJson.bbox[2] ? this._BBox[2] : geoJson.bbox[2]),
                (this._BBox[3] > geoJson.bbox[3] ? this._BBox[3] : geoJson.bbox[3])
            ];
        }
        var layer = new ol.layer.Vector({
            source: new ol.source.Vector({
                features: (new ol.format.GeoJSON()).readFeatures(geoJson),
                projection: Kaart.EPSG28992
            }),
            style: Kaartgegevens.Instantie._Symbolisaties[symbolisatieNaam]
        });
        collectie.push(layer);

        if (geoJson.properties !== undefined) {
            this._LagenMetProperties++;
            layer._PopupNaam = naam;
            layer._PopupProperties = geoJson.properties;
        }

        if (inControls) {
            layer._AanUit = naam;
            layer.setVisible(toonInitieel);
        } else {
            layer._AanUit = false
        }

        return layer;
    }

    Toon(kaartElementId, kaartElementWidth, kaartElementHeight) {
        var self = this;
        // Bepaal eerst welk deel van Nederland getoond moet worden
        var kaartElement = document.getElementById(kaartElementId);
        kaartElement.style.width = kaartElementWidth + "px"
        kaartElement.style.height = kaartElementHeight + "px"
        var legeRuimteOmGeometrie = 0.25;
        if (this._BBox === false) {
            this._BBox = Kaart._BGT_BBox;
            legeRuimteOmGeometrie = 0;
        }
        var zoomLevel = 20 - Kaart._BGT_Resolutions.length;
        var zoomLevelX = Math.max(Math.floor(Math.log2((kaartElementWidth * (1 - legeRuimteOmGeometrie) * Kaart._BGT_Resolutions[0]) / (this._BBox[2] - this._BBox[0]))), 0);
        var zoomLevelY = Math.max(Math.floor(Math.log2((kaartElementHeight * (1 - legeRuimteOmGeometrie) * Kaart._BGT_Resolutions[0]) / (this._BBox[3] - this._BBox[1]))), 0);
        zoomLevel += (zoomLevelX < zoomLevelY ? zoomLevelX : zoomLevelY);

        // Achtergrondkaart
        var matrixIds = [];
        for (var z = 0; z < Kaart._BGT_Resolutions.length; z++) {
            matrixIds.push('urn:ogc:def:crs:EPSG::28992:' + z);
        }
        var mapLayers = [new ol.layer.Tile({
            extent: Kaart._BGT_BBox,
            source: new ol.source.WMTS({
                url: 'https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0',
                layer: 'pastel',
                matrixSet: 'EPSG:28992',
                format: 'image/png',
                projection: Kaart.EPSG28992,
                tileGrid: new ol.tilegrid.WMTS({
                    origin: ol.extent.getTopLeft(Kaart._BGT_BBox),
                    resolutions: Kaart._BGT_Resolutions,
                    matrixIds: matrixIds
                })
            })
        })];

        // Eerst de onderste lagen
        for (var i = 0; i < this._Onderlagen.length; i++) {
            mapLayers.push(this._Onderlagen[i]);
        }

        // Dan de oud/nieuw lagen
        if (this._OudLagen.length > 0 || this._NieuwLagen.length > 0) {
            this._SliderPositie = kaartElementWidth / 2;
            for (var i = 0; i < this._OudLagen.length; i++) {
                mapLayers.push(this._OudLagen[i]);
            }
            for (var i = 0; i < this._NieuwLagen.length; i++) {
                mapLayers.push(this._NieuwLagen[i]);
            }
        }

        // Dan de bovenste lagen
        for (var i = 0; i < this._Toplagen.length; i++) {
            mapLayers.push(this._Toplagen[i]);
        }

        // Tot slot de overlays / popup
        var mapOverlays = []
        const popup_content = document.getElementById(kaartElementId + '_popup-content');
        const popup_closer = document.getElementById(kaartElementId + '_popup-closer');
        var popup_overlay = false;
        if (this._LagenMetProperties > 0) {
            // Popup wordt als overlay op de kaart getoond
            popup_overlay = new ol.Overlay({
                element: document.getElementById(kaartElementId + '_popup'),
                autoPan: true,
                autoPanAnimation: {
                    duration: 250
                }
            });
            mapOverlays.push(popup_overlay);

            popup_closer.onclick = function () {
                popup_overlay.setPosition(undefined);
                popup_closer.blur();
                return false;
            };
        } else {
            var popup = document.getElementById(kaartElementId + '_popup');
            if (popup) {
                popup.remove();
            }
        }

        // Maak het kaartbeeld
        var map = new ol.Map({
            layers: mapLayers,
            overlays: mapOverlays,
            target: kaartElementId,
            view: new ol.View({
                center: ol.extent.getCenter(this._BBox),
                zoom: zoomLevel
            })
        });
        map.render();

        if (this._LagenMetProperties > 0) {
            // Vulling van de popup
            const toonNamen = (this._LagenMetProperties > 1);
            map.on('click', function (e) {
                var content = false;
                map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {
                    if (layer._PopupNaam !== undefined) {
                        var attr = feature.getProperties();
                        if (content === false) {
                            content = '';
                        }
                        if (toonNamen) {
                            content += '<div><b>' + layer._PopupNaam + '</b></div>';
                        }
                        for (var prop in layer._PopupProperties) {
                            var info = layer._PopupProperties[prop]
                            content += '<div>' + info[0] + ': ' + attr[prop] + (info[1] ? ' ' + info[1] : '') + '</div>';
                        }
                    }
                });
                if (content !== false) {
                    popup_content.innerHTML = content;
                    popup_overlay.setPosition(e.coordinate);
                }
            });
        }
        if (this._OudLagen.length > 0 || this._NieuwLagen.length > 0) {
            var self = this;
            new Slider(kaartElement, function (positie) {
                self._SliderPositie = positie;
                map.render();
            })
        }

        this._AanUitLagen = {};
        var aanUitLagenElt = null;
        for (var i = mapLayers.length - 1; i >= 0; i--) {
            if (mapLayers[i]._AanUit) {
                if (aanUitLagenElt === null) {
                    aanUitLagenElt = document.createElement('p');
                    aanUitLagenElt.innerHTML = 'Gegevens in de kaart die wel/niet zichtbaar gemaakt kunnen worden:</br>'
                    kaartElement.insertAdjacentElement('afterend', aanUitLagenElt);
                } else {
                    aanUitLagenElt.append(document.createElement('br'));
                }
                var ctrl = document.createElement('input');
                ctrl.type = 'checkbox';
                ctrl.id = kaartElementId + '_laag_' + i;
                ctrl.checked = mapLayers[i].getVisible();
                aanUitLagenElt.append(ctrl);
                var label = document.createElement('label');
                label.htmlFor = ctrl.id;
                label.innerText = mapLayers[i]._AanUit
                aanUitLagenElt.append(label);
                this._AanUitLagen[ctrl.id] = [];
                for (var j = 0; j <= i; j++) {
                    if (mapLayers[j]._AanUit == mapLayers[i]._AanUit) {
                        this._AanUitLagen[ctrl.id].push(mapLayers[j]);
                        mapLayers[j]._AanUit = false;
                    }
                }
                ctrl.addEventListener('click', (e) => {
                    var layers = self._AanUitLagen[e.srcElement.id];
                    for (var k = 0; k < layers.length; k++) {
                        layers[k].setVisible(e.srcElement.checked);
                    }
                });
            }
        }
    }

    static _BGT_BBox = [-285401.92, 22598.08, 595401.9199999999, 903401.9199999999];
    static _BGT_Resolutions = [3440.64, 1720.32, 860.16, 430.08, 215.04, 107.52, 53.76, 26.88, 13.44, 6.72, 3.36, 1.68, 0.84, 0.42];
}

class Slider {
    // Inspiratie: https://www.w3schools.com/howto/howto_js_image_comparison.asp
    constructor(kaartElement, onSlide) {
        this._Kaartelement = kaartElement;
        var kaartRect = kaartElement.getBoundingClientRect();
        this._Left = kaartRect.left;
        this._Width = kaartRect.right - kaartRect.left;
        this._OnSlide = onSlide;
        this._Clicked = false;

        this._Sliders = [document.createElement("DIV"), document.createElement("DIV")];
        this._Sliders[0].setAttribute("class", "kaart-slider knop");
        this._Sliders[1].setAttribute("class", "kaart-slider lijn");
        this._Sliders[1].style.height = (kaartRect.bottom - kaartRect.top) + "px";
        var self = this;
        for (var i = 0; i < this._Sliders.length; i++) {
            var slider = this._Sliders[i]
            kaartElement.parentElement.insertBefore(slider, kaartElement);
            slider.style.top = ((kaartRect.top + kaartRect.bottom) / 2 - slider.offsetHeight / 2) + "px";
            slider.style.left = (this._Left + this._Width / 2 - slider.offsetWidth / 2) + "px";
            slider.addEventListener("mousedown", (e) => self._SlideReady(e));
            window.addEventListener("mouseup", (e) => self._SlideFinish(e));
            slider.addEventListener("touchstart", (e) => self._SlideReady(e));
        }
    }
    _SlideReady(e) {
        e.preventDefault();
        this._Clicked = true;
        var self = this;
        window.addEventListener("mousemove", (e) => self._SlideMove(e));
        window.addEventListener("touchmove", (e) => self._SlideMove(e));
    }
    _SlideFinish() {
        this._Clicked = false;
    }
    _SlideMove(e) {
        if (!this._Clicked) return false;
        var pos = this._GetCursorPos(e)
        if (pos < 0) pos = 0;
        if (pos > this._Width) pos = this._Width;
        for (var i = 0; i < this._Sliders.length; i++) {
            var slider = this._Sliders[i]
            slider.style.left = this._Left + (pos - (slider.offsetWidth / 2)) + "px";
        }
        this._OnSlide(pos)
    }
    _GetCursorPos(e) {
        e = (e.changedTouches) ? e.changedTouches[0] : e;
        var a = this._Kaartelement.getBoundingClientRect();
        var x = e.pageX - a.left;
        x = x - window.pageXOffset;
        return x;
    }
}

