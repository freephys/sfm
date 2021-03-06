#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: pay_repo.py
@time: 16/11/10 下午11:21
"""

from service.repository.base_repo import BaseRepo


class PayRepo(BaseRepo):
    TABLE_NAME = 'sfm_pay'

    def insert(self, water_id, channel_id, channel_water_id, amount, order_id, time, target_type):
        sql = """
            insert into {} set water_id=%s, channel_id=%s, channel_water_id=%s, amount=%s, order_id=%s, time=%s, target_type=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_lastrowid(sql, water_id, channel_id, channel_water_id, amount, order_id, time, target_type)
        return res

    def select_order_id(self, order_id):
        sql = """
            select * from {} where order_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.query(sql, order_id)
        return res
