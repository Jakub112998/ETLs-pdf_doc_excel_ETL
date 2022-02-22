replacements = {
    # WAŻNE!!!!! - zapisujemy tutaj bez odstępów i małymi literami
    # todo: [na ogół] istnieje ograniczona liczba literówek które można popełnić - wrzucić to w oddzielny plik i ładować
    #  z pliku na początku pipeline'u a później dawać notify w ramach któregoś z scenariuszy do ręcznego
    #  sprawdzenia po wykonaniu
    "%vat": ["vat", "podatek%vat"],
    "vat": ["%vat", "podatek%vat"],
    "podatek%vat": ["vat", "%vat"],
    "wartośćbruttowpln/kolumna6x7/": ["wartośćbruttowPLN/kolumna6+7/"],
    "wartośćbruttowpln/kolumna6+7/": ["wartośćbruttowPLN/kolumna6x7/"],
    "ilośćopakowańna3miesiące": ["ilośćopak.na3miesiące", "ilośćopak.3miesiące"],
    "ilośćopak3miesiące": ["ilośćopak.na3miesiące"],
    "ilośćopak.3miesiące": ["ilośćopak.na3miesiące"],
}
from typing import List
import pandas as pd


def header_detection(list_df: List[pd.DataFrame], columns: List) -> int:
    """
    może być tak, że arkusz 1,2,3 odpowiadają headerowi df o indexie 0
    później w arkuszu 4,5 mamy headery df o indexac 1 i 2
    a następnie znowu w arkuszu 6,7 wracamy do headera df o indexie 0 ->
    ta funkcja ma za zadanie to wykryć i przekazać do którego df ma dodać.

    więc jeśli df_concatenated ma już df'my

    todo: dokończyć podmienianie
    """
    for df_id, dataframe in enumerate(list_df):
        dataframe = dataframe[1]  # take only pd.DataFrame object - not intrested in types_dict()
        # tylko podstawowe operacje
        col1 = list(map(str.lower, dataframe.columns))
        col2 = list(map(str.lower, columns))
        col1 = ["".join(x.split()) for x in col1]
        col2 = ["".join(x.split()) for x in col2]
        # w tych kolumnach jest różnica
        el = [(i, x) for i, x in enumerate(col1) if x not in col2]
        # jeśli różnica jest w conajmniej 1 kolumnie to podmieniamy
        if len(el) > 0:
            # ile jest różniących się kolumn - trzeba podmienić wszystkie by dodać do jednego z dotychczasowych df
            diff_num = len(el)
            # print(diff_num)
            how_many_replaced = 0
            for e in el:  # przeszukuję każdą różniącą się kolumnę
                tmp_e = '%s' % e[1]
                for key in replacements.keys():
                    if tmp_e == key:
                        for value in replacements[key]:
                            # print("-------------\n"
                            #       "Liczymy różnicę między:\n",
                            #       value,
                            #       "\noraz;\n",
                            #       col2[e[0]],
                            #       "\n-----------------")
                            difference = list(set(value).symmetric_difference(set(col2[e[0]])))
                            # print(difference)
                            # todo: implementacja podmieniania tutaj
                            #  narazie robię tak, że jak różni się tylko 4 znakami jakaś nazwa kolumny
                            #  to traktuj je jako takie same
                            if len(difference) <= 4:
                                # print("succeffully replaced")
                                how_many_replaced += 1
                                break
            # if all correctly replaced
            if diff_num == how_many_replaced:
                # print("\n--------------\n", "We were comparing: \n", columns, "\nand;\n", list(dataframe.columns),
                #       "\nand replaced ", how_many_replaced, " of ", diff_num, "\n--------------")
                return df_id
        # jeśli oba nagłówki są takie same
        elif len(set(col1).intersection(col2)) == len(col1):
            # print(f"Dodaję do identycznej, istniejącej już tabeli {df_id}")
            return df_id
    # print("Nie znaleziono takigo nagłówka -> powstanie nowy dataframe z tymi kolumnami:\n", columns)
    return -1


def datatypes_check(data: List, types_dict=None):
    if types_dict is None:
        types_dict = dict()
    for row in data:
        # find datatype for each column in row
        for col_id, col_value in enumerate(row):
            # jeśli już jest taki klucz
            if col_id in types_dict.keys():
                # i jego wartość == str
                if type(types_dict[col_id]) == str:
                    # to jeśli aktualna wartość nie jest str to zamień
                    if type(col_value) == int:
                        types_dict[col_id] = int
                    if type(col_value) == float:
                        types_dict[col_id] = float
                else:
                    # w pozostałych przypadkach nie zamieniaj
                    pass
            if type(col_value) == str:
                types_dict[col_id] = str
            if type(col_value) == int:
                types_dict[col_id] = int
            if type(col_value) == float:
                types_dict[col_id] = float
    return types_dict
