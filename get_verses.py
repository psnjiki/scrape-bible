
import time
from joblib import Parallel, delayed
from src.jwreader import Reader
from argparse import ArgumentParser


if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument('--save-dir', type=str, help='where to save the texts')
    parser.add_argument('--lang-url', type=str, help='language portion of language specific url')
    parser.add_argument('--min-chapter-num', type=int)
    parser.add_argument('--n-jobs', type=int)

    parsed_args = parser.parse_args().__dict__

    n_jobs = parsed_args['n_jobs']
    lang_url = parsed_args['save_dir']
    save_dir = parsed_args['lang_url']

    min_chapter_num = parsed_args['min_chapter_num']
    if min_chapter_num is None:
        min_chapter_num = -1

    rd = Reader(
        home_url="https://www.jw.org",
        lang_url=lang_url,
        save_dir=save_dir
        )

    def books_loop(book):
        start_time = time.time()
        chapters = rd.collect_chapters(books[book])
        for chapter in chapters:
            verses = rd.collect_verses(
                chapter=chapters[chapter],
                )
        end_time = time.time()
        duration = (end_time - start_time)/60
        print(books[book]["title"], f": \n completed in {duration} min")
        return verses

    books = rd.set_books()
    books = {k: v for k, v in books.items() if k >= min_chapter_num}

    Parallel(n_jobs=n_jobs)(
        delayed(books_loop)(book) for book in books
        )
