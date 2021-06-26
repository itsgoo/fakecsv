from celery import Celery

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakecsv_project.settings')
app = Celery('fakecsv_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')