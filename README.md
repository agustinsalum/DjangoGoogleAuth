# DjangoGoogleAuth
Google Login Integration in Django: A repository providing an easy and secure implementation of Google authentication in Django web applications. Leveraging the Google API to allow users to quickly and securely sign in using their Google accounts.

## Google OAuth 2.0

The following is an explanatory guide on how to obtain and configure Google authentication in your project.

### what is OAuth?

That's an open authorization service that allows websites or applications to share user information with other websites without being given a user's password. Users can sign in to multiple sites using the same account without creating other credentials.

### Get and set up sign-in with Google

We start by installing django-allauth. To do this, we add the following dependency to our requirements.txt

```
django-allauth==0.61.1
```

Next, we need to modify our project settings.py file, and I am adding the following new lines to our existing settings

```
SITE_ID = 1

INSTALLED_APPS = [
    ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #
    'allauth.socialaccount.providers.google',
]

SOCIALACCOUNT_LOGIN_ON_GET=True

AUTHENTICATION_BACKENDS = [
    ...
    'allauth.account.auth_backends.AuthenticationBackend'
    ]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
```

With the line "allauth.socialaccount.providers.google", we specify the OAuth provider since django-allauth supports many of them. You can check the list at https://docs.allauth.org/en/latest/installation/quickstart.html

We will also append django-allauth to an existing authentication backend for our application in the AUTHENTICATION_BACKEND configurations.

Finally, we enable email scope to receive users' email addresses after successful social login. Also, we need to add SITE_ID=1 and register our site on our Django admin page.

If you're creating a project from scratch, you may need additional parameters

```
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

Finally, add "allauth.account.middleware.AccountMiddleware" to the MIDDLEWARE list in settings.py

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
	@@ -42,6 +75,8 @@
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Google Oauth 2.0
    "allauth.account.middleware.AccountMiddleware",
]
```

Great, now as your intuition can tell, we will add a button in our login template, so the user can choose whether type in his login details or log in by using Google

```
<-- users/templates/users/login.html -->
{% load socialaccount %}
{% block content %}
    ...
    <button class="btn btn-outline-info">
        <a href="{% provider_login_url 'google'%}?next=/">
            <i class="fab fa-google"></i>
            Login with Google
        </a>
    </button>
    ...
{% endblock content %}
```

Now we need to navigate to the urls.py file of our project and include allauth URLs to existing ones. All OAuth operations will be performed under this route

```

from django.urls import path, include

urlpatterns = [
    path("", include("allauth.urls")), #most important
]

```

### Configuring Google APIs

You'll need to set up an OAuth application through https://console.developers.google.com/ to add Google sign-in to your application. We start by creating a new project. We need to create our OAuth client. To do this, navigate to the "Credentials" tab and click a button to "create credentials," and from the list of options choose "OAuth client ID."
We add a URI with http://127.0.0.1:8000 in the JavaScript origins tab of the Authorizer. If you're doing this for your existing domain, it should be your domain name. Additionally, we need to create an authorized redirect URI, where we input http://127.0.0.1:8000/google/login/callback/.
After completing these details, Google will provide us with the "client id" and "secret key".

### Create a social application on the Django admin page

Open the page http://127.0.0.1:8000/admin/ and log in to Django Admin. In "Social applications," create a new application. You'll be prompted to fill out the following fields:

- Provider ID: This is a unique identifier for the OAuth provider.
- Name: This is the descriptive name you assign to the social application. It can be any name that helps you identify the social application.
- Client ID: This is the OAuth client ID you obtained when registering your application in the Google Developer Console.
- Secret key: This is the OAuth client secret key you obtained when registering your application in the Google Developer Console.
- Key: This field is used to store an additional key associated with the social application. It's not necessary for basic OAuth authentication, and you can leave it blank if you don't need it.
- Settings: This field is used to store additional application-specific settings for the social application. You can use this field to provide specific settings for authentication with this social provider, such as additional scopes or custom settings. You can refer to the django-allauth documentation for more information on available settings, or you can leave it blank if you don't need it.

### sources of information

 - https://docs.allauth.org/en/latest/

## Steps to start the project


1. Clone the repository:

    ```
    git clone git@github.com:agustinsalum/DjangoGoogleAuth.git
    ```

2. Access the project folder:

    ```
    cd DjangoGoogleAuth
    ```

3. Create and activate a virtual environment named 'venv'

    ```
    pip install virtualenv
    ```
    ```
    virtualenv -p python venv
    ```
    ```
    source venv/bin/activate
    ```

4. Install the necessary dependencies:

    ```
    pip install -r requirements.txt
    ```

5. Create a file named .env next to your settings.py file

   ```
   touch .env
   ```

6. Copy the following template into your .env file and enter your personal credentials

```
SECRET_KEY=
DEBUG=true
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=localhost
DATABASE_PORT=
```

7. Perform migrations:

    ```
    python manage.py makemigrations
    ```
    ```
    python manage.py migrate
    ```

8. Run the project:

    ```
    python manage.py runserver
    ```

Remember to create the PostgreSQL database before performing the migrations.

## Contact

If you have any questions or suggestions, feel free to contact me via email.