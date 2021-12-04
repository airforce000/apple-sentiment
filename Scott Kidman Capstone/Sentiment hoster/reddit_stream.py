import datetime
import time

import mysql.connector
import praw
from unidecode import unidecode
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# connect to reddit api bot "redditadmin13"
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent='<Reddit scrape 1.0 by /u/Airforce0001>'
)

# connent to mysql database
mydb = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    database=""
)

mycursor = mydb.cursor()

# creates the database if not already present
mycursor.execute("CREATE DATABASE IF NOT EXISTS reddit_data")

# although not using all data in current design all data from comment is stored
mycursor.execute("""CREATE TABLE IF NOT EXISTS reddit_data.reddit_data_sentiment
                (date_time DATETIME,
                subreddit VARCHAR(500),
                title VARCHAR(500),
                body VARCHAR(2000),
                author VARCHAR(500),
                sentiment DECIMAL(5,4)
                )
                """)

# pushing the data to the database 
sqlFormula = "INSERT INTO reddit_data.reddit_data_sentiment (date_time, subreddit, title, body, author, sentiment) VALUES (%s, %s, %s, %s, %s, %s)"

## constant loop to fill database as comments are created on the below sub reddits
while True:
    try:
        # list of subreddits to be tracked -- you can add the ones you think are important to track 
        subreddit = reddit.subreddit(
            "wallstreetbets+investing+stocks+pennystocks+weedstocks+StockMarket+Trading+Daytrading+algotrading")
        for comment in subreddit.stream.comments(skip_existing=True):
            current_time = datetime.datetime.now()
            subreddit = str(comment.subreddit)
            author = str(comment.author)
            title = str(comment.link_title)
            body = str(comment.body)
            if len(body) < 2000:
                body = body
            elif len(body) > 2000:
                body = "data is too big"  ## extremely uncommon
            vs = analyzer.polarity_scores(unidecode(body))
            sentiment = vs['compound']
            db = (current_time, subreddit, title, body, author, sentiment)
            mycursor.execute(sqlFormula, db)
            mydb.commit()
    # so that crashes dont occur
    except Exception as e:
        print(str(e))
        time.sleep(10)
