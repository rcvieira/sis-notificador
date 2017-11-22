from mailchimp3 import MailChimp
import configparser
import sys


def get_configs(notificador_cfg_filename):
    config = configparser.RawConfigParser()
    config.read(notificador_cfg_filename)
    props = {'mailchimp_api_key': config.get('MAILCHIMP', 'API_KEY'),
             'mailchimp_list_id': config.get('MAILCHIMP', 'LIST'),
             'receivers_filename': config.get('FILES', 'RECEIVERS')}
    return props


def save_receivers_list_to_file(receivers_filename, receivers):
    file = open(receivers_filename, 'w')
    for r in receivers:
        file.write(r + '\n')
    file.close()


class MailChimp_Client():

    def __init__(self, api_key):
        self.client = MailChimp('', api_key)

    def get_members_emails(self, list_id):
        members = self.client.lists.members.all(
            list_id=list_id,
            get_all=True,
            fields="members.email_address",
            status='subscribed')

        emails = [member['email_address'] for member in members['members']]
        return emails


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('notificador.py <notificador.cfg>')
        sys.exit()

    notificador_cfg_filename = sys.argv[1]

    props = get_configs(notificador_cfg_filename)

    try:
        cliente = MailChimp_Client(props['mailchimp_api_key'])
        receivers = cliente.get_members_emails(props['mailchimp_list_id'])

        save_receivers_list_to_file(props['receivers_filename'], receivers)
    except Exception:
        sys.exit()
