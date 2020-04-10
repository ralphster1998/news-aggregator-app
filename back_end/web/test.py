#!/usr/bin/env python3
""" Chopping vegetables with a ThreadPool """

import threading
from concurrent.futures import ThreadPoolExecutor # thread pool executer

list_news = ["1","2"]

def parallel(id):
    global list_news
    name = threading.current_thread().getName()
    print(name, 'Thread ID:', id)

    if id == 0 and "1" not in list_news:
        list_news.append("1")
    if id == 1 and "2" not in list_news:
        list_news.append("2")
    if id == 2 and "3" not in list_news:
        list_news.append("3")
    if id == 3 and "4" not in list_news:
        list_news.append("4")
    if id == 4 and "5" not in list_news:
        list_news.append("5")
    return list_news

if __name__ == '__main__':
    # pool = ThreadPoolExecutor(max_workers=3) # limit to only 5 threads

    pool = ThreadPoolExecutor(max_workers=5) # limit to only 5 threads
    for id in range(5):
        pool.submit(parallel, id)
    pool.shutdown()
    print(list_news)
   # frees up any resources as tasks are finished executing. 

# Use same 5 threads in thread pool to execute all the tasks. 

"""
Create five threads as many threads as CPUS.

Within for loop rather than creating thread object, submit vegetable to thread pool.

After loop 

"""