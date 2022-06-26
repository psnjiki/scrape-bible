"""
tools for reading from bible onlline
Class: Trip
"""
import os
import requests
from bs4 import BeautifulSoup
from translator import utils

class Reader():
    def __init__(
            self, home_url, lang_url,
            classes_to_decompose=["footnoteLink", "parabreak",
                                  "xrefLink jsBibleLink"],
            chars_to_ignore=["\xa0", "\n", "\t", "  "],
            chars_to_drop=["\u200b", "ʹ", "·", "[", "]"],
            save_dir="./"
            ):
        self.home_url = home_url
        self.lang_url = lang_url
        self.language = lang_url.split('/')[1]
        self.classes_to_decompose = classes_to_decompose
        self.chars_to_ignore = chars_to_ignore
        self.chars_to_drop = chars_to_drop
        self.save_dir = os.path.join(
            save_dir,
            lang_url.split('/')[1]
            )
        self.books = None
        self.chapters = None
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def get_verse_content(self, verse):
        try:
            _ = verse.find(class_="verseNum").extract()
        except:
            pass
        try:
            _ = verse.find(class_="chapterNum").extract()
        except:
            pass
        for class_name in self.classes_to_decompose:
            utils.decompose_list(verse.find_all(class_=class_name))
        return utils.get_text(
            verse,
            ignore=self.chars_to_ignore,
            drop=self.chars_to_drop
            )

    def collect_books(self, save=True, save_path=None):
        # collect available books's (id, href) pairs
        url = f"{self.home_url}{self.lang_url}/"
        data = requests.get(url).text
        soup = BeautifulSoup(data, "lxml")
        soup = soup.find(
            "select",
            class_="jsPublicationFilter",
            id="Book"
            )
        books = {}
        for i, option in enumerate(soup.find_all("option")):
            href = utils.get_text(option)
            title = href.split("/")[-1]
            href = href.strip().replace(" ", "-")
            href = f"{url}{href}"
            key = int(option.get("value"))
            books[key] = {
                "book_num": key,
                "book_ref": href,
                "title": title
                }
        if save or save_path:
            if save_path is None:
                save_path = self.save_dir + "/books_ref.csv"
            utils.write_dict(
                list_to_write=list(books.values()),
                path=save_path,
                delimiter=",",
                mode='w'
                )
        return books

    def collect_chapters(self, book):
        # collect chapters from a particular book
        book_url = book["book_ref"]
        data = requests.get(book_url).text
        soup = BeautifulSoup(data, "lxml").find_all(
            "a", class_="chapter"
            )
        chapters = {}
        for elt in soup:
            key = int(elt.get('data-chapter'))
            chapters[key] = {
                **book,
                "chap_num": key,
                "chap_ref": f"{self.home_url}{elt.get('href')}"
                }
        return chapters

    def collect_verses(self, chapter, save=True, save_path=None, mode='a'):
        # collect verses from a particular chapter ref
        chap_ref = chapter["chap_ref"]
        data = requests.get(chap_ref).text
        soup = BeautifulSoup(data, "lxml").find(id="bibleText")
        soup_verses = soup.find_all(class_="verse")
        verses = []
        for i, verse in enumerate(soup_verses):
            verses.append(
                {
                    "book": chapter["title"],
                    "book_id": chapter["book_num"],
                    "chapter": chapter["chap_num"],
                    "verse": 1 + i,
                    "text": self.get_verse_content(verse)
                    }
                )
        if save or save_path:
            if save_path is None:
                save_path = self.save_dir + f"/{chapter['title']}.csv"
            utils.write_dict(
                list_to_write=verses,
                path=save_path,
                delimiter="\t",
                mode=mode
                )
        return verses

    def set_books(self, save=True, save_path=None):
        self.books = self.collect_books(save=save, save_path=save_path)
        return self.books

    def set_chapters(self, book_num):
        if self.books is None:
            _ = self.set_books()
        if self.chapters is None:
            self.chapters = {}
        self.chapters[book_num] = self.collect_chapters(self.books[book_num])
        return self.chapters[book_num]

    def get_chapters(self, book_num):
        if book_num not in self.chapters:
            _ = self.set_chapters(book_num)
        return self.chapters[book_num]

    def get_verses(self, book_num, chap_num, save=False, save_path=None):
        try:
            chapters = self.get_chapters(book_num)
        except:
            chapters = self.set_chapters(book_num)        
        return self.collect_verses(
            chapter=chapters[chap_num],
            save=save,
            save_path=save_path
            )
  