# !/usr/bin/env python
import sys
from os.path import dirname, abspath

import django
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='khipu.urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'khipu',
    ),
    LOGGER_KHIPU='logger_khipu',
    USE_TZ=True,
    KHIPU_RECEIVER_ID="148653",
    KHIPU_SECRET_KEY="73ebf4fc9d41f9892ab00a12d5070cdf389767f6"
)

try:
    # Django < 1.8
    from django.test.simple import DjangoTestSuiteRunner
except ImportError:
    # Django >= 1.8
    from django.test.runner import DiscoverRunner as DjangoTestSuiteRunner


def runtests():
    django.setup()
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    test_runner = DjangoTestSuiteRunner(verbosity=1)
    failures = test_runner.run_tests(['khipu'], verbosity=1, interactive=True)
    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    runtests()
