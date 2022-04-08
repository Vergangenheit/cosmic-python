# This is a sample Python script.
from typing import Dict, List

import requests
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def main():

    params = dict(q='Sausages', format='json')
    parsed: Dict = requests.get('http://api.duckduckgo.com/', params=params).json()

    results: List = parsed['RelatedTopics']
    for r in results:
        if 'Text' in r:
            print(r['FirstURL'] + ' - ' + r['Text'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
