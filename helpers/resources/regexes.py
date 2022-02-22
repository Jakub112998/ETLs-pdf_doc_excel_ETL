from typing import List
import re


def regex_part_name_row(row: str) -> bool:
    # print("regex_part_name_row")
    # print(row)
    # print(type(row))
    for el in row:
        if 'Pakiet nr' in el:
            # match everything after test
            # re.search(r'(?<=test).*', row)
            after = re.search(r'(?<=Pakiet nr).*', el)
            # print(after)
            return True
        elif 'Czesc nr' in el:
            after = re.search(r'(?<=Czesc nr).*', el)
            # print(after)
            return True
        elif 'Część nr' in el:
            after = re.search(r'(?<=Część nr).*', el)
            # print(after)
            return True
    patterns = [
        r"Część nr [0-9]*\.[0-9]+"
        r"Czesr nr [0-9]*\.[0-9]+",
        r"Pakiet nr [0-9]*\.[0-9]+",
        r"[a-zA-Z]+ęść\s[a-zA-Z] + ([+-]?(?=\.\d | \d)(?:\d +)?(?:\.?\d *))(?:[eE]([+-]?\d+))?",
        r"[a-zA-Z]+\s[a-zA-Z]+\s([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?",
    ]
    for str_pattern in patterns:
        for el in row:
            pattern = re.compile(str_pattern)
            # print(pattern.match(el, re.IGNORECASE))
            if pattern.match(el, re.IGNORECASE):
                after = re.search(fr'(?<={pattern}).*', el)
                return True

    return False


def regex_header_row(row: List[str]) -> bool:
    if any(word in row for word in ["Lp", "L.p.", "Nr poz."]):
        return True
    return False


def regex_data_row(row: List[str]) -> bool:
    """
    tutaj dodajemy słowa charakterystyczne dla podsumowań (sumowań), zwykle pod i nad tabelą
    by ich nie zaliczyć do danych z tabeli
    """
    patterns = [
        r"([+-]?(?=\\.\\d|\\d)(?:\\d+)?(?:\\.?\\d*))(?:[eE]([+-]?\\d+))?",
    ]
    # nie dane ale podsumowanie a tego nie potrzebuję
    for str_pattern in patterns:
        pattern = re.compile(str_pattern)
        # if not any(word in row for word in ["Razem", "Podsumowanie", "netto", "brutto"]) and pattern.match(row, re.IGNORECASE):
        if not any(word in row.lower() for word in ['razem', 'podsumowanie', 'netto', 'brutto']):
            return True
    return False


def find_words_in_row(row: str, num_of_columns_in_excel_row: int, word='empty') -> bool:
    """
    W excelach z przetargów zawsze jest jakiś opis w wierszu (co najmniej 1 kolumna typu str),
    jeśli dany wiersz ma sens i warto go zapisać
    """
    # if 'empty' in row found less times than number of columns
    if row.count(word) < num_of_columns_in_excel_row:
        return True
    return False


ROW_HAS_DATA = find_words_in_row
PART_NAME = regex_part_name_row
HEADER = regex_header_row
DATA_ROW = regex_data_row
