from typing import List


def nan_generator(data: List, types_dict: dict) -> List:
    """
    generujemy odpowiednie NaN values dla odpowiednich kolumn
    Wcześniej mieliśmy Nan values jako '' w int-kolumnach
    Teraz jako NaN value w kolumnie int mamy 0 a w kolumnie float mamy 0.0
    """
    for row_id, row in enumerate(data):
        for col_id, col_value in enumerate(row):
            if col_value == '':  # NaN value dla typu str
                if types_dict[col_id] == int:
                    data[row_id][col_id] = 0  # NaN value dla typu int
                if types_dict[col_id] == float:
                    data[row_id][col_id] = 0.0  # Nan value dla typu float
            if col_value == 'sz' or col_value == 'sz.' or col_value == "szt":
                data[row_id][col_id] = 'szt.'
            if col_value == 'op':
                data[row_id][col_id] = 'op.'
    return data


def lists_comparator(l1, l2):
    result = all(map(lambda x, y: x == y, l1, l2))
    return result and len(l1) == len(l2)