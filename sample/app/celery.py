import os
_BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# part of app.settings
from kombu import Exchange, Queue
from datetime import timedelta

DEFAULT_JOBQ = 'sandbox'

CELERY_TASK_SERIALIZER = 'pickle'           # pickle required signal `sender`
CELERY_RESULT_BACKEND = 'amqp'
BROKER_URL = 'amqp://{JOBQ}:{JOBQ}@localhost:5672/{JOBQ}'.format(
    JOBQ=DEFAULT_JOBQ)
CELERY_DEFAULT_QUEUE = DEFAULT_JOBQ
CELERY_QUEUES = (Queue(DEFAULT_JOBQ, Exchange(DEFAULT_JOBQ),
                 routing_key=DEFAULT_JOBQ),)
# CELERY_ALWAYS_EAGER = True

# Beat
CELERYBEAT_SCHEDULE_FILENAME = os.path.join(_BASE_DIR,
                                            'logs/celerybeat-schedule')
CELERYBEAT_SCHEDULE = {
    'smtp-inbound': {
        'task': 'flier.smtp.tasks.process_drop',
        'schedule': timedelta(seconds=30),
        'args': ()
    },
    #     'enqueue-mails': {
    #         'task': 'flier.mails.tasks.enqueue_mails',
    #         'schedule': timedelta(seconds=60),
    #         'args': ()
    #     },
}

# State
CELERYD_STATE_DB = os.path.join(_BASE_DIR, 'logs/celery_state')
