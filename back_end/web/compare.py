#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
from flask_jwt_extended import JWTManager 
from flask_jwt_extended import create_access_token
import time
import multiprocessing as mp

# d9aac332ec5044139d950b0060a89933 --> API Key For News

# For Web Scraping
import requests
from bs4 import BeautifulSoup

# For multithreading
import threading
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017") # change to db when using Docker
db = client.UsersManagementDB
users = db["Users"]

# Global variables to keep track of the CURRENT USER
current_user = {}
user_list_news = dict()
tracked_urls = []

app.config["JWT_SECRET_KEY"] = "secret"

jwt = JWTManager(app)


"""
REST API SECTION
This is where we gather the information from APIs whether it is through webscraping or using a news source api 
from the Internet.
"""
def NewsFromTechRadar():
    # Mashable news api 
    main_url = "https://newsapi.org/v2/top-headlines?sources=techradar&apiKey=d9aac332ec5044139d950b0060a89933"
  
    open_polygon= requests.get(main_url).json()

    list_articles = open_polygon["articles"]
    news_links = dict()
    for news in list_articles:
        article_title = news["title"]
        article_link = news["url"]
        news_links[article_title] = article_link
    return news_links

def NewsFromMedicalToday():
    URL = "https://www.medicalnewstoday.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="css-stl7tm")
    elems = results.find_all("div", class_="css-8sm3l3")
    news_links = dict()
    for news in elems:
        title = news.find("a", class_="css-ni2lnp")
        links = news.find("a", class_="css-ni2lnp")["href"]
        if None in (title, links):
            continue

        news_links[title.text.strip()] = URL + links
    return news_links

def NewsFromBuzzFeed():
    URL = "https://www.buzzfeednews.com/section/books"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="grid-layout-wrapper content-column")
    elems = results.find_all("span", class_="newsblock-story-card__info xs-pr1 xs-block")
    news_links = dict()
    for news in elems:
        links = news.find("a", class_="newsblock-story-card__link xs-flex")["href"]
        title = news.find("a", class_="newsblock-story-card__link xs-flex")
        if None in (title, links):
            continue

        news_links[title.text.strip()] = links
    return news_links

def NewsFromPolygon(): 
    # Mashable news api 
    main_url = "https://newsapi.org/v2/top-headlines?sources=polygon&apiKey=d9aac332ec5044139d950b0060a89933"
  
    open_polygon= requests.get(main_url).json()

    list_articles = open_polygon["articles"]
    news_links = dict()
    for news in list_articles:
        article_title = news["title"]
        article_link = news["url"]
        news_links[article_title] = article_link
    return news_links

def NewsFromESPN(): 
    # Mashable news api 
    main_url = "https://newsapi.org/v2/top-headlines?sources=espn&apiKey=d9aac332ec5044139d950b0060a89933"
  
    open_polygon= requests.get(main_url).json()

    list_articles = open_polygon["articles"]
    news_links = dict()
    for news in list_articles:
        article_title = news["title"]
        article_link = news["url"]
        news_links[article_title] = article_link
    return news_links

class WebScraperTechRadar(Resource):
    def get(self):
        return NewsFromTechRadar()
        
class WebScraperMedicalToday(Resource):
    def get(self):
        return NewsFromMedicalToday()

class WebScraperBuzzFeedBooks(Resource):
    def get(self):
        return NewsFromBuzzFeed()
class WebScraperPolygon(Resource):
    def get(self):
        return NewsFromPolygon()

class WebScraperESPN(Resource):
    def get(self):
        return NewsFromESPN()

class WebScraperUser(Resource): #MAIN FUNCTION TO GET USER'S FEEDS
    def get(self):
        return user_feeds()

"""
PARALLEL SECTION
This is where we put the parallelism.
"""
def gatherFeed(news_source):
    global user_list_news
    feeds = news_source

    for title in feeds: # Iterate through each url and put it in one big dictionary
        print("Title: ", title)
        print("Link: ", feeds[title])
        user_list_news[title] = feeds[title]
    print("List of news: " ,user_list_news)

def parallel(id):
    name = threading.current_thread().getName()
    print(name, 'Thread ID:', id)
    global tracked_urls
    global user_list_news

    if id not in tracked_urls:
        tracked_urls.append(id)

        if id == 'Tech Radar':
            print('Tech Radar')
            gatherFeed(NewsFromTechRadar())
        elif id == 'ESPN':
            print('ESPN')
            gatherFeed(NewsFromESPN())
        elif id == 'Polygon':
            print('Polygon')
            gatherFeed(NewsFromPolygon())
        elif id == 'BuzzFeed':
            print('BuzzFeed')
            gatherFeed(NewsFromBuzzFeed())
        elif id == 'Medical News Today':
            print('Medical News Today')
            gatherFeed(NewsFromMedicalToday())

    # print("News feeds", user_list_news)
    return user_list_news


def user_feeds():
    pool = ThreadPoolExecutor(max_workers=5) # limit to only 5 threads
    global user_list_news
    global tracked_urls
    user_list_news = dict() # restart the news feeds when user logs in
    tracked_urls = []

    #  Put all five URLS to test out the threads
    selected_urls = ['Medical News Today', 'BuzzFeed', 'ESPN', 'Polygon', 'Tech Radar']
    for id in range(len(selected_urls)):
        pool.submit(parallel, selected_urls[id])
    pool.shutdown()
    return user_list_news

# Gather all news for one user (SEQUENTIAL)
def user_feeds_seq():
    global user_list_news
    global tracked_urls
    user_list_news = dict() # restart the news feeds when user logs in
    tracked_urls = []

    #  Put all five URLS to test out sequence code
    selected_urls = ['Medical News Today', 'BuzzFeed', 'ESPN', 'Polygon', 'Tech Radar']
    for id in range(len(selected_urls)):
        parallel(selected_urls[id])
    return user_list_news

api.add_resource(WebScraperTechRadar, "/api/techradar/scrape")
api.add_resource(WebScraperMedicalToday, "/api/medical/scrape")
api.add_resource(WebScraperBuzzFeedBooks, "/api/books/scrape")
api.add_resource(WebScraperPolygon, "/api/polygon/scrape")
api.add_resource(WebScraperESPN, "/api/espn/scrape")
api.add_resource(WebScraperUser, "/api/user/scrape")

if __name__ == '__main__':
    NUM_EVAL_RUNS = 10

    print('Evaluating Sequential Implementation...')
    sequential_result = user_feeds_seq() # "warm up"
    sequential_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        user_feeds_seq()
        sequential_time += time.perf_counter() - start
    sequential_time /= NUM_EVAL_RUNS

    print('Evaluating Parallel Implementation...')
    parallel_result = user_feeds()  # "warm up"
    parallel_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        user_feeds()
        parallel_time += time.perf_counter() - start
    parallel_time /= NUM_EVAL_RUNS

    print('Average Sequential Time: {:.2f} ms'.format(sequential_time*1000))
    print('Average Parallel Time: {:.2f} ms'.format(parallel_time*1000))
    print('Speedup: {:.2f}'.format(sequential_time/parallel_time))
    print('Efficiency: {:.2f}%'.format(100*(sequential_time/parallel_time)/mp.cpu_count()))
