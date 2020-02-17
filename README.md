# news-aggregator-app
This application gathers a set of the user's chosen and personalized news sources,
and it is refreshed each time a user checks the latest set of news. For example,
a user who is interested in psychological news will have mainly psychological news
sources placed on their dashboard.

By now, the application has RESTful API using Python Flask-RESTful library. The application can
register and login the user. Each of the user's info is in Mongo database. The application is
also stored in the cloud through an EC2 AWS instance. 
The application can also webscrape three news sites: yahoo.com, medicalnewstoday.com, and buzzfeed.com (Books Web Section). 

You can access the AWS URL and play around with the API of the application:

Link to the AWS RESTful API: **ec2-3-15-28-3.us-east-2.compute.amazonaws.com:5000/api**

### Example of Registering a User Through Postman
![image](https://user-images.githubusercontent.com/34559304/74641670-86c6bd00-5126-11ea-8e8e-4486db37e9af.png)











