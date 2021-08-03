# import os

# import celery
# from celery.schedules import crontab # scheduler

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proiect.settings')

# # rabbit_broker_url = "amqp://rabbit:abcd12!!@127.0.0.1:5672"
# # redis_broker_url = 'redis://:abcd12!!@127.0.0.1:6379'
# # app = celery.Celery('proiect', broker=redis_broker_url, backend='redis')
# app = celery.Celery()

# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django apps.
# app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
