# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/categories/clothing')
def clothing_category():
    category_name = "Одежда"
    products = [...]  # Получите список товаров категории из базы данных
    return render_template('category_template.html', category_name=category_name, products=products)

@app.route('/products/<int:product_id>')
def product_details(product_id):
    product = [...]  # Получите информацию о товаре из базы данных по его идентификатору
    return render_template('product_template.html', product=product)

if __name__ == '__main__':
    app.run()
