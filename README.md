# Since we do not use the software anymore it is now **unmaintained**

## Make task management better! 
[![Build Status](https://travis-ci.org/d120/pyticket.svg?branch=master)](https://travis-ci.org/d120/pyticket)
[![Coverage Status](https://coveralls.io/repos/github/d120/pyticket/badge.svg?branch=master)](https://coveralls.io/github/d120/pyticket?branch=master)
## Installation (development)

Install a virtual environment:
```
sudo pip3 install virtualenv
```

Clone the repo
```
git clone https://github.com/d120/pyticket.git
```

Create and activate the virtual environment:
```
virtualenv venv
source venv/bin/activate
```

With the new terminal look (like: (venv)username@hostname:~/projectname) you are ready to install the requirements:
```
pip3 install -r requirements.txt
```

Now all requirements for the project are downloaded and installed.
Open settings within mysite:
```
cd pyticket
```

Edit the settings.py file with an editor and enter your site configurations:
```
BASE_URL = "<your base url without trailing slash"
ALLOWED_HOSTS = ['allowed hosts']
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
