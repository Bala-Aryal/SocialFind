import threading
from queue import Queue
from spider import Spider
from urllib.request import *
from domain import *
from general import *
import pandas as pd

PROJECT_NAME = ''
HOMEPAGE = ''
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        if(url == ''):
            print('URL not found')
        else:
            spider = Spider(url)
            spider.crawl_page(threading.current_thread().name)
            print(spider.socialLinks())
        queue.task_done()


def displayResults():
    findSocialLinks(PROJECT_NAME)


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

def getWebsiteName(nameString):
    websiteName = 'https://www.'+nameString.replace(' ','')+'.com'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url=websiteName, headers=headers)
    try:
        response = urlopen(req, timeout=3)
        if response.status == 200:
            print (websiteName)
            return websiteName
    except:
        return ''

def start():
    create_workers()
    brand_name = str(input('What is the name of the company? \n'))
    brand_website = getWebsiteName(brand_name)
    queue.put(brand_website)
    queue.join()

start()
