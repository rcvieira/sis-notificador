import keyring
import unittest
from sis_notificador import keyring_store


class TesteKeyringStore(unittest.TestCase):

    def testStore(self):
        password = 'senhaTeste'
        store = keyring_store.KeyringStore()
        store.set_pass(password)

        storedPass = keyring.get_password(store.SIS_KEYRING, store.SIS_USER)

        self.assertEqual(storedPass, password)

    def testGetPass(self):
        password = 'senhaTeste'
        store = keyring_store.KeyringStore()

        keyring.set_password(store.SIS_KEYRING, store.SIS_USER, password)

        storedPass = store.get_pass()

        self.assertEqual(storedPass, password)
