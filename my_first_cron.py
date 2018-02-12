import os, sys
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pymysql
import time
from google_translation import translation_tool as T_tool

test_string = """Card 6:  The likely outcome »
The Hermit
This is a time for you to be alone or may herald a time of loneliness. Take this time for quiet introspection and rest.
Don't worry, you will find the answers, but the Hermit signals a warning not to make hasty decisions.
If you have been unwell this is a time for rest and recuperation."""

xpath_list = ["/html/body/div[2]/div/div[2]/div[2]", "/html/body/div[2]/div/div[3]/div[2]",
              "/html/body/div[2]/div/div[4]/div[2]",
              "/html/body/div[2]/div/div[5]/div[2]", "/html/body/div[2]/div/div[6]/div[2]",
              "/html/body/div[2]/div/div[7]/div[2]"]

big_arcana_dict = {0: 'Fool', 1: 'Magician', 2: 'Priestess', 3: 'Empress', 4: 'Emperor', 5: 'Hierophant',
                   6: 'Lovers', 7: 'Chariot', 8: 'Strength', 9: 'Hermit', 10: 'Fortune', 11: 'Justice',
                   12: 'Hanged', 13: 'Death', 14: 'Temperance', 15: 'Devil', 16: 'Tower', 17: 'Star', 18: 'Moon',
                   19: 'Sun', 20: 'Judgement', 21: 'World'}
error_hander = {
    "no id": "[-] Cannot Catch ID from data",
    "no card": "[-] Cannot Judge Card from data",
    "no article": "[-] Cannot Get Article from data",
    "db fail": "[-] Fail To Connect Mysql"
}


def errorhander(fail_log):
    f = open("errorlog", "a")
    try:
        f.write(error_hander[fail_log] + time.ctime())
    except:
        f.write("[!]" + fail_log + time.ctime())
    f.close()


def big_arcana_count(name):
    big_arcana_dict = {}
    for i in range(0, 22):
        big_arcana_dict[i] = name[i]
    return big_arcana_dict


def locate():
    path = "C:\\Users\\ninthDVEIL HUNSTER\\Downloads\\WS_Images"
    os.chdir(path)
    list = os.listdir(path)
    name = []
    for i in list:
        name.append(i[3:-4])
    return name[1:1 + 22]


import random


def random_list():
    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
           30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
           57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
           84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
           109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130,
           131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152,
           153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174,
           175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196,
           197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218,
           219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240,
           241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262,
           263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284,
           285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306,
           307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328,
           329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350,
           351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372,
           373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394,
           395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416,
           417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438,
           439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460,
           461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482,
           483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504,
           505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526,
           527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548,
           549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570,
           571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592,
           593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614,
           615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627]

    try:
        for i in range(135434556 - 135432416):
            a = random.choice(lst)
            wdriver(a)
            lst.remove(a)
            time.sleep(5)
    except KeyboardInterrupt:
        # print(lst)
        print("记得改list啊！！！！")
        savelst(lst)


def savelst(lst):
    f = open("list.txt", "a")
    f.write("[*] saving time :" + str(time.ctime()) + "\n")
    f.write("[")
    for i in lst:
        f.write(str(i) + ",")
    f.write("]")
    f.close()


def wdriver(a):
    x = webdriver.Firefox()
    i = 0
    startnum = 135432416
    url = "https://www.free-tarot-reading.net/readings/%s" % (startnum + a)
    for i in range(0, 6):
        try:
            x.get(url)
            print("[+] Get payload %s" % (startnum + a), time.ctime())
            content_1 = (x.find_element_by_xpath(xpath_list[i]).text)
            # print (content_1)
            stringmaker(content_1)

        except:
            errorhander("wdriver error")
    time.sleep(5)
    x.close()


def stringmaker(string):
    string = string.split("\n")
    i = 0
    id = 0
    card = ""
    text = ""
    if "Card" in string[0] and ord(string[0][5]) > 48 and ord(string[0][5]) < 57:
        id = int(string[0][5])
    else:
        errorhander("no id")
    for i in range(0, 22):
        if big_arcana_dict[i] in string[1]:
            card = big_arcana_dict[i]
            break

    for i in range(2, len(string)):
        text += string[i].replace("'", "\\'") + '\\n'

    if text == "":
        errorhander("no text")

    database_write(id, card, text)


def database_create():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "tarot")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    for i in range(0, 22):
        string = "alter table tarot.%s CONVERT TO CHARACTER SET utf8" % big_arcana_dict[i]
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(string)

    cursor.close()

    # 关闭数据库连接
    db.close()


def database_write(id, tables_name, text):
    # 打开数据库连接
    if database_avoid_cycle(tables_name, id) == True:
        db = pymysql.connect("localhost", "root", "", "tarot")

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句

        sql = "INSERT INTO %s VALUES (%s, '%s')" % (tables_name, id, text)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print("[+] Success to upload data with ", id, tables_name, time.ctime())
        except:
            # 如果发生错误则回滚
            db.rollback()
            print("Error")

        # 关闭数据库连接
        db.close()
    else:
        pass


def database_select(id, table):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "tarot")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * from %s WHERE id=%s LIMIT 0,1" % (table, id)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            text = row[1]
            print(text)

    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


def database_avoid_cycle(table, id):
    # 防止数据重复上传
    db = pymysql.connect("localhost", "root", "", "tarot")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * from %s WHERE id=%s LIMIT 0,1" % (table, id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if results == ():
            db.close()
            return True
        for row in results:
            text = row[1]
            if text != "":
                db.close()
                print("[-] Fail to upload data for the data has been existed")
                return False
    except:
        print("[-] error ")
        db.close()
        return True


def database_delete_all():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "tarot")
    for i in range(0, 22):
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 删除语句
        sql = "DELETE FROM %s" % (big_arcana_dict[i])
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

    # 关闭连接
    db.close()


def database_translate_content(table, id):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "tarot")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * from %s WHERE id=%s LIMIT 0,1" % (table, id)
    # print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            text = row[1]
            text = (T_tool(text))
            #print(text)
            database_insert_translate(table, id, text)
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


def database_insert_translate(tables_name, id, text):
    """
    不知道咋中文就是进不去，后来觉得写个文件得了。
    :param tables_name:
    :param id:
    :param text:
    :return:
    """
    sql = "UPDATE %s SET cn_data='%s' WHERE id=%s;" % (tables_name, text, id)
    f = open("sql.txt", "a")
    f.write(sql + "\n" + "COMMIT;" + "\n")


def translate_main_function():
    for table_name in big_arcana_dict.values():
        for id in "123456":
            database_translate_content(table_name, id)


def main():
    """
    135432416-135434556
135433044-135432416
    Done 135432416-135433044
        135433378
    :return:
    """
    random_list()


if __name__ == '__main__':
    #translate_main_function()
    # main()
    # stringmaker(string)
    # stringmaker(string=test_string)
    # database_select(6,"hermit")
    # database_delete_all()
    # database_create()
    for i in range(0,22):
        print (str(i)+"=>"+"\""+big_arcana_dict[i]+"\""+",")