# OrderFood
**POC! Sample django app for ordering food**

It's a project for university classes.

### Mandatory system requirements
* PostgreSQL 9.6 (or any other DB)
* Python > 3.5
* git
* Optional: virtualenv

### Manual
1. Clone repo to your desired directory: ```https://github.com/kamilgregorczyk/OrderFood.git && cd orderfood```
2. Create a virtualenv for the project ```mkvirtualenv orderfood```
3. Install the requirements ```pip install -r requirements.txt```
4. Update your database settings in a local settings file ```nano pyszne/settings.py```
5. Create tables in your database (migrations) ```./manage.py migrate```
6. Create an account ```./manage.py createsuperuser```
7. Start a server on http://localhost:8000 ```./manage.py runserver```
