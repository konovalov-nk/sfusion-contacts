## Contact details

A simple project for managing people's contact details using Vue.js (`vue-cli 3.0` scaffold), Django (REST API), PostgreSQL, Docker, `nginx-proxy`, TDD/BDD testing tools (`chai`, `mocha`, `mamba`, `expects`), a few things from [12-factor](https://12factor.net/) (such as `.env` configuration files). For a full list, see [Built with](#built-with).

### Getting Started

This project uses [Docker](https://www.docker.com/) to make initial setup easy for development, deployment, and testing purposes. See deployment for notes on how to deploy the project on a live system.

#### Prerequisites

If you don't have `docker` and `docker-compose` installed, [get it](https://store.docker.com/search?type=edition&offering=community) (available for Linux/OS X/Windows).


#### Installing

To build and run basic development environment, run

```
$ docker-compose up
```

Press `ctrl+c` to stop containers. Another way to do it is

```
$ docker-compose down
```

If you need to rebuild containers, use

```
$ docker-compose up --build
```

Next thing you need is `/etc/hosts` and `.env.example`. Copy `.env.example` to `.env`

```
$ cp .env.example .env
```

Then add `FRONTEND_HOST` and `BACKEND_HOST` values (from `.env` file) to your `/etc/hosts` file, example

```
127.0.0.1  localhost contacts.local api.contacts.local
```

**Please note, in case you are using Docker toolbox it would run under Vagrant VM, so you have to [find IP of your docker machine](https://docs.docker.com/machine/reference/ip/)**:

```
$ docker-machine ip dev
192.168.99.104
```

In that case you have to add a different record to the `/etc/hosts`

```
192.168.99.104  contacts.local api.contacts.local
```

If you did everything right up to this point, you should now be able to access [http://contacts.local](http://contacts.local) and [http://api.contacts.local](http://api.contacts.local)

### Testing

To run **backend** development environment with unit/integration tests (reload on file changes), execute

```
$ docker-compose -f docker-compose.yml -f docker-compose.test-backend.yml run backend-test
```

To run **frontend** development environment with unit/integration tests (reload on file changes), execute

```
$ docker-compose -f docker-compose.yml -f docker-compose.test-frontend.yml run frontend-test
```

Make sure there is an output from them by changing files inside `./backend/spec` or `./frontend/tests`. Otherwise, there could be a problem. Feel free to open any issues.


### Deployment

.. To-do ..

### Built with

* [axios](https://github.com/axios/axios) - Promise based HTTP client for the browser and `node`
* [chai](https://github.com/chaijs/chai) - TDD/BDD assertion library for `node`
* [django](https://www.djangoproject.com) - Backend framework
* [djangorestframework](https://github.com/encode/django-rest-framework) - Django REST framework
* [docker](https://www.docker.com) - Containerization
* [expects](https://github.com/jaimegildesagredo/expects) - TDD/BDD assertion library for Python
* [factory-girl](https://github.com/aexmachina/factory-girl) - A factory library for Node.js and the browser
* [factory_boy](https://github.com/FactoryBoy/factory_boy) - A test fixtures replacement for Python
* [faker.js](https://github.com/Marak/Faker.js) - Generate massive amounts of fake data in the browser and `node`
* [faker](https://github.com/joke2k/faker/) - A Python package that generates fake data
* [gunicorn](https://github.com/benoitc/gunicorn) - Python WSGI HTTP server
* [mamba](https://github.com/nestorsalceda/mamba) - BDD-style test runner for Python
* [mocha](https://github.com/mochajs/mocha) - Javascript test framework for `node` & the browser
* [moxios](https://github.com/axios/moxios) - Mock `axios` requests for testing
* [nginx-proxy](https://github.com/jwilder/nginx-proxy) - Automated `nginx` proxy for Docker containers
* [nginx](https://github.com/nginx/nginx) - HTTP and reverse proxy server
* [postgres](https://github.com/postgres/postgres) - PostgreSQL DBMS
* [vue.js](https://vuejs.org) - The frontend library used

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### Acknowledgements

* Thanks to [fago](https://github.com/fago) for his awesome `inotifywait` [script](https://gist.github.com/fago/9608238). It just works.
* Database diagrams created with [QuickDBD](https://www.quickdatabasediagrams.com)
* BPMN diagram created with [BPMN Viewer and Editor](https://bpmn.io/)
