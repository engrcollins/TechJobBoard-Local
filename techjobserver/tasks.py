from celery import Celery
from .views import scrape

BROKER_URL = 'mongodb://localhost:27017/jobs'

celery = Celery('EOD_TASKS',broker=BROKER_URL)

@celery.task

def elast():
    print("Gotcha mf")
    scrape()