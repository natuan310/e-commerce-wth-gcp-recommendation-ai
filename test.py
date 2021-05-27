from bs4 import BeautifulSoup
from flask import Flask, render_template
import requests
import re

base_url = 'https://www.bookdepository.com/'


def get_url(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def make_data(ul):
    # make a dict for ul elements
    d = {}
    for a in ul.find_all('a'):
        d[a.text] = {'href': a.attrs['href']}
    lis = ul.find_all('li', recursive=False)
    children = {}
    for li in lis:
        child = li.ul
        if child:
            children[li.a.attrs['href']] = make_data(child)
    if children:
        d['children'] = children
    for k, v in d.items():
        print(k, ' - ', v)
    return d


# test get UL
# soup = get_url(base_url)
# ulitem = soup.find('ul', class_='tbd-dropdown-menu')
# print(type(ulitem))
# uldict = []
# for a in ulitem.find_all('a'):
#     uldict.append(a.text)

# # for k, v in uldict.items():
# #     print(k, ' - ', v)

# for i in uldict:
#     print(i)

soup = get_url(base_url)
# books = soup.find_all('div', class_='book-item')
# for book in books[:20]:
#     author =  book.select_one('a[itemprop=url]')['href'].replace('/author/', '')
#     print(author)

# categories = soup.find_all('li', class_='top-category')
# category = categories[0]
# # for i in categories[:5]:
# #     print(i.a.get_text().strip(), i.a['href'][10:])
# btype = 'comingsoon'
# # https://www.bookdepository.com/comingsoon

# url = base_url + btype
# print(url)
# type_url = base_url + category.a['href'][1:]
# typee = get_url('https://www.bookdepository.com/comingsoon')
# books = typee.find_all('div', class_='book-item')

# data = []
# for book in books:
#     b = {'id': '', 'title': '', 'author': '', 'author_url': '',
#          'price': '', 'price-save': '', 'img_url': '', 'link': ''}
#     try:
#         b['id'] = re.findall(r'\d{13}', book.a['href'])[0]
#         b['title'] = book.img['alt']
#         b['author'] = book.select_one('a[itemprop=author]').get_text()
#         b['author_url'] = book.select_one('a[itemprop=author]')[
#             'href'].replace('/author/', '')
#         b['price'] = book.select_one('p[class=price]').get_text().strip().split('\n                            \xa0')[0]
#         b['price-save'] = b['price'] = book.select_one('p[class=price]').get_text().strip().split('\n                            \xa0')[1]
#         b['img_url'] = book.img['src']
#         b['link'] = book.select_one('a[itemprop=url]')['href']
#     except:
#         pass
#     data.append(b)

# for i in data[:5]:
#     print(i)


    
# page_html = get_url('https://tiki.vn/dien-tu-dien-lanh/c4221?src=c.4221.hamburger_menu_fly_out_banner')
# # products_wrapper_div = page_html.find_all('div', class_='product-box-list')[0]
# products_div = page_html.find_all('div', class_='product-item')
# result = []
# if len(products_div) > 0:
#     print('PRODUCT DIV NOT BLANK')
#     for product_div in products_div:
#         product_id = None
#         title = product_div.a['title']
#         url = product_div.a['href']
#         img_url = product_div.img['src']
#         regular_price = product_div.find('span', class_='price-regular').text
#         final_price = product_div.find('span', class_='final-price').text.split()[0]
#         sale_tag = product_div.find('span', class_='sale-tag').text
#         comment = product_div.find('p', class_='review').text.split()[0] + ' review(s))'
#         rating = product_div.find('span', class_='rating-content').span['style'].split(":")[-1]
#         print(title, url, img_url, regular_price)
import sqlite3
conn = sqlite3.connect(
    '/home/max/Desktop/Coder School Projects/_tonga/week2/w2-webscraping-with-sql/tiki_complete_v1.db', uri=True, check_same_thread=False)

cur = conn.cursor()

query = """
    SELECT id, name, url FROM categories
    WHERE parent_id BETWEEN 100 AND 113;
    """
try:
    cur.execute(query)
except Exception as err:
    print('ERROR BY SELECT TABLE', err)

rows = cur.fetchall()

for i in rows:
    id = i[0]
    name = " ".join(i[1].strip().split()[:-1])
    url = i[2].strip()
    print(name, url)