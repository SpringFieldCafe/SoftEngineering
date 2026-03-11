#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图书管理系统Web后端
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

# 数据文件路径
BOOKS_FILE = '../books.json'
BORROWS_FILE = '../borrows.json'

# 全局数据结构
books = []  # 图书列表
borrows = []  # 借阅记录列表

app = Flask(__name__)


def load_data():
    """加载数据"""
    global books, borrows
    
    # 初始化数据结构
    books = []
    borrows = []
    
    # 加载图书数据
    if os.path.exists(BOOKS_FILE):
        try:
            with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
                books = json.load(f)
                # 验证数据格式
                if not isinstance(books, list):
                    books = []
        except Exception:
            books = []
    
    # 加载借阅记录数据
    if os.path.exists(BORROWS_FILE):
        try:
            with open(BORROWS_FILE, 'r', encoding='utf-8') as f:
                borrows = json.load(f)
                # 验证数据格式
                if not isinstance(borrows, list):
                    borrows = []
        except Exception:
            borrows = []


def save_data():
    """保存数据"""
    global books, borrows
    
    # 确保数据目录存在
    try:
        os.makedirs(os.path.dirname(os.path.abspath(BOOKS_FILE)), exist_ok=True)
    except Exception:
        pass
    
    # 保存图书数据
    try:
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    
    # 保存借阅记录数据
    try:
        with open(BORROWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(borrows, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# 加载初始数据
load_data()


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/books', methods=['GET'])
def get_books():
    """获取所有图书"""
    return jsonify(books)


@app.route('/books/search', methods=['GET'])
def search_books():
    """搜索图书"""
    keyword = request.args.get('keyword', '')
    search_type = request.args.get('type', 'title')
    
    results = []
    if search_type == 'title':
        results = [book for book in books if keyword in book['title']]
    elif search_type == 'author':
        results = [book for book in books if keyword in book['author']]
    elif search_type == 'isbn':
        results = [book for book in books if book['isbn'] == keyword]
    
    return jsonify(results)


@app.route('/books', methods=['POST'])
def add_book():
    """新增图书"""
    data = request.get_json()
    
    # 检查ISBN是否已存在
    for book in books:
        if book['isbn'] == data['isbn']:
            return jsonify({'error': '该ISBN的图书已存在！'}), 400
    
    # 创建图书字典
    book = {
        'isbn': data['isbn'],
        'title': data['title'],
        'author': data['author'],
        'publisher': data['publisher'],
        'publish_date': data['publish_date'],
        'stock': int(data['stock'])
    }
    
    # 添加到图书列表
    books.append(book)
    save_data()
    
    return jsonify({'message': '图书添加成功！'})


@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    """修改图书"""
    data = request.get_json()
    
    # 查找图书
    book_index = -1
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            book_index = i
            break
    
    if book_index == -1:
        return jsonify({'error': '未找到该ISBN的图书！'}), 404
    
    # 更新图书信息
    book = books[book_index]
    book['title'] = data.get('title', book['title'])
    book['author'] = data.get('author', book['author'])
    book['publisher'] = data.get('publisher', book['publisher'])
    book['publish_date'] = data.get('publish_date', book['publish_date'])
    if 'stock' in data:
        book['stock'] = int(data['stock'])
    
    books[book_index] = book
    save_data()
    
    return jsonify({'message': '图书信息修改成功！'})


@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """删除图书"""
    # 查找图书
    book_index = -1
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            book_index = i
            break
    
    if book_index == -1:
        return jsonify({'error': '未找到该ISBN的图书！'}), 404
    
    # 检查是否有未归还的借阅记录
    has_unreturned = False
    for borrow in borrows:
        if borrow['isbn'] == isbn and borrow['return_date'] is None:
            has_unreturned = True
            break
    
    if has_unreturned:
        return jsonify({'error': '该图书有未归还的借阅记录，无法删除！'}), 400
    
    # 删除图书
    books.pop(book_index)
    save_data()
    
    return jsonify({'message': '图书删除成功！'})


@app.route('/borrows', methods=['GET'])
def get_borrows():
    """获取借阅记录"""
    borrower = request.args.get('borrower')
    unreturned = request.args.get('unreturned', 'false').lower() == 'true'
    
    records = borrows
    if borrower:
        records = [b for b in records if b['borrower'] == borrower]
    if unreturned:
        records = [b for b in records if b['return_date'] is None]
    
    # 为每条记录添加图书标题
    for record in records:
        book_title = "未知"
        for book in books:
            if book['isbn'] == record['isbn']:
                book_title = book['title']
                break
        record['book_title'] = book_title
    
    return jsonify(records)


@app.route('/borrows', methods=['POST'])
def borrow_book():
    """借阅图书"""
    data = request.get_json()
    isbn = data['isbn']
    borrower = data['borrower']
    
    # 查找图书
    book_index = -1
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            book_index = i
            break
    
    if book_index == -1:
        return jsonify({'error': '未找到该ISBN的图书！'}), 404
    
    book = books[book_index]
    
    # 检查库存
    if book['stock'] <= 0:
        return jsonify({'error': '该图书库存不足，无法借阅！'}), 400
    
    # 检查是否已借阅未归还
    for borrow in borrows:
        if borrow['isbn'] == isbn and borrow['borrower'] == borrower and borrow['return_date'] is None:
            return jsonify({'error': '该图书已被该借阅人借阅且未归还！'}), 400
    
    # 生成借阅记录
    borrow_record = {
        'id': len(borrows) + 1,
        'isbn': isbn,
        'borrower': borrower,
        'borrow_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'return_date': None
    }
    
    # 添加借阅记录
    borrows.append(borrow_record)
    
    # 扣减库存
    book['stock'] -= 1
    books[book_index] = book
    
    save_data()
    
    return jsonify({'message': '图书借阅成功！'})


@app.route('/borrows/return', methods=['POST'])
def return_book():
    """归还图书"""
    data = request.get_json()
    isbn = data['isbn']
    borrower = data['borrower']
    
    # 查找借阅记录
    borrow_index = -1
    for i, borrow in enumerate(borrows):
        if borrow['isbn'] == isbn and borrow['borrower'] == borrower and borrow['return_date'] is None:
            borrow_index = i
            break
    
    if borrow_index == -1:
        return jsonify({'error': '未找到该借阅记录！'}), 404
    
    # 查找图书
    book_index = -1
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            book_index = i
            break
    
    if book_index == -1:
        return jsonify({'error': '未找到该图书！'}), 404
    
    # 更新借阅记录
    borrows[borrow_index]['return_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 恢复库存
    books[book_index]['stock'] += 1
    
    save_data()
    
    return jsonify({'message': '图书归还成功！'})


if __name__ == '__main__':
    try:
        print("启动Flask应用...")
        print(f"数据文件路径: {os.path.abspath(BOOKS_FILE)}")
        print(f"当前工作目录: {os.getcwd()}")
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
