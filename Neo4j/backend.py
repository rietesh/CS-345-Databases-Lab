# -*- coding: UTF-8 -*-
from flask import Flask
from flask import render_template,request
from py2neo.ogm import *
from py2neo import Node, Relationship, Graph
import os,json

app = Flask(__name__)

def session_conn():
    try:
        graph = Graph(host="localhost", password="'")
        return graph
    except:
        raise("coudn't connect to neo4j")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query/<int:query_id>',methods=['GET', 'POST'])
def show_post(query_id):
    if (query_id == 1):
        if request.method=="GET":
            return render_template('index.html',query=1)
        elif request.method=="POST":
            hashtag = request.form.get('hashtag')
            if hashtag == '':
                hashtag="HappyBirthdayJustinBieber"
            print(hashtag)
            error = ''
            querymain1="match((a:hashtag)<-[:contains_hashtag]-(t:tweet)-[:mentions]->(b:user)) where a.hashtag='"+hashtag+"' return a.hashtag as hashtag ,b.author_screen_name as author_screen_name ,collect(t.tid) as tids ,count(*) as cnt order by cnt DESC limit 3;"
            session = session_conn()
            output = session.run(querymain1)
            temp = output.data()
            status = 1
            return render_template('index.html',query=1,request=request,status=status,error=error,output=temp,output2=temp)
    if (query_id == 2):
        if request.method=="GET":
            return render_template('index.html',query=2)
        elif request.method=="POST":
            usermention = request.form.get('usermention')
            if usermention == '' :
                usermention="narendramodi"
            error = ""
            session = session_conn()
            querymain2="match((a:hashtag)<-[:contains_hashtag]-(t:tweet)-[:mentions]->(b:user)) where b.author_screen_name='"+usermention+"' return b.author_screen_name as author_screen_name,a.hashtag as hashtag,collect(t.tid) as tids,count(*) as cnt order by cnt DESC limit 3;"
            output = session.run(querymain2)
            temp = output.data()
            status = 1
            return render_template('index.html',query=2, request=request, status=status, error=error, output=temp,output2=temp)