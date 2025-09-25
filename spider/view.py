
import json
from pathlib import Path
from typing import Dict, List
from textwrap import wrap


def print_list(table: List[Dict]) -> None:
    """
    """
    ws_len = 15
    for row in table:
        for key, value in row.items():
            print('{}'.format(key), end='')
            txt: List = wrap(value, width=50)
            space = ' '*(ws_len - len(key))
            print('{}{}'.format(space, txt[0]))
            for line in txt[1:]:
                print('{}{}'.format(' '*ws_len, line))
        print('\n')
    return

def store_data(data, filename=Path('../target/data.json')):
    with open(filename, 'w') as f:
        json.dump(data, f)
    return

def load_data(filename=Path('../target/data.json')):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data
    

# if __name__ == '__main__':
