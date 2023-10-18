# Functional Fashion Server
The purpose of this repository is to enable a backend to directly interact with the front-facing watch application, for the purpose of recording relevant biometric data. Using Django, we enable running our application by configuring `mod_wsgi` Apache module.

The following installation will assume that nothing has been configured with regards to installed packages or Apache.

## Installation and Deployment
### Install Requisite Packages (Linux)
Using Django with Python3 (as per this particular repository):
```
sudo apt-get update
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
```

Git clone the project into a desired directory with: `git clone https://github.com/ehng359/functional_fashion_server`. This will contain the virtual environment being used for this project as well as the files necessary for starting up the server. Change directory into the newly cloned folder and perform the command `source env/bin/activate` which will activate the virtual environment.

Run the following command:
```
pip3 install django django-rest-framework django-debug-toolbar
```
This will install the necessary Python frameworks if they do not already exist. Next we create an superuser (to manage the database/models) and collect static content into the folders.
```
python3 manage.py createsuperuser
...
python3 manage.py collectstatic
```

At this point, if you run `python3 manage.py runserver 0.0.0.0:8000` you should be able to visit the server domain name or IP address followed by :8000. This will display a JSONObject of heartBeat data. If it states there exists a disallowed host, edit the file settings.py contained in the hb_read_server2 folder to add a string of the IP or hostname this server is attempted to be run on.

* `http://domain_or_IP:8000/` - base endpoint for GET/PUT/POST HTTP request data
* `http://domain_or_IP:8000/admin` - admin panel

### Configure Apache
First, edit the default virtual host file in order to use Apache to translate client connections into WSGI format Django expects: 
`sudo txt_editor /etc/apache2/sites-available/000-default.conf`

Keeping the existing content within the file, add:
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
sudo chown :www-data /path/to/repo/db.sqlite3
sudo chown :www-data /path/to/repo
```
Once these permissions are granted, we can restart the service with `sudo service apache2 restart`.
<br>

These processes enable us to setup the DJango project in its own virtual environment and configure Apache with mod_wsgi to handle client requests to directly interface with Django. If not launching on a public server accessible via some domain, ensure that all devices in which want to make the request belnog to the same network as the server.

### Required Python Modules
```
-- requirements.txt
django 
django-rest-framework 
django-debug-toolbar 
cpython 
numpy 
neurokit2
```

## HTTP Requests and Usage
### GET
Available parameters for the HTTP request while retrieving live data from the Apple Watch:
- id : (alpha_numeric_value)-... Watch identifier unique to each Apple Watch.
- since_day :(yyyy-mm-dd) which evaluates all the information that has occurred since the provided date, defaulting from 00:00:00, or since_time if specified.
- since_time : (hh:mm:ss) which evaluates all the information that has occurred since the provided time at current day (default) or the since_date day provided.
- past : (numeric_value)_(metric) which indicates the range from which you want to retrieve data from current time. (i.e. 5_days, 4_hours, 3_minutes, 2_seconds). Note: This feature does not work interchangeably with since_day or since_time.
- num_instances : (numeric_value) which indicates the number of instances that you want to query for at a given time.

#### Example GET requests
```
-- Retrieving the data since a certain day --
https://[url].com/?id=XXXXXX-XXXXXX-XXXXXXX-XXXXXX&2023-01-01
-- Retrieving the data since a certain day-time --
https://[url].com/?id=XXXXX-XXXXX-XXXXX-XXXXX&since_day=2021-10-21&since_time=14:27:12
-- Retrieving the data since --
https://[url].com/?id=XXXXX-XXXXX-XXXXX-XXXXX&past=10_minutes
-- Retrieving x amount of samples --
https://[url].com/?id=XXXXX-XXXXX-XXXXX-XXXXX&num_instances=5
-- Retrieving x amount of samples since certain day-time --
https://[url].com/?id=XXXXX-XXXXX-XXXXX-XXXXX&since_day=2021-10-21&since_time=14:27:12&num_instances=5
```
Providing none of these values will simply return all the values accordingly.
Note: providing past and since_* parameters will conflict; do not place it in the same query call.

If you are gathering data via Python, look at the `requests` module to simplify this process easier by simply calling:
```python
import requests
url = https://www.some_end_point.com/
params = {"id" : "someID"}                          # some dictionary type adhearing to the aforementioned parameters
response = requests.get(url=url, PARAMS=params)     # making request directly to the particular endpoint with aforementioned parameters

# --- Handle response here --- "
```

### POST
Adds biometric data in the format of:
```json
[{
    "watchUser": "B6B2A8D5-CA77-4D2D-AFE3-F1074690BA3F", 
    "date": "2023-08-16 13:27:17 +0000", 
    "heartBeat": 76, 
    "respiratoryRate": null, 
    "heartBeatVar": null, 
    "restingHeartRate": null, 
    "valence": 0.04870128631591797, 
    "arousal": 0.0, 
    "activity": "Work/Study"
}, ...]
```
These values will then store into the User & Biometric models which contain the information related to all the information held in the provided JSON-format.

### PUT
Takes all values from a given session and consolidates the values to a .json file compiled together underneath the data folder constructed with the makeData.sh shell script. If an email is provided to the watch application, it will additionally be indicated to the server and call upon the emailUserData.py script and send a summary of the session to the user's email.

## Django Apps and Models
Within the `collect` app, there exist are two primary models handling the data from the Apple Watch (users and biometrics) where the User model and Biometrics model is defined by:
```python
class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=40, default="")
    biometricData = models.ManyToManyField('Biometrics', blank=True, null=True)

    def __str__(self):
        return self.id
```
```python
class Biometrics(models.Model):
    watchUser = models.ForeignKey(Users,blank=True, null=True, on_delete=models.DO_NOTHING)
    date = models.CharField(max_length=30, default="")

    # Biometric label values
    heartBeat = models.IntegerField(default=None, null=True)
    respiratoryRate = models.IntegerField(default=None, null=True)
    heartBeatVar = models.IntegerField(default=None, null=True)
    restingHeartRate = models.IntegerField(default=None, null=True)

    # Emotion-Spectrum Grid Values
    valence = models.FloatField(default=None, null=True)
    arousal = models.FloatField(default=None, null=True)

    # Context
    activity = models.CharField(max_length=20, default="None")

    def __str__(self):
        return self.watchUser.id + " " + self.date
```
This provides the information necessary relative for Django to understand what type of data is needed to be stored in the SQLite.db file and in what structure. The views.py file indicates how each request mentioned above is handled relative to the models provided.

The `process_ecg` application allows users to send their ECG data to a different access point within the server that is dedicated to processing raw ECG data and providing metrics regarding data (i.e. heart-rate, heart-rate variability, and ECG-derived respiration); this application has no connected models and only returns processed information back towards the source of the request. This is powered primarily through the `Neurokit2` module as well as `scipy`.