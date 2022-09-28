#!/usr/bin/python
# -*- coding: UTF-8 -*-
# CGI处理模块
import cgi
# 创建FieldStorage实例化
form = cgi.FieldStorage()

flag_num1 = 0
flag_num2 = 0
flag_op = 0

# 判断input框是否有内容，有内容flag值赋1，无内容flag值赋0
if form.getvalue('num1'):
    site_num1 = form.getvalue('num1')
    flag_num1 = 1
else:
    site_num1 = "empty_num1"
if form.getvalue('num2'):
    site_num2 = form.getvalue('num2')
    flag_num2 = 1
else:
    site_num2 = "empty_num2"
if form.getvalue('option'):
    op = form.getvalue('option')
    flag_op = 1
else:
    op = "empty_option"

res = ""
with open("cgi-bin/calculator.html", "r", encoding="utf-8") as f:
    for line in f:
        res += line
# 判断三个input框中是否均有内容，如果都有的话，3个flag乘积为1
if (flag_num1 * flag_num2 * flag_op):
    res = res.replace("$num1", site_num1)
    res = res.replace("$num2", site_num2)
    if(op == "add"):
        res = res.replace("$option", "+")
        res = res.replace("$ans", str(float(site_num1) + float(site_num2)))
    elif(op == "sub"):
        res = res.replace("$option", "-")
        res = res.replace("$ans", str(float(site_num1) - float(site_num2)))
    elif(op == "mul"):
        res = res.replace("$option", "*")
        res = res.replace("$ans", str(float(site_num1) * float(site_num2)))
    else:
        res = res.replace("$option", "/")
        res = res.replace("$ans", str(float(site_num1) / float(site_num2)))
# 如果不全有值，则直接输出对应input的内容，然后结果ans赋null
else:
    res = res.replace("$num1", site_num1)
    res = res.replace("$num2", site_num2)
    res = res.replace("$option", op)
    res = res.replace("$ans", "null")

filename = "res.html"
with open(filename, "wb") as f:
    f.write(res.encode('utf-8'))
