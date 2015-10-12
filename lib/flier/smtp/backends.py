from django.core.mail.backends import smtp
from django.core.mail.message import sanitize_address
from flier import models


class SmtpBackend(smtp.EmailBackend):

    def _send(self, message):
        res = super(SmtpBackend, self)._send(message)
        self.create_send_status(message)
        return res

    def create_send_status(self, email_message):
        from_email = sanitize_address(
            email_message.extra_headers.get('From'),
            email_message.encoding)
        recipients = [sanitize_address(addr, email_message.encoding)
                      for addr in email_message.recipients()]
        sender = models.Sender.objects.filter(address=from_email).first()

        for to in recipients:
            _to, _c = models.Address.objects.get_or_create(address=to)
            models.Recipient.objects.send_status(
                sender=sender, to=_to,
                message_id=email_message.extra_headers.get('Message-ID'),
                key=email_message.from_email)       # VERP
