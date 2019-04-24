# Make task management better! 
[![Build Status](https://travis-ci.org/AlexZie/ticketsystem.svg?branch=master)](https://travis-ci.org/AlexZie/ticketsystem)
[![Coverage Status](https://coveralls.io/repos/github/AlexZie/ticketsystem/badge.svg?branch=master)](https://coveralls.io/github/AlexZie/ticketsystem?branch=master)
# Installation

Install a virtual environment:
```
sudo pip3 install virtualenv
```

Create a new project directory:
```
mkdir ~/projectname
cd ~/projectname
```

Download the repo and move the project into that directory:
```
cp -r /path_of_downloads /path_of_project_directory
```

Start the virtual environment in the specific directory:
```
virtualenv venv
source venv/bin/activate
```

With the new terminal look (like: (venv)username@hostname:~/projectname) you are ready to install the requirements:
```
cd /ticketsystem

pip3 install -r requirements.txt
```

Now all requirements for the project are downloaded and installed.
Open settings within mysite:
```
cd /mysite
```

Edit the settings.py file with an editor and enter your site configurations:
```
BASE_URL = ""
ALLOWED_HOSTS = []
```

To enable the email summary functionality. You have to set the parameters for your email host:
```
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''
```

To connect the ticketsytem with an LDAP the following parameters must be set.
```
AUTH_LDAP_SERVER_URI = ""
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=example,dc=com",
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
```

The database must be updated:
```
python3 manage.py makemigrations
python3 manage.py migrate
```


Create an admin to control the ticketsystem:
```
python3 manage.py createsuperuser
```

Run the server:
```
To run local on 127.0.0.1:
python3 manage.py runserver

To run on your server for example 12.12.134.11
python3 manage.py runserver 12.12.134.11
```
