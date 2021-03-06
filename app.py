from bs4 import BeautifulSoup
import time
import requests
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
# import sqlite3
import pandas as pd
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tiki_complete_v1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

engine = create_engine('sqlite:///tiki_complete_v1.db')
engine.connect()

# conn = sqlite3.connect(
#     '/home/max/Desktop/Coder School Projects/_tonga/week2/w2-webscraping-with-sql/tiki_complete_v1.db', uri=True, check_same_thread=False)

# cur = conn.cursor()

# categories = pd.read_sql_query('SELECT * FROM categories', conn)
# items = pd.read_sql_query('SELECT * FROM items', conn)

# categories = engine.execute('SELECT * FROM categories;')
# items = engine.execute('SELECT * FROM items')

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return 'ID: {}, Name: {}'.format(self.id, self.name)
    
class categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    parent_id = db.Column(db.Integer)
    last = db.Column(db.String(20))
    create_at = db.Column(db.Date)

    def __repr__(self):
        return 'ID: {}, Name: {}, URL: {}, Parent_id: {}'.format(self.id, self.name, self.url, self.parent_id)

class items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=False)
    cat_id = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    regular_price = db.Column(db.Integer)
    sale_tag = db.Column(db.Integer)
    final_price = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    create_at = db.Column(db.Date)

    def __repr__(self):
        return """ID: {}, Path: {}, Cat_ID: {}, Name: {}, Brand: {}, URL: {}, IMG: {}, Reg-Price: {},
                    Sale: {}, Final-Price: {}"""\
                    .format(self.item_id, self.item_path, self.cat_id,  self.name, self.brand,
                    self.url, self.img_url, self.regular_price, self.sale_tag, self.final_price)

def get_url(url):
    time.sleep(1)
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, 'html.parser')
        return response
    except Exception as err:
        print('ERROR BY REQUEST: ', err)

@app.route('/index/')
@app.route('/index/<int:page>', methods=['POST', 'GET'])
@app.route('/')
def index(page=0):
    # using sqlalchemy connection
    main_categories = engine.execute('SELECT * FROM categories WHERE parent_id IS NULL;').fetchall()
    items = engine.execute('SELECT * FROM items ORDER BY RANDOM() LIMIT 10000').fetchall()
    
    
    """ DATA ANALYZE
        - Total items in category.
        - Average, max, min price of items.
        - How many items have sale_tag.
    """
    """
    analyze = {'total': 0, 'max_price': 0, 'min_price': 0, 'avg_price': 0, 'sale_items': 0}
    analyze['total'] = len(items)

    analyze['max_price'] = max([int(i.final_price[:-1].replace('.', '')) for i in items])
    analyze['min_price'] = min([int(i.final_price[:-1].replace('.', '')) for i in items])
    analyze['avg_price'] = round(sum([int(i.final_price.replace('??', '').replace('.', '')) for i in items])/len(items))
    analyze['sale_items'] = sum([len(i.sale_tag.strip())>0 for i in items])
    """
    # pages = len(items)//40
    items = items[page*40:(page+1)*40]
    return render_template('index.html', categories=main_categories, items=items, page=page)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/category/<id>', methods=['POST', 'GET'])
@app.route('/category/<id>/<int:page>', methods=['POST', 'GET'])
def category(id,page=0):
    # using sqlalchemy connection
    cat_name = engine.execute(f'SELECT name FROM categories WHERE id = {id}').fetchone()
    sub_cate = engine.execute(
        f'SELECT * FROM categories WHERE parent_id = {id}').fetchall()

    # return same generation category list for the lasts child selected
    if not sub_cate:
        sub_cate = engine.execute(
        f"""SELECT * FROM categories WHERE parent_id = 
            (SELECT c2.parent_id FROM categories as c2
                WHERE c2.id={id})""").fetchall()
        cat_name = engine.execute(f'SELECT name FROM categories WHERE id = {id}').fetchone()


    items = engine.execute(f'SELECT * FROM items WHERE cat_id = {id}').fetchall()
    if not items:
        items = engine.execute(f"""SELECT * FROM items 
                                        WHERE parent_id = {id}
                                        ORDER BY RANDOM()""").fetchall()
        if not items:
            items = engine.execute(f"""SELECT * FROM items 
                                        WHERE parent_id IN 
                                        (SELECT id FROM categories 
                                            WHERE parent_id = {id})
                                        ORDER BY RANDOM()""").fetchall()
    item = items[page*40:(page+1)*40]

    """ DATA ANALYZE
        - Total items in category.
        - Average, max, min price of items.
        - How many items have sale_tag.
    """
    analyze = {'total': 0, 'max_price': 0, 'min_price': 0, 'avg_price': 0, 'sale_items': 0}
    analyze['total'] = len(items)

    analyze['max_price'] = max([int(i.final_price[:-1].replace('.', '')) for i in items])
    analyze['min_price'] = min([int(i.final_price[:-1].replace('.', '')) for i in items])
    analyze['avg_price'] = round(sum([int(i.final_price.replace('??', '').replace('.', '')) for i in items])/len(items))
    analyze['sale_items'] = sum([len(i.sale_tag.strip())>0 for i in items])
    
    return render_template('search_items.html', cat_name=cat_name[0], categories=sub_cate, items=item, cat_id=id, page=page, analyze=analyze)


@app.route('/detail/')
def detail(id):
    pass


@app.route('/search', methods=['POST', 'GET'])
@app.route('/search/<int:page>', methods=['POST', 'GET'])
def search(page=0):
    keyword = request.form['search']
    main_categories = engine.execute('SELECT * FROM categories WHERE parent_id IS NULL;').fetchall()

    items = engine.execute(
        f"""SELECT * FROM items
                WHERE name LIKE "{keyword}%"
                OR brand LIKE "{keyword}%"; """).fetchall()

    analyze = {'total': 0, 'max_price': 0, 'min_price': 0, 'avg_price': 0, 'sale_items': 0}
    analyze['total'] = len(items)

    analyze['max_price'] = max([int(i.final_price[:-1].replace('.', '')) for i in items])
    analyze['min_price'] = min([int(i.final_price[:-1].replace('.', '')) for i in items])
    analyze['avg_price'] = round(sum([int(i.final_price.replace('??', '').replace('.', '')) for i in items])/len(items))
    analyze['sale_items'] = sum([len(i.sale_tag.strip())>0 for i in items])

    items = items[page*40:(page+1)*40]
    return render_template('search_items.html', keyword=keyword, categories=main_categories, items=items, page=page, analyze=analyze)

@app.route('/data_analysis')
def data_analysis():
    all_categories = engine.execute('SELECT * FROM categories').fetchall()
    return render_template('data_analysis.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
