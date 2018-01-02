import requests
import re
import datetime
import sys
from bs4 import BeautifulSoup
import keyring_store
import gmail


def send_email(user, pwd, recipient, subject, text):

    list_unsubscribe_url = 'https://mailchimp.us11.list-manage.com/unsubscribe?u=f802950604ac577d5b91757e4&id=7c1edc91ae'

    try:
        gmail_sender = gmail.Gmail()
        gmail_sender.login(user, pwd)
        gmail_sender.send_mails(recipient,
                                subject,
                                text,
                                List_Unsubscribe=list_unsubscribe_url)
        gmail_sender.close()
        print('successfully sent the mail')
    except Exception as ex:
        print("failed to send mail")
        print(ex)


def send_emails(receivers, url_pdf, data_publicacao):
    subject = '[Notificador] SIS - Temos novidades'
    texto = '''
    Ol&aacute;!<br>
    <br>
    J&aacute; viu as novidades da SIS?<br>
    <br>
    <a href="{url_pdf}">CLIQUE AQUI e veja o Esta Semana de {data}</a><br>
    <br>
    Abra&ccedil;o,<br>
    Rodrigo Vieira<br><br>
    P.S.: Este n&atilde;o &eacute; um email oficial da escola SIS<br>
    <br>
    <br>Voc&ecirc; est&aacute; recebendo este e-mail por que se cadastrou<br>
    na lista do notificador de Esta Semana da SIS.<br><br>
    Se n&atilde;o quiser receber mais estas notifica&ccedil;&otilde;es,
    <a href="https://mailchimp.us11.list-manage.com/unsubscribe?u=f802950604ac577d5b91757e4&id=7c1edc91ae">
    CLIQUE AQUI
    </a>.<br>
    Voc&ecirc; ser&aacute; redirecionado para uma p&aacute;gina 
    onde dever&aacute; informar seu email.
    '''
    body = texto.format(url_pdf=url_pdf,
                        data=data_publicacao.strftime('%d/%m/%Y'))

    usuario = 'rodrigovieirabot'
    senha = passStore.get_pass(usuario)
    send_email(usuario, senha, receivers, subject, body)


def string_to_data(dataString):
    try:
        ano = str(int(dataString[0:2]) + 2000)
        mes = dataString[2:4]
        dia = dataString[4:6]
        dt = datetime.datetime.strptime(ano + mes + dia, '%Y%m%d')
        return dt
    except Exception:
        return None


def data_to_string(data):
    return data.strftime('%y%m%d')


def get_receivers_list(receivers_filename):
    file = open(receivers_filename, 'r')
    receivers = [line.strip() for line in file]
    file.close()
    return receivers


def get_ultimo_esta_semana_enviado(esta_semana_filename):
    file = open(esta_semana_filename, 'r')
    dataString = file.read(6)
    data = string_to_data(dataString)
    file.close()

    if data is None:
        data = string_to_data('20171101')

    return data


def set_ultimo_esta_semana_enviado(esta_semana_filename, data):
    file = open(esta_semana_filename, 'w')
    file.write(data_to_string(data))
    file.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('notificador.py <arquivo de controle do esta semana> <arquivo de recebedores de email>')
        sys.exit()

    esta_semana_filename = sys.argv[1]
    receivers_filename = sys.argv[2]

    userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
    headers = {"User-Agent": userAgent}
    url_sis = 'https://www.swissinternationalschool.com.br'
    url_login = url_sis + '/en-GB/Parents-Section'

    usuarioSIS = 'ParentsBR'

    # Assume que a senha ja esta armazenada no keyring
    # e so recupera a senha
    passStore = keyring_store.KeyringStore()
    senha = passStore.get_pass(usuarioSIS)

    if senha is None or senha == '':
        print('senha não encontrada para o usuário: ' + usuarioSIS)
        sys.exit()

    s = requests.Session()
    s.headers.update(headers)
    r = s.get(url_login)
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

    r = s.post(url_login, data=login_data)

    if 'Welcome! In this section' not in r.text:
        print('Não logou!')
        sys.exit()

    url_estasemana = url_sis + \
        '/en-GB/School-Locations/Brasilia/Parents-Section/Current-Information/Parent-Letters'

    resposta = s.get(url_estasemana,
                     allow_redirects=True)

    print(resposta)
    print(resposta.text)

    p = re.compile('href=\"(.*[0-9]+EstaSemana.*pdf)\"')
    pdfs = p.findall(resposta.text)

    p_data = re.compile('[0-9]{6}')
    pdf_novo = False
    for pdf in pdfs:
        data = p_data.findall(pdf)[0]
        data_publicacao = string_to_data(data)
        data_ultimo_enviado = get_ultimo_esta_semana_enviado(esta_semana_filename)
        if (data_ultimo_enviado < data_publicacao):
            print('Existe Esta Semana novo')
            pdf_novo = True
            break

    if pdf_novo:
        url_pdf = url_sis + pdf
        receivers = get_receivers_list(receivers_filename)
        send_emails(receivers, url_pdf, data_publicacao)
        set_ultimo_esta_semana_enviado(esta_semana_filename, data_publicacao)
    else:
        print('Nao encontrei PDF novo')
