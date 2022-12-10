
import math
import os.path

def CirkelNaarPolygon (x, y, r, maxAfwijking, starthoek = 0, eindhoek = 360):
    # Maximale hoek van hoekpunt - middelpunt - volgend hoekpunt:
    # r * (1- - cos (helve hoek)) <= maxAfwijking
    # halve hoek = acos (1 - maxAfwijking/r)
    halveHoek = math.acos (1 - maxAfwijking / r)
    deltaHoek = (2 * math.pi * math.fabs (eindhoek - starthoek)) / 360
    numSegmenten = math.ceil ( deltaHoek / (2 * halveHoek))
    segmentHoek = deltaHoek / numSegmenten * (1 if eindhoek > starthoek else -1)
    hoek = starthoek * (2 * math.pi) / 360
    gml = ''
    #gml = '<gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992"><gml:exterior><gml:LinearRing><gml:posList>'
    for i in range (0, numSegmenten+1):
        if i > 0:
            gml += ' '
        gml += "{:.2f}".format(x - r * math.sin (hoek)) + ' ' + "{:.2f}".format(y + r * math.cos (hoek))
        hoek += segmentHoek
    #gml += '</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon>'
    gml += '\n'
    return gml

with open (os.path.splitext(__file__)[0] + '.txt', 'w') as txtFile:
    txtFile.write ('Cirkel 98750,462500 r = 100, delta = 0.1 \n')
    txtFile.write (CirkelNaarPolygon (98750,462500, 100, 0.1))
    txtFile.write ('\nCirkel 98750,462500 r = 100, delta = 0.1 0 tot 180 \n')
    txtFile.write (CirkelNaarPolygon (98750,462500, 100, 0.1, 0, 180))
    txtFile.write ('Cirkel 98750,462500 r = 100, delta = 0.1 180 tot 360\n')
    txtFile.write (CirkelNaarPolygon (98750,462500, 100, 0.1, 180, 360))
    txtFile.write ('Cirkel 98750,462500 r = 200, delta = 0.1 360 tot 180\n')
    txtFile.write (CirkelNaarPolygon (98750,462500, 200, 0.1, 360, 180))


    txtFile.write ('\n\n\nCirkel 99250,462500 r = 100, delta = 5 \n')
    txtFile.write (CirkelNaarPolygon (99250,462500, 100, 5))
    txtFile.write ('\nCirkel 99250,462500 r = 100, delta = 5 \n')
    txtFile.write (CirkelNaarPolygon (99250,462500, 100, 5, 90, 90+360))
    txtFile.write ('Cirkel 99250,462500 r = 100, delta = 5 180 tot 0\n')
    txtFile.write (CirkelNaarPolygon (99250,462500, 100, 5, 360, 180))
    txtFile.write ('Cirkel 99250,462500 r = 150, delta = 5 0 tot 180\n')
    txtFile.write (CirkelNaarPolygon (99250,462500, 200, 5, 180, 360))

