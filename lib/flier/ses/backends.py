from django.core.mail.backends import base
from flier import models
from flier.ses.aws import SendRawEmailResponse


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
        '''
        - http://bit.ly/flier_ses_sendrawemail
        '''
        # TODO: exception handling
        sender = models.Sender.objects.filter(
            address=message.from_email).first()
        message_id = message.extra_headers.get('Message-ID')

        for to in message.recipients():
            _to = models.Address.objects.filter(address=to).first()

            try:
                self._send_single(message, message_id,  sender, _to)
            except Exception, ex:
                models.Recipient.objects.send_failed_status(
                    sender=sender, to=_to, message_id=message_id,
                    status=ex.__class__.__name__, message=ex.message)

        return True

    def _send_single(self, message, message_id, sender, to):
        res = self.connection.send_raw_email(
            raw_message=message.message().as_string(),
            source=message.from_email,
            destinations=to.address,)

        res = SendRawEmailResponse(res['SendRawEmailResponse'])

        models.Recipient.objects.send_status(
            sender=sender, to=to, message_id=message_id,
            key=res.SendRawEmailResult.MessageId,
            status='SendRawEmailResponse', message=res.format())
