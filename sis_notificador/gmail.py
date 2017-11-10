import smtplib
import keyring_store


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

    def send_mails(self, recipient, subject, text):
        recipients = recipient if type(recipient) is list else [recipient]
        for r in recipients:
            self.send_mail(r, subject, text)


if __name__ == '__main__':
    gmail_sender = Gmail()

    user = 'rodrigovieirabot'
    passStore = keyring_store.KeyringStore()
    password = passStore.get_pass(user)
    gmail_sender.login(user, password)

    recipients = ['rcardoso@gmail.com']
    subject = 'teste'
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

    #titulo = 'J&aacute; viu o novo Esta Semana da SIS?<br><br>'
    #link = '<a href="{url_pdf}">CLIQUE AQUI e veja o Esta Semana de {data}</a>'.format(
    #    url_pdf='http://rodrigovieira.me', data='01/01/2001')
    #unsub1 = '<br><br><br><br>Voc&ecirc; est&aacute; recebendo este e-mail por que se cadastrou na lista do notificador de Esta Semana da SIS'
    #unsub2 = '<br>Se n&atilde;o quiser receber mais estas notifica&ccedil;&otilde;es, basta responder este email escrevendo SAIR no corpo do e-mail.'
    #disclaimer = '<br><br>Rodrigo Vieira<br>O notificador não tem qualquer ligação oficial com a escola SIS.'
    #text = inicio + titulo + link + unsub1 + unsub2 + disclaimer
    #text = 'Teste de envio de email'
    gmail_sender.send_mails(recipients, subject, text)
    gmail_sender.close()
