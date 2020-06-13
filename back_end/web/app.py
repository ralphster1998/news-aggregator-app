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

app = Flask(__name__, static_folder="build/static", template_folder="build")
api = Api(app)

client = MongoClient("mongodb://localhost:27017") # change to db when using Docker
db = client.UsersManagementDB
users = db["Users"]

# Global variables to keep track of the CURRENT USER'S INFO
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

def UserExist(username):
    if users.count_documents({"username":username}) == 0:
        return False
    else:
        return True

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

    selected_urls = current_user['urls']
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
    selected_urls = current_user['urls']
    for id in range(len(selected_urls)):
        parallel(selected_urls[id])
    return user_list_news

"""
DATABASE AND BACK-END HANDLING: PUT USER'S INFO AND SUGGESTED URLS IN THE MONGODB DATABASE
"""
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
                global current_user
                global user_list_news
                current_user = found_username # server keeps track of current user when web scraping
                
                access_token = create_access_token(identity = {
                    'username': found_username ['username'],
                    'urls': found_username['urls'] # connect with front-end the info
                })
                result = jsonify({'token':access_token})
            else:
                result = jsonify({"error":"Invalid username and password"})
        else:
            result = jsonify({"result":"No results found"})
        print("Current User: ", current_user )
        return result

api.add_resource(Register, "/api/register")
api.add_resource(Login, "/api/login")
api.add_resource(WebScraperTechRadar, "/api/techradar/scrape")
api.add_resource(WebScraperMedicalToday, "/api/medical/scrape")
api.add_resource(WebScraperBuzzFeedBooks, "/api/books/scrape")
api.add_resource(WebScraperPolygon, "/api/polygon/scrape")
api.add_resource(WebScraperESPN, "/api/espn/scrape")
api.add_resource(WebScraperUser, "/api/user/scrape")

@app.route("/manifest.json")
def manifest():
    return send_from_directory('./build', 'manifest.json')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./build', 'favicon.ico')

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


