import keyring
import getpass
import sys


class KeyringStore():

    SIS_KEYRING = 'SIS-DOMAIN'

    def __init__(self):
        self.keyringSystem = self.SIS_KEYRING

    def set_pass(self, user, password):
        keyring.set_password(self.SIS_KEYRING, user, password)

    def get_pass(self, user):
        return keyring.get_password(self.SIS_KEYRING, user)

    def ask_pass_and_store(self, user):
        password = getpass.getpass(prompt='Password for {0}: '.format(user))
        self.set_pass(user, password)
        return password


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('> keyting_store USER')
        sys.exit()

    user = sys.argv[1]
    store = KeyringStore()
    store.ask_pass_and_store(user)
