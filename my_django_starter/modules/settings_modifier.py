import os
from my_django_starter.builder.base import Step

class SettingsModifier(Step):
    def execute(self, context: dict):
        # Get project and app details from context
        project_path = context.get('project_path')
        project_name = context.get('project_name')
        app_names = context.get('app_names', [])
        if not project_path or not project_name or not app_names:
            raise ValueError("Required context data (project_path, project_name, or app_names) missing!")

        # Create global static directory
        static_dir = os.path.join(project_path, "static")
        try:
            os.makedirs(static_dir, exist_ok=True)
        except OSError:
            raise

        # Create global templates directory
        templates_dir = os.path.join(project_path, "templates")
        try:
            os.makedirs(templates_dir, exist_ok=True)
        except OSError:
            raise
        
        # Create base.html with Tailwind CSS
        base_html_path = os.path.join(templates_dir, "base.html")
        try:
            with open(base_html_path, "w") as f:
                f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Django Project{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    {% block content %}
    {% endblock %}
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
""")
        except IOError:
            raise

        # Create 404.html
        not_found_html_path = os.path.join(templates_dir, "404.html")
        try:
            with open(not_found_html_path, "w") as f:
                f.write("""<!DOCTYPE html>
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
""")
        except IOError:
            raise

        # Paths to settings.py and urls.py
        settings_path = os.path.join(project_path, project_name, "settings.py")
        urls_path = os.path.join(project_path, project_name, "urls.py")

        # --- Update settings.py ---
        try:
            with open(settings_path, "r") as f:
                settings_content = f.readlines()

            # 1. Add user-specified apps to INSTALLED_APPS
            installed_apps_line = None
            for i, line in enumerate(settings_content):
                if line.strip().startswith("INSTALLED_APPS"):
                    installed_apps_line = i
                    break

            if installed_apps_line is None:
                raise ValueError("INSTALLED_APPS not found in settings.py!")

            # Insert app names before the closing bracket of INSTALLED_APPS
            app_insertions = [f"    '{app_name}',\n" for app_name in app_names]
            for i, line in enumerate(settings_content[installed_apps_line:]):
                if ']' in line:
                    settings_content[installed_apps_line + i:installed_apps_line + i] = app_insertions
                    break

            # 2. Update TEMPLATES configuration
            templates_line = None
            for i, line in enumerate(settings_content):
                if line.strip().startswith("TEMPLATES"):
                    templates_line = i
                    break

            if templates_line is None:
                raise ValueError("TEMPLATES not found in settings.py!")

            # Ensure 'DIRS' includes BASE_DIR / 'templates'
            for i, line in enumerate(settings_content[templates_line:]):
                if "'DIRS'" in line:
                    settings_content[templates_line + i] = "        'DIRS': [BASE_DIR / 'templates'],\n"
                    break
                elif ']' in line:
                    settings_content[templates_line + i:templates_line + i] = ["        'DIRS': [BASE_DIR / 'templates'],\n"]
                    break

            # 3. Add STATIC_URL and STATICFILES_DIRS
            static_settings = [
                "\n",
                "# Static files configuration\n",
                "STATIC_URL = 'static/'\n",
                "STATICFILES_DIRS = [\n",
                "    BASE_DIR / 'static',\n",
                "]\n"
            ]
            settings_content.extend(static_settings)

            # Write updated settings.py
            with open(settings_path, "w") as f:
                f.writelines(settings_content)
        except IOError:
            raise

        # --- Update urls.py ---
        try:
            with open(urls_path, "r") as f:
                urls_content = f.readlines()

            # Ensure necessary imports
            imports = [
                "from django.contrib import admin\n",
                "from django.urls import path, include\n",
                "\n"
            ]

            # Prepare URL patterns for user-specified apps
            url_patterns = [
                f"    path('{app_name}/', include('{app_name}.api_of_{app_name}.urls')),\n"
                for app_name in app_names
            ]
            url_patterns.insert(0, "    path('admin/', admin.site.urls),\n")

            # Replace or create urlpatterns
            new_urls_content = imports
            new_urls_content.append("urlpatterns = [\n")
            new_urls_content.extend(url_patterns)
            new_urls_content.append("]\n")

            # Write updated urls.py
            with open(urls_path, "w") as f:
                f.writelines(new_urls_content)
        except IOError:
            raise