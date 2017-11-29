import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import keyring_store
import random


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

    def send_mail(self, recipient, subject, text, headers):
        email_from = self.user
        email_to = recipient if type(recipient) is list else [recipient]

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = ", ".join(email_to)

        for header in headers:
            msg[header] = headers[header]

        part = MIMEText(text, 'html')
        msg.attach(part)

        self.server.sendmail(email_from, email_to, msg.as_string())

    def send_mails(self, recipient, subject, text, **headers):
        recipients = recipient if type(recipient) is list else [recipient]
        for r in recipients:
            self.send_mail(r, subject, text, headers)


if __name__ == '__main__':
    gmail_sender = Gmail()

    user = 'rodrigovieirabot'
    passStore = keyring_store.KeyringStore()
    password = passStore.get_pass(user)
    gmail_sender.login(user, password)

    recipients = ['rcardoso@gmail.com']
    subject = 'teste' + str(random.randrange(1000))
    inicio = 'Ol&aacute;!<br><br>'
    texto = '''
    Ol&aacute;!<br>
    <br>
    J&aacute; viu as novidades da SIS?<br>
    <br>
    <a href="{url_pdf}">CLIQUE AQUI e veja o Esta Semana de {data}</a><br>
    <br>
    <br>
    Rodrigo Vieira<br>
    Este email n&atilde;o &eacute; um email oficial da escola SIS<br>
    <br>
    <br>Voc&ecirc; est&aacute; recebendo este e-mail por que&nbsp;
    se cadastrou na lista do notificador de Esta Semana da SIS&nbsp;
    desenvolvido por mim.<br>
    Se n&atilde;o quiser receber mais estas notifica&ccedil;&otilde;es,&nbsp;
    basta responder este email escrevendo SAIR no corpo do e-mail.
    '''
    text = texto.format(url_pdf='http://rodrigovieira.me', data='01/01/2001')

    list_unsubscribe_url = 'https://mailchimp.us11.list-manage.com/unsubscribe?u=f802950604ac577d5b91757e4&id=7c1edc91ae'

    gmail_sender.send_mails(recipients,
                            subject,
                            text,
                            List_Unsubscribe=list_unsubscribe_url)
    gmail_sender.close()
