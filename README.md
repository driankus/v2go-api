# v2go-web-ap
V2go web app's repo contains client and server apps (django angular), and infastructure setup for both apps, postgres, redis, and nginx using docker 

## REQUIREMENTS
1. Docker
2. Docker-compose

### Docker
To install docker on your system, please go to [this link](https://docs.docker.com/install/)

### Docker-compose
To install docker-compose on your system, please go to [this link](https://docs.docker.com/compose/install/)

Once you have installed docker and docker-compose, you will be able to run the project locally

### Giving Sudo Privilege to Docker (Optional)
By default if you would like to run `docker` or `docker-compose`, you would have to use `sudo`.
If you would like to not use `sudo` then follow this [tutorial](https://docs.docker.com/install/linux/linux-postinstall/) on how to provide sudo privilege to docker

If you choose to not provide sudo privilege to docker then simply make sure to use `sudo` whenever you see a command that begins with `docker` or `docker-compose`

## RUN PROJECT LOCALLY with DOCKER
This project has been set up to run all it's components in Docker containers. The 5 main services are: Django (back-end server), Angular/ev-finder-client (front end application), Redis (fast read/write db, 'cached db'), PostgresQL (persistent db), and Nginx (proxy server, routs requests to django or angular accordingly). 

You simply have to run docker-compose from the root directory. 
```bash
# To lunch all 4 services:
$ docker-compose up -d --build

# To check that services are running:
$ docker-compose ps 

# Run django migrations
$ docker-compose run django-server python django-server/manage.py makemigrations
$ docker-compose run django-server python django-server/manage.py migrate

# Go to http://localhost:8080 in your browser to use the app
```

To stop the services and kill the containers
```bash
# End all services:
$ docker-compose down
```

### Run tests inside Docker
Before running tests, make sure docker services are running and all Django migrations were applied
```bash
# Python/Django tests
#$ docker-compose run django-server python django-server/manage.py test <file-name>.tests

# Angular/node tests
#$ docker-compose run ev-finder-client ng test
```

## PROJECT SET UP FOR DEVELOPMENT (developers only)
In order to make changes to this project, you have to install key tools and packages, and set up a development environment. Follow these steps:

### 1. Setup Python and install django (+ other packages)
**Required:** Python3.7 (doesn't need to be the default system python) and pip

```bash
# Install Python3.7, if it's not yet installed
$ sudo apt-get update
$ sudo apt-get install python3.7

# install pipenv
$ pip install pipenv

# Go into /django_server/, create a new virtual env and activate it
$ pipenv --python 3.7  # or path/to/python if no python 
$ pipenv shell

# Make sure pip is not v18.1, while venv is active.(Known issue with v18.1, fix src: https://github.com/pypa/pipenv/issues/2924)
$ (venv) pip --version

# IF pip==18.1, THEN downgrade to 18.0 (from within venv)
$ (venv) pip install pipenv
$ (venv) pipenv run pip install pip==18.0

# If pip ==18.0 and Pipfile available,  then install packages
$ (venv) pipenv install

# IF not using pipenv or no Pipfile already available, use this to install packages
# $ (vevn) pip install \
#               channels==2.1.2 \
#               channels-redis==2.3.0 \
#               Django==2.1.5 \
#               djangorestframework==3.8.2 \
#               nose==1.3.7 \
#               Pillow==5.2.0 \
#               pytest-asyncio==0.9.0 \
#               pytest-django==3.4.2

# Check that packages were installed
$ (venv) pipenv graph
```


### 2. Instal and setup Angular, node, and node-packages for Angular
Install node and angular
```bash
#If npm and node.js aren't installed, do that first:
$ sudo snap install node --channel=10/stable --classic

# install Angular CLI
$ npm install -g @angular/cli@6.1.4   #TODO: Need to UPGRADE to newer LTE 

# check version
$ ng v
```

Launch project
```bash 
# cd into aungular-ui and launch server
$ ng serve --open
```

If you were taken to the welcome page (http://localhost:4200), Kill server (ctr+c) and install packages
```bash
# cd into /angular-ui/ and install packages
$ npm install 

# If this doesn't work, do a manual install (DANGEROUS!... This is a quick fix, make the other work instead)
#  $ npm install \
#        bootstrap \
#        jquery \
#        popper.js \
#        bootswatch --save
```

