#!/usr/bin/env python3
#coding=utf-8

'''
name : Ma　Jinquan
date : 2018-10-15
email: ...
modules: pymysql,time,sys,re
function: 此模块为酒店前台主模块
'''

import pymysql
import time,sys
import re
import VIP
import room_manage
import check_manage

def main():
    # 一级界面
    while True:
        print('''
        +-----------------------+
        |         前台          |
        +-----------------------+
        |      1:实时房态       |
        |      2:房间预定       |
        |      3:入住登记       |
        +-----------------------+
        |      4:更换房间       |
        |      5:房间续住       |
        |      6:结算退房       |
        +-----------------------+
        |      7:会员管理       |
        |      8:信息查询       |
        |      9:退出系统       |
        +-----------------------+
        ''')
        s = input("请输入命令>>")
        cmd = s.strip()
        if cmd == '1':
            R.room_show()
        elif cmd == '2':
            R.room_book()
        elif cmd == '3':
            R.room_checkin()            
        elif cmd == '4':
            R.room_change()
        elif cmd == '5':
            R.room_extend()
        elif cmd == '6':
            R.room_checkout()
        elif cmd == '7':
            R.vip_manage()
        elif cmd == '8':
            R.info_query()
        elif cmd == '9':
            sys.exit("退出系统")
        else:
            print("命令错误，请输入正确命令！")
            continue
class Reception(object):
    def __init__(self):
        pass
    def room_show(self):
        room_manage.select()
    def room_book(self):
        check_manage.reverse_register()
    def room_checkin(self):
        check_manage.check_in_register()
    def room_change(self):
        check_manage.change_room()
    def room_extend(self):
        check_manage.extend_live()
    def room_checkout(self):
        check_manage.check_out()
    def vip_manage(self):
        VIP.main()
    def info_query(self):
        check_manage.info_query()

if __name__ == '__main__':
    R = Reception()
    main()