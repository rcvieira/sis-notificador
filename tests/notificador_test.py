import unittest
from sis_notificador import notificador


class TesteNotificador(unittest.TestCase):

    def testReadFile(self):
        filename = './tests/ultimo_esta_semana.txt'
        file = open(filename, 'w')
        file.write('171025')
        file.close()

        data = notificador.get_ultimo_esta_semana_enviado(filename)

        esperado = '171025'
        dt = notificador.string_to_data(esperado)

        self.assertEqual(dt, data)

    def testWriteFile(self):
        filename = './tests/ultimo_esta_semana.txt'
        file = open(filename, 'w')
        file.write('171025')
        file.close()

        esperado = '171031'
        data_nova = notificador.string_to_data(esperado)
        notificador.set_ultimo_esta_semana_enviado(filename, data_nova)

        file = open(filename, 'r')
        dataGravada = file.read(6)
        file.close()

        self.assertEqual(esperado, dataGravada)
