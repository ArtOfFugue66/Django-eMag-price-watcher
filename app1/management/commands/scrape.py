from django.core.management.base import BaseCommand, CommandError
import bs4
import requests  # used to actually download the web page content
import datetime
import sqlite3 as sql
from django.shortcuts import render

DB_PATH = "C:\WORK\Personal\Google-Aterlierul-Digital\django\proiect\db.sqlite3"


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

    elems = []

    price = soup.find("div", {"class": "w-100"})  # Get <div> container for price
    if price is not None:
        price = price.find("p", {"class": "product-new-price"})  # Only the "discounted" price is of interest
        if price is not None:
            price = price.contents[0].strip()
        else:
            price = "None"
    else:
        price = "None"
    elems.append(price)  # scraped price

    date = datetime.datetime.now()  # get current date
    dateNow = date.strftime("%d/%m/%Y")  # format date as needed
    elems.append(dateNow)  # date of scrape

    timeNow = date.strftime("%H:%M:%S")  # get time of day
    elems.append(timeNow)  # time of scrape

    return elems


def write_scrape(scrapeInfo):
    """
    Write scraped info to project database file
    :param scrapeInfo: list of form [item ID, item name, item URL, item's user ID, prod. price, date, time]
    """

    # Prepare POST request body
    body = {
        "item": scrapeInfo[0],
        "price": scrapeInfo[4],
        "date": scrapeInfo[5],
        "time": scrapeInfo[6]
    }

    # Send HTTP POST request to 'app1:add_scrape'
    # URL = 'http://127.0.0.1:8000/watchlist/add_scrape/'
    # requests.post(URL, data=body)



    return


class Command(BaseCommand):
    help = 'Command to start scraping prices for product records in "app1_watchitem" table'

    def handle(self, *args, **options):
        try:
            # Populate list with records from 'app1_watchitem' table
            watchlist = read_watchlist()

            for item in watchlist:  # item should be (item ID, item name, item URL, item's user ID)
                # Call price scraping function with item URL as parameter
                scrape = price_scrape(item[2])  # 'scrape' should be [product price, current date, current time]
                scrapeInfo = list(item) + list(
                    scrape)  # 'scrapeInfo' should be [item ID, item name, item URL, item's user ID, prod. price, date, time]
                print(scrapeInfo)
                write_scrape(scrapeInfo)
        except Exception as e:
            print(e)
            raise CommandError('[x] Scrape command failed to execute!')
