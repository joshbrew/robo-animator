# -*- coding: utf-8 -*-
#This is broken
from sshtunnel import SSHTunnelForwarder
import pymongo

MONGO_HOST = 'localhost'
MONGO_PORT = 5001
MONGO_DB = 'db'
MONGO_USERNAME = 'bob'
MONGO_PASSWORD = 'ross'

server = SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USERNAME,
        ssh_password=MONGO_PASSWORD,
        remote_bind_address=(MONGO_HOST,MONGO_PORT)
        )

server.start()

client = pymongo.MongoClient('0.0.0.0', server.local_bind_port)
db = client[MONGO_DB]
print(db.collection_names())

server.stop()