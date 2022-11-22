#======================================================================
#
# /sld_maker
#
#======================================================================
#
# Webpagina om een *.sld bestand voor een STOP symbolisatie te maken.
# Functionaliteit wordt geïmplementeerd via client-side javascript.
#
#======================================================================

from weergave_webpagina import WebpaginaGenerator

class SLDMaker:
    @staticmethod
    def Html():
        generator = WebpaginaGenerator ("SLD voor STOP symbolisatie")
        generator.LeesHtmlTemplate ('')
        generator.LeesCssTemplate ('')
        generator.LeesJSTemplate ('')
        return generator.Html ()
