# from asyncio.windows_events import NULL
from pickle import NONE
from re import T
import urllib.request
from flask import Flask, jsonify, request
from flask_cors import cross_origin
import pymysql
import json
import os
from dotenv import load_dotenv
import logging
import math
import pymysql

pymysql.install_as_MySQLdb()
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import asyncio

# from rest_framework.response import Response

#X+Ve\'nz"W"~7CT
#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

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
#APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

mysql_host = "ae1-sum02-rds01.cafrrlsc91pe.us-east-1.rds.amazonaws.com"
mysql_port = "3306"
mysql_dbname = "ome_star_schema"
mysql_user = "omealerts_sql_access"
mysql_password = "wORgj&6pk@d!"

connection = None
CONNECTION_TIMEOUT = 5000

print(mysql_host)
print(mysql_port)
print(mysql_dbname)
print(mysql_user)

def connect_db():
  connection = pymysql.connect(host=mysql_host, user=mysql_user, port=int(mysql_port), password=mysql_password, database=mysql_dbname, connect_timeout=CONNECTION_TIMEOUT)
  print("connected to db", flush=True)
  return connection

def get_cursor(connection): 
  connection.ping(reconnect=True)
  return connection.cursor()

app = Flask(__name__)

@app.route('/', methods=["POST"])
@cross_origin()
def docs():
  connection = connect_db()
  cur = connection.cursor()
  doc_query = '''SELECT *
    FROM `disease_adjacency_rank_storage`
    '''
  
  cur.execute(doc_query)
  docs = cur.fetchall()
  d = dict()
  d['removed_documents'] = docs
  
  connection.commit()
  connection.close()

  return jsonify(d)

if __name__ == '__main__':
  app.run(debug=False)