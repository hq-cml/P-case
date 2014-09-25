#!/usr/bin/env python
# -*- coding: utf-8 -*-

#--------- 通用的配模块，包含常用函数和方法的实现 ---------------#
import MySQLdb
import cStringIO
import pycurl
import simplejson as json
import logging
import redis
import traceback
import os 
import sys
import pprint

#--------- 程序运行环境: test | production ---------------#
ENVIRONMENT = "test"

if ENVIRONMENT == "test":
    #----------------- Base 目录--------------------#
    BASE_FILE       = "/data/xxx/"
    LOG_PATH        = "log/log"
  
    #-----------------本地 Redis 配置 -------------------#
    REDISHOST        = "localhost"
    REDISPORT        = 6375
    TIMEOUT          = 5 
    REDIS_DB         = 0
    
    #-----------------数据库配置--------------------#
    MYSQLHOST         = "127.0.0.1"
    MYSQLUSER         = "root"
    MYSQLPASS         = "123456"
    MYSQLDB           = "my_db"
    

elif ENVIRONMENT == "production":
    #----------------- Base 目录--------------------#
    BASE_FILE       = "/data/xxx/"
    LOG_PATH        = "log/log"
  
    #-----------------本地 Redis 配置 -------------------#
    REDISHOST        = "localhost"
    REDISPORT        = 6375
    TIMEOUT          = 5 
    REDIS_DB         = 0
    
    #-----------------数据库配置--------------------#
    MYSQLHOST         = "127.0.0.1"
    MYSQLUSER         = "root"
    MYSQLPASS         = "123456"
    MYSQLDB           = "my_db"

#-----------------Mysql函数-----------------#
def get_mysql_connection():
    try: 
        db = MySQLdb.connect(host=MYSQLHOST, user=MYSQLUSER, passwd=MYSQLPASS, db=MYSQLDB, charset='utf8')
    except Exception, error:
        print "Mysql connect error!"+str(error)
        write_log("Mysql connect error!"+str(error))
    return db

def close_mysql_connection(db):
	db.close()
	
#查询
def mysql_query(sql):
    db  = get_mysql_connection()
    cur = db.cursor()

    cur.execute(sql)
    index = cur.description
    all = cur.fetchall()
    
    idx = 0
    result = {}  
    for line in all:
        ret = {}
        for i in range(len(index)):
            ret[index[i][0]] = line[i]
        if ret.has_key('id'):
            result[ret['id']] = ret
        else:
            result[idx] = ret
        idx = idx+1
    cur.close()
    close_mysql_connection(db)
    
    return result

#执行
def mysql_execute(sql):
    db  = get_mysql_connection()
    cur = db.cursor()

    cur.execute(sql)
    db.commit()
    cur.close()
    close_mysql_connection(db)

#-----------------Http接口函数-----------------#
def post_curl(url, argu1, argu2):
    result = "" 
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.CONNECTTIMEOUT, 20)
    c.setopt(c.TIMEOUT, 60)
    #c.setopt(c.COOKIEFILE, '')
    c.setopt(c.FAILONERROR, True)
    #c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])

    try:
        c.setopt(c.POSTFIELDS, 'argu1='+str(argu1)+'&argu2='+str(argu2))
        c.perform()
        result = buf.getvalue()
        buf.close()
    except pycurl.error, error:
        (errno, errstr) = error
        print 'Curl error: ', errstr
        write_log('Curl error: ' + errstr, "exception")
        buf.close() 
    return result
    
    
