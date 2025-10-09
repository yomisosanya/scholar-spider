
import csv
import json
from pathlib import Path
from typing import Dict, List
from textwrap import wrap


#TODO: fix errors in this function
# def print_list(table: List[Dict]) -> None:
#     """
#     """
#     ws_len = 15
#     for row in table:
#         for key, value in row.items():
#             print('{}'.format(key), end='')
#             txt: List = wrap(value, width=50)
#             space = ' '*(ws_len - len(key))
#             print('{}{}'.format(space, txt[0]))
#             for line in txt[1:]:
#                 print('{}{}'.format(' '*ws_len, line))
#         print('\n')
#     return

def store_data(data, filename=Path('../target/data.json')):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return

def load_data(filename=Path('../target/data.json')):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
    

def convert_to_csv(data: List[Dict], filename=Path('../target/data.csv')) -> None:
    """
    """
    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)    
    return

def read_csv(filename, delimiter=','):
    """Reads a csv file and returns a list of dictionaries"""
    with open(filename, 'r', encoding='utf-8') as f:
        rows = csv.DictReader(f, delimiter=delimiter)
        result = list(rows)
    return result
