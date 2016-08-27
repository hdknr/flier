from django.core.mail.backends import smtp
from django.core.mail.message import sanitize_address
from django.utils.encoding import force_bytes
from flier.backends import BackendSignal
import smtplib
import traceback
from logging import getLogger
logger = getLogger()


class SmtpBackend(smtp.EmailBackend, BackendSignal):

    def _send(self, email_message):
        try:
            res = super(SmtpBackend, self)._send(email_message)
            self.create_send_status(email_message)
            return res
        except:
            self.create_send_status(
                email_message,
                status='smtp not send',
                message=traceback.format_exc())

    def create_send_status(
            self, email_message, status='smtp send', message=''):
        from_email = sanitize_address(
            email_message.extra_headers.get('From'),
            email_message.encoding)
        recipients = [sanitize_address(addr, email_message.encoding)
                      for addr in email_message.recipients()]

        for to in recipients:
            self.sent_signal.send(
                sender=self.__class__,
                key=email_message.from_email,       # Envelope From for bounces
                from_email=from_email, to=to,
                message_id=email_message.extra_headers.get('Message-ID'),
                status=status, message=message)

    def send_raw_message(self, from_email, to_email, message_string):
        try:
            self.open()
            self.connection.sendmail(
                from_email, [to_email], force_bytes(message_string))
        except smtplib.SMTPException, ex:
            logger.error(_("SmtpBackend.send_raw_message:{}").format(ex))
            if not self.fail_silently:
                raise
            return False
        return True
