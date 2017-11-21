from setuptools import setup

setup(name='sis_notificador',
      version='0.1',
      description='Notifica por email novidades no site da SIS',
      url='https://github.com/rcvieira/sis-notificador',
      author='Rodrigo Veira',
      author_email='rcardoso@gmail.com',
      license='MIT',
      packages=['sis_notificador'],
      install_requires=[
          'requests',
          'keyring',
          'BeautifulSoup4',
          'mailchimp3'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
