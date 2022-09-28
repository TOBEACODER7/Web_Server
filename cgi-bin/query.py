#!/usr/bin/python
# -*- coding: UTF-8 -*-
from fileinput import filename
import sqlite3
# CGI处理模块
import cgi


# 创建FieldStorage实例化
form = cgi.FieldStorage()
# 判断stuID是否为0，input是否为数字
flag_stuID = 0
flag_dig = 0
# 初始化的输出语句部分
reAns = ""
errorAnsOne = 'The studentID is empty, please search again!'
errorAnsSec = 'The studentID is wrong, please search again!'

# 判断input框是否有内容，有内容flag_stuID值赋1，无内容flag_stuID值赋0
if form.getvalue('id'):
    getStudentID = form.getvalue('id')
    flag_dig = getStudentID.isdigit()
    # 判断在有input的情况下，input是否为数字，此时flag_stuID必为1
    if (getStudentID == "all"):
        flag_dig = 1
    flag_stuID = 1
else:
    # 无input，则flag_stuID==0，flag_dig==0
    getStudentID = "empty_ID"
    flag_stuID = 0
    flag_dig = 0

db = sqlite3.connect('database/CN_0905_SQLite.db')   # 连接db文件，db为已经内置好的数据库
cursor = db.cursor()

# sql查询语句开始：
sql = ""
# 如果getStudentID非空，是合理的，则输出结果；
# 如果getStudentID找不到，则输出“wrong studentID”
# 如果 有输入 且 输入是数字
if (flag_stuID * flag_dig):
    if getStudentID == "all":
        sql = "SELECT * from cnStuData;"
    else:
        sql = "select * from cnStuData where studentID = " + getStudentID + ";"
    cursor.execute(sql)         # 向数据库传入查询指令
    getData = cursor.fetchall()     # 用getData获得返回的数据库中的数据
    # 判断getData是否为空，如果不为空，就输出；如果为空，就说明学号错误，是getStudentID找不到的情况
    # 如果getData不为空
    if (getData):
        with open("cgi-bin/dataSearch.html", "r", encoding="utf-8") as f:
            for line in f:
                reAns += line
            outCome = ''
            # theTablebegin = "<table style=text-align:center>"
            inCen = "<div style="+"\""+"text-align:center" "\"" + ">"
            # theTablebegin = "<table style="+"\""+"text-align:center" "\"" + ">"
            theTablebegin = "<table class="+"\""+"tableType" "\"" + ">"
            theTableend = "</table></div>"
            outCome += inCen
            outCome += theTablebegin
            for traverse in getData:
                temp = "<tr>"
                temp += "<td>" + str(traverse[0]) + "</td>"
                temp += "<td>" + traverse[1] + "</td>"
                temp += "<td>" + traverse[2] + "</td>"
                temp += "<td>" + traverse[3] + "</td>"
                temp += "</tr>\n"
                outCome += temp
            outCome += theTableend
        reAns = reAns.replace("$stuInformation", outCome)
    # 如果getData为空
    else:
        with open("cgi-bin/dataSearch.html", "r", encoding="utf-8") as f:
            for line in f:
                reAns += line
        reAns = reAns.replace("$stuInformation", errorAnsSec)
# 如果flag_stuID==1且flag_dig==0，说明有input，但input是字符串而非数字，无法查询
elif (flag_stuID + flag_dig == 1):
    with open("cgi-bin/dataSearch.html", "r", encoding="utf-8") as f:
        for line in f:
            reAns += line
    reAns = reAns.replace("$stuInformation", errorAnsSec)
# 否则说明input为空，则输出“empty”提示语句
else:
    with open("cgi-bin/dataSearch.html", "r", encoding="utf-8") as f:
        for line in f:
            reAns += line
    reAns = reAns.replace("$stuInformation", errorAnsOne)

filename = "res.html"
with open(filename, "wb") as f:
    f.write(reAns.encode('utf-8'))
