import requests
import re
import datetime
import smtplib
import keyring_store
from bs4 import BeautifulSoup


def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nMIME-Version: 1.0\nContent-type: text/html\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except Exception as ex:
        print("failed to send mail")
        print(ex)


userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
headers = {"User-Agent": userAgent}
url_sis = 'http://www.swissinternationalschool.com.br'
url_login = url_sis + '/en-GB/Parents-Section'

usuarioSIS = 'ParentsBR'

# Assume que a senha ja esta armazenada no keyring
# e so recupera a senha
passStore = keyring_store.KeyringStore()
senha = passStore.get_pass(usuarioSIS)

s = requests.Session()
s.headers.update(headers)
r = s.get(url_login)
# print(s.cookies)
soup = BeautifulSoup(r.content, 'html.parser')

VIEWSTATE = soup.find(id="__VIEWSTATE")['value']
VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value']
EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value']

login_data = {"__VIEWSTATE": VIEWSTATE,
              "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
              "__EVENTVALIDATION": EVENTVALIDATION,
              "inhalt_0$UserName": usuarioSIS,
              "inhalt_0$Password": senha,
              "inhalt_0$submitButton": "Log In"}

# print(login_data)

r = s.post(url_login, data=login_data)

url_estasemana = url_sis + \
    '/en-GB/School-Locations/Brasilia/Parents-Section/Current-Information/Parent-Letters'

# print(s.cookies)
# print(r.cookies)
resposta = s.get(url_estasemana,
                 allow_redirects=True)

# print(resposta)
# print(resposta.text)

p = re.compile('href=\"(.*[0-9]+EstaSemana.*pdf)\"')
pdfs = p.findall(resposta.text)

p_data = re.compile('[0-9]{6}')
pdf_novo = False
for pdf in pdfs:
    data = p_data.findall(pdf)[0]
    ano = str(int(data[0:2]) + 2000)
    mes = data[2:4]
    dia = data[4:6]
    dt = datetime.datetime.strptime(ano + mes + dia, '%Y%m%d')
    ultima_vez = datetime.datetime.now() - datetime.timedelta(days=20)
    if (ultima_vez < dt):
        print('Existe Esta Semana novo')
        print(pdf)
        pdf_novo = True
        break

if pdf_novo:
    url_pdf = url_sis + pdf
    sender = 'rcardoso@gmail.com'
    receivers = ['rcardoso@gmail.com', 'luavelar@gmail.com']
    subject = '[Notificador] SIS - Temos novidades'
    titulo = 'J&aacute; viu o novo Esta Semana da SIS?<br><br>'
    link = '<a href="{url_pdf}">CLIQUE AQUI para ver o Esta Semana de {data}</a>'.format(
        url_pdf=url_pdf, data=dt.strftime('%d/%m/%Y'))
    unsub1 = '<br><br>Voc&ecirc; est&aacute; recebendo este e-mail por que se cadastrou na lista do notificador de Esta Semana da SIS'
    unsub2 = '<br>Para n&atilde;o receber mais estas notifica&ccedil;&otilde;es, basta responder este email escrevendo SAIR no corpo do e-mail.'
    body = titulo + link + unsub1 + unsub2
    usuario = 'rodrigovieirabot'
    senha = passStore.get_pass(usuario)
    send_email(usuario, senha, receivers, subject, body)
