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
import ast

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

  rowCount = request.json['rowCount']
  convertedRowCount = int (rowCount)
  #print(convertedRowCount, flush=True)

  doc_query = '''
    SELECT * from `disease_adjacency_rank_storage` order by curation_u_id desc limit %s;
  '''
  
  cur.execute(doc_query, (convertedRowCount))
  docs = cur.fetchall()
  #print("docs", docs, flush=True)

  subgraph = []
  allIds = []

  for doc in docs:
    ids = doc[2]
    ids = ast.literal_eval(ids)
    ids =[int(i) for i in ids]
    allIds.append(ids)

    subquery = '''MATCH (p) where id(p) IN {}
      with collect(id(p)) as nodes
      CALL apoc.algo.cover(nodes)
      YIELD rel
      RETURN  startNode(rel), rel, endNode(rel),id(startNode(rel)),id(rel),id(endNode(rel));'''.format(ids)
    subgraph.append(subquery)


  print("allIds", allIds, flush=True)    
  REPLACE_WITH_ALL_UNIQUE_IDS  = list(set([item for sublist in allIds for item in sublist]))
  

  fullgraph = '''MATCH (p) where id(p) IN  {}
    with collect(id(p)) as nodes
    CALL apoc.algo.cover(nodes)
    YIELD rel
    RETURN  startNode(rel), rel, endNode(rel),id(startNode(rel)),id(rel),id(endNode(rel));'''.format(REPLACE_WITH_ALL_UNIQUE_IDS)

  print("docs0", type(docs[0]), flush=True)

  d = dict()
  d['documents'] = docs
  d['subgraphs'] = subgraph
  d['fullgraph'] = fullgraph
  
  connection.commit()
  connection.close()

  return jsonify(d)

@app.route('/update', methods=["POST"])
@cross_origin()
def update_docs():
  print("Inside update", flush=True)
  connection = connect_db()
  cur = connection.cursor()

  docs = request.json['documents']
  print(docs)

  for doc in docs:
    print('\n doc', doc, flush=True)
    doc_query = '''
      UPDATE disease_adjacency_rank_storage
      SET rank = %s, adjacency_curation = %s
      WHERE curation_u_id = %s;
    '''
    curationId = doc[0]
    # convertedCurationId = int(curationId)

    cur.execute(doc_query, (doc[3], doc[4], curationId))

  d = dict()
  d['message'] = 'updated'
  
  connection.commit()
  connection.close()

  return jsonify(d)

if __name__ == '__main__':
  app.run(debug=False)