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

    #建立连接，返回fd
    #参数：role，角色
    #      idx，server配置索引，默认是0
    def create_connect(self, role):
        #建立socket
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockfd.setblocking(False)
        
        #SO_LINGER选项设置
        #optval = struct.pack("ii",0,0)
        #self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, optval)
        
        #建立connect，根据desc_idx的值，不断切换
        if self.desc_idx==0:
            self.desc_idx = 1
            desc_address = (config.ADDR_1, int(config.PORT_1))
        elif self.desc_idx==1:
            self.desc_idx = 0
            desc_address = (config.ADDR_2, int(config.PORT_2))

        try:
            self.sockfd.connect(desc_address)
        except socket.error, ex:  
            (code, msg) = ex 
            if code == 115:
                # 当设置了noblock之后，115错误表示服务器忙，其实已经建立连接了
                # 所以可以忽略这个错误（当服务器当掉了，也会报这个错误）
                config.write_log("the socket.connect error! code:%d"%code+", msg:"+msg, role)
                pass 
            else:
                self.sockfd.close()
                print "the socket.connect error! code:%d"%code+", msg:"+msg
                config.write_log("the socket.connect error! code:%d"%code+", msg:"+msg, role)
                sys.exit(1)
        
        return self.sockfd
if __name__ == '__main__':
    net = Network()

    data = "xxxxxxxxxx"
    #print data
    net.send_data("127.0.0.1", 9527 ,data)
	
    del net
