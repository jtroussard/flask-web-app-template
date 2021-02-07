# Mail Server

Summary This section is ment to provide information regarding the setup/configuration/implementation of the mail server in this application.

## Login Credentials

### Storage

Login credentials should be saved in the `secrets.cfg` file. This file does not come with the project repository. Adminsitrator should modify the `secrets_template.cfg` file and save it as the `secrets.cfg` file. __DO NOT COMMIT THIS FILE TO THE REPOSITORY.__

### Server Configuration Considerations

Depending on the service provider choosen, account credentials used to log into the service via the web might not be acceptable for logging into the service as a third party. Here are a list of example providers and their perfered method of authentication as of this commit:

* Yahoo mail: In the account settings there is a section to generate unquie passwords for third party applications. This password should be used instead of the main account login password set when creating the account.

## Debugging

SMTP debugging console output can be turned on by uncommenting the MAIL_DEBUG variable in `flaskblog/__init__.py`

###### reference files
> secrets_template.cfg, secrets.cfg, flaskblog/__init__.py


# Database Document

Summary: This section is ment to provide information regarding the database.

## Updating Tables' Schema (sqlite)

* Update the table in the model.py file
* Install the Flask-Migrate package `pip install Flask-Migrate`
* Initialize the migration folder `flask db init` (NOTE: you might have to set the FLASK_APP variable before being able to successfully run these commands)
* Generate migrations `flask db migrate`
* On success mirgration can be review here: `migrations/versions/<migration>.py`

### Setting FLASK_APP environment variable

`~/Projects/flask_blog$ export FLASK_APP=flaskblog`