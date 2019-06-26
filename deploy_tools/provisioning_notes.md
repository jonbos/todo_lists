Provisioning a new site
=======================

## Required packages:
* nginx
* Python 3.6
* Git
* virtualenv + pip

## Nginx Virtual Host config
* see nginx.template.conf
* replace DOMAIN with path to site


## Systemd config
* see gunicorn-systemd.template.service
* replace DOMAIN with path to site

## Folder structure:

Assume we have a user account at /home/username

/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc

