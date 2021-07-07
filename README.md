## Introduction

This project is the back end for an eCommerce web site as a RESTful microservice for the suppliers. An supplier is a vendor from whom we get products from. This microservice supports the complete Create, Read, Update, & Delete (CRUD) lifecycle

## Repository Structure
```
service
├─ __init__.py     - package initializer
├─ models.py       - service database models
├─ routes.py       - service routes settings
└─ status.py       - service status codes

tests
├─ __init__.py     - test initializer
├─ factories.py    - module to generate the fake data
├─ test_models.py  - test case for the models service
└─ test_routes.py  - test case for the routes service
```

## Database Deisgn Attributes

| Field | Type | Primary Key | Descriptions 
| :--- | :--- | :--- | :--- |
| id | Integer | True | Id of the supplier 
| name | String | False | Name of the individual or company name 
| phone | String | False | Phone number of the supplier 
| address | String | False| Address of the supplier
| available | Boolean(default True) |False | supplier availbility
| product_list | Integer List | False | Product id lists for each supplier
| rating | Float | False | Supplier rating 

## Run the test service on Your Local PC

### Prerequisite Installations
Download [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/).

For unix user, we recommend to install the environment via Homebrew:
```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then Executing the command to finish the installation:
```
$ brew install git
$ brew install --cask virtualbox
$ brew install --cask vagrant
```

### Executing the TDD Unit Test
To executing the service, type the following command in the terminal SSH:
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
Once finish, to close the VM and terminate service. Please type:
```
$ exit
$ vagrant halt
```
Once finish testing and no longer need it again. Please type following command to delete the service.
```
$ vagrant destroy
```
