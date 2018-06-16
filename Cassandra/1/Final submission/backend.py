# -*- coding: UTF-8 -*-
from flask import Flask
from flask import render_template,request
from cassandra.cluster import Cluster
import json, os
import datetime as mod_datetime

app = Flask(__name__)

def session_conn():
    try:
        cluster = Cluster()
    except:
        print("couldn't connect to the localhost cluster")
        raise ("error in localhost connection to cassandra")
    try:
        session = cluster.connect('a1')
    except:
        print("couldn't connect to the keyspace")
        raise ("error in keyspace connection")
    return session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query/<int:query_id>',methods=['GET', 'POST'])
def show_post(query_id):
    if (query_id == 1):
        if request.method=="GET":
            return render_template('index.html',query=1)
        elif request.method=="POST":
            status = 0
            output = ''
            error = ''
            query = "select * from helper1;"
            session = session_conn()
            output = session.execute(query)
            status = 1
            return render_template('index.html',query=1,request=request,status=status,error=error,output=output)
    if (query_id == 2):
        if request.method=="GET":
            return render_template('index.html',query=2)
        elif request.method=="POST":
            keyword = request.form.get('keyword')
            error = ""
            status = 0
            output = ''
            query = "select * from helper2;"
            session = session_conn()
            output = session.execute(query)
            status = 1
            return render_template('index.html',query=2, request=request, status=status, error=error, output=output)