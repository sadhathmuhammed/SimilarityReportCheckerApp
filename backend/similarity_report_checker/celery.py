import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'similarity_report_checker.settings')
app = Celery('similarity_report_checker')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    """
    A Celery task that prints the request object when run.

    This task is useful for testing and debugging Celery tasks. It takes no
    arguments and simply prints the request object to the console.

    Example:
        >>> from similarity_report_checker.celery import debug_task
        >>> debug_task.apply_async()
        <AsyncResult: db34f8a5-7e1f-4f9e-96f4-2c9c4f4e6e54>
        Request: <Request: db34f8a5-7e1f-4f9e-96f4-2c9c4f4e6e54 [debug_task()]>
    """
    print(f'Request: {self.request!r}')