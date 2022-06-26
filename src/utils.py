"""
utility functions.
"""
import csv
from bs4.element import NavigableString


def get_text(elt, ignore=None, drop=None):
    """
    get text from BeautifulSoup element
    """
    txt = elt if isinstance(elt, NavigableString) else elt.text
    return normalize_txt(txt, ignore, drop)

def decompose_list(element_list):
    """
    removes elements from their parent element
    """
    for elt in element_list:
        elt.decompose()

def normalize_txt(txt, ignore, drop):
    """
    clean text from undesired elements elements
    """
    if ignore is not None:
        for char in ignore:
            txt = txt.replace(char, ' ')
    if drop is not None:
        for char in drop:
            txt = txt.replace(char, '')
    return txt.strip()

def write_dict(list_to_write, path, delimiter='\t', mode='w'):
    """
    write list_to_write to path
    list_to_write is a list of dict
    """
    fieldnames = list(list_to_write[0].keys())
    with open(path, mode) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            delimiter=delimiter
            )
        writer.writeheader()
        writer.writerows(list_to_write)