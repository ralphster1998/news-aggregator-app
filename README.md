# news-aggregator-app
This application gathers a set of the user's chosen and personalized news sources,
and it is refreshed each time a user checks the latest set of news. For example,
a user who is interested in psychological news will have mainly psychological news
sources placed on their dashboard.

The application has RESTful APIs using Python Flask-RESTful library. The application has authentication, which can
register and login the user. Each of the user's info is stored in Mongo database. The application is
also stored in the cloud through an EC2 AWS instance. 
The application can also webscrape some sites, such medicalnewstoday.com, buzzfeed.com (Books Web Section) and ESPN.
The front-end part of the web application is also included to help the user interact with their own news feeds. 

Here's a quick walkthrough of what the news aggregation app looks like when you're a new user : 

**News Aggregator App Walkthrough:**
1) Create an account by going to the 'Register' tab in the Navigation Bar.
<img width="1280" alt="1" src="https://user-images.githubusercontent.com/34559304/95709958-9a261b80-0c14-11eb-8151-2f11816d8948.png">
2) In Register Page, put your username, password and set of listed news sources you want to aggregate from.
<img width="1280" alt="2" src="https://user-images.githubusercontent.com/34559304/95710110-e40f0180-0c14-11eb-9c5d-7f76f6d3f395.png">
3) After pressing 'Register', the page will redirect you to the Login page. Then, enter your username, password and press the 'Sign In' button.
<img width="1278" alt="3" src="https://user-images.githubusercontent.com/34559304/95710136-f0935a00-0c14-11eb-9323-4487826dd533.png">
4) After, it will then show your Profile Page along with a set of news sources you've selected.
<img width="1280" alt="4" src="https://user-images.githubusercontent.com/34559304/95710189-0b65ce80-0c15-11eb-891b-c838160d7f71.png">
5) Then, click on the 'Your News' tab, and you should be able to see the latest news feeds for today.
<img width="1280" alt="5" src="https://user-images.githubusercontent.com/34559304/95710220-16b8fa00-0c15-11eb-8e86-00a736334cd3.png">
6) You then should see your list of news feeds. And if you click on any 'Go To Page' buttons, you should be 
directed to new tabs to read them off of those news sites' articles. 
<img width="1280" alt="6" src="https://user-images.githubusercontent.com/34559304/95710252-289a9d00-0c15-11eb-8d4c-bc156d0ffc21.png">

**What It Looks Like After Clicking:**
<img width="1280" alt="7" src="https://user-images.githubusercontent.com/34559304/95710327-4831c580-0c15-11eb-8324-c3db12843da2.png">











