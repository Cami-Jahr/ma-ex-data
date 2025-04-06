import character_pages
import kioku_pages
import collect_max_stats
import uploader
import re

if __name__ == "__main__":
    if re.search("[Yy][eEsS]*", input("Is new char? [y/N]")) != None:
        collect_max_stats.run()
    character_pages.create_character_pages()
    kioku_pages.create_kioku_pages()
    uploader.upload()
