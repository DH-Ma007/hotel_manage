#!/usr/bin/env python3
#coding=utf-8
'''
name : Xu Weiwei
date : 2018-10-13
email: ...
modules: pymysql,time
function: 此模块功能为酒店客户预定,入住,换房,退房模块
		客户信息的存储及查询都通过连接mysql数据库,操作数据库中的表
'''

import pymysql

import time


#建一个预定客户的类
class Reverse_client(object):
	def __init__(self, name, room_num, phone_num, end_date):
		self.name = name
		self.room_num = room_num
		self.phone_num = phone_num
		self.end_date = end_date
	#将预定客户的信息插入到数据库
	def reverse_insert(self):
		#连接数据库，创建游标
		db = connect_db()
		cursor = db.cursor()
		try:
			sql_insert = "insert into book_info(name, phone_num,\
						room_num, end_date) values('%s', '%s', '%s', '%s')"\
						%(self.name, self.phone_num, self.room_num, self.end_date)
			cursor.execute(sql_insert)
			sql_update = "update room_info set 房间状态='已预定' where 房间号='%s'"%self.room_num
			cursor.execute(sql_update)
			db.commit()
			print("预定信息录入成功")
		except Exception as e:
			db.rollback()
			print("预定信息录入失败")
		cursor.close()
		db.close()

#建一个入住客户的类
class Client(object):
	def __init__(self, name, gender, ID_num, room_num,\
				phone_num, people_count, end_date):
		self.name = name
		self.gender = gender
		self.ID_num = ID_num
		self.room_num = room_num
		self.phone_num = phone_num
		self.people_count = people_count
		self.end_date = end_date
	#将入住客户的信息插入到数据库
	def check_in_insert(self):
		#链接数据库
		db = connect_db()
		cursor = db.cursor()
		try:
			sql_insert = "insert into check_in_info(name, gender,\
						ID_num,room_num, phone_num, people_count, end_date)\
						values('%s','%s','%s','%s','%s','%d', '%s')"\
						%(self.name,self.gender,self.ID_num,\
						self.room_num,self.phone_num,self.people_count,self.end_date)
			cursor.execute(sql_insert)

			sql_update = "update room_info set 房间状态='入住' where 房间号='%s'"%self.room_num
			cursor.execute(sql_update)

			sql_select = "select 押金,价格,会员价 from room_info where 房间号='%s'"%self.room_num
			cursor.execute(sql_select)
			deposit, price, vip_price = cursor.fetchone()

			sql_update = "update check_in_info set deposit='%d',price='%d',vip_price='%d'\
						where room_num='%s'"%(deposit, price, vip_price, self.room_num)
			cursor.execute(sql_update)

			db.commit()
			print("入住信息录入成功")
		except Exception as e:
			db.rollback()
			print("入住信息录入失败")
		cursor.close()
		db.close()

#创建一个函数来连接数据库
def connect_db():
	db = pymysql.connect(host = "localhost", user = "root",\
						password = "xuwei", database = "hotelDB",\
						charset = "utf8")
	return db


#客户预定登记		
def reverse_register():
	while True:
		name = input("请输入客户姓名:")
		if name == "##":
			break
		elif not name:
			print("请重新输入姓名")
			continue
		else:
			while True:
				room_num = input("请输入客户入住房号:")
				if len(room_num) == 4:
					break
				else:
					print("请重新输入")
			while True:
				phone_num = input("请输入客户手机号码:")
				if len(phone_num) == 11:
					break
				else:
					print("请重新输入手机号")
			end_date = input("请输入离店时间:")
		#创建客户对象
		people = Reverse_client(name, room_num, phone_num, end_date)
		people.reverse_insert()


#预定客户查询
def reverse_inquire():
	#连接数据库
	db = connect_db()
	#创建游标
	cursor = db.cursor()
	#输入预定客户手机号
	while True:
		number = input("请输入预定客户手机号码>>")
		if len(number) == 11:
			break
		else:
			print("请重新输入手机号")
	try:
		sql_select = "select * from book_info where phone_num = '%s'\
					order by id DESC limit 1"%number
		cursor.execute(sql_select)
		data = cursor.fetchone()
		if not data:
			print("没有此客户预定信息")
		else:
			print(data)
	except Exception as e:
		print("操作有误")
	cursor.close()
	db.close()


#入住客户登记
def check_in_register():
	while True:
		name = input("输入客户姓名:")
		if name == "##":
			break
		elif not name:
			continue
		else:
			while True:
				gender = input("输入客户性别 男(/女):")
				if gender == '男' or gender == '女':
					break
				else:
					print("请重新输入")
			while True:
				ID_num = input("输入客户身份证号码:")
				if len(ID_num) == 18:
					break
				else:
					print("请重新输入")
			while True:
				room_num = input("输入客户入住房号:")
				if len(room_num) == 4:
					break
				else:
					print("请重新输入房号")
			while True:
				phone_num = input("输入客户手机号码:")
				if len(phone_num) == 11:
					break
				else:
					print("请重新输入手机号")
			while True:
				try:
					people_count = int(input("输入客户入住人数:"))
					break
				except Exception as e:
					print("请重新输入")
			end_date = input("请输入退房时间:")
		#创建客户对象
		people = Client(name, gender, ID_num, room_num,\
						phone_num, people_count, end_date)	
		
		#将客户信息插入到客户入住信息数据表
		people.check_in_insert()


#入住房号查询
def check_in_require():
	room_num = input("请输入房间号>>")
	db = connect_db()
	cursor = db.cursor()
	try:
		sql_select = "select * from check_in_info where room_num = %s"%room_num
		cursor.execute(sql_select)
		data = cursor.fetchone()
		if not data:
			print("没有此房间入住信息")
		else:
			print(data)
	except Exception as e:
		print("操作有误")
	cursor.close()
	db.close()

#修改房号
def change_room():
	old_room_num = input("请输入原来的房间号>>")
	new_room_num = input("请输入新的房间号>>")
	db = connect_db()
	cursor = db.cursor()
	try:
		sql_select = "select * from check_in_info where room_num = %s"%old_room_num
		cursor.execute(sql_select)
		data = cursor.fetchall()
		if not data:
			print("没有此房间入住信息")
			return
		sql_update = "update check_in_info set room_num = '%s'\
		where room_num = '%s'"%(new_room_num, old_room_num)
		cursor.execute(sql_update)

		sql_update = "update room_info set 房间状态='入住' where 房间号='%s'"%new_room_num
		cursor.execute(sql_update)

		sql_update = "update room_info set 房间状态='空余' where 房间号='%s'"%old_room_num
		cursor.execute(sql_update)

		sql_select = "select 押金,价格,会员价 from room_info where 房间号='%s'"%new_room_num
		cursor.execute(sql_select)
		deposit, price, vip_price = cursor.fetchone()

		sql_update = "update check_in_info set deposit='%d',price='%d',vip_price='%d'\
						where room_num='%s'"%(deposit, price, vip_price,new_room_num)
		cursor.execute(sql_update)
		db.commit()
		print("房号修改成功")
	except Exception as e:
		db.rollback()
		print("房号修改失败")

#修改入离店时间
def extend_live():
	while True:
		room_num = input("请输入房间号>>")
		if room_num == "##":
			break
		elif len(room_num) != 4:
			print("请重新输入")
			continue
		end_date = input("请输入客户离店时间>>")
		db = connect_db()
		cursor = db.cursor()
		try:
			sql_select = "select * from check_in_info where room_num = %s"%room_num
			cursor.execute(sql_select)
			data = cursor.fetchone()
			if not data:
				print("没有此房间入住信息")
				return
			sql_update = "update check_in_info set end_date = '%s'\
						where room_num = '%s'"%(end_date, room_num)
			cursor.execute(sql_update)
			db.commit()
			print("修改离店时间成功")
		except Exception as e:
			db.rollback()
			print("离店时间修改失败")
		cursor.close()
		db.close()

#退房
def check_out():
	while True:
		room_num = input("请输入客户离店房间号>>")
		if room_num == "##":
			break
		elif len(room_num) != 4:
			print("请重新输入")
			continue
		print("请确定是否%s退房?y/n>>"%room_num)
		data = input()
		if data == 'n':
			print("请重新输入房号")
			break
		elif data == 'y':
			print("正在进行退房操作...")
			db = connect_db()
			cursor = db.cursor()
			try:
				sql_select = "select name,room_num,deposit,price,vip_price from\
							check_in_info where room_num='%s'"%room_num
				cursor.execute(sql_select)
				date = cursor.fetchone()
				if not date:
					print("没有此房间入住信息")
					return
				print(date)
				sql_update = "update room_info set 房间状态='空余' where 房间号='%s'"%room_num
				cursor.execute(sql_update)
				sql_update = "update check_in_info set end_date = '%s' where room_num = '%s'"%\
							(time.ctime(), room_num)
				cursor.execute(sql_update)
				sql_insert = "insert into live_history(name, gender, ID_num,room_num,\
						deposit, price, phone_num, people_count, start_date, end_date)\
						select name, gender, ID_num, room_num, deposit, price, phone_num,\
						people_count, start_date, end_date from check_in_info where\
						room_num = '%s'"%room_num
				cursor.execute(sql_insert)
				sql_delete = "delete from check_in_info where room_num = '%s'"%room_num
				cursor.execute(sql_delete)
				db.commit()
				print("退房成功")
			except Exception as e:
				print("退房失败")
		else:
			print("输入有误...")
			return

#查询所有正在入住的信息
def check_all_require():
	db = connect_db()
	cursor = db.cursor()
	try:
		sql_select = "select * from check_in_info"
		cursor.execute(sql_select)
		date = cursor.fetchall()
		if not data:
			print("没有入住信息")
		else:
			for i in date:
				print(i)
	except Exception as e:
		print("查询操作有误")

#查询入住历史
def history_require():
	db = connect_db()
	cursor = db.cursor()
	phone_num = input("请输入客户手机号:")
	try:
		sql_select = "select * from live_history where phone_num='%s'"%phone_num
		cursor.execute(sql_select)
		date = cursor.fetchall()
		if not date:
			print("没有入住历史")
		else:
			for i in date:
				print(i)
	except Exception as e:
		print("查询入住历史异常")

#查询界面
def info_query():
	while True:
		print('''
	=======信息查询========
	    1.预定信息查询
	    2.入住信息查询
	    3.所有入住查询
	    4.入住历史查询
	    5.返回上级
	=======================
			''')
		cmd = input("请输入命令>>")
		if cmd == "5":
			break
		elif cmd == "1":
			reverse_inquire()
		elif cmd == "2":
			check_in_require()
		elif cmd == "3":
			check_all_require()
		elif cmd == "4":
			history_require()
		else:
			print("输入错误,请重新输入")

