#======================================================================
#
# /toon_gio_wijziging
#
#======================================================================
#
# Script om een GIO-wijziging samen met een was- en een wordt-versie 
# van de GIO te tonen in een viewer. De wordt-versie wordt afgeleid
# uit de wijziging en was-versie.
#
#======================================================================

from applicatie_meldingen import Meldingen
from applicatie_request import Parameters
from weergave_webpagina import WebpaginaGenerator

class GIOWijzigingViewer:
#======================================================================
#
# Webpagina's
#
#======================================================================
    @staticmethod
    def InvoerHtml():
        generator = WebpaginaGenerator ("Tonen van een GIO-wijziging")
        generator.LeesHtmlTemplate ('invoer')
        generator.LeesCssTemplate ('invoer')
        generator.LeesJSTemplate ('invoer')
        return generator.Html ()

    @staticmethod
    def ResultaatHtml(request : Parameters):
        log = Meldingen (False)
        log.Informatie ("Tonen van een GIO-wijziging, versie 2022-11-23 00:22:24.")
        try:
            generator = WebpaginaGenerator ("GIO-wijziging in beeld")
            generator.LeesHtmlTemplate ('resultaat')
            generator.LeesCssTemplate ('resultaat')
            generator.LeesJSTemplate ('resultaat')

            generator.VoegHtmlToe ("<h2>Verslag van het maken van de viewer</h2>")
            log.MaakHtml (generator, None)
            return generator.Html ()
        except Exception as e:
            log.Fout ("Oeps, deze fout is niet verwacht: " + str(e))
            generator = WebpaginaGenerator ("GIO-wijziging - geen beeld")
            log.MaakHtml (generator, None, "Het maken van de viewer voor de GIO-wijziging is afgebroken.")
            return generator.Html ()

