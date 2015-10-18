from django.core.mail.backends import smtp
from django.core.mail.message import sanitize_address
from django.utils.encoding import force_bytes
from flier.backends import BackendSignal
import smtplib


class SmtpBackend(smtp.EmailBackend, BackendSignal):

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

        for to in recipients:
            self.sent_signal.send(
                sender=self,
                from_email=from_email, to=to,
                message_id=email_message.extra_headers.get('Message-ID'),
                status='smtp send',
                key=email_message.from_email, message='')

    def send_raw_message(self, from_email, to_email, message_string):
        try:
            self.open()
            self.connection.sendmail(
                from_email, [to_email], force_bytes(message_string))
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise
            return False
        return True
