SERIALIZERS_PY_CONTENT = "# serializers.py\n\n"

VIEWS_PY_CONTENT = """# views.py
from django.shortcuts import render
from django.http import HttpResponse
"""

URLS_PY_CONTENT = """# urls.py
from django.urls import path
from . import views

urlpatterns = [

]
"""

ALLOWED_APP_FILES = {
    "__init__.py",
    "admin.py",
    "apps.py",
    "models.py",
    "api_of_{app_name}",
    "templates",
    "static"
}
