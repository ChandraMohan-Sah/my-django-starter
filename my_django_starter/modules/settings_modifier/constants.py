# HTML content for template files
BASE_HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Django Project{% endblock %}</title>
    <link rel="icon" type="image/svg+xml" href="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg">
    <script src="https://cdn.tailwindcss.com"></script>
    {% load static %}
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
"""




NOT_FOUND_HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Page Not Found</title>
    <script src="https://cdn.tailwindcss.com"></script>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body class="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
    <h1 class="text-5xl font-bold text-red-600 mb-4">404 - Page Not Found</h1>
    <p class="text-xl text-gray-700 mb-8">Sorry, the page you are looking for does not exist.</p>
    <a href="{% url 'home' %}" class="bg-blue-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-blue-700 transition">Return to Home</a>
</body>
</html>
"""

# Static files configuration for settings.py
STATIC_SETTINGS = [
    "\n",
    "# Static files configuration\n",
    "STATIC_URL = 'static/'\n",
    "STATICFILES_DIRS = [\n",
    "    BASE_DIR / 'static',\n",
    "]\n"
]

# URL imports for urls.py
URL_IMPORTS = [
    "from django.contrib import admin\n",
    "from django.urls import path, include\n",
    "\n"
]