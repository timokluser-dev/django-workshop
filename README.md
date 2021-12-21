# django-workshop

<a href="https://www.djangoproject.com/">
    <img style="width: 150px;" src="https://static.djangoproject.com/img/logos/django-logo-negative.png" alt="django logo" />
</a>

- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Django](https://www.djangoproject.com/)
- [Django Docs v4.0](https://docs.djangoproject.com/en/4.0/)

## create project

- copy .env.sample to .env
- `docker-compose run django bash`
- `pip freeze` (show dependencies) 
- `pip install django`
- `pip freeze` (show dependencies)
- `pip freeze > requirements.txt`
- `django-admin startproject app .`
- `exit`
- .docker/Dockerfile (remove comment on line 38)
- `docker-compose up --build`

## debugging with PyCharm

:arrow_right: [engineering-playbook/python/django_debug/debug.md](https://gitlab.liip.ch/eastside-customs/engineering-playbook/-/blob/master/python/django_debug/debug.md)

## creating new models

file: `db/models.py`

- build models
- add `__str__(self)` method
- (add Meta class)

```bash
# after model created / changed:
./manage.py  makemigrations

# apply the newly created migration [for app db]
./manage.py  migrate [db]
```
→ Make small migrations for better maintainability

<br>

file: `db/admin.py`

- register model for django admin
  - `admin.site.register(Model)`

## updating models

when doing changed to the models, pay attention to the following:

- set default or null values for existing entries:
  - `models.TextField(null=True, ...)` 
  - _or_ 
  - `models.TextField(default="some defaults", ...)`
- when renaming attributes, do one migration only for renaming

## Wagtail CMS

:information_source: wagtail is currently not compatible with Django 4.
It will perform a downgrade of Django to version 3 during install.

```bash
pip install wagtail
pip install wagtailmedia
pip freeze > requirements.txt
```

:arrow_right: https://docs.wagtail.io/en/stable/getting_started/integrating_into_django.html

→ add `'wagtailmedia'` to `INSTALLED_APPS` in settings.py

---

# Django template

## Add Hosts file

Add the following to your `/etc/hosts` file.

    127.0.0.1       django.what-ever.lo

## Setup environment variables 

    make init

## Docker shortcuts

    make up
    make down
    make bash

## Django Admin GUI
You can access the Admin Gui through [http://django.what-ever.lo/admin/](http://django.what-ever.lo/admin/).
    
    Username: admin
    Password: admin
