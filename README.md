#Wireless orchestration

Setup
====
Install dependencies:

    pip install python-openstackclient
    pip install python-heatclient
    pip install python-ceilometerclient 
Launch virtualenv:
    
    source bin/active
    cd aloeo/NFVO
    python manage.py runserver

OpenStack Endpoints
====
    heat=http://controller:8004/v1/
    nova=http://controller:5000/v2.0/
    keystone=http://controller:5000/v2.0/
    ceilometer=http://controller:8777


