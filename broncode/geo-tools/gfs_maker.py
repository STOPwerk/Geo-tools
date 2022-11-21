#======================================================================
#
# /gfs_maker
#
#======================================================================
#
# Webpagina om een *.gfs bestand voor een GIO te maken.
# Functionaliteit wordt geïmplementeerd via client-side javascript
#
#======================================================================

from weergave_webpagina import WebpaginaGenerator

class GFSMaker:
    @staticmethod
    def Html():
        generator = WebpaginaGenerator ("GFS voor STOP GML")
        generator.LeesHtmlTemplate ('')
        generator.LeesCssTemplate ('')
        generator.LeesJSTemplate ('')
        return generator.Html ()
