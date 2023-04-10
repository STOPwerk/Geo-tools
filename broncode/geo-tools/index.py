#======================================================================
#
# Simulator als web applicatie: startpunt voor Flask / vercel hosting
#
#----------------------------------------------------------------------
#
# Een Flask web applicatie om de geo-tools online aan te bieden.
#
#======================================================================

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from weergave_webpagina import WebpaginaGenerator

from gfs_maker import GFSMaker
from sld_maker import SLDMaker
from operatie_toon_geo import ToonGeo
from operatie_maak_gio_wijziging import MaakGIOWijziging
from operatie_toon_gio_wijziging import ToonGIOWijziging
from voorbeeld import Voorbeeld


#----------------------------------------------------------------------
# Flask app
#----------------------------------------------------------------------
from flask import Flask, request
app = Flask("STOPwerk Geo-tools")
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#----------------------------------------------------------------------
#
# Routering
#
#----------------------------------------------------------------------
@app.route('/')
def index():
    """Startpagina"""
    generator = WebpaginaGenerator ("Geo-tools online")
    generator.LeesHtmlTemplate ('pagina')
    return generator.Html ()

@app.route('/gfs_maker')
def gfs_maker():
    return GFSMaker.Html ()

@app.route('/sld_maker')
def sld_maker():
    return SLDMaker.Html ()

@app.route('/toon_geo')
def toon_geo():
    return ToonGeo.InvoerHtml ()

@app.route('/toon_geo_resultaat', methods = ['POST'])
def toon_geo_resultaat():
    return ToonGeo.ResultaatHtml (Parameters (None, request.form, request.files, None), Meldingen (True))

@app.route('/maak_gio_wijziging')
def gio_wijziging():
    return MaakGIOWijziging.InvoerHtml ()

@app.route('/maak_gio_wijziging_resultaat', methods = ['POST'])
def gio_wijziging_resultaat():
    return MaakGIOWijziging.ResultaatHtml (Parameters (None, request.form, request.files, None), Meldingen (True))


@app.route('/toon_gio_wijziging')
def toon_gio_wijziging():
    return ToonGIOWijziging.InvoerHtml ()

@app.route('/toon_gio_wijziging_resultaat', methods = ['POST'])
def toon_gio_wijziging_resultaat():
    return ToonGIOWijziging.ResultaatHtml (Parameters (None, request.form, request.files, None), Meldingen (True))

@app.route('/voorbeeld')
def voorbeeld():
    return Voorbeeld.SelectieHtml ()

@app.route('/start_voorbeeld')
def start_voorbeeld():
    return Voorbeeld.VoerUit (Parameters (None, request.args, None, None))

#----------------------------------------------------------------------
#
# Flask server voor ontwikkeling
# Wordt niet gebruikt bij starten vanuit Visual Studio
#
#----------------------------------------------------------------------
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
