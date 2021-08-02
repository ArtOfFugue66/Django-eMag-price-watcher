import bs4
import requests  # used to actually download the web page content
import datetime
import json
import sqlite3 as sql

DB_PATH = "/db.sqlite3"


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
    URL = '127.0.0.1:8000/watchlist/add_scrape/'
    requests.post(URL, data=body)


