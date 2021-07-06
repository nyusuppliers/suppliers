## Introduction

This project is the back end for an eCommerce web site as a RESTful microservice for the suppliers. An supplier is a vendor from whom we get products from. This microservice supports the complete Create, Read, Update, & Delete (CRUD) lifecycle

## Repository Structure
```
service
├─ __init__.py     - package initializer
├─ models.py      
├─ routes.py
└─ status.py

tests
├─ __init__.py
├─ factories.py
├─ test_models.py
└─ test_routes.py
```


## Run the Service on Your Local PC

### Prerequisite Installations
Download [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/).

### Executing the TDD Unit Test
To exectunig the service, type the following command in the terminal SSH:
```
$ git clone https://github.com/nyusuppliers/suppliers.git
$ cd suppliers
$ vagrant up
$ vagrant ssh
$ cd /vagrant
$ nosetests
```
To see the coverage report, type:
```
$ coverage report -m
```

### Close Service
Once finish, to close the VM and terminate servce. Please type
```
$ exit
$ vagrant halt
```
