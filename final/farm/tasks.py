from celery import Celery

app = Celery('farm')

@app.task
def add(x , y):
    return x + y