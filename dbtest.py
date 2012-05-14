import os
import logging 
from sqlite3 import *
from pyencoder import db

myDB = db.DBConnection()
request = myDB.select("SELECT * from watch WHERE id = 0")
myDB.upsert("watch",{'abitrate': '44800','acodec':'ac3'},{'id': '1'})