import smtplib
from sis_notificador import keyring_store


class Gmail():

    GMAIL_SMTP_SERVER = "smtp.gmail.com"
    GMAIL_SMTP_SLL_PORT = 465

    def __init__(self):
        self.server = smtplib.SMTP_SSL(self.GMAIL_SMTP_SERVER,
                                       self.GMAIL_SMTP_SLL_PORT)

    def login(self, user, password):
        self.user = user
        self.server.ehlo()
        self.server.login(user, password)

    def close(self):
        self.server.close()

    def send_mail(self, recipient, subject, text):
        email_from = self.user
        email_to = recipient if type(recipient) is list else [recipient]
        email_message = """From: %s\nTo: %s\nMIME-Version: 1.0\nContent-type: text/html\nSubject: %s\n\n%s
        """ % (email_from, ", ".join(email_to), subject, text)

        self.server.sendmail(email_from, email_to, email_message)


if __name__ == '__main__':
    gmail_sender = Gmail()

    user = 'rodrigovieirabot'
    passStore = keyring_store.KeyringStore()
    password = passStore.get_pass(user)
    gmail_sender.login(user, password)

    recipient = 'rcardoso@gmail.com'
    subject = 'teste'
    text = 'Teste de envio de email'
    gmail_sender.send_mail(recipient, subject, text)
    gmail_sender.close()
