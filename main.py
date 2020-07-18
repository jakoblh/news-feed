#!/usr/bin/python

from newsapi import NewsApiClient
from termcolor import colored
from time import sleep
from random import shuffle
from random import uniform
import threading

interval = 15 * 60
colors = ['red','green','yellow','blue','magenta','cyan']
articles = []

api = NewsApiClient(api_key='6fd0646c45f74952b9069576e3105d53')



def print_headline(source, title):
    color = colors[hash(source) % len(colors)]
    
    print(colored(source, color=color, attrs=['bold']) + ": " + title)



def pull_articles():
    global articles
    while True:
        articles  = api.get_top_headlines(page_size=100, country='de')['articles']
        articles += api.get_top_headlines(page_size=100, country='fr')['articles']
        articles += api.get_top_headlines(page_size=100, country='ca')['articles']
        articles += api.get_top_headlines(page_size=100, category='science')['articles']

        shuffle(articles)

        print_headline("news-feed update", "pulled %d articles" % len(articles))
        sleep(interval)



thread = threading.Thread(target=pull_articles)
thread.start()
while True:
    for article in articles:
        array = article['title'].split(" - ")
        source = array[-1]
        title = " - ".join(array[:-1])
        
        print_headline(source, title)

        sleep(uniform(1,3))
    sleep(0.5)

thread.join()
