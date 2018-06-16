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
tx = graph.begin()
a = tx.run("MATCH (n) DETACH DELETE n")
pres = []
newpres = []
for file_name in (os.listdir(directory)):
    file_data = open(os.path.join(directory, file_name)).read()
    read_data = json.loads(file_data)
    for key in read_data.keys():
        read = read_data[key]
        location = 'none' if read['location'] is None else read['location']
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
        location_node = Node("location",location=location)

        tx.merge(user_node, primary_label="user",primary_key="author_screen_name")
        tx.merge(tweet_node,primary_label="tweet", primary_key="tid")
        tx.merge(location_node,primary_label="location", primary_key="location")


        relation_user_tweet = Relationship(user_node,"tweets",tweet_node)
        tx.create(relation_user_tweet)

        relation_tweet_location = Relationship(location_node,"hastweet",tweet_node)
        tx.create(relation_tweet_location)

        if hashtags is not None:
            for hashtag in hashtags:
                count = count+1
                hashtag_node = Node("hashtag",hashtag=hashtag)
                tx.merge(hashtag_node,primary_label="hashtag",primary_key="hashtag")
                relation_tweet_hashtag = Relationship(tweet_node,"contains_hashtag",hashtag_node)
                tx.create(relation_tweet_hashtag)
        if mentions is not None:
            for mention in mentions:
                count2 = count2 + 1
                mention_node = Node("user",author_screen_name=mention)
                tx.merge(mention_node,primary_label="user",primary_key="author_screen_name")

                relation_tweet_mention = Relationship(tweet_node,"mentions",mention_node)
                tx.create(relation_tweet_mention)
        if retweet_source_id is not None:
            retweet_source = Node("tweet",tid=retweet_source_id)
            count3 = count3  +1
            tx.merge(retweet_source,primary_label="tweet", primary_key="tid")
            relation_retweet_user = Relationship(retweet_source,"retweeted_by",user_node)
            tx.create(relation_retweet_user)

        if reply_source_id is not None :
            reply_source = Node("tweet",tid=reply_source_id)
            count4 = count4  +1
            tx.merge(reply_source,primary_label="tweet", primary_key="tid")
            relation_reply_user = Relationship(reply_source,"replied_by",user_node)
            tx.create(relation_reply_user)

        # if (flag == 0):
        #     tx.commit()
        #     graph.run("create index on :user(author_screen_name)")
        #     graph.run("create index on :tweet(tid)")
        #     graph.run("create index on :hashtag(hashtag)")
        #     print("index set")
        #     tx=graph.begin()
        #     flag = 1
    endtime = time.time()
    print(endtime,starttime)
    print("Before comitz")
    print(count,count2,count3,count4)
    print(file_name)
tx.commit()
    # break
# from py2neo.ogm import *
# from py2neo import Node, Relationship, Graph
# import os,json
#
# # a = Node("Person", name="Alice")
# # b = Node("Person", name="Bob")
# # ab = Relationship(a, "KNOWS", b)
# # print ab
#
# # NODES :
# # Author
# # Hashtag
# # tweet
#
#
# # RELATIONSHIPS:
# # Reply(user , tweet)
# # Retweet(user , tweet)
# # Post(user, tweet)
# # Mention(tweet,user)
# # Hashtag(tweet,hashtag)
#
# class user(GraphObject):
#     __primarykey__ = "author_id"
#
#     author_id = Property()
#     author = Property()
#     author_screen_name = Property()
#
#     post = RelatedTo("tweet")
#     reply = RelatedTo("tweet")
#     retweet = RelatedTo("tweet")
#
#     mentioned_in = RelatedFrom("tweet")
#
#
# class tweet(GraphObject):
#     __primarykey__ = "tid"
#
#     tid = Property()
#     datetime = Property()
#     date = Property()
#
#     post = RelatedFrom("user")
#     reply = RelatedFrom("user")
#     retweet = RelatedFrom("user")
#
#     mention = RelatedTo("user")
#
# graph = ''
# try:
#     graph = Graph(host="localhost",password="'")
#     # graph = Graph(password="'")
# except:
#     print("coudn't connect to neo4j")
#     exit()
# print(graph)
# directory = 'ds/'
# count =0
# a = graph.run("MATCH (n) DETACH DELETE n")
# tx = graph.begin()
# print(a.data())
# for file_name in (os.listdir(directory)):
#     file_data = open(os.path.join(directory, file_name)).read()
#     read_data = json.loads(file_data)
#     for key in read_data.keys():
#         read = read_data[key]
#         location = 'none' if read['location'] is None else read['location']
#         quote_count = read['quote_count']
#         reply_count = read['reply_count']
#         hashtags = read['hashtags']
#         datetime = read['datetime']
#         date_tweet = read['date']
#         like_count = read['like_count']
#         verified = True if read['verified'] else False
#         sentiment = read['sentiment']
#         author = read['author']
#         tid = read['tid']
#         retweet_count = read['retweet_count']
#         tweet_type = read['type']
#         media_list = read['media_list'] if read['media_list'] is not None else None
#         quoted_source_id = read['quoted_source_id']
#         url_list = read['url_list']
#         tweet_text = read['tweet_text']
#         author_profile_image = read['author_profile_image']
#         author_screen_name = read['author_screen_name']
#         author_id = read['author_id']
#         lang = read['lang']
#         keywords_processed_list = read['keywords_processed_list']
#         retweet_source_id = read['retweet_source_id']
#         mentions = read['mentions']
#         replyto_source_id = read['replyto_source_id']
#
#         # user_node = Node("user",author_id = author_id,author = author,author_screen_name = author_screen_name)
#         tx.run("create (:user {author:{arg1}} ) ;",{"arg1":author})
#         print("run")
#     print("Before comit")
#     tx.commit()
#     break
#
#         # user_node = user()
#         # user_node.author_id=author_id
#         # user_node.author=author
#         # user_node.author_screen_name=author_screen_name
#         # tweet_node = tweet()
#         # tweet_node.tid=tid
#         # tweet_node.datetime=datetime
#         # tweet_node.date=date_tweet
#         #
#         # user_node.post.add(tweet_node)
#         #
#         # graph.push(user_node)
#         # graph.push(tweet_node)
#
#         # print("pushed")
#     # break
#
# from py2neo.ogm import *
# from py2neo import Node, Relationship, Graph
# import os, json
#
# # NODES :
# # Author
# # Hashtag
# # tweet
#
# # RELATIONSHIPS:
# # Reply(user , tweet)
# # Retweet(user , tweet)
# # Post(user, tweet)
# # Mention(tweet,user)
# # Hashtag(tweet,hashtag)
#
# '''
# class user(GraphObject):
#     __primarykey__ = "author_id"
#
#     author_id = Property()
#     author = Property()
#     author_screen_name = Property()
#
#     post = RelatedTo("tweet")
#     reply = RelatedTo("tweet")
#     retweet = RelatedTo("tweet")
#
#     mentioned_in = RelatedFrom("tweet")
#
# class tweet(GraphObject):
#     __primarykey__ = "tid"
#
#     tid = Property()
#     datetime = Property()
#     date = Property()
#
#     post = RelatedFrom("user")
#     reply = RelatedFrom("user")
#     retweet = RelatedFrom("user")
#
#     mention = RelatedTo("user")
#
#
# # user_node = user()
# # user_node.author_id=author_id
# # user_node.author=author
# # user_node.author_screen_name=author_screen_name
# # tweet_node = tweet()
# # tweet_node.tid=tid
# # tweet_node.datetime=datetime
# # tweet_node.date=date_tweet
# #
# # user_node.post.add(tweet_node)
# #
# # graph.push(user_node)
# # graph.push(tweet_node)
# '''
#
# graph = ''
# try:
#     graph = Graph(host="localhost", password="'")
#     # graph = Graph(password="'")
# except:
#     print("coudn't connect to neo4j")
#     exit()
#
# directory = 'ds/'
# count = 0
# count2 = 0
# # a = graph.run("MATCH (n) DETACH DELETE n")
# # tx = graph.begin()
# # pres = []
# # newpres = []
# # for file_name in (os.listdir(directory)):
# #     file_data = open(os.path.join(directory, file_name)).read()
# #     read_data = json.loads(file_data)
# #     for key in read_data.keys():
# #         read = read_data[key]
# #         location = 'none' if read['location'] is None else read['location']
# #         quote_count = read['quote_count']
# #         reply_count = read['reply_count']
# #         hashtags = read['hashtags']
# #         datetime = read['datetime']
# #         date_tweet = read['date']
# #         like_count = read['like_count']
# #         verified = True if read['verified'] else False
# #         sentiment = read['sentiment']
# #         author = read['author']
# #         tid = read['tid']
# #         retweet_count = read['retweet_count']
# #         tweet_type = read['type']
# #         media_list = read['media_list'] if read['media_list'] is not None else None
# #         quoted_source_id = read['quoted_source_id']
# #         url_list = read['url_list']
# #         tweet_text = read['tweet_text']
# #         author_profile_image = read['author_profile_image']
# #         author_screen_name = read['author_screen_name']
# #         author_id = read['author_id']
# #         lang = read['lang']
# #         keywords_processed_list = read['keywords_processed_list']
# #         retweet_source_id = read['retweet_source_id']
# #         mentions = read['mentions']
# #         replyto_source_id = read['replyto_source_id']
# #
# #         user_node = Node("user",author_id = author_id,author = author,author_screen_name = author_screen_name)
# #         tweet_node = Node("tweet",tid = tid,date = date_tweet,datetime= datetime)
# #         relation_user_tweet = Relationship(user_node,"tweets",tweet_node)
# #
# #
# #         tx.merge(user_node, primary_key="author_screen_name")
# #         tx.merge(tweet_node, primary_key="tid")
# #         tx.create(relation_user_tweet)
# #         if hashtags is not None:
# #             for hashtag in hashtags:
# #                 count = count+1
# #                 hashtag_node = Node("hashtag",hashtag=hashtag)
# #                 relation_tweet_hashtag = Relationship(tweet_node,"contains_hashtag",hashtag_node)
# #                 tx.merge(hashtag_node,primary_key="hashtag")
# #                 tx.create(relation_tweet_hashtag)
# #
# #     print("Before comitz")
# #     print(count)
# #     print(file_name)
# #     tx.commit()
# #     break
#
# tx = graph.begin()
# for file_name in (os.listdir(directory)):
#     file_data = open(os.path.join(directory, file_name)).read()
#     read_data = json.loads(file_data)
#     for key in read_data.keys():
#         read = read_data[key]
#         mentions = read['mentions']
#         tid = read['tid']
#         if mentions is not None:
#             for mention in mentions:
#                 count2 = count2 + 1
#                 mention_node = Node("user", author_screen_name=mention)
#                 tweet_node = Node("tweet", tid=tid)
#                 relation_tweet_mention = Relationship(tweet_node, "mentions", mention_node)
#                 tx.merge(mention_node, primary_key="author_screen_name")
#                 tx.create(relation_tweet_mention)
#     tx.commit()
#     break