import time
from py2neo.ogm import *
from py2neo import Node, Relationship, Graph
import os,json

# NODES Author Hashtag tweet
#  RELATIONSHIPS: Reply(user , tweet) Retweet(user , tweet) Post(user, tweet) Mention(tweet,user Hashtag(tweet,hashtag)

graph = ''
try:
    graph = Graph(host="localhost",password="'")
except:
    print("coudn't connect to neo4j")
    exit()

count = 0
count2 = 0
count3 = 0
count4 = 0
flag=0
a = graph.run("MATCH (n) DETACH DELETE n")
pres = []
newpres = []
file_data = open('ds.json').read()
read_data = json.loads(file_data)
tx = graph.begin(autocommit=False)

for key in read_data.keys():
    read = read_data[key]
    hashtags = read['hashtags']
    mentions = read['mentions']
    tid = read['tid']
    type = read['type']
    author_screen_name = read['author_screen_name']
    author_id = read['author_id']

    user_node = Node("user",author_screen_name = author_screen_name)
    tx.merge(user_node, primary_key="author_screen_name")

    count3 = count3+1
    if(type=="Tweet"):
        count4 = count4+1
        tweet_node = Node("tweet",tid = tid)
        tx.merge(tweet_node, primary_key="tid")
        relation_user_tweet = Relationship(user_node,"tweets",tweet_node)
        tx.create(relation_user_tweet)

        if hashtags is not None:
            for hashtag in hashtags:
                count = count+1
                hashtag_node = Node("hashtag",hashtag=hashtag)
                tx.merge(hashtag_node,primary_key="hashtag")
                relation_tweet_hashtag = Relationship(tweet_node,"contains_hashtag",hashtag_node)
                tx.create(relation_tweet_hashtag)

        if mentions is not None:
            for mention in mentions:
                count2 = count2 + 1
                mention_node = Node("user",author_screen_name=mention)
                tx.merge(mention_node,primary_key="author_screen_name")
                relation_tweet_mention = Relationship(tweet_node,"mentions",mention_node)
                tx.create(relation_tweet_mention)
    if (flag == 0):
        tx.commit()
        graph.run("CREATE CONSTRAINT ON (a:user) ASSERT a.author_screen_name IS UNIQUE ")
        graph.run("CREATE CONSTRAINT ON (t:tweet) ASSERT t.tid IS UNIQUE ")
        graph.run("CREATE CONSTRAINT ON (h:hashtag) ASSERT h.hastag IS UNIQUE ")
        print("Constraints set")
        tx=graph.begin(autocommit=False)
        flag = 1
print("commiting now")
if flag==1:
    tx.commit()