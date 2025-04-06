import pywikibot as pwb
from pywikibot.specialbots import UploadRobot
import os


class WikiBot:
    def __init__(self):
        self.site = pwb.Site()
        self.site.login()

    def download_text(self, url):
        return pwb.Page(self.site, url).text

    def download_parsed_page(self, url):
        return pwb.Page(self.site, url).get_parsed_page()

    def image_usage(self, filename, namespaces=None):
        file = pwb.FilePage(self.site, filename)
        return list(file.using_pages(namespaces=namespaces))

    def image_exists(self, filename, namespaces=None) -> bool:
        file = pwb.FilePage(self.site, filename)
        return file.exists()

    def upload(self, url, text):
        page = pwb.Page(self.site, url)
        if page.text == text:  # Don't write if there's 0 changes
            return
        page.text = text
        page.save()

    def upload_image(
        self, file_path: str, target_filename=None, description=None, override=False
    ):
        if target_filename is None:
            target_filename = os.path.basename(file_path)
        if self.image_exists(target_filename) and not override:
            return

        upload_bot = UploadRobot(
            file_path,
            description=description or "Image uploaded by bot",
            use_filename=target_filename,
            keep_filename=True,
            verify_description=False,
            ignore_warning=True,
        )
        upload_bot.run()


wikibot = WikiBot()
