import requests
import json
from bs4 import BeautifulSoup


def get_list_tokens():
    root_url = 'https://vestlab.io/'
    r = requests.get(root_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    trs = soup.select('tr.border-bottom.text-nowrap')
    data_popups = [tr.get('data-popup') for tr in trs]
    return data_popups

def main():
    tokens = get_list_tokens()
    print(len(tokens))

if __name__ == "__main__":
    main()

