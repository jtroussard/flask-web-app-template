# Database Document

Summary: This document is ment to provide information regarding the database.

## Updating Tables' Schema (sqlite)

* Update the table in the model.py file
* Install the Flask-Migrate package `pip install Flask-Migrate`
* Initialize the migration folder `flask db init` (NOTE: you might have to set the FLASK_APP variable before being able to successfully run these commands)
* Generate migrations `flask db migrate`
* On success mirgration can be review here: `migrations/versions/<migration>.py`

### Setting FLASK_APP environment variable

`~/Projects/flask_blog$ export FLASK_APP=flaskblog`