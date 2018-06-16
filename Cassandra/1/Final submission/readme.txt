Backend Technology: Flask(Python)
FroneEnd Technology : HTML,CSS,Bootstrap

How to Run: 

In terminal Write following commands:
 
EXPORT FLASK_APP=backend.py
EXPORT FLASK_DEBUG=1
flask run


Language to Insert: Python


Files Desctiption:
    query_insert.py = Put the file in same folder where 'workshop_dataset1' directory is present
    Backend.py: Commands to run to display the output
    templates/index.html: Front End file
    150101072_query5.csv : Output of query5
    150101072_query8.csv : Output of query8
    150101072_schema_query5.txt: Schema of table for query5
    150101072_schema_query8.txt: Schema of table for query8


Data Model:

Query1 :

Table Name: t_by_hashtag1, helper1

t_by_hashtag1:
    Primary key : ((date_tweet),hashtag,tid))
	    date_tweet: Partition key
	    hashtag,tid : clustering key

    tid has been put in clustering key to maintain uniqueness so that tweets with same date and hastag can also enter in database

After inserting data in t_by_hashtag,since we need data to be sorted by count of hashtag and count of hastag is not in clustering key .
I'm using helper1 table to insert the required values

helper1:
    Primary key : (hashtag,cnt,date_tweet)
    hashtag: Partition key
    cnt,date_tweet: clustering key

Now we can pick the hashtags in sorted order of count since cnt is a clustering key


Query2 :

Table Name: t_by_hashtag2, helper2

t_by_hashtag2:
    Primary key : ((date_tweet),hashtag,mention,tid))
	    date_tweet: Partition key
	    hashtag,mention,tid : clustering key

	Since we want hashtag mention pair count the clustering keys are hashtag and mention.

	To fetch the counts of hashtag mention pair the select query has group by on date_tweet,hashtag,mention and hence we get the counts.

	Once the counts are with us, we use helper2 table to insert the pairs in the table where cnt is present in clustering key with descending order.

helper2:
    Primary key : (date_tweet,cnt,hashtag,mention)
    date_tweet: Partition key
    cnt,hashtag,mention: clustering key

Now we can pick the desired pairs of hashtag and mention in descendingg order of counts.