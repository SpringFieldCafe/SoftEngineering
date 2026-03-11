#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的HTTP服务器，用于测试前端页面
"""

import http.server
import socketserver
import os

# 定义端口
PORT = 8000

# 更改工作目录到当前目录
os.chdir('.')

# 创建请求处理器
Handler = http.server.SimpleHTTPRequestHandler

# 创建服务器
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print(f"服务器运行在 http://localhost:{PORT}")
    print("按 Ctrl+C 停止服务器")
    httpd.serve_forever()
