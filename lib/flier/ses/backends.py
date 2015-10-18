from django.core.mail.backends import base
from flier.backends import BackendSignal
from flier.ses.aws import SendRawEmailResponse


class SesBackend(base.BaseEmailBackend, BackendSignal):

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
        '''
        - http://bit.ly/flier_ses_sendrawemail
        '''
        # TODO: exception handling
        sender = message.from_email

        for to in message.recipients():
            self._send_single(message,  sender, to)

        return True

    def _send_single(self, message, sender, destinations):
        try:
            message_id = message.extra_headers.get('Message-ID')
            res = self.connection.send_raw_email(
                raw_message=message.message().as_string(),
                source=sender, destinations=destinations,)

            res = SendRawEmailResponse(res['SendRawEmailResponse'])

            self.sent_signal.send(
                sender=self,
                from_email=sender, to=destinations, message_id=message_id,
                key=res.SendRawEmailResult.MessageId,
                status='SendRawEmailResponse', message=res.format())
        except Exception, ex:
            self.failed_signal.send(
                sender=self,
                from_email=sender, to=destinations, message_id=message_id,
                status=ex.__class__.__name__, message=ex.message)
