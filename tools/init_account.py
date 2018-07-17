# -*- coding:utf-8 -*-
import time
import pymongo

conn = pymongo.MongoClient()
db = conn.kiwi

timestamp = int(time.time())
docs = {
    "mail": "lonersun@126.com",
    "password": "123456",
    "sex": 1,
    "mobile": "18310751050",
    "name": "Lonersun",
    "created_at": timestamp,
    "updated_at": timestamp,
}

account = db.account.insert(docs)
print account

