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
