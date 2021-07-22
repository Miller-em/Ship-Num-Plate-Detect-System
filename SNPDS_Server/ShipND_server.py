__author__ = 'xiaozong zhou'
import base64
from flask import request
from flask import Flask
import mysql.connector as mysql
import os
import time

app=Flask(__name__, static_folder="./det_results_imgs") #建立一个flask app
fire_db = mysql.connect(
    host = "localhost",
    user = "",
    password = "",
    database = "",
    charset='utf8'
) #连接本地数据库
mycursor = fire_db.cursor() #建立游标

# 定义路由
@app.route("/1", methods=['POST'])
def push_frame():
    json = request.json
    now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
    deted_img_path = './deted_ship_number/' + now + r"_SND.jpg"
    deted_img_info = str(json['info'])
    if json:
        """将路径，推理信息存入数据库"""
        sql = "INSERT INTO xxx (PATH, INFO) VALUES (%s, %s)"
        val = (deted_img_path, deted_img_info)
        mycursor.execute(sql, val)
        fire_db.commit()
        """保存到文件系统"""
        img_data = base64.b64decode(json["image_str"])
        with open(deted_img_path, 'wb') as f:
            f.write(img_data)
        f.close()
        return 'success'
    else:
        return 'failed'

@app.route("/2", methods=['POST'])
def pull_db():
    fire_db = mysql.connect(
    host = "localhost",
    user = "",
    password = "",
    database = "",
    charset='utf8'
    ) #连接本地数据库
    mycursor = fire_db.cursor() #建立游标
    json = request.json
    sql = json['info']
    if json:
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return str(myresult)
    else:
        return 'failed'

@app.route("/3", methods=['POST'])
def push_sn():
    json = request.json
    s = json['info']
    if json:
        sql = "INSERT INTO  () VALUES ('%s')" % s
        mycursor.execute(sql)
        fire_db.commit()
        return 'success'
    else:
        return 'failed'

@app.route("/4", methods=['POST'])
def pull_legaldb():
    fire_db = mysql.connect(
    host = "localhost",
    user = "",
    password = "",
    database = "",
    charset='utf8'
    ) #连接本地数据库
    mycursor = fire_db.cursor() #建立游标
    json = request.json
    sql = json['info']
    if json:
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return str(myresult)
    else:
        return 'failed'

@app.route("/4", methods=['POST'])
def pull_img():
    json = request.json
    img_id = json['img_id']
    if json:
        sql = "select PATH from  where img_id = " + img_id
        mycursor.execute(sql)
        img_path = mycursor.fetchall()
        with open(img_path[0][0], 'rb') as f: 
            res = base64.b64encode(f.read())
            return res
    

if __name__ == "__main__":
    app.run()
