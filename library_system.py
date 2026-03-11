#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图书管理系统主程序
"""

import json
import os
import time
from datetime import datetime

# 尝试导入tabulate库，如果没有则使用内置打印
try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

# 数据文件路径
BOOKS_FILE = 'books.json'
BORROWS_FILE = 'borrows.json'

# 全局数据结构
books = []  # 图书列表
borrows = []  # 借阅记录列表


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
                    print("图书数据格式错误，已重置为空列表")
                    books = []
        except json.JSONDecodeError:
            print("图书数据文件格式错误，已重置为空列表")
            books = []
        except UnicodeDecodeError:
            print("图书数据文件编码错误，已重置为空列表")
            books = []
        except Exception as e:
            print(f"加载图书数据失败: {e}")
            books = []
    
    # 加载借阅记录数据
    if os.path.exists(BORROWS_FILE):
        try:
            with open(BORROWS_FILE, 'r', encoding='utf-8') as f:
                borrows = json.load(f)
                # 验证数据格式
                if not isinstance(borrows, list):
                    print("借阅记录数据格式错误，已重置为空列表")
                    borrows = []
        except json.JSONDecodeError:
            print("借阅记录数据文件格式错误，已重置为空列表")
            borrows = []
        except UnicodeDecodeError:
            print("借阅记录数据文件编码错误，已重置为空列表")
            borrows = []
        except Exception as e:
            print(f"加载借阅记录失败: {e}")
            borrows = []

def save_data():
    """保存数据"""
    global books, borrows
    
    # 确保数据目录存在
    try:
        os.makedirs(os.path.dirname(os.path.abspath(BOOKS_FILE)), exist_ok=True)
    except Exception as e:
        print(f"创建数据目录失败: {e}")
        return
    
    # 保存图书数据
    try:
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
    except PermissionError:
        print("保存图书数据失败：权限不足")
    except IOError:
        print("保存图书数据失败：IO错误")
    except Exception as e:
        print(f"保存图书数据失败: {e}")
    
    # 保存借阅记录数据
    try:
        with open(BORROWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(borrows, f, ensure_ascii=False, indent=2)
    except PermissionError:
        print("保存借阅记录失败：权限不足")
    except IOError:
        print("保存借阅记录失败：IO错误")
    except Exception as e:
        print(f"保存借阅记录失败: {e}")


def print_menu():
    """打印主菜单"""
    print("\n" + "=" * 50)
    print("        图书管理系统")
    print("=" * 50)
    print("1. 图书管理")
    print("2. 借阅管理")
    print("3. 退出系统")
    print("=" * 50)


def print_book_menu():
    """打印图书管理子菜单"""
    print("\n" + "-" * 50)
    print("        图书管理")
    print("-" * 50)
    print("1. 新增图书")
    print("2. 查询图书")
    print("3. 修改图书")
    print("4. 删除图书")
    print("5. 返回主菜单")
    print("-" * 50)


def print_borrow_menu():
    """打印借阅管理子菜单"""
    print("\n" + "-" * 50)
    print("        借阅管理")
    print("-" * 50)
    print("1. 借阅图书")
    print("2. 归还图书")
    print("3. 查看借阅记录")
    print("4. 返回主菜单")
    print("-" * 50)


def get_input(prompt, required=True, default=None):
    """获取用户输入"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                if required:
                    print("输入不能为空，请重新输入！")
                    continue
                else:
                    return default
            return user_input
        except KeyboardInterrupt:
            print("\n操作已取消！")
            return default
        except Exception as e:
            print(f"输入错误: {e}，请重新输入！")
            continue

def get_integer(prompt, min_val=None, max_val=None):
    """获取整数输入"""
    while True:
        try:
            user_input = input(prompt).strip()
            value = int(user_input)
            if min_val is not None and value < min_val:
                print(f"输入值不能小于{min_val}，请重新输入！")
                continue
            if max_val is not None and value > max_val:
                print(f"输入值不能大于{max_val}，请重新输入！")
                continue
            return value
        except ValueError:
            print("请输入有效的整数！")
        except KeyboardInterrupt:
            print("\n操作已取消！")
            return None
        except Exception as e:
            print(f"输入错误: {e}，请重新输入！")
            continue


def add_book():
    """新增图书"""
    global books
    
    print("\n" + "=" * 50)
    print("        新增图书")
    print("=" * 50)
    
    # 获取图书信息
    isbn = get_input("请输入ISBN: ")
    
    # 检查ISBN是否已存在
    for book in books:
        if book['isbn'] == isbn:
            print("该ISBN的图书已存在！")
            return
    
    title = get_input("请输入书名: ")
    author = get_input("请输入作者: ")
    publisher = get_input("请输入出版社: ")
    publish_date = get_input("请输入出版日期 (YYYY-MM-DD): ")
    stock = get_integer("请输入库存数量: ", 0)
    
    # 创建图书字典
    book = {
        'isbn': isbn,
        'title': title,
        'author': author,
        'publisher': publisher,
        'publish_date': publish_date,
        'stock': stock
    }
    
    # 添加到图书列表
    books.append(book)
    print("图书添加成功！")
    save_data()


def search_book():
    """查询图书"""
    global books
    
    print("\n" + "=" * 50)
    print("        查询图书")
    print("=" * 50)
    
    print("1. 按书名查询")
    print("2. 按作者查询")
    print("3. 按ISBN查询")
    choice = get_integer("请选择查询方式: ", 1, 3)
    
    keyword = get_input("请输入查询关键词: ")
    results = []
    
    if choice == 1:
        # 按书名查询
        for book in books:
            if keyword in book['title']:
                results.append(book)
    elif choice == 2:
        # 按作者查询
        for book in books:
            if keyword in book['author']:
                results.append(book)
    elif choice == 3:
        # 按ISBN查询
        for book in books:
            if book['isbn'] == keyword:
                results.append(book)
    
    # 显示查询结果
    if results:
        if tabulate:
            # 使用tabulate美化输出
            table_data = []
            for book in results:
                table_data.append([
                    book['isbn'],
                    book['title'],
                    book['author'],
                    book['publisher'],
                    book['publish_date'],
                    book['stock']
                ])
            print("\n查询结果:")
            print(tabulate(table_data, headers=['ISBN', '书名', '作者', '出版社', '出版日期', '库存'], tablefmt='grid'))
        else:
            # 普通打印
            print("\n查询结果:")
            for book in results:
                print(f"ISBN: {book['isbn']}")
                print(f"书名: {book['title']}")
                print(f"作者: {book['author']}")
                print(f"出版社: {book['publisher']}")
                print(f"出版日期: {book['publish_date']}")
                print(f"库存: {book['stock']}")
                print("-" * 30)
    else:
        print("未找到匹配的图书！")


def update_book():
    """修改图书"""
    global books
    
    print("\n" + "=" * 50)
    print("        修改图书")
    print("=" * 50)
    
    isbn = get_input("请输入要修改的图书ISBN: ")
    
    # 查找图书
    book_index = -1
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            book_index = i
            break
    
    if book_index == -1:
        print("未找到该ISBN的图书！")
        return
    
    book = books[book_index]
    print(f"当前图书信息:")
    print(f"书名: {book['title']}")
    print(f"作者: {book['author']}")
    print(f"出版社: {book['publisher']}")
    print(f"出版日期: {book['publish_date']}")
    print(f"库存: {book['stock']}")
    
    # 获取新信息
    title = get_input("请输入新书名 (按回车保持不变): ", required=False, default=book['title'])
    author = get_input("请输入新作者 (按回车保持不变): ", required=False, default=book['author'])
    publisher = get_input("请输入新出版社 (按回车保持不变): ", required=False, default=book['publisher'])
    publish_date = get_input("请输入新出版日期 (按回车保持不变): ", required=False, default=book['publish_date'])
    stock = get_integer(f"请输入新库存数量 (当前: {book['stock']}): ", 0)
    
    # 更新图书信息
    book['title'] = title
    book['author'] = author
    book['publisher'] = publisher
    book['publish_date'] = publish_date
    book['stock'] = stock
    
    books[book_index] = book
    print("图书信息修改成功！")
    save_data()


def delete_book():
    """删除图书"""
    global books, borrows
    
    print("\n" + "=" * 50)
    print("        删除图书")
    print("=" * 50)
    
    isbn = get_input("请输入要删除的图书ISBN: ")
    
    # 查找图书
    book_index = -1
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            book_index = i
            break
    
    if book_index == -1:
        print("未找到该ISBN的图书！")
        return
    
    # 检查是否有未归还的借阅记录
    has_unreturned = False
    for borrow in borrows:
        if borrow['isbn'] == isbn and borrow['return_date'] is None:
            has_unreturned = True
            break
    
    if has_unreturned:
        print("该图书有未归还的借阅记录，无法删除！")
        return
    
    # 确认删除
    confirm = get_input("确定要删除该图书吗？(y/n): ")
    if confirm.lower() != 'y':
        print("删除操作已取消！")
        return
    
    # 删除图书
    books.pop(book_index)
    print("图书删除成功！")
    save_data()


def main():
    """主函数"""
    # 加载数据
    load_data()
    
    while True:
        print_menu()
        choice = get_integer("请选择操作: ", 1, 3)
        
        if choice == 1:
            # 图书管理
            while True:
                print_book_menu()
                book_choice = get_integer("请选择操作: ", 1, 5)
                
                if book_choice == 1:
                    # 新增图书
                    add_book()
                elif book_choice == 2:
                    # 查询图书
                    search_book()
                elif book_choice == 3:
                    # 修改图书
                    update_book()
                elif book_choice == 4:
                    # 删除图书
                    delete_book()
                elif book_choice == 5:
                    # 返回主菜单
                    break
        
def borrow_book():
    """借阅图书"""
    global books, borrows
    
    print("\n" + "=" * 50)
    print("        借阅图书")
    print("=" * 50)
    
    # 获取借阅信息
    isbn = get_input("请输入图书ISBN: ")
    borrower = get_input("请输入借阅人姓名: ")
    
    # 查找图书
    book_index = -1
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            book_index = i
            break
    
    if book_index == -1:
        print("未找到该ISBN的图书！")
        return
    
    book = books[book_index]
    
    # 检查库存
    if book['stock'] <= 0:
        print("该图书库存不足，无法借阅！")
        return
    
    # 检查是否已借阅未归还
    for borrow in borrows:
        if borrow['isbn'] == isbn and borrow['borrower'] == borrower and borrow['return_date'] is None:
            print("该图书已被该借阅人借阅且未归还！")
            return
    
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
    
    print("图书借阅成功！")
    save_data()


def return_book():
    """归还图书"""
    global books, borrows
    
    print("\n" + "=" * 50)
    print("        归还图书")
    print("=" * 50)
    
    # 获取归还信息
    isbn = get_input("请输入图书ISBN: ")
    borrower = get_input("请输入借阅人姓名: ")
    
    # 查找借阅记录
    borrow_index = -1
    for i, borrow in enumerate(borrows):
        if borrow['isbn'] == isbn and borrow['borrower'] == borrower and borrow['return_date'] is None:
            borrow_index = i
            break
    
    if borrow_index == -1:
        print("未找到该借阅记录！")
        return
    
    # 查找图书
    book_index = -1
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            book_index = i
            break
    
    if book_index == -1:
        print("未找到该图书！")
        return
    
    # 更新借阅记录
    borrows[borrow_index]['return_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 恢复库存
    books[book_index]['stock'] += 1
    
    print("图书归还成功！")
    save_data()


def view_borrow_records():
    """查看借阅记录"""
    global borrows, books
    
    print("\n" + "=" * 50)
    print("        查看借阅记录")
    print("=" * 50)
    
    print("1. 查看所有记录")
    print("2. 查看指定借阅人记录")
    print("3. 查看未归还记录")
    choice = get_integer("请选择查看方式: ", 1, 3)
    
    if choice == 1:
        # 查看所有记录
        records = borrows
    elif choice == 2:
        # 查看指定借阅人记录
        borrower = get_input("请输入借阅人姓名: ")
        records = [b for b in borrows if b['borrower'] == borrower]
    elif choice == 3:
        # 查看未归还记录
        records = [b for b in borrows if b['return_date'] is None]
    
    # 显示记录
    if records:
        if tabulate:
            # 使用tabulate美化输出
            table_data = []
            for record in records:
                # 查找图书信息
                book_title = "未知"
                for book in books:
                    if book['isbn'] == record['isbn']:
                        book_title = book['title']
                        break
                
                table_data.append([
                    record['id'],
                    record['isbn'],
                    book_title,
                    record['borrower'],
                    record['borrow_date'],
                    record['return_date'] or "未归还"
                ])
            print("\n借阅记录:")
            print(tabulate(table_data, headers=['编号', 'ISBN', '书名', '借阅人', '借阅时间', '归还时间'], tablefmt='grid'))
        else:
            # 普通打印
            print("\n借阅记录:")
            for record in records:
                # 查找图书信息
                book_title = "未知"
                for book in books:
                    if book['isbn'] == record['isbn']:
                        book_title = book['title']
                        break
                
                print(f"编号: {record['id']}")
                print(f"ISBN: {record['isbn']}")
                print(f"书名: {book_title}")
                print(f"借阅人: {record['borrower']}")
                print(f"借阅时间: {record['borrow_date']}")
                print(f"归还时间: {record['return_date'] or '未归还'}")
                print("-" * 30)
    else:
        print("未找到借阅记录！")


def main():
    """主函数"""
    # 加载数据
    load_data()
    
    while True:
        print_menu()
        choice = get_integer("请选择操作: ", 1, 3)
        
        if choice is None:
            continue
        
        if choice == 1:
            # 图书管理
            while True:
                print_book_menu()
                book_choice = get_integer("请选择操作: ", 1, 5)
                
                if book_choice is None:
                    continue
                
                if book_choice == 1:
                    # 新增图书
                    add_book()
                elif book_choice == 2:
                    # 查询图书
                    search_book()
                elif book_choice == 3:
                    # 修改图书
                    update_book()
                elif book_choice == 4:
                    # 删除图书
                    delete_book()
                elif book_choice == 5:
                    # 返回主菜单
                    break
        
        elif choice == 2:
            # 借阅管理
            while True:
                print_borrow_menu()
                borrow_choice = get_integer("请选择操作: ", 1, 4)
                
                if borrow_choice is None:
                    continue
                
                if borrow_choice == 1:
                    # 借阅图书
                    borrow_book()
                elif borrow_choice == 2:
                    # 归还图书
                    return_book()
                elif borrow_choice == 3:
                    # 查看借阅记录
                    view_borrow_records()
                elif borrow_choice == 4:
                    # 返回主菜单
                    break
        
        elif choice == 3:
            # 退出系统
            save_data()
            print("感谢使用图书管理系统，再见！")
            break


if __name__ == "__main__":
    main()
