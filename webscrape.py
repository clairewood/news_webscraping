
# SOURCE
# All of my articles were showing up as blank when using newspaper's Article import, 
# but the solution at this link  (accessed 6/3/2023) solved my problem: 
# https://stackoverflow.com/questions/75542842/why-is-summary-on-the-python-newspaper3k-module-returning-blank 
# All code involving "config" was adapted from the solution at the above link. 
 


import json
import os 
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from GoogleNews import GoogleNews # https://www.youtube.com/watch?v=rQXL9A0ST5k 
from newspaper import Article, Config
import nltk
nltk.download('punkt')
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config() 
config.request_timeout = 10
config.browser_user_agent = user_agent
# Fixed config error and timeout error: f
# https://stackoverflow.com/questions/75542842/why-is-summary-on-the-python-newspaper3k-module-returning-blank  


def getNewsData(): # (topic)
    url = 'https://news.google.com/rss/search?q=salmon&hl=en-US&gl=US&ceid=US:en'
    session = HTMLSession()
    response = session.get(url)
    print(response)

    soup = BeautifulSoup(response.content, features="xml")
    news_results = [] 
    print("After BeautifulSoup")

    i=0
    for el in soup.select("item"):
        print("In soup loop")
        if i < 5: # Get 5 articles from each news topic 
            # Get link from google news
            google_url = el.find("link").get_text()
            snippet = get_snippet(google_url)
            print("Got snippet")
            # print(f"Article authors: {article.authors}")
            news_results.append(
                {
                    "link": el.find("link").get_text(),
                    "title": el.find("title").get_text(),
                    "date": el.find("pubDate").get_text(),
                    "snippet": snippet,
                    "source": el.find("source").get_text()
                    # TODO load this as new method of scraping
                    # Write something that gets snippet 
                }
            )
        else:
            print("Breaking")
            break
        i += 1
        print("i += 1")
    print(news_results)


def get_snippet(google_url):
    snippet = None 
    print("in get_snippet")
    r = requests.get(google_url)
    # use newspaper3k to scrape the real article for a summary 
    redirected_url = r.url 
    article = Article(redirected_url, config=config)
    print("got article")
    
    try: 
        print("trying")
        article.download()
        article.parse()
        article.nlp() 
        snippet = article.summary[0:150] + "..."
    except: 
        print("exception")
        snippet = "Click the link to view the full article."
    print("returning")
    return snippet 


getNewsData()



def addToJSON(json_object):
    existing_file = "flask_SE/news.json"
    data = [] # we'll fill this with existing json data in a sec

    if os.stat(existing_file).st_size == 0:
        with open(existing_file, "w") as outfile:
                outfile.write(json_object) 
    else:
        with open(existing_file, "r") as file:
            data = json.load(file) 

        temp = json_object
        json_object = json.loads(temp)

        for article in json_object:
            data.append(article)

        with open(existing_file, "w") as file:
            json.dump(data, file, indent=2, separators=(',',': '))
