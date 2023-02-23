To run project:
1. Setup postgres user and database, then input login credentials to settings or change database in settings to sqlite (does not require any additional setup).
2. Run command: python manage.py makemigrations
3. Run command: python manage.py migrate
4. Run tests: python manage.py test
5. To create requested account tiers + test user in each tier + test admin account, run commands:
python manage.py shell -> from setup import setup_test_env -> setup_test_env()
6. Run command: python manage.py runserver




NOTES:
Index page is just login screen which redirects to DRF UI, registration is done via admin panel. 
To customize expiring link duration, user has to add ?duration=value to the url, e.g. http://127.0.0.1:8000/links/5/?duration=500.
Admins can specify any number of arbitrary thumbnail sizes by passing a list of integers when creating account tier, e.g. [100, 300, 700].


