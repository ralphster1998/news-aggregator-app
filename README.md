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












