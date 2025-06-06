My Django Starter
A CLI tool to bootstrap Django projects with a pre-configured setup, including virtual environment, apps, media handling, and a Tailwind CSS homepage.
Installation
pip install my-django-starter

Usage
my-django-starter project_name --apps app1 app2


project_name: Name of the Django project.
--apps: List of apps to create (default: blog, shop).

Features

Creates a Django project with a virtual environment.
Configures settings, URLs, .env, and .gitignore.
Sets up a home app with a Tailwind CSS homepage.
Configures media file handling (MEDIA_URL, MEDIA_ROOT).
Applies database migrations and starts the development server.

Requirements

Python 3.8+
pip

Extending the Project

Add a simple app: pip install starter-extend-app
Add a media upload app: pip install starter-extend-media-app

