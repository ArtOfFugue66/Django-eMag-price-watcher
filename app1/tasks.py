# Price scraping tasks

from app1.models import Scrape, WatchItem
import bs4  # Used for parsing contents of web pages 
import requests  # Used to make requests to web pages
from django.utils import timezone
import datetime
import pytz
import json
import sqlite3 as sql  # Used to read watchlist table contents
from proiect import settings

# import sys
# from proiect import celery_app
# from celery.schedules import crontab
# # from celery.task import periodic_task

DB_PATH = "/home/george/django/proiect/db.sqlite3"


def read_watchlist():
    """
    Get DB watchlist records (table 'app1_watchitem') for all existing users
    :return: a populated [] of (item ID, item name, item URL, item's user ID) items
    """

    watchlist = []

    con = sql.connect(DB_PATH)  # Connect to DB

    cursor = con.cursor()
    # Returns a tuple with selected column data
    for selectedRow in cursor.execute(
        """
        SELECT id, name, url, user_id 
        FROM app1_watchitem
        """
    ):
        watchlist.append(selectedRow)  # Populate watchlist variable with data fetched from the DB

    con.commit()  # IDK if this is necessary, probably not because we make no changes to the DB
    con.close()  # Disconnect from the DB

    return watchlist


def price_scrape(p_url):
    """
    Scrape price from eMag product page.
    :param p_url: URL to scrape
    :return: list of relevant info: scraped item price, current date, current time
    """

    res = requests.get(p_url)
    res.raise_for_status()  # Will raise an error depending on HTTP response code.
    soup = bs4.BeautifulSoup(res.text, "html.parser")  # Returns a "beautiful soup" object.

    # elems = []

    price = soup.find("div", {"class": "w-100"})  # Get <div> container for price
    if price is not None:
        price = price.find("p", {"class": "product-new-price"})  # Only the "discounted" price is of interest
        if price is not None:
            price = price.contents[0].strip()
        else:
            price = "None"
    else:
        price = "None"

    return price


# @shared_task(serializer='json')
def save_function(scrapeItem):
    """
    Function to insert a new record in the DB with price info scraped from the website.
    :param scrapeItem: JSON-format object containing info for the new record
    :return: Execution flow information
    """

    print('[[[!]]] Starting "save_function()"')

    try:
        scrapeObject = Scrape(
            item=WatchItem.objects.get(id=scrapeItem['item']),
            price=scrapeItem['price'],
            dateTime=scrapeItem['dateTime']
        )
        scrapeObject.save()
    except Exception as e:
        print('[[[X]]] Failed to save scrape to database. See exception:')
        print(e)
        return
    
    return print('[[[!]]] Finished "save_function()"')

# @shared_task
def scrape_prices():
    """
    Periodic job for price scraping of products in the 'app1_watchitem' table
    """

    try:
        # Populate list with records from 'app1_watchitem' table
        watchlist = read_watchlist()
        
        for item in watchlist:  # item should be (item ID, item name, item URL, item's user ID)
            # Call price scraping function with item URL as parameter
            scrapedPrice = price_scrape(item[2])  # 'scrape' should be [product price, current date, current time]

            # tz_settings = pytz.timezone(None if settings.TIME_ZONE is None else settings.TIME_ZONE)
            # dateTime = datetime.datetime.now(tz=tz_settings)

            dateTime = datetime.datetime.now()  # FIXME: This gives the correct time, however a time of -3 hrs is inserted into the DB 
            
            scrapeItem = {
                    "item": item[0],
                    "price": scrapedPrice.replace('.',''),
                    "dateTime": dateTime
                }

            save_function(scrapeItem)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
