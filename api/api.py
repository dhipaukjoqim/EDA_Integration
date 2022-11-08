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

# from api.marklogic_queries.retrieve_doc_titles import fetch_meta_prev, fetch_prev
from marklogic_queries.retrieve_doc_titles import fetch_meta_prev, fetch_prev

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

# mysql_host = os.getenv("DB_HOST")
# mysql_port = os.getenv("DB_PORT")
# mysql_dbname = os.getenv("DB_DATABASE")
# mysql_user = os.getenv("DB_USERNAME")
# mysql_password = os.getenv("DB_PASSWORD")

mysql_host = "ae1-sum02-rds01.cafrrlsc91pe.us-east-1.rds.amazonaws.com"
mysql_port = "3306"
mysql_dbname = "ome_star_schema"
mysql_user = "joqim-rds"
mysql_password = "?QMK7bBosMve"

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
def get_removed_docs():
  print('Inside get removed docs')
  connection = connect_db()
  cur = connection.cursor()

  givenDate = request.json['formattedDate']
  print("givenDate", givenDate)
  
  removed_doc_query = '''SELECT removed_doc_cause, COUNT(*) AS magnitude 
    FROM `removed_doc_analysis`
    WHERE date_processed > '{}'
    GROUP BY removed_doc_cause
    '''.format(givenDate)
  
  cur.execute(removed_doc_query)
  removed_docs = cur.fetchall()
  #print(removed_docs, flush=True)
  
  d = dict()
  d['removed_documents'] = removed_docs
  
  connection.commit()
  connection.close()

  return jsonify(d)

@app.route('/meta_prev', methods=["POST"])
@cross_origin()
def get_meta_prev():
  print('Inside get META previous curations')
  connection = connect_db()
  cur = connection.cursor()

  removedPieDate = request.json['removedPieDate']+":00Z"
  oneWeekAgoRemovedPieDate = request.json['oneWeekAgoRemovedPieDate']+":00Z"
  userGroupArray = request.json['userGroupArray']

  meta_prev_list = fetch_meta_prev(removedPieDate, oneWeekAgoRemovedPieDate, userGroupArray)
  print("meta_prev_list", meta_prev_list)

  connection.commit()
  connection.close()

  return jsonify(meta_prev_list)

@app.route('/prev', methods=["POST"])
@cross_origin()
def prev():
  print('Inside get previous curations')
  connection = connect_db()
  cur = connection.cursor()

  removedPieDate = request.json['removedPieDate']+":00Z"
  oneWeekAgoRemovedPieDate = request.json['oneWeekAgoRemovedPieDate']+":00Z"
  userGroup = request.json['userGroupSelected']

  prev_list = fetch_prev(removedPieDate, oneWeekAgoRemovedPieDate, userGroup)

  connection.commit()
  connection.close()

  return jsonify(prev_list)

if __name__ == '__main__':
  app.run(debug=False)