#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
封装网络发送请求，采用select 多路I/O复用，长连接模式
'''
import socket
import select
import sys
import time
import struct

import traceback
import config

class Network(object):
    #类成员
    select_timeout = 3             # select超时时间
    sockfd         = 0             # 与后端连接的fd
    desc_idx       = 0             # 后端配置索引

    def __init__(self): 
        self.select_timeout = 3
        self.sockfd         = 0
        self.desc_idx       = 0
    
    def __del__(self):
        print "destruct\n"
