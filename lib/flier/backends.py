from django.dispatch import dispatcher


SignalArgs = ['from_email', 'to', 'message_id', 'key', 'status', 'message']


class BackendSignal(object):
    sent_signal = dispatcher.Signal(providing_args=SignalArgs)
    failed_signal = dispatcher.Signal(providing_args=SignalArgs)
