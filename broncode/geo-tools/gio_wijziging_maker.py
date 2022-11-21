#======================================================================
#
# /gio_wijziging
#
#======================================================================
#
# Webpagina om een *.sld bestand voor een STOP symbolisatie te maken.
# Functionaliteit wordt geïmplementeerd via client-side javascript.
#
#======================================================================

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from weergave_webpagina import WebpaginaGenerator

class GIOWijzigingMaker:
#======================================================================
#
# Webpagina's
#
#======================================================================
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("GIO-wijziging - invoer")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters):
        log = Meldingen (False)
        log.Informatie ("GIO-wijziging maker, versie @@@VERSIE@@@.")
        try:
            generator = WebpaginaGenerator ("GIO-wijziging - resultaat")
            generator.LeesHtmlTemplate ('')
            generator.LeesCssTemplate ('')
            generator.LeesJSTemplate ('')

            generator.VoegHtmlToe ("<h2>Verslag van de bepaling</h2>")
            log.MaakHtml (generator, None)
            return generator.Html ()
        except Exception as e:
            log.Fout ("Oeps, deze fout is niet verwacht: " + str(e))
            generator = WebpaginaGenerator ("GIO-wijziging - geen resultaat")
            log.MaakHtml (generator, None, "De bepaling van de GIO-wijziging is afgebroken.")
            return generator.Html ()

