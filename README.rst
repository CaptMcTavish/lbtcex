========================================
LocalBitcoins API test and example app
========================================

:content: :local:

Setting up
===========

.. note ::

    If you are running several Django local development environments
    on your computer at the same time, you cannot run them simultaneously.

This is a web-based API testing application for LocalBitcoins.
It is based on Django and Python.

To set up::

    git clone git@github.com:LocalBitcoins/lbtcex.git
    cd lbtcex

    virtualenv-2.7 venv  # Create virtualenv
    source venv/bin/activate  # Start virtualenv
    pip install -r requirements.txt  # Install dependencies

Go to LocalBitcoins site, go to ``accounts/api/``.
Use **Create API client** to create API credentials for you.

Fill in the informarmation in the advanced options:

* Type: Public

* URL: ``http://localhost:8001/``

* Redirect URL: ``http://localhost:8001/authorize/success/``

Create a file::

    lbtcex/local_settings.py

With the following content::

    LBTC_CLIENT_ID = "xxx"  # Get from LocalBitcoins
    LBTC_CLIENT_SECRET = "yyy" # Get from LocalBitcoins
    #LBTC_URL = "http://localhost:8000"   # Proxyed, testing
    LBTC_URL = "http://localbitcoins.com"
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

Create temp database::

    python manage.py syncdb

Start the server::

    python manage.py runserver 127.0.0.1:8001

Visit at::

    http://localhost:8001/

Register a dummy user (verification email is printed to console).

Verify user by picking up the link from the email.

Login.

Press Authorize with LocalBitcoins. Now you should be taken to LocalBitcoins login,
then you grant the app permissions, and then redirected back to ``http://localhost:8001``.


Testing API calls
====================

You can perform this manual test through test client dashboard.

contact_create: Creating a buy bitcoins locally trade request
----------------------------------------------------------------

Prerequisitement: You have a ``LOCAL_SELL`` (Sell bitcoins locally for cash) advertisement running on LocalBitcoins.

Path: ``/api/contact_create/{{AD_ID}}``

Method: ``POST`

Payload::

    {"amount":100.0, message:"Test"}

Verifying the result:

* Login to LocalBitcoins as the user who is running LOCAL_SELL ad

* See that the new contact request appears in the notifications



