#!/usr/bin/env python3
#coding=utf-8

'''
name : Ma　Jinquan
date : 2018-10-13
email: ...
modules: pymysql,time,sys,re
function: 此模块功能为会员卡办理，充值，查询和注销
'''

import pymysql
import time,sys
import re

def main():
    while True:
        print('''
            ===================会员管理==================
            --1.开卡   2.充值   3.查询　 4.销卡  5.退出--
            =============================================
            ''')
        try:
            cmd = int(input("请选择："))
        except Exception:
            print("命令错误！")
            continue
        if cmd not in [1,2,3,4,5]:
            print("请输入正确选项")
            sys.stdin.flush()
            continue
        elif cmd == 1:
            A.do_open()
        elif cmd == 2:
            A.do_charge()
        elif cmd == 3:
            tel = input('请输入会员手机号：')
            A.do_query(tel)
        elif cmd == 4:
            A.do_cancell()
        elif cmd == 5:
            return

#统计字符串中文字符个数
def chinese_cnt(n):
    l=[]
    for i in range(len(n)):
        b=n[i]
        if ord(b)>127:
            l.append(b)
    return len(l)

#功能函数的类
class vip_manager(object):
    def __init__(self, db):
        self.db=db

    def do_open(self):
        while True:
            name = input("请输入姓名：")
            if name == '':
                print("姓名不能为空，请重新输入！")
                continue
            else:
                break

        while True:
            s = input("请选择性别(1.男,2.女):")    #图形界面为选择界面
            if s == '1':
                sex = '男'
                break
            elif s == '2':
                sex = '女'
                break
            else:
                print('输入有误，请重新输入')
                continue
        while True:
            tel = input("输入手机号（11位）：")
            l = re.findall('1[0-9]{10}',tel)
            if len(l) == 0:
                print("请输入正确的电话号码！")
                continue
            break
        while True:
            try:    
                money = int(input("请输入充值金额（最低充值金额500元）："))
                if money < 500:
                    print("最低充值金额500元！")
                    continue
                else:
                    break
            except ValueError:
                print("请正确输入金额！")
                continue

        sql = "insert into vip_info(name,sex,tel,YE) values(\
            '%s','%s','%s',%d)"%(name,sex,tel,money)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        print("开卡成功！")

    def do_charge(self):
        cursor = self.db.cursor()
        while True:
            tel = input('请输入会员手机号：')
            sql = "select * from vip_info where tel='%s'"%tel
            cursor.execute(sql)
            r = cursor.fetchone()
            if r == None:
                s = input("无该会员信息,重新输入(y/n)?")
                if s in ('y','Y'):
                    continue
                else:
                    print('充值失败，退出充值！')
                    break
            self.do_query(tel)
            s = input("请核对会员信息，确认后选择(1.确认;2.取消)")
            if s == '1':
                money = int(input("请输入充值金额："))
                tip = input("1.确认2.取消")
                if tip == "2":
                    print('充值取消！')
                    break
                YE = r[4]+money
                sql = "update vip_info set YE=%d where tel='%s'"%(YE,tel)
                cursor.execute(sql)
                self.db.commit()
                print('充值成功，卡余额为 %d 元'%YE)
                break
            else:
                print('充值取消！')  #跳转到会员服务界面
                break

    def do_query(self,tel):
        cursor = self.db.cursor()
        sql = "select * from vip_info where tel='%s'"%tel
        cursor.execute(sql)
        r = cursor.fetchone()
        if r == None:
            print("无此会员信息!")
            return 1
        ID,name,sex,tel,YE,time = r
        ch=chinese_cnt(name)
        i = str(ID).center(8)
        n = name.center(10-ch)
        s = sex.center(5)
        t1 = tel.center(13)
        y = str(YE).center(9)
        t2 = str(time).center(21)
        
        print('会员信息如下：')
        print('+--------+----------+------+-------------+---------+---------------------+')
        print('|   ID   |   姓名   | 性别 |   手机号    |   余额  |      开卡时间       |')
        print('+--------+----------+------+-------------+---------+---------------------+')
        print("|%s|%s|%s|%s|%s|%s|" % (i,n,s,t1,y,t2))                
        print('+--------+----------+------+-------------+---------+---------------------+')

    def do_cancell(self):
        tel = input('请输入会员手机号：')
        n = self.do_query(tel) 
        if n == 1:
            return
        print("请验证会员身份并核对会员信息...")
        s = input("验证是否通过？(1.信息符合，验证通过2.信息不符，验证不通过)\n") #弹出选择框
        if s == '1':
            print("身份验证已通过！")
            s = input("是否完成退款并销卡？(1.是2.否)")
            if s == "1":
                print("正在注销此会员...")
                time.sleep(3)
                cursor = self.db.cursor()
                sql = "delete from vip_info where tel='%s'"%tel
                cursor.execute(sql)
                self.db.commit()
                print("注销成功！")
            else:
                print("放弃操作！")
        else:
            print("验证未通过，销卡失败！")

db = pymysql.connect('localhost','root','xuwei','hotelDB',use_unicode=True, charset="utf8")
A = vip_manager(db)

if __name__ == "__main__":
    main()