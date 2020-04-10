# Work at Olist

## Project Description

This project consists of an API for a library, which saves data from authors and books in its base. To build these APIs was used the programming language **Python** and the **Django Rest Framework**.


The API Documentation is available at https://library-airton.herokuapp.com/swagger/

## Instalation and test instructions

To run this project it is necessary to have python >= 3.5 installed and follow the steps below:

#### Install the virtual environment:
```sh
$ sudo apt install -y python3-venv
```

#### Create the environment:
```sh
$ python3 -m venv env
```

#### Activate the environment:
```sh
$ source env/bin/activate
```

#### Install the requirements:
```sh
$ pip install requirements.txt
```

#### Run migrations:
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

### Run the command to import the authors data from the **authors.csv** file in path **/library/management/commands**:
```sh
$ python manage.py import_authors authors.csv
```

#### Output example:
```sh
$ Reading:authors.csv
$ - Author Luciano Ramalho saved
$ - Author Osvaldo Santana Neto saved
$ - Author David Beazley saved
$ - Author Chetan Giridhar saved
$ - Author Brian K. Jones saved
$ - Author J.K Rowling saved
$ Authors saved successfully
```

#### Run project:
```sh
$ python manage.py runserver 0.0.0.0:8000
```

#### Access the local API documentation at http://0.0.0.0:8000/swagger/

#### Run tests:
```sh
$ python manage.py test
```

## Setup work environment

The machine used was an ***Intel® Core ™ i7***, **16Gb** with ***Ubuntu 18.04*** operating system. The code was written in IDE ***Visual Studio Code*** using **pylint** plugin. The main dependencies used were **Django**, **Djando Rest Framework**, **pylint** and **drf-yasg**.
