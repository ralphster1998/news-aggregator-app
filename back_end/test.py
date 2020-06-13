#!/usr/bin/env python3
""" Chopping vegetables with a ThreadPool """

import threading
from concurrent.futures import ThreadPoolExecutor # thread pool executer

list_news = []

user_urls = ['Tech Radar', 'ESPN', 'Polygon', 'BuzzFeed', ]

def parallel(id):
    global list_news
    global user_urls
    name = threading.current_thread().getName()
    print(name, 'Thread ID:', id)

    if id not in list_news:
        list_news.append(id)

    return list_news


def main():
    pool = ThreadPoolExecutor(max_workers=5) # limit to only 5 threads (b/c there's 5 news sources)
    global list_news
    global user_urls
    list_news = []
    print(user_urls)
    for id in range(len(user_urls)):
        pool.submit(parallel, user_urls[id])
    pool.shutdown()
    print(list_news)
main()
   # frees up any resources as tasks are finished executing. 

# Use same 5 threads in thread pool to execute all the tasks. 

"""
Create five threads as many threads as CPUS.

Within for loop rather than creating thread object, submit vegetable to thread pool.

After loop 

"""