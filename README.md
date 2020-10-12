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

You can access the AWS URL and play around with the web application:

Link to the AWS RESTful API: **ec2-13-58-2-116.us-east-2.compute.amazonaws.com:5000/**

**How To Use The News Aggregator App:**
1) Create an account by going to the 'Register' tab in the Navigation Bar.
<img width="1280" alt="1" src="https://user-images.githubusercontent.com/34559304/95709958-9a261b80-0c14-11eb-8151-2f11816d8948.png">
2) In Register Page, put your username, password and set of listed news sources you want to aggregate from.
3) After pressing 'Register', the page will redirect you to the Login page. Then, enter your username, password and
press the 'Sign In' button.
4) After, it will then show your Profile Page along with a set of news sources you've selected.
5) Then, click on the 'Your News' tab, and you should be able to see the latest news feeds for today.
6) You then should see your list of news feeds. And if you click on any 'Go To Page' buttons, you should be 
directed to new tabs to read them off of those news sites' articles. 











