#OOCRAN: Open Orchestrator Cloud Radio Access Network 

OOCRAN is an implementation of the architecture NFV MANO standard designed for wireless communications introducing the management of the radio spectrum. It will necessary to have an OpenStack cluster (tested on Mitaka release).

Setup
====
Install dependencies:

    sudo apt-get install virtualenv
    virtualenv project_name
    cd project_name
    source bin/activate

    add-apt-repository cloud-archive:mitaka
    apt-get update && apt-get dist-upgrade
    pip install numpy
    pip install django-bootstrap-form
    pip install django_crontab
    
    pip install python-openstackclient
    pip install python-heatclient
    pip install python-ceilometerclient

Launch virtualenv:
    
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

OpenStack Endpoints
====
    heat=http://controller:8004/v1/
    nova=http://controller:5000/v2.0/
    keystone=http://controller:5000/v2.0/
    ceilometer=http://controller:8777


