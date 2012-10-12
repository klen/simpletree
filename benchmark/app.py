import sys
from os import path as op

from django.conf.urls.defaults import patterns
from django.template.response import TemplateResponse


# helper function to locate this dir
here = lambda x: op.join(op.abspath(op.dirname(__file__)), x)


# VIEW
def index(request, name):
    return TemplateResponse(request, 'index.html', {'name': name})


# URLS
urlpatterns = patterns('', (r'^(?P<name>\w+)?$', index))

if __name__ == '__main__':

    # set the ENV
    from django.conf import settings
    settings.configure(
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        INSTALLED_APPS=('django.contrib.auth', 'django.contrib.contenttypes', 'main'),
        DEBUG=True,
        TEMPLATE_DEBUG=True
    )

    sys.path += (here('.'),)

    # run the development server
    from django.test.simple import DjangoTestSuiteRunner
    tests_runner = DjangoTestSuiteRunner(
        verbosity=1, interactive=True, failfast=False)
    failures = tests_runner.run_tests(['main'])
