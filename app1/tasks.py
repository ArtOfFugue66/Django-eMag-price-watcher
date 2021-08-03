# Price scraping tasks

from app1.models import Scrape, WatchItem
# from celery import shared_task

import bs4
import requests  # used to actually download the web page content
# import datetime
from django.utils import timezone
import json
# # import lxml
import sqlite3 as sql

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
    # elems.append(price)  # scraped price

    # date = datetime.datetime.now()  # get current date
    # dateNow = date.strftime("%d/%m/%Y")  # format date as needed
    # elems.append(dateNow)  # date of scrape

    # timeNow = date.strftime("%H:%M:%S")  # get time of day
    # elems.append(timeNow)  # time of scrape

    # elems.append(date)
    return price


# @shared_task(serializer='json')
def save_function(scrapeItem):
    print('[!] Starting "save_function()"')

    try:
        scrapeObject = Scrape(
            item=WatchItem.objects.get(id=scrapeItem['item']),
            price=scrapeItem['price'],
            dateTime=scrapeItem['dateTime']
        )
        scrapeObject.save()
    except Exception as e:
        print('[x] Failed to save scrape to database. See exception:')
        print(e)
        return
    
    return print('[!] Finished "save_function()"')

# @shared_task
def scrape_prices():
    try:
        # Populate list with records from 'app1_watchitem' table
        watchlist = read_watchlist()
        
        for item in watchlist:  # item should be (item ID, item name, item URL, item's user ID)
            # Call price scraping function with item URL as parameter
            scrapedPrice = price_scrape(item[2])  # 'scrape' should be [product price, current date, current time]
            # scrapeInfo = list(item) + list(scrape)  # 'scrapeInfo' should be [item ID, item name, item URL, item's user ID, prod. price, dateTime]

            dateTime = timezone.now()
            # watchItem = 
            scrapeItem = {
                    "item": item[0],
                    "price": scrapedPrice.replace('.',''),
                    "dateTime": dateTime
                }

            print(item)
            save_function(scrapeItem)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
