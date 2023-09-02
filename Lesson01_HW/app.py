# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category')
def category():
    return render_template('category.html')

@app.route('/products/clothing')
def clothing():
    return render_template('/products/clothing.html')

@app.route('/products/shoes')
def shoes():
    return render_template('/products/shoes.html')

@app.route('/products/jacket')
def jacket():
    return render_template('/products/jacket.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()