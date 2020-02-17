from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt, json
from flask_jwt_extended import JWTManager 
from flask_jwt_extended import create_access_token

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://localhost:27017')
db = client.NewsAggregatorDB
users = db['Users']

app.config['JWT_SECRET_KEY'] = 'secret'

jwt = JWTManager(app)


# For Web Scraping
import requests
from bs4 import BeautifulSoup

def UserExist(username):
    if users.find({'Username':username}).count() == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        first_name = postedData['first_name']
        last_name = postedData['last_name']
        username = postedData['username']
        password = postedData['password'] #'123xyz'
        urls = postedData['urls']

        retObj = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password,
            'urls': urls
        }

        
        if UserExist(username):
            retJson = {
                'status':301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': hashed_pw,
            'urls': urls
        })

        retJson = {
            'status': 200,
            'msg': retObj
        }
        return jsonify(retJson)

class Login(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData['username']
        password = postedData['password'] #'123xyz'

        result = ''

        foundUsername = users.find_one({'username': username})
        hashed_pw = users.find({ "username":username })[0]["password"]

        if foundUsername:
            if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
                access_token = create_access_token(identity = {
                    'first_name': foundUsername['first_name'],
                    'last_name': foundUsername['last_name'],
                    'username': foundUsername['username']
                })
                result = jsonify({'token':access_token})
            else:
                result = jsonify({"error":"Invalid username and password"})
        else:
            result = jsonify({"result":"No results found"})

        return result

class WebScraperYahoo(Resource):
    def get(self):
        URL = 'https://www.yahoo.com'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='applet_p_50000313')
        elems = results.find_all('li', class_='ntk-item W(1/5) Whs(n) Va(t) D(ib) Lts(0) Bdend(none) Pos(r)')
        news_links = dict()
        for news in elems:
            links = news.find('a', class_='Pos(r) D(b) Mend(9px) C($link) C($m_blue):h C($m_blue):f O(n):f Op(0.9):h Op(0.9):f Td(n) W(a) ntk-footer-link js-content-viewer rapidnofollow wafer-caas')['href']
            title = news.find('h3', class_='Mx(0) Mb(0) Mt(4px) Fz(12px) LineClamp(2,2.6em) LineClamp(3,4em)!--md1100 js-stream-content-link:f_Td(u) T(70%) js-stream-content-link:f_Td(n)! Start(2px) Td(u):h')
            if None in (title, links):
                continue
            print("Title: " + title.text.strip(), end='\n' * 2)
            print(links, end='\n' * 2)
            news_links[title.text.strip()] = "www.yahoo.com" + links
        return news_links

class WebScraperMedicalToday(Resource):
    def get(self):
        URL = 'https://www.medicalnewstoday.com/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('div', class_='css-stl7tm')
        elems = results.find_all('div', class_='css-8sm3l3')
        news_links = dict()
        for news in elems:
            title = news.find('a', class_='css-ni2lnp')
            links = news.find('a', class_='css-ni2lnp')['href']
            if None in (title, links):
                continue
            print("Title: " + title.text.strip(), end='\n' * 2)
            print(links, end='\n' * 2)
            news_links[title.text.strip()] = "www.medicalnewstoday.com" + links
        return news_links

class WebScraperBuzzFeedBooks(Resource):
    def get(self):
        URL = 'https://www.buzzfeednews.com/section/books'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('div', class_='grid-layout-wrapper content-column')
        elems = results.find_all('span', class_='newsblock-story-card__info xs-pr1 xs-block')
        news_links = dict()
        for news in elems:
            links = news.find('a', class_='newsblock-story-card__link xs-flex')['href']
            title = news.find('a', class_='newsblock-story-card__link xs-flex')
            if None in (title, links):
                continue
            print("Title: " + title.text.strip(), end='\n' * 2)
            print(links, end='\n' * 2)
            news_links[title.text.strip()] = "www.yahoo.com" + links
        return news_links

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(WebScraperYahoo, '/api/yahoo/scrape')
api.add_resource(WebScraperMedicalToday, '/api/medical/scrape')
api.add_resource(WebScraperBuzzFeedBooks, '/api/books/scrape')



if __name__=='__main__':
    app.run(host='0.0.0.0')
