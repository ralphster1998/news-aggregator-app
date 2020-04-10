#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
from flask_jwt_extended import JWTManager 
from flask_jwt_extended import create_access_token
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

app.config["JWT_SECRET_KEY"] = "secret"

jwt = JWTManager(app)

#global user news list
list_news = []

def tech_radar():
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

def medical():
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
        print("Title: " + title.text.strip(), end="\n" * 2)
        print(links, end="\n" * 2)
        news_links[title.text.strip()] = URL + links
    return news_links

def buzzfeed():
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
        print("Title: " + title.text.strip(), end="\n" * 2)
        print(links, end="\n" * 2)
        news_links[title.text.strip()] = URL + links
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

# Gather all news for one user (SEQUENTIAL)
def gatherNews(id):
    list_news.append(NewsFromESPN())
    list_news.append(NewsFromPolygon())
    list_news.append(buzzfeed())
    list_news.append(medical())
    list_news.append(tech_radar())
    return list_news

class WebScraperTechRadar(Resource):
    def get(self):
        return tech_radar()
        
class WebScraperMedicalToday(Resource):
    def get(self):
        return medical()

class WebScraperBuzzFeedBooks(Resource):
    def get(self):
        return buzzfeed()
class WebScraperPolygon(Resource):
    def get(self):
        return NewsFromPolygon()

class WebScraperESPN(Resource):
    def get(self):
        return NewsFromESPN()

class WebScraperUser(Resource):
    def get(self):
        return gatherNews()

def UserExist(username):
    if users.count_documents({"username":username}) == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"
        urls = postedData["urls"]

        if UserExist(username):
            retJson = {
                'status':301,
                'msg': 'Invalid username'
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert_one({
            "username": username,
            "password": hashed_pw,
            "urls": urls
        })

        retJson = {
            "status": 200,
            "msg": "Success"
        }
        return jsonify(retJson)

class Login(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData['username']
        password = postedData['password'] #'123xyz'

        result = ""
        found_username = users.find_one({'username': username})
        print(found_username)
        hashed_pw = users.find_one({ "username":username })['password']

        
        if found_username:
            if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
                access_token = create_access_token(identity = {
                    'username': found_username ['username'],
                    'urls': found_username['urls'] # connect with front-end the info
                })
                result = jsonify({'token':access_token})
            else:
                result = jsonify({"error":"Invalid username and password"})
        else:
            result = jsonify({"result":"No results found"})
        return result

api.add_resource(Register, "/api/register")
api.add_resource(Login, "/api/login")
api.add_resource(WebScraperTechRadar, "/api/techradar/scrape")
api.add_resource(WebScraperMedicalToday, "/api/medical/scrape")
api.add_resource(WebScraperBuzzFeedBooks, "/api/books/scrape")
api.add_resource(WebScraperPolygon, "/api/polygon/scrape")
api.add_resource(WebScraperESPN, "/api/espn/scrape")
api.add_resource(WebScraperUser, "/api/user/scrape")


"""
PLAN FOR CS 159 IMPLEMENTATION
- ADD TWO MORE WEBSITES (JUST USE THE APIS --> NO NEED TO WEBSCRAPE ANYMORE) $
- PASS IN THE PICKED URLS THAT THE USER WANTS $

IMPORTANT!!!
- ADD PARALLELISM TO A USER'S SET OF PICKED FEEDS (BASED FROM THE SET OF URLS) 
    - GO THROUGH THE WHOLE PYTHON PARALLEL COURSE AND SEE WHAT YOU CAN IMPLEMENT
    - RUN YOUR NEWS FEEDS THROUGHT THE PARALLEISM
- MEASURE THE SPEEDUP AND OTHER THINGS BASED FROM THE PYTHON PARALLEL COURSE


- THEN UPLOAD IT ON REACT
- THEN PUT ALL OF IT IN DOCKER AND AWS WHEN YOU HAVE TIME

- IMPORTANT: WRITE YOUR REPORT AT END OF THE DAY WHILE DOING THIS. 
"""


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


