import logging
import sys

from django.conf import settings


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d.%m %H:%M:%S')
settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=('django.contrib.auth', 'django.contrib.contenttypes', 'tests.main'),
    DEBUG=True,
    TEMPLATE_DEBUG=True
)


def run_tests(*test_args):
    from django.test.simple import DjangoTestSuiteRunner
    if not test_args:
        test_args = ['main']
    tests_runner = DjangoTestSuiteRunner(
        verbosity=1, interactive=True, failfast=False)
    failures = tests_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    run_tests(*sys.argv[1:])
