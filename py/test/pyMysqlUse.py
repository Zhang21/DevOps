#!/bin/python3
#-*- coding: utf-8 -*-

import pymysql


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1314520',
    port=3306,
    db='testDB',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    #commit to save
    connection.commit()

    with connection.cursor() as cursor:
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()















































