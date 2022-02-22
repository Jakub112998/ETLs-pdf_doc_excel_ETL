import logging
import xlrd
from base import OutputManager, BaseOutputManager, CustomOutputManager
import pandas as pd
from typing import List, Union, Type
import argparse
from resources.similar_words import replacements, header_detection, datatypes_check
from resources.table_helper import nan_generator, lists_comparator
from resources.regexes import PART_NAME, HEADER, DATA_ROW, ROW_HAS_DATA
from dataclasses import dataclass, make_dataclass
import re


class XLSXExtractor():
    """
    Ta klasa odpowiada za nazewnictwo wewnątrz folderu stworzonego za pomocą base_extractor.py:
    - każdy arkusz pliku .xlsx posiada własny zestaw plików .csv oraz .txt
    - pliki dla danego arkusza znajdują się w oddzielnym folderze.
    Nazwa folderu = nazwa arkusza + nagłówek odnaleziony w orginalnym pliku
    - jeśli na jednym arkuszu jest kilka tabel - jest kilka plików .csv w jednym folderze dla danego arkusza.

    W jednym przejściu:
    IF new header detected -> create new DF
    IF new header not detected -> append to the last DF
    """

    def __init__(self, path_manager: OutputManager):
        self.path_manager = path_manager
        # print("input", self.path_manager.input)
        # print("out", self.path_manager.base_path)

    def process(self) -> List[Union[pd.DataFrame, Type[pd.DataFrame]]]:
        """
        Jeśli nagłówek w kolejnych arkuszach się zmienia - utwórz listę dataframes

        todo: jeśli nie budujemy df a są dane tekstowe lub numeryczne to żeby ich nie tracić to zapisuję do pliku txt do przetworzenia
        """
        book = xlrd.open_workbook(self.path_manager.input)
        columns = []
        df_concatenated = []
        data = []
        for idx in range(len(book.sheets())):
            first_sheet = book.sheet_by_index(idx)
            print(first_sheet.name)
            df_building = False
            file_object = open(f"{self.path_manager.base_path}/{first_sheet.name}_{idx}.txt", 'a')
            for row_idx in range(first_sheet.nrows):
                row = first_sheet.row(row_idx)

                if ROW_HAS_DATA(str(row), first_sheet.ncols):
                    # znajdź nazwę pakietu / części
                    if 'text' in str(row) and PART_NAME(str(row)):
                        # todo: find everything after word 'Pakiet nr X' or 'Część nr X' and pass it as .csv file name
                        continue
                    if HEADER(str(row)) and not df_building:
                        columns = [x.value for x in row[1:]]
                        df_building = True
                        # todo: kiedy napotkam na nowy header trzeba sprawdzić czy jest już taki header
                        #  może być case gdzie w headerze na innym arkuszu jest tylko literówka np. x zamiast +
                        #  należy takie przypadki wynaleźć oraz dopisać do resources/similar_words.py
                        # if df_concatenated is empty -> create first one
                        if not df_concatenated:
                            # print("buduję pierwszą tabelę")
                            pass
                        # if at least one df in df_concatenated exists -> select to which df to add
                        df_id = header_detection(df_concatenated, columns)
                        # if found to which df to add
                        if df_id is not -1:
                            assert len(df_concatenated) >= 1
                            # then add - dodajemy do istniejącej po kolumnach
                            columns = df_concatenated[df_id][1].columns
                        # if no such df found -> create a new one
                        elif df_id is -1:
                            # budujemy nowy
                            pass
                        continue
                    # znajdź dane dla tabeli
                    if df_building and DATA_ROW(str(row)) and ROW_HAS_DATA(str(row), first_sheet.ncols, word='number'):
                        # -1 bo liczę bez kolumny Lp
                        assert first_sheet.ncols - 1 == len(columns)
                        data_row = []
                        # [1:] żeby ominąć Lp - df indexowany z automatu
                        for x in row[1:]:
                            if type(x.value) != float:
                                # print("!= float")
                                # print(x.value)
                                # print(type(x.value))
                                data_row.append(x.value)
                            elif type(x.value) == float:
                                # print("== float")
                                # print(x.value)
                                # print(type(x.value))
                                if float(x.value - int(x.value)) == 0.0:  # wtedy wiadomo, że to int
                                    # print(int(x.value))
                                    data_row.append(int(x.value))
                                else:
                                    # print(x.value - int(x.value))
                                    data_row.append(float(x.value - int(x.value)))
                            continue
                        data.append(data_row)
                        continue
                    # jeśli przejrzeliśmy cały plik xlsx albo znaleźliśmy nowy header -> zapisz df
                    if df_building:
                        # Clean and organize new data
                        df_id = header_detection(df_concatenated, columns)
                        # jeśli wykryto, że taki df już istnieje
                        if df_id is not -1:
                            # print("TABELA ", df_id, "\n", df_concatenated[df_id][1])
                            # print("Do niej dodaję te dane:")
                            # sprawdzam nowe dane, które chce do niego dodać & update data types
                            df_concatenated[df_id][0] = datatypes_check(data, df_concatenated[df_id][0])
                            # wiemy jakie typy udało się zadeklarować dla każdej z kolumn więc konwertujemy wszystkie
                            # NaN values na odpowiedni typ dla danej kolumny
                            data = nan_generator(data, df_concatenated[df_id][0])
                            # append list of lists to existing df
                            # print("Dodaję DF: ", pd.DataFrame(data, columns=columns))

                            # compare 2 lists of headers - they have to be the same for df to be appended
                            out = lists_comparator(list(columns), list(df_concatenated[df_id][1].columns))
                            # should be equal
                            assert out

                            # df appending is not inplace operation - need to =
                            df_concatenated[df_id][1] = df_concatenated[df_id][1].append(
                                pd.DataFrame(data, columns=columns),
                                ignore_index=True
                            )
                            # print("Powiększona tabela: ", df_concatenated[df_id][1])

                        # if df with such header not found -> create a new one
                        elif df_id == -1:
                            # print("Tworzę nową tabelę z tych danych:")
                            # create new types_dict for this data frame
                            types_dict = datatypes_check(data)
                            data = nan_generator(data, types_dict)
                            # create a new df
                            # print("Dodaję DF: ", pd.DataFrame(data, columns=columns))
                            df_concatenated.append([types_dict, pd.DataFrame(data, columns=columns)])
                            # print("Utworzona tabela:\n", df_concatenated[-1][1])
                            # df.to_csv(f"Part_{part_name}_{first_sheet.name}_{idx}_{row_idx}.csv", index=False,
                            # encoding="utf-8")
                        data = []
                    # todo: jeśli są dane tekstowe poza tabelą to żeby ich nie tracić to zapisuję
                    #   do pliku txt do późniejszego przetworzenia
                    elif not df_building:
                        # zapisz plik .txt z pozostałymi danymi
                        for el in row:
                            if str(el.value) is not None or str(el.value) is not '':
                                file_object.write(str(el.value))
                                # file_object.write("\n")
                        continue
                df_building = False
        # todo: df'my które mają te same typy danych dla odpowiadających kolumn zbieram w jeden df
        # todo: aggregate pozycje z takim samym opisem / nazwą.
        for i, el in enumerate(df_concatenated):
            print(el[1].to_csv(f"{self.path_manager.base_path}/Part_{i}.csv", index=False, encoding="utf-8"))
        return df_concatenated


def main(target_path):
    handler = XLSXExtractor(BaseOutputManager(target_path))
    df = handler.process()
    print("output **************************")
    for el in df:
        print(el[0])
        print(el[1].columns)
        print(el[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Choose input folder directory")
    args = parser.parse_args()

    """
    python xls_extractor.py ../data/input/b.xlsx
    """

    main(target_path=args.input)
