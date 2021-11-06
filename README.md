# Django price scraper for 'emag.ro'
Web app built on Django framework for monitoring prices of products from 'emag.ro'.
## Demo
![Demo gif](demo.gif)
# ~~Django + Celery + RabbitMQ~~ (too much hassle)
### ~~Tutorial: https://codeburst.io/making-a-web-scraping-application-with-python-celery-and-django-23162397c0b6~~
- ~~OS: __Ubuntu 21.04__~~
- ~~'celery.py' init file in __proiect/celery.py__~~
- ~~Celery-specific settings in __proiect/settings.py__~~
- ~~RabbitMQ instance running on __amqp://127.0.0.1:5672__~~
- ~~Running Celery tasks using command __celery -A proiect worker -B -E -l INFO__~~
- ~~! No insertion in __'app1_scrape'__ table in the DB~~

# Django-Q (amazing)
### Tutorial: https://pythonrepo.com/repo/Koed00-django-q-python-django-utilities
- OS: __Ubuntu 21.04__
- Price scraping job defined in __app1.tasks__, named __scrape_prices()__
- Job created using __Django admin interface__ (http://127.0.0.1/admin) or through `python3 manage.py shell` command
- Django-Q cluster ran with `python3 manage.py qcluster`
- Insertion of scraped prices into DB going ___swimmingly___

# TODO:
- ~~Set up static files (css, js, images)~~
- ~~Set up background task in Django for price scraping based on items in the 'app1_watchitem' table (using Celery / similar 3rd party library or some other method)~~
- ~~Populate DB tables with dummy data in 'app1_watchitem' and 'auth_user' tables~~
- ~~Write code to SELECT scrapes for item selected by user from DB~~
- ~~Write view to render graph (plotly) on a page based on item scrapes~~
  - ~~Use markers / lines+markers for graph mode~~
- Fix Django / Django-Q reference time (3 hours behind actual timezone)
- Try resizing the /watchlist/ table to half and displaying the graph onto the other half of the page
  - Preferrably without making a new request to the page
  - Preferrably with animations (CSS)
- Write unit tests for background scraping task
- ~~Create & load fixtures for 'app1_scrape' table (data with varying 'price' values for graph viewing & testing)~~
- ~~Style the web app using UIkit~~ 
- Finally, test the whole app manually
