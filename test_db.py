from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pandas as pd
from sqlalchemy import create_engine


conn = sqlite3.connect(
    '/home/max/Desktop/Coder School Projects/_tonga/week2/w2-webscraping-with-sql/tiki_complete_v1.db', uri=True, check_same_thread=False)

cur = conn.cursor()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tiki_complete_v1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db = SQLAlchemy(app)

engine = create_engine('sqlite:///tiki_complete_v1.db')

# engine.connect()

# categories = engine.execute('SELECT * FROM categories;').fetchall()
# print(type(categories))

# cate = pd.read_sql_query('SELECT * FROM categories;', conn)
# print(type(cate))

# cat = cur.execute('SELECT * FROM categories;')
# print(type(cat))

# cat = db.Query.paginate(db)
# print(cat)

# base = automap_base()

engine = create_engine('sqlite:///tiki_complete_v1.db')

# base.prepare(engine, reflect=True)

# # categories = base.classes.categories
# # items = base.classes.items

# session = Session(engine)

# class categories(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     url = db.Column(db.String(200), nullable=False)
#     parent_id = db.Column(db.Integer)
#     last = db.Column(db.String(20))
#     create_at = db.Column(db.Date)

#     def __repr__(self):
#         return 'ID: {}, Name: {}, URL: {}, Parent_id: {}'.format(self.id, self.name, self.url, self.parent_id)

# class items(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     path = db.Column(db.String(200), nullable=False)
#     cat_id = db.Column(db.Integer)
#     name = db.Column(db.String(200), nullable=False)
#     brand = db.Column(db.String(200), nullable=False)
#     img_url = db.Column(db.String(200), nullable=False)
#     url = db.Column(db.String(200), nullable=False)
#     regular_price = db.Column(db.Integer)
#     sale_tag = db.Column(db.Integer)
#     final_price = db.Column(db.Integer)
#     parent_id = db.Column(db.Integer)
#     create_at = db.Column(db.Date)

#     def __repr__(self):
#         return """ID: {}, Path: {}, Cat_ID: {}, Name: {}, Brand: {}, URL: {}, IMG: {}, Reg-Price: {},
#                     Sale: {}, Final-Price: {}"""\
#                     .format(self.item_id, self.item_path, self.cat_id,  self.name, self.brand,
#                     self.url, self.img_url, self.regular_price, self.sale_tag, self.final_price)
    

# class Category:
#     def __init__(self, cat_id, name, url, parent_id):
#         self.cat_id = cat_id
#         self.name = name
#         self.url = url
#         self.parent_id = parent_id

#     def __repr__(self):
#         return 'ID: {}, Name: {}, URL: {}, Parent_id: {}'.format(self.cat_id, self.name, self.url, self.parent_id)

#     def save_into_db(self):
#         query = """
#             INSERT INTO categories (name, url, parent_id)
#             VALUES (?, ?, ?);
#         """
#         val = (self.name, self.url, self.parent_id)
#         try:
#             cur.execute(query, val)
#             self.cat_id = cur.lastrowid
#             print(f'SAVED {self.name} INTO categories')
#         except Exception as err:
#             print('ERROR BY INSERT: ', err)
#     id = db.Column(db.Integer, primary_key=True)

# class Items:
#     def __init__(self, item_id, item_path, cat_id, name, brand, img_url, url, regular_price, sale_tag='', final_price=''):
#         self.item_id = item_id
#         self.item_path = item_path
#         self.cat_id = cat_id
#         self.name = name
#         self.brand = brand
#         self.url = url
#         self.img_url = img_url
#         self.regular_price = regular_price
#         self.sale_tag = sale_tag
#         self.final_price = final_price

#     def __repr__(self):
#         return """ID: {}, Path: {}, Cat_ID: {}, Name: {}, Brand: {}, URL: {}, IMG: {}, Reg-Price: {},
#                     Sale: {}, Final-Price: {}""".format(self.item_id, self.item_path, self.cat_id,  self.name, self.brand,
#                                                         self.url, self.img_url, self.regular_price, self.sale_tag, self.final_price)

#     def save_into_db(self):
#         query = """ INSERT INTO items2 (path, cat_id, name, brand, url, img_url, regular_price, sale_tag, final_price)
#                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 """
#         val = (self.item_path, self.cat_id, self.name, self.brand, self.url, self.img_url,
#                self.regular_price, self.sale_tag, self.final_price)

#         try:
#             cur.execute(query, val)
#             self.item_id = cur.lastrowid
#             # print(f'INSERT {self.name} INTO TABLE items2')
#         except Exception as err:
#             print('ERROR BY INSERT ITEMS: ', err)


# cate = categories.query.filter_by(parent_id=12)
# for cat in cate:
#     print(cat)


# id = 1
# items = engine.execute(f'SELECT * FROM items WHERE cat_id = {id}').fetchall()
# if not items:
#     items = engine.execute(f"""SELECT * FROM items 
#                                     WHERE parent_id = {id}
#                                     ORDER BY RANDOM()""").fetchall()
#     if not items:
#         items = engine.execute(f"""SELECT * FROM items 
#                                     WHERE parent_id IN 
#                                     (SELECT id FROM categories 
#                                         WHERE parent_id = {id})
#                                     ORDER BY RANDOM()""").fetchall()

# total = len(items)
# # f_price = items[0].final_price

# max_price = max([int(i.final_price[:-1].replace('.', '')) for i in items])
# min_price = min([int(i.final_price[:-1].replace('.', '')) for i in items])
# avg_price = round(sum([int(i.final_price[:-1].replace('.', '')) for i in items])/len(items))
# sale_items = sum([len(i.sale_tag.strip())>0 for i in items])
# # print(total, max_price, min_price, avg_price, sale_items)
# print(f'{max_price:3d,}')



# main_categories = engine.execute('SELECT * FROM categories WHERE parent_id IS NULL').fetchall()

# def print_cate(cate, generation):
#     print(' '*3*generation + str(cate.id) + ' - ' + cate.name[:30].rstrip())
#     sub_cat = engine.execute(f'SELECT * FROM categories WHERE parent_id = {cate.id}').fetchall()
#     if sub_cat:
#         generation += 1
#         print_cate(sub_cat, generation)
#     else:
#         print(' '*3*generation + str(cate.id) + ' - ' + cate.name[:30].rstrip())
        

# # import sys
# # sys.stdout = open("full_category.txt", "w")
# # for i in main_categories:
# #     print_cate(i,0)
# # sys.stdout.close()

# for cate in main_categories:
#     print_cate(cate, 0)


def find_sub_cate(id, parent_id):
    query = "SELECT id FROM categories WHERE parent_id=" + str(id)
    ids = cur.execute(query).fetchall()
    if len(ids) == 0:
        return cur.execute(f"SELECT id FROM categories WHERE parent_id={parent_id}").fetchall()
    else:
        for cat_id in ids:
            return [find_sub_cate(cat_id[0], id)]

main_cate = cur.execute('SELECT id, name FROM categories WHERE parent_id IS NULL;').fetchall()
# print(main_cate[9])
# child_id = []
# child_id += find_sub_cate(main_cate[9][0], None)

# print(child_id)

def print_cate(cate, generation):
    sub_cat = engine.execute(f'SELECT * FROM categories WHERE parent_id = {cate[0]}').fetchall()
    if sub_cat:
        print('gen '+str(generation)+' '*3*generation + str(cate[0]) + ' - ' + str(cate[1])[:-10].rstrip() + str(cate[1])[-10:].strip())
        generation += 1
        for sub in sub_cat:
            print_cate(sub, generation)
    else:
        print('gen '+str(generation)+' '*3*generation + str(cate[0]) + ' - ' + str(cate[1])[:-10].rstrip() + str(cate[1])[-10:].strip())

main_categories = engine.execute('SELECT * FROM categories WHERE parent_id IS NULL').fetchall()

print_cate(main_categories[9], 0)

def create_dict_cate(cate):
    d = {}
    s = {}
    sub_cat = engine.execute(f'SELECT * FROM categories WHERE parent_id = {cate[0]}').fetchall()
    if sub_cat:
        for sub in sub_cat:
            s[sub[0]] = create_dict_cate(sub)
        d[cate[0]] = s
        return d
    else:
        return None


d9 = create_dict_cate(main_categories[9])

def print_tree(d):
    for k, v in d.items():
        if v:
            print(k, v)
            print_tree(v)
        else:
            print(k, v)
            break

# print_tree(d9)
# print(type(d9))