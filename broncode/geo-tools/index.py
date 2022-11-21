#======================================================================
#
# Simulator als web applicatie: startpunt voor Flask / vercel hosting
#
#----------------------------------------------------------------------
#
# Een Flask web applicatie om de geo-tools online aan te bieden.
#
#======================================================================

from applicatie_request import Parameters
from weergave_webpagina import WebpaginaGenerator

from gfs_maker import GFSMaker
from sld_maker import SLDMaker
from gio_wijziging_maker import GIOWijzigingMaker


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
    generator.LeesHtmlTemplate ('')
    return generator.Html ()

@app.route('/gfs_maker')
def gfs_maker():
    return GFSMaker.Html ()

@app.route('/sld_maker')
def sld_maker():
    return SLDMaker.Html ()

@app.route('/gio_wijziging')
def gio_wijziging():
    return GIOWijzigingMaker.InvoerHtml ()

@app.route('/gio_wijziging_resultaat', methods = ['POST'])
def gio_wijziging_resultaat():
    return GIOWijzigingMaker.ResultaatHtml (Parameters (request.form, request.files, None))

#----------------------------------------------------------------------
#
# Flask server voor ontwikkeling
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
