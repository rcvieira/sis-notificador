from mailchimp3 import MailChimp


class MailChimp_Client():

    def __init__(self, api_key):
        self.client = MailChimp('', api_key)

    def get_members_emails(self, list_id):
        members = self.client.lists.members.all(
            list_id=list_id,
            fields="members.email_address")

        emails = [member['email_address'] for member in members['members']]
        return emails

# Como usar
#if __name__ == '__main__':
#    cliente = MailChimp_Client('api_key')
#    print(cliente.get_members_emails('7c1edc91ae'))
