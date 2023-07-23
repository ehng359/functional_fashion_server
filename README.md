# Functional Fashion Server
The purpose of this repository is to enable a backend to directly interact with the front-facing watch application, for the purpose of recording relevant biometric data. Using Django, we enable running our application by configuring `mod_wsgi` Apache module.

The following installation will assume that nothing has been configured with regards to installed packages or Apache.

## Installation and Deployment
### Install Requisite Packages (Linux)
Using Django with Python3 (as per this particular repository):
```
sudo apt-get update
sudo apt-get install apache2 libapache2-mod-wsgi
```

Git clone the project into a desired directory with: `https://github.com/ehng359/functional_fashion_server`. This will contain the virtual environment being used for this project as well as the files necessary for starting up the server. Change directory into the newly cloned folder and perform the command `source env/bin/activate` which will activate the virtual environment.

Run the following command:
```
pip3 install django django-rest-framework
```
This will install the necessary Python frameworks if they do not already exist. Next we create an superuser (to manage the database/models) and collect static content into the folders.
```
python3 manage.py createsuperuser
...
python3 manage.py collectstatic
```

At this point, if you run `./manage.py runserver 0.0.0.0:8000` you should be able to visit the server domain name or IP address followed by :8000. This will display a JSONObject of heartBeat data.

* `http://domain_or_IP:8000/` - base endpoint for GET/PUT/POST HTTP request data
* `http://domain_or_IP:8000/admin` - admin panel

### Configure Apache
First we edit the default vritual host file in order to use Apache to translate client connections into WSGI format Django expects: 
`sudo txt_editor /etc/apache2/sites-available/000-default.conf`

Keeping the existing content within the file, we add:
```
<VirtualHost *:80>
    . . .

    Alias /static /path/to/repo/static
    <Directory /path/to/repo/static>
        Require all granted
    </Directory>

    <Directory /path/to/repo/hb_read_server2>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess repo_name python-path=/path/to/repo python-home=/path/to/repo/env
    WSGIProcessGroup repo_name
    WSGIScriptAlias / /path/to/repo/hb_read_server2/wsgi.py
</VirtualHost>
```

### Permissions Adjustment
With the SQLite database, we require the established Apache process access to the file itself:
```
chmod 664 /path/to/repo/db.sqlite3
chown :www-data /path/to/repo/db.sqlite3
sudo chown :www-data /path/to/repo
```
Once these permissions are granted, we can restart the service with `sudo service apache2 restart`

<br>
These processes enable us to setup the DJango project in its own virtual environment and configure Apache with mod_wsgi to handle client requests to directly interface with Django.