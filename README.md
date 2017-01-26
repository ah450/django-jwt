# django-jwt
[![PyPI](https://img.shields.io/pypi/pyversions/django-jwt.svg)](https://pypi.python.org/pypi/django-jwt)
[![pypi Badge](https://img.shields.io/pypi/v/djang-jwt.svg)](https://pypi.python.org/pypi/django-jwt)
[![Travis](https://img.shields.io/travis/ah450/django-jwt.svg)](https://travis-ci.org/ah450/django-jwt)
[![Code Climate](https://codeclimate.com/github/ah450/django-jwt/badges/gpa.svg)](https://codeclimate.com/github/ah450/django-jwt)
[![Test Coverage](https://codeclimate.com/github/ah450/django-jwt/badges/coverage.svg)](https://codeclimate.com/github/ah450/django-jwt/coverage)
[![Issue Count](https://codeclimate.com/github/ah450/django-jwt/badges/issue_count.svg)](https://codeclimate.com/github/ah450/django-jwt)
[![license](https://img.shields.io/github/license/ah450/django-jwt.svg)](https://en.wikipedia.org/wiki/MIT_License)
[![GitHub issues](https://img.shields.io/github/issues/ah450/django-jwt.svg)](https://github.com/ah450/django-jwt/issues)
[![Gemnasium](https://img.shields.io/gemnasium/ah450/django-jwt.svg)]()



A package that provides JWT authentication and related functionality for django and [DRF](https://django-rest-framework.org).

# Installation
`pip install djang-jwt`
If you require DRF support install the drf extras via `pip install django-jwt[drf]`


# Settings
profile_klass should be set to your profile model


user_reverse_profile_key should be the related name of profile on user model

jwt_realm should be set to your app name, user friendly version

email_subject should be set to your a user friendly string that will appear in email subjects

FROM_EMAIL_ADDRESS should also be set.


email_templates_dir should be set to a directory that contains activate_account.txt andreset_pass.txt