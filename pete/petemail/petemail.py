from abc import abstractproperty
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib


class EmailMixin(object):
    """
    Helps sending emails.  Requires a config file json file that looks something like this:
    """
    sample_config = {
        "username": "myuser@gmail.com",
        "from": "myuser@gmail.com",
        "password": "mypassword",
        "smtp": "smtp.gmail.com:587",
        "to": [
            "myuser@gmail.com",
            "youruser@gmail.com"
        ]
    }

    @abstractproperty
    def email_config_filename(self):
        return None

    @abstractproperty
    def subject_formatter(self):
        return None

    @abstractproperty
    def message_formatter(self):
        return None

    def _get_config(self):
        with open(self.email_config_filename, 'r') as buff:
            config = json.load(buff)
        for required_key in EmailMixin.sample_config:
            if required_key not in config:
                raise KeyError('Config missing {}'.format(required_key))
        return config

    def send_message(self, message_dict):
        """Email a message given a dictionary.

        Formatting is set using EmailMixin.subject_formatter and
        EmailMixin.message_formatter, and configuration is loaded from
        EmailMixin.email_config_filename.

        Args:
            message_dict: A json string defining a message.
        """
        config = self._get_config()
        from_email = config['from']
        to_emails = config['to']

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject_formatter.format(**message_dict)
        msg['From'] = from_email
        msg['To'] = ",".join(to_emails)

        msg.attach(MIMEText(self.message_formatter.format(**message_dict), 'plain'))

        server = smtplib.SMTP(config['smtp'])
        server.ehlo()
        server.starttls()
        server.login(config['username'], config['password'])
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()
