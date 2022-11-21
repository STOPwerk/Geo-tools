import json
import os

# Data verkregen met https://data.ndw.nu/api/rest/static-road-data/traffic-signs/v1/current-state?rvv_code=B07
# Uitgevoerd 17-11-2022

datadir = os.path.dirname (os.path.realpath (__file__))

with open (os.path.join (datadir, 'verkeersborden_STOP.json'), 'r') as json_file:
    data = json.load (json_file)

borden = [{
            "x": pt["location"]["rd"]["x"],
            "y": pt["location"]["rd"]["y"],
            "gemeente": pt["location"]["county"]["code"],
            "jaar": int(pt["details"]["first_seen"][6:10])
          } 
          for pt in data]

def __GIO (filename, version, filter):
    with open (os.path.join (datadir, filename), 'w') as gml_file:
        gml_file.write ('''<?xml version="1.0" encoding="UTF-8"?>
    <geo:GeoInformatieObjectVersie schemaversie="1.3.0"
      xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
      xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
      xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/"
      xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="https://standaarden.overheid.nl/stop/imop/geo/
      https://standaarden.overheid.nl/stop/1.3.0/imop-geo.xsd">
        <geo:FRBRWork>/join/id/regdata/mnre9999/2022/stopborden</geo:FRBRWork>
        <geo:FRBRExpression>/join/id/regdata/mnre9999/2022/stopborden/nld@''' + version + '''</geo:FRBRExpression>
        <geo:locaties>''')
        index = 0
        for b in borden:
            index += 1
            if filter(b):
                gml_file.write ('''
                <geo:Locatie>
                    <geo:geometrie>
                        <basisgeo:Geometrie>
                            <basisgeo:id>37b0a09f-36a0-4e69-80c1-''' + str(index).zfill(12) + '''</basisgeo:id>
                            <basisgeo:geometrie>
                                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992">
                                    <gml:pos>''' + b['x'] + ' ' + b['y'] + '''</gml:pos>
                                </gml:Point>
                            </basisgeo:geometrie>
                        </basisgeo:Geometrie>
                    </geo:geometrie>
                </geo:Locatie>''')
        gml_file.write ('''
        </geo:locaties>
    </geo:GeoInformatieObjectVersie>
    ''')

__GIO ('verkeersborden_STOP_was.gml', '2019', lambda b: b["jaar"] <= 2019)
__GIO ('verkeersborden_STOP_wordt.gml', '2022', lambda b: b["jaar"] <= 2016 or b["jaar"] >= 2020)
