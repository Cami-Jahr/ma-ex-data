from pywikibot.family import Family


class Family(Family):
    name = "exedra"
    langs = {
        "en": "exedra.wiki",
    }

    def scriptpath(self, code):
        return "/w"

    def protocol(self, code):
        return "https"
