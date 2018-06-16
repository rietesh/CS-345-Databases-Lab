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

directory = 'ds/'
count = 0
count2 = 0
count3 = 0
count4 = 0
flag = 0
starttime = time.time()
a = graph.run("MATCH (n) DETACH DELETE n")
pres = []
newpres = []
for file_name in (os.listdir(directory)):
    file_data = open(os.path.join(directory, file_name)).read()
    read_data = json.loads(file_data)
    tx = graph.begin(autocommit=False)
    for key in read_data.keys():
        read = read_data[key]
        location = read['location']
        hashtags = read['hashtags']
        mentions = read['mentions']
        author = read['author']
        date_tweet = read['date']
        datetime = read['datetime']
        tid = read['tid']
        author_profile_image = read['author_profile_image']
        author_screen_name = read['author_screen_name']
        author_id = read['author_id']
        retweet_source_id = read['retweet_source_id']
        reply_source_id = read['replyto_source_id']
        user_node = Node("user",author_id = author_id,author = author,author_screen_name = author_screen_name)
        tweet_node = Node("tweet",tid = tid,date = date_tweet,datetime= datetime)

        tx.merge(user_node, primary_key="author_screen_name")
        tx.merge(tweet_node, primary_key="tid")


        relation_user_tweet = Relationship(user_node,"tweets",tweet_node)
        tx.create(relation_user_tweet)

        if location is not None:
            location_node = Node("location", location=location)
            tx.merge(location_node, primary_key="location")
            relation_tweet_location = Relationship(location_node,"hastweet",tweet_node)
            tx.create(relation_tweet_location)

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
        if retweet_source_id is not None:
            retweet_source = Node("tweet",tid=retweet_source_id)
            count3 = count3  +1
            tx.merge(retweet_source, primary_key="tid")
            relation_retweet_user = Relationship(retweet_source,"retweet_of",tweet_node)
            tx.create(relation_retweet_user)

        if reply_source_id is not None :
            reply_source = Node("tweet",tid=reply_source_id)
            count4 = count4  +1
            tx.merge(reply_source, primary_key="tid")
            relation_reply_user = Relationship(reply_source,"reply_of",tweet_node)
            tx.create(relation_reply_user)

        if (flag == 0):
            tx.commit()
            graph.run("create index on :user(author_screen_name)")
            graph.run("create index on :tweet(tid)")
            graph.run("create index on :hashtag(hashtag)")
            graph.run("create index on :location(location)")
            print("index set")
            tx=graph.begin(autocommit=False)
            flag = 1
    endtime = time.time()
    print(endtime,starttime)
    print("Before comitz")
    print(count,count2,count3,count4)
    print(file_name)
    if flag==1:
        tx.commit()
    # break