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

    VoegOnderlaagToe(naam, dataNaam, symbolisatieNaam) {
        this._MaakKaartlaag(this._Onderlagen, naam, dataNaam, symbolisatieNaam);
        return this;
    }

    VoegOudNieuwLaagToe(naam, oudeDataNaam, nieuweDataNaam, symbolisatieNaam) {
        this._MaakKaartlaag(this._OudLagen, naam + ' (was)', oudeDataNaam, symbolisatieNaam);
        this._MaakKaartlaag(this._NieuwLagen, naam + ' (wordt)', nieuweDataNaam, symbolisatieNaam);
        return this;
    }

    _MaakKaartlaag(collectie, naam, dataNaam, symbolisatieNaam) {
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
        return layer;
    }

    Toon(kaartElementId) {
        // Bepaal eerst welk deel van Nederland getoond moet worden
        var legeRuimteOmGeometrie = 0.5;
        if (this._BBox === false) {
            this._BBox = Kaart._BGT_BBox;
            legeRuimteOmGeometrie = 0;
        }
        var zoomLevel = 20 - Kaart._BGT_Resolutions.length;
        const defaultSize = 500 * (1 - legeRuimteOmGeometrie);
        var elementSize = document.getElementById(kaartElementId).offsetWidth * (1 - legeRuimteOmGeometrie); if (elementSize <= 0) { elementSize = defaultSize; }
        var zoomLevelX = Math.max(Math.floor(Math.log2((elementSize * Kaart._BGT_Resolutions[0]) / (this._BBox[2] - this._BBox[0]))), 0);
        elementSize = document.getElementById(kaartElementId).offsetHeight * (1 - legeRuimteOmGeometrie); if (elementSize <= 0) { elementSize = defaultSize; }
        var zoomLevelY = Math.max(Math.floor(Math.log2((elementSize * Kaart._BGT_Resolutions[0]) / (this._BBox[3] - this._BBox[1]))), 0);
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

        // Tot slot de overlays
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
                closer.blur();
                return false;
            };
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
                            content += '<div>' + layer._PopupProperties[prop] + ': ' + attr[prop] + '</div>';
                        }
                    }
                });
                if (content !== false) {
                    popup_content.innerHTML = content;
                    popup_overlay.setPosition(e.coordinate);
                }
            });
        }
    }

    static _BGT_BBox = [-285401.92, 22598.08, 595401.9199999999, 903401.9199999999];
    static _BGT_Resolutions = [3440.64, 1720.32, 860.16, 430.08, 215.04, 107.52, 53.76, 26.88, 13.44, 6.72, 3.36, 1.68, 0.84, 0.42];
}

