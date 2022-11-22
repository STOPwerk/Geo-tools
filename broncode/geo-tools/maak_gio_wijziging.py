#======================================================================
#
# /gio_wijziging
#
#======================================================================
#
# Script om een GIO-wijziging samen te stellen uit een was- en 
# een wordt-versie van een GIO.
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
        generator = WebpaginaGenerator ("Bepaling van een GIO-wijziging")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters):
        log = Meldingen (False)
        log.Informatie ("Bepaling van een GIO-wijziging, versie 2022-11-23 00:25:27.")
        try:
            generator = WebpaginaGenerator ("GIO-wijziging")
            generator.LeesHtmlTemplate ('resultaat')
            generator.LeesCssTemplate ('resultaat')
            generator.LeesJSTemplate ('resultaat')

            generator.VoegHtmlToe ("<h2>Verslag van de bepaling</h2>")
            log.MaakHtml (generator, None)
            return generator.Html ()
        except Exception as e:
            log.Fout ("Oeps, deze fout is niet verwacht: " + str(e))
            generator = WebpaginaGenerator ("GIO-wijziging - geen resultaat")
            log.MaakHtml (generator, None, "De bepaling van de GIO-wijziging is afgebroken.")
            return generator.Html ()

