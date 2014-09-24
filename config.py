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
