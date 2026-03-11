// 页面加载完成后执行
 document.addEventListener('DOMContentLoaded', function() {
    // 导航切换
    setupNavigation();
    
    // 图书管理相关事件
    setupBookEvents();
    
    // 借阅管理相关事件
    setupBorrowEvents();
    
    // 加载图书列表
    loadBooks();
 });

// 设置导航切换
function setupNavigation() {
    // 首页导航
    document.getElementById('nav-home').addEventListener('click', function(e) {
        e.preventDefault();
        showSection('home-content');
        setActiveNav('nav-home');
    });
    
    // 图书管理导航
    document.getElementById('nav-books').addEventListener('click', function(e) {
        e.preventDefault();
        showSection('books-content');
        setActiveNav('nav-books');
        loadBooks();
    });
    
    // 借阅管理导航
    document.getElementById('nav-borrows').addEventListener('click', function(e) {
        e.preventDefault();
        showSection('borrows-content');
        setActiveNav('nav-borrows');
        loadBorrows();
    });
}

// 显示指定内容区域
function showSection(sectionId) {
    // 隐藏所有内容区域
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.add('d-none');
    });
    
    // 显示选中的内容区域
    document.getElementById(sectionId).classList.remove('d-none');
}

// 设置导航项为活动状态
function setActiveNav(navId) {
    // 移除所有导航项的活动状态
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // 设置选中的导航项为活动状态
    document.getElementById(navId).classList.add('active');
}

// 设置图书管理相关事件
function setupBookEvents() {
    // 搜索按钮点击事件
    document.getElementById('search-btn').addEventListener('click', function() {
        searchBooks();
    });
    
    // 新增图书按钮点击事件
    document.getElementById('save-book-btn').addEventListener('click', function() {
        addBook();
    });
    
    // 更新图书按钮点击事件
    document.getElementById('update-book-btn').addEventListener('click', function() {
        updateBook();
    });
}

// 设置借阅管理相关事件
function setupBorrowEvents() {
    // 借阅表单提交事件
    document.getElementById('borrow-form').addEventListener('submit', function(e) {
        e.preventDefault();
        borrowBook();
    });
    
    // 归还表单提交事件
    document.getElementById('return-form').addEventListener('submit', function(e) {
        e.preventDefault();
        returnBook();
    });
    
    // 查看记录按钮点击事件
    document.getElementById('view-records-btn').addEventListener('click', function() {
        loadBorrows();
    });
    
    // 查看未归还记录按钮点击事件
    document.getElementById('view-unreturned-btn').addEventListener('click', function() {
        loadUnreturnedBorrows();
    });
}

// 加载图书列表
function loadBooks() {
    fetch('/books')
        .then(response => response.json())
        .then(data => {
            renderBooksTable(data);
        })
        .catch(error => {
            showMessage('加载图书失败', 'danger');
        });
}

// 搜索图书
function searchBooks() {
    const searchType = document.getElementById('search-type').value;
    const keyword = document.getElementById('search-keyword').value;
    
    fetch(`/books/search?type=${searchType}&keyword=${encodeURIComponent(keyword)}`)
        .then(response => response.json())
        .then(data => {
            renderBooksTable(data);
        })
        .catch(error => {
            showMessage('搜索图书失败', 'danger');
        });
}

// 渲染图书表格
function renderBooksTable(books) {
    const tableBody = document.getElementById('books-table-body');
    tableBody.innerHTML = '';
    
    if (books.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center">暂无图书数据</td></tr>';
        return;
    }
    
    books.forEach(book => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${book.isbn}</td>
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td>${book.publisher}</td>
            <td>${book.publish_date}</td>
            <td>${book.stock}</td>
            <td>
                <div class="btn-group">
                    <button class="btn btn-sm btn-primary edit-book" data-isbn="${book.isbn}">修改</button>
                    <button class="btn btn-sm btn-danger delete-book" data-isbn="${book.isbn}">删除</button>
                </div>
            </td>
        `;
        tableBody.appendChild(row);
    });
    
    // 添加修改和删除事件
    document.querySelectorAll('.edit-book').forEach(btn => {
        btn.addEventListener('click', function() {
            editBook(this.dataset.isbn);
        });
    });
    
    document.querySelectorAll('.delete-book').forEach(btn => {
        btn.addEventListener('click', function() {
            deleteBook(this.dataset.isbn);
        });
    });
}

// 新增图书
function addBook() {
    const bookData = {
        isbn: document.getElementById('book-isbn').value,
        title: document.getElementById('book-title').value,
        author: document.getElementById('book-author').value,
        publisher: document.getElementById('book-publisher').value,
        publish_date: document.getElementById('book-date').value,
        stock: document.getElementById('book-stock').value
    };
    
    fetch('/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'danger');
        } else {
            showMessage(data.message, 'success');
            // 关闭模态框
            const modal = bootstrap.Modal.getInstance(document.getElementById('add-book-modal'));
            modal.hide();
            // 清空表单
            document.getElementById('add-book-form').reset();
            // 重新加载图书列表
            loadBooks();
        }
    })
    .catch(error => {
        showMessage('添加图书失败', 'danger');
    });
}

// 编辑图书
function editBook(isbn) {
    // 查找图书信息
    fetch(`/books/search?type=isbn&keyword=${isbn}`)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                showMessage('未找到图书信息', 'danger');
                return;
            }
            
            const book = data[0];
            // 填充表单
            document.getElementById('edit-book-isbn').value = book.isbn;
            document.getElementById('edit-book-title').value = book.title;
            document.getElementById('edit-book-author').value = book.author;
            document.getElementById('edit-book-publisher').value = book.publisher;
            document.getElementById('edit-book-date').value = book.publish_date;
            document.getElementById('edit-book-stock').value = book.stock;
            
            // 显示模态框
            const modal = new bootstrap.Modal(document.getElementById('edit-book-modal'));
            modal.show();
        })
        .catch(error => {
            showMessage('获取图书信息失败', 'danger');
        });
}

// 更新图书
function updateBook() {
    const isbn = document.getElementById('edit-book-isbn').value;
    const bookData = {
        title: document.getElementById('edit-book-title').value,
        author: document.getElementById('edit-book-author').value,
        publisher: document.getElementById('edit-book-publisher').value,
        publish_date: document.getElementById('edit-book-date').value,
        stock: document.getElementById('edit-book-stock').value
    };
    
    fetch(`/books/${isbn}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'danger');
        } else {
            showMessage(data.message, 'success');
            // 关闭模态框
            const modal = bootstrap.Modal.getInstance(document.getElementById('edit-book-modal'));
            modal.hide();
            // 重新加载图书列表
            loadBooks();
        }
    })
    .catch(error => {
        showMessage('更新图书失败', 'danger');
    });
}

// 删除图书
function deleteBook(isbn) {
    if (confirm('确定要删除该图书吗？')) {
        fetch(`/books/${isbn}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showMessage(data.error, 'danger');
            } else {
                showMessage(data.message, 'success');
                // 重新加载图书列表
                loadBooks();
            }
        })
        .catch(error => {
            showMessage('删除图书失败', 'danger');
        });
    }
}

// 加载借阅记录
function loadBorrows() {
    const borrower = document.getElementById('record-borrower').value;
    let url = '/borrows';
    if (borrower) {
        url += `?borrower=${encodeURIComponent(borrower)}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderBorrowsTable(data);
        })
        .catch(error => {
            showMessage('加载借阅记录失败', 'danger');
        });
}

// 加载未归还记录
function loadUnreturnedBorrows() {
    fetch('/borrows?unreturned=true')
        .then(response => response.json())
        .then(data => {
            renderBorrowsTable(data);
        })
        .catch(error => {
            showMessage('加载未归还记录失败', 'danger');
        });
}

// 渲染借阅记录表格
function renderBorrowsTable(borrows) {
    const tableBody = document.getElementById('borrows-table-body');
    tableBody.innerHTML = '';
    
    if (borrows.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center">暂无借阅记录</td></tr>';
        return;
    }
    
    borrows.forEach(record => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${record.id}</td>
            <td>${record.isbn}</td>
            <td>${record.book_title || '未知'}</td>
            <td>${record.borrower}</td>
            <td>${record.borrow_date}</td>
            <td>${record.return_date || '<span class="text-danger">未归还</span>'}</td>
        `;
        tableBody.appendChild(row);
    });
}

// 借阅图书
function borrowBook() {
    const borrowData = {
        isbn: document.getElementById('borrow-isbn').value,
        borrower: document.getElementById('borrower').value
    };
    
    fetch('/borrows', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(borrowData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'danger');
        } else {
            showMessage(data.message, 'success');
            // 清空表单
            document.getElementById('borrow-form').reset();
            // 重新加载借阅记录
            loadBorrows();
            // 重新加载图书列表
            loadBooks();
        }
    })
    .catch(error => {
        showMessage('借阅图书失败', 'danger');
    });
}

// 归还图书
function returnBook() {
    const returnData = {
        isbn: document.getElementById('return-isbn').value,
        borrower: document.getElementById('return-borrower').value
    };
    
    fetch('/borrows/return', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(returnData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'danger');
        } else {
            showMessage(data.message, 'success');
            // 清空表单
            document.getElementById('return-form').reset();
            // 重新加载借阅记录
            loadBorrows();
            // 重新加载图书列表
            loadBooks();
        }
    })
    .catch(error => {
        showMessage('归还图书失败', 'danger');
    });
}

// 显示消息提示
function showMessage(message, type = 'info') {
    const toast = document.getElementById('message-toast');
    const toastMessage = document.getElementById('toast-message');
    
    // 设置消息内容
    toastMessage.textContent = message;
    
    // 设置消息类型样式
    toast.className = 'toast';
    if (type === 'success') {
        toast.classList.add('bg-success', 'text-white');
    } else if (type === 'danger') {
        toast.classList.add('bg-danger', 'text-white');
    } else if (type === 'warning') {
        toast.classList.add('bg-warning', 'text-dark');
    } else {
        toast.classList.add('bg-info', 'text-white');
    }
    
    // 显示消息
    const toastInstance = new bootstrap.Toast(toast);
    toastInstance.show();
}
