import csv
import requests
from bs4 import BeautifulSoup

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}


def read_data_from_detmir():
    data = []
    page = 1
    for i in range(1, 66):
        response = requests.get(f'https://www.detmir.ru/catalog/index/name/lego/page/{page}', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_items = soup.find_all('div', class_='mO m_1')
        for item in all_items:
            url = item.find('a').get('href')
            id = url.split('/')[-2]
            title = item.find('p', class_='M_1').text
            if item.find('p', class_='Nc'):
                price = item.find('p', class_='Nc').text.replace(u'\xa0', '').replace('\u2009', '').replace('₽', '')
            else:
                price = 'None'
            if item.find('span', class_='Ne'):
                promo = item.find('span', class_='Ne').text.replace(u'\xa0', '').replace('\u2009', '').replace('₽', '')
            else:
                promo = 'None'
            data_for_one_item = {'id': id, 'title': title, 'price': price, 'promo_price': promo, 'url': url}
            data.append(data_for_one_item)
        page += 1
    return data


def write_in_csv():
    headers_for_table = ('id', 'title', 'price', 'promo_price', 'url')
    with open('my_file.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers_for_table)
        writer.writeheader()
        for value in read_data_from_detmir():
            writer.writerow(value)


if __name__ == '__main__':
    read_data_from_detmir()
    write_in_csv()
