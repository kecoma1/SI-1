# -*- coding: utf-8 -*-
import os
import sys, traceback
import pymongo
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select
import datetime
import random

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["si1"]

mycol = mydb["topUSA"]