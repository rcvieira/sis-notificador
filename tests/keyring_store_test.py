import keyring
import unittest
from sis_notificador import keyring_store


class TesteKeyringStore(unittest.TestCase):

    def testStore(self):
        user = 'TestUser'
        password = 'senhaTeste'
        store = keyring_store.KeyringStore()
        store.set_pass(user, password)

        storedPass = keyring.get_password(store.SIS_KEYRING, user)

        self.assertEqual(storedPass, password)

    def testGetPass(self):
        user = 'TestUser'
        password = 'senhaTeste'
        store = keyring_store.KeyringStore()

        keyring.set_password(store.SIS_KEYRING, user, password)

        storedPass = store.get_pass(user)

        self.assertEqual(storedPass, password)
