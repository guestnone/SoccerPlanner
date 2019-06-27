Soccer Planner
==============
This is the "Web Application" final project that implements the manager for soccer championships. It is not the best code and it breaks the ReST standards. It was made to learn the basics of Django Framework and Python.

Installation
------------
You will need Python 3.6+ and following Python libraries installed
```
django
django-recaptcha2
python-decouple
django-mailjet
```
The `requirements.txt` file is provided. After that, use manage.py to start the website locally.
This website also contains the Visual Studio 2019 project. Load `SoccerPlanner.sln` to use it.

Mail sending
------------
This code supports sending password reset mails using the Mailjet service, but is disabled in public distribution. To enable this, uncomment the following lines in the `SoccerPlanner/SoccerPlanner/settings.py` folder.

```
EMAIL_BACKEND = 'django_mailjet.backends.MailjetBackend'
MAILJET_API_KEY = 'API_KEY'
MAILJET_API_SECRET = 'SECRET_KEY'
# same as registered on mailjet's control panel
DEFAULT_FROM_EMAIL = 'default@example.com'
```

*NOTE:* remember to comment the lines for the file-based email backend:
```
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
```

Use
---
Feel free to use for any purpose, but this code is not the best.
