# encoding=utf-8
import pymysql
import sys
import time

# reload(sys)
# sys.setdefaultencodding('utf-8')

# 创建数据库连接对象
def connect_db():
    db = pymysql.connect(host="localhost", user="root",
                     password="xuwei",database="hotelDB",
                     charset="utf8")
    # 利用db创建游标对象
    return db

class Rooms_select(object):

    def selec_any(self):
        db = connect_db()
        cursor = db.cursor()
        try:
            sql = "select * from room_info;"
            cursor.execute(sql)
        except Exception as e:
            print(e)
            db.rollback()
        print("房间类型 房间号 押金 价格 会员价 房间状态 楼层")
        result = cursor.fetchall()
        for line in result:
            print(line[0], " ", line[1], ' ', line[2], ' ',
                  line[3], ' ', line[4], ' ', line[5], ' ', line[6])
        cursor.close()
        db.close()

    def selec_floor(self):
        db = connect_db()
        cursor = db.cursor()
        while True:
            try:
                floor = int(input("请输入楼层:"))
                sql = "select * from room_info where 楼层='%s'" % floor
                cursor.execute(sql)
            except Exception as e:
                print(e)
                db.rollback()
            if floor == 0:
                break
            print("房间类型 房间号 押金 价格 会员价 房间状态 楼层")
            result = cursor.fetchall()
            for line in result:
                print(line[0], " ", line[1], ' ', line[2], ' ',
                      line[3], ' ', line[4], ' ', line[5], ' ', line[6])
        cursor.close()
        db.close()

    def selec_type(self, db):
        db = connect_db()
        cursor = db.cursor()
        while True:
            try:
                tp = input("请输入房间类型:")
                sql = "select * from room_info where 房间类型='%s'" % tp
                cursor.execute(sql)
            except Exception as e:
                print(e)
                db.rollback()

            if tp == '##':
                break
            print("房间类型 房间号 押金 价格 会员价 房间状态 楼层")
            result = cursor.fetchall()
            for line in result:
                print(line[0], " ", line[1], ' ', line[2], ' ',
                      line[3], ' ', line[4], ' ', line[5], ' ', line[6])
        cursor.close()
        db.close()

# class Rooms_update(object):
#     def updat_check_in(self):
#         db = connect_db()
#         cursor = db.cursor()
#         while True:
#             try:
#                 floor = int(input('请输入楼层:'))
#                 sql = "select * from room_info where 房间状态='空余' and 楼层='%s'"%floor
#                 count = cursor.execute(sql)
#                 room = int(input('请输入房间号:'))
#                 sql = "update room_info set 房间状态='入住' where 房间号='%s'"%room
#                 count = cursor.execute(sql)
#                 sql = "select* from room_info where 房间状态='入住' and 房间号='%s'"%room
#                 count = cursor.execute(sql)
#             except Exception as e:
#                 print(e)
#                 db.rollback()
#             print('ok')
#             if room == 0 or floor == 0:
#                 break

#     def fix_in_advance(self):
#         db = connect_db()
#         cursor = db.cursor()
#         while True:
#             try:
#                 floor = int(input('请输入楼层:'))
#                 sql = "select * from room_info where 房间状态='空余' and 楼层='%s'"%floor
#                 count = cursor.execute(sql)
#                 room = int(input('请输入房间号:'))
#                 sql = "update room_info set 房间状态='入住' where 房间号='%s'"%room
#                 count = cursor.execute(sql)
#                 sql = "select * from room_info where 房间状态='预订' and 房间号='%s'"%room
#                 count = cursor.execute(sql)
#             except Exception as e:
#                 print(e)
#                 db.rollback()
#             print('ok')
#             if room == 0 or floor == 0:
#                 break

#     def vacation(self):
#         db = connect_db()
#         cursor = db.cursor()
#         while True:
#             try:
#                 floor = int(input('请输入楼层:'))
#                 sql = "select * from room_info where 房间状态='入住' and 楼层='%s'"%floor
#                 count = cursor.execute(sql)
#                 room = int(input('请输入房间号:'))
#                 sql = "update room_info set 房间状态='入住' where 房间号='%s'"%room
#                 count = cursor.execute(sql)
#                 sql = "select * from room_info where 房间状态='空余' and 房间号='%s'"%room
#                 count = cursor.execute(sql)
#             except Exception as e:
#                 print(e)
#                 db.rollback()
#             print('ok')
#             if room == 0 or floor == 0:
#                 break


def select():
    while True:
        print('''
            ==========================
                1.查看全部房间
                2.按类型查看房间
                3.按楼层查看房间
                4.返回上级
            ==========================
            ''')
        rs = Rooms_select()

        try:
            cmd = int(input('请输入:'))
        except Exception:
            print('输入错误')
        if cmd == 0:
            break
        elif cmd == 1:
            rs.selec_any()
        elif cmd == 2:
            rs.selec_type()
        elif cmd == 3:
            rs.selec_floor()
        elif cmd == 4:
            return


# def update():
#     print('''
#         ==========================
#             1.入住
#             2.预订
#             3.退房
#             4.返回上级
#         ==========================
#         ''')
#     ru = Rooms_update()
#     while True:
#         try:
#             cmd = int(input('请输入:'))
#         except Exception:
#             print('输入错误')
#         if cmd == 0:
#             break
#         elif cmd == 1:
#             ru.updat_check_in(db)
#         elif cmd == 2:
#             ru.fix_in_advance(db)
#         elif cmd == 3:
#             ru.vacation(db)
#         elif cmd == 4:
#             return


# def main():
#     while True:
#         print('''
#             ========================
#                 1.查看房态
#                 2.修改房态
#                 3.返回上级
#             ========================
#             ''')
#         try:
#             cmd = int(input('请输入命令:'))
#         except Exception:
#             print('输入错误')
#         if not cmd:
#             break
#         elif cmd == 1:
#             select()
#         elif cmd == 2:
#             update()
#         elif cmd == 3:
#             break
#     cursor.close()
#     db.close()

# if __name__ == "__main__":
#     main()

