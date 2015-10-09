from django.core.mail.backends import base


class SesBackend(base.BaseEmailBackend):

    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently

        # boto connection
        self.connection = kwargs.get('connection', None)

    def send_messages(self, email_messages):
        '''Django API for Email Backend

        TODO: exception handling
        '''
        num = 0
        for msg in email_messages:
            self._send(msg)
            num = num + 1
        return num

    def _send(self, message):
        # TODO: exception handling
        for to in message.recipients():
            self .connection.send_raw_email(
                raw_message=message.message().as_string(),
                source=message.from_email,
                destinations=to,)
        return True
