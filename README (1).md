
# Scott Kidman Capstone

This project was inspired by the influence of Reddit specifically stock subreddits such as wallstreetbets. 
In the months from January 2021~ to March 2021~ they pushed and ignited a short squeeze on GameStop in a 
way that forced Reddit into the spotlight of mainstream media. This project seeks to find what the general 
public using Reddit’s stock subreddits opinions on individual stocks.

	By gathering comments from stock subreddits we can use algorithms to interpretate the sentiment of the 
    user when talking about a stock. While one user’s input on a stock is not important and influential 
    when analyzing all comments you can begin to see patterns of group sentiment. This project then seeks 
    to graph all sentiment mentioning the desired stock into a digestible way for a person to view that to
    see what others are thinking. This is a very common and useful way to get information for trading in 
    other forms of data gathering but new to reddit. 
	
	This data will be graphed and uploaded to a local site though the python library Dash by Plottly. 
    Which allows graphical information to be shown and hosted on a website. For our purpose it will 
    be a offline local website.  Graphs made on the site are also for apple as an example as it is 
    talked about a lot in those subreddit’s comments. 
 



## Environment Variables

Make sure that MySQL is running correctly, I used workbench which worked out well to manage the DB.




## Deployment
1: To deploy this project dependencys rely on methods in legacy libraries, the text at the bottom is the list of all
package versions for the project. 
2: You also must fill all data for your mysql server and Reddit API
3: Run the reddit stream.py and keep it running for the entire duration you look to collect data.
4: At this point you should view your MySQL database and ensure that it is filling with comments then go ahead and
launch the dev server.py then in the terminal of the progam it should list the local ip connection link. click 
it and you should see the webpage with graph of the sentiment of your database.

    "Brotli	1.0.9	1.0.9
    Flask	1.1.2	2.0.2
    Flask-Compress	1.9.0	1.10.1
    Jinja2	2.11.3	3.0.3
    MarkupSafe	1.1.1	2.0.1
    Pillow	8.2.0	8.4.0
    PySocks	1.7.1	1.7.1
    Unidecode	1.2.0	1.3.2
    Werkzeug	1.0.1	2.0.2
    appdirs	1.4.4	1.4.4
    beautifulsoup4	4.10.0	4.10.0
    bs4	0.0.1	0.0.1
    cachetools	4.2.1	4.2.4
    certifi	2021.5.30	2021.10.8
    chardet	4.0.0	4.0.0
    click	7.1.2	8.0.3
    colorama	0.4.4	0.4.4
    cssselect	1.1.0	1.1.0
    cycler	0.10.0	0.11.0
    dash	0.30.0	2.0.0
    dash-core-components	0.38.0	2.0.0
    dash-html-components	0.13.2	2.0.0
    dash-renderer	0.15.0	1.9.1
    dash-table	4.11.2	5.0.0
    fake-useragent	0.1.11	0.1.11
    feedparser	6.0.8	6.0.8
    future	0.18.2	0.18.2
    idna	2.10	3.3
    importlib-metadata	4.8.1	4.8.2
    itsdangerous	1.1.0	2.0.1
    kiwisolver	1.3.1	1.3.2
    lxml	4.6.3	4.6.4
    matplotlib	3.4.2	3.5.0
    mysql	0.0.2	0.0.3
    mysql-connector-python	8.0.23	8.0.27
    mysqlclient	2.0.3	2.1.0
    numpy	1.20.2	1.21.4
    oauthlib	3.1.0	3.1.1
    pandas	1.2.3	1.3.4
    parse	1.19.0	1.19.0
    pip	21.0.1	21.3.1
    plotly	4.14.3	5.4.0
    praw	7.2.0	7.5.0
    prawcore	2.0.0	2.3.0
    protobuf	3.15.7	3.19.1
    pyee	8.2.2	8.2.2
    pyparsing	2.4.7	3.0.6
    pyppeteer	0.2.6	0.2.6
    pyquery	1.4.3	1.4.3
    python-dateutil	2.8.1	2.8.2
    pytz	2021.1	2021.3
    regex	2021.4.4	2021.11.10
    requests	2.25.1	2.26.0
    requests-html	0.10.0	0.10.0
    requests-oauthlib	1.3.0	1.3.0
    retrying	1.3.3	1.3.3
    setuptools	58.1.0	59.4.0
    sgmllib3k	1.0.0	1.0.0
    six	1.15.0	1.16.0
    soupsieve	2.2.1	2.3.1
    tqdm	4.62.3	4.62.3
    tweepy	3.10.0	4.4.0
    update-checker	0.18.0	0.18.0
    urllib3	1.26.4	1.26.7
    vaderSentiment	3.3.2	3.3.2
    w3lib	1.22.0	1.22.0
    websocket-client	0.58.0	1.2.1
    websockets	9.1	10.1
    yahoo-fin	0.8.9.1	0.8.9.1
    zipp	3.6.0	3.6.0"

