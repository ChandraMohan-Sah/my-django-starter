import os
import subprocess
import shutil
from my_django_starter.builder.base import Step

class HomePageRenderer(Step):
    def execute(self, context: dict):
        # Get python command, project path, and project name from context
        python_cmd = context.get('python_cmd')
        project_path = context.get('project_path')
        project_name = context.get('project_name')
        app_names = context.get('app_names', [])
        if not python_cmd or not project_path or not project_name:
            raise ValueError("Required context data (python_cmd, project_path, or project_name) missing!")

        # Determine manage.py path
        manage_py = os.path.join(project_path, "manage.py")

        # Create home app
        home_app_name = "home"
        try:
            subprocess.run([python_cmd, manage_py, "startapp", home_app_name], check=True)
        except subprocess.CalledProcessError:
            raise

        # Restructure home app
        app_path = os.path.join(project_path, home_app_name)
        api_path = os.path.join(app_path, f"api_of_{home_app_name}")
        templates_path = os.path.join(app_path, "templates", home_app_name)
        static_path = os.path.join(app_path, "static", home_app_name)

        # Create directories
        try:
            os.makedirs(api_path, exist_ok=True)
            os.makedirs(templates_path, exist_ok=True)
            os.makedirs(os.path.join(static_path, "images"), exist_ok=True)
            os.makedirs(os.path.join(static_path, "css"), exist_ok=True)
            os.makedirs(os.path.join(static_path, "js"), exist_ok=True)
        except OSError:
            raise

        # Create api_of_home files
        try:
            with open(os.path.join(api_path, "serializers.py"), "w") as f:
                f.write("# serializers.py\n\n")
            with open(os.path.join(api_path, "views.py"), "w") as f:
                f.write("""# views.py
from django.shortcuts import render

def home_view(request):
    return render(request, 'home/home.html')
""")
            with open(os.path.join(api_path, "urls.py"), "w") as f:
                f.write("""# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
]
""")
        except IOError:
            raise

        # Create home.html
        try:
            with open(os.path.join(templates_path, "home.html"), "w") as f:
                f.write("""{% extends 'base.html' %}
{% block title %}Django - Home Page App{% endblock %}
{% block content %}
<div class="min-h-screen bg-gradient-to-r from-green-900 via-emerald-800 to-lime-700 flex flex-col items-center justify-center text-white">
    <h1 class="text-5xl font-bold mb-4 animate-pulse">Welcome to Your Django Project!</h1>
    <p class="text-xl mb-8">Start with my-django-starter for rapid development.</p>
    <div class="space-x-4">
        {% for app in apps %}
        <a href="{% url app|add:'_home' %}" class="bg-emerald-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-emerald-500 transition">
            Visit {{ app|capfirst }}
        </a>
        {% endfor %}
    </div>
</div>
{% endblock %}
""")
        except IOError:
            raise

        # Keep only specified files and delete others
        try:
            allowed_files = {
                "__init__.py",
                "admin.py",
                "apps.py",
                "models.py",
                f"api_of_{home_app_name}",
                "templates",
                "static"
            }
            for item in os.listdir(app_path):
                item_path = os.path.join(app_path, item)
                if item not in allowed_files:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
        except (OSError, IOError):
            raise

        # Update settings.py to add home app to INSTALLED_APPS
        settings_path = os.path.join(project_path, project_name, "settings.py")
        try:
            with open(settings_path, "r") as f:
                settings_content = f.readlines()

            installed_apps_line = None
            for i, line in enumerate(settings_content):
                if line.strip().startswith("INSTALLED_APPS"):
                    installed_apps_line = i
                    break

            if installed_apps_line is None:
                raise ValueError("INSTALLED_APPS not found in settings.py!")

            for i, line in enumerate(settings_content[installed_apps_line:]):
                if ']' in line:
                    settings_content[installed_apps_line + i:installed_apps_line + i] = [f"    '{home_app_name}',\n"]
                    break

            with open(settings_path, "w") as f:
                f.writelines(settings_content)
        except IOError:
            raise

        # Update urls.py to include home app URLs
        urls_path = os.path.join(project_path, project_name, "urls.py")
        try:
            with open(urls_path, "r") as f:
                urls_content = f.readlines()

            for i, line in enumerate(urls_content):
                if line.strip().startswith("urlpatterns"):
                    for j, subline in enumerate(urls_content[i:]):
                        if "[" in subline:
                            urls_content[i + j + 1:i + j + 1] = [f"    path('', include('{home_app_name}.api_of_{home_app_name}.urls')),\n"]
                            break
                    break

            with open(urls_path, "w") as f:
                f.writelines(urls_content)
        except IOError:
            raise

        # Add app names to context for home.html
        context['apps'] = app_names