# bombeiros-opendata
Santa Catarina fire brigade project to open data of occurrences.

## Requirements

* [Git](http://git-scm.com/) >= ?
* [Python](https://www.python.org/) >= 3.5
* [Pip](http://www.pip-installer.org/en/latest/) >= ?
* [Virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) >= ?
* [PostgreSQL](http://www.postgresql.org/) >= 9.5

## Preparing the machine (Ubuntu 16.04 LTS)

 `sudo apt-get install python-pip`
 `sudo pip install --upgrade pip setuptools

* virtualenvwrapper

```
$ sudo pip install virtualenvwrapper

$ echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
$ source ~/.bashrc

$ mkvirtualenv my-virtualenv -p /usr/bin/python3.x
$ workon my-virtualenv
```
### Instaling python dependencies(not sudo)

`(my-virtualenv)  $ pip install -r requirements.txt`

### PostgreSQL install and setup

```
$ sudo apt-get update
$ sudo apt-get install postgresql postgresql-contrib
```

```
$ sudo -i -u postgres
$ psql
$ # CREATE USER my_user WITH PASSWORD 'password';
$ # CREATE DATABASE e193;
```
### Preparing the database

You must have database dump available at the following link: https://drive.google.com/file/d/1eQOwdp6mGnczK6IYXLbnCkA6pq_hZEqF/view?usp=sharing

`$ sudo psql e193 < e193-schema.dump -U meu_user -W`

### Running App

`(meu-virtualenv)$ python app.py`

### Para colocar o processo em segundo plano e jogar a saida em log.log
`(meu-virtualenv)$ python app.py &>> log.log&`

### Para acompanhar a saida no arquivo
`(meu-virtualenv)$ tail -f log.log`
