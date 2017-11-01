import keyring
import getpass

class KeyringStore():

    SIS_KEYRING = 'SIS-DOMAIN'
    SIS_USER = 'ParentsBR'

    def __init__(self):
        self.keyringSystem = self.SIS_KEYRING
        self.user = self.SIS_USER

    def set_pass(self, password):
    	keyring.set_password(self.SIS_KEYRING, self.user, password)

    def get_pass(self):
    	return keyring.get_password(self.SIS_KEYRING, self.user)

    def ask_pass_and_store(self):
        password = getpass.getpass(prompt='Password for {0}: '.format(self.user))
        self.set_pass(password)
        return password

if __name__ == '__main__':
	store = KeyringStore()
	store.ask_pass_and_store()
