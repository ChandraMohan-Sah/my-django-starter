# modules/app_creator.py
import os
import shutil
import subprocess
import re
from builder.base import Step
from animations.terminal_fx import status_tag, type_writer


class AppCreator(Step):
    def execute(self, context: dict):
        print()  # spacing

        venv_path = context.get('venv_path')
        project_path = context.get('project_path')
        if not venv_path or not project_path:
            raise ValueError("❌ Virtual environment or project path not found in context!")

        os_name = context.get('os', '').lower()
        manage_py = os.path.join(project_path, "manage.py")
        python_cmd = f"{venv_path}/Scripts/python" if "windows" in os_name else f"{venv_path}/bin/python"

        # Ask for total number of apps
        while True:
            total_apps = input("5) TOTAL APPS TO CREATE : ").strip()
            try:
                total_apps = int(total_apps)
                if total_apps <= 0:
                    raise ValueError()
                break
            except ValueError:
                status_tag("Please enter a valid positive number!", symbol="❌", color="RED")
                print()

        app_names = []
        for i in range(total_apps):
            while True:
                app_name = input(f"6) NAME OF APP{i+1}: ").strip()
                print()

                if not app_name:
                    status_tag("App name cannot be empty!", symbol="❌", color="RED")
                    print()
                    continue

                if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', app_name):
                    suggested_name = re.sub(r'[^a-zA-Z0-9_]', '_', app_name).strip('_')

                    status_tag(f"'{app_name}' is NOT a valid Python identifier", symbol="❌", color="RED")
                    print()
                    type_writer(f"[💡 SUGGESTION]: Try '{suggested_name}' or enter a new name.", color="YELLOW")

                    retry = input("Use suggested name? (y/n, or press enter for new input): ").strip().lower()
                    print()
                    if retry == 'y' and suggested_name:
                        app_name = suggested_name
                        break
                    continue

                if app_name in app_names:
                    status_tag(f"App name '{app_name}' is already used. Please choose a unique name.", symbol="❌", color="RED")
                    print()
                    continue

                break

            app_names.append(app_name)

        context['app_names'] = app_names

        for app_name in app_names:
            type_writer(f"[🔧 CREATING APP '{app_name.upper()}'...]", color="CYAN")
            print()

            try:
                subprocess.run([python_cmd, manage_py, "startapp", app_name], check=True)
                status_tag(f"APP '{app_name}' CREATED", symbol="✅", color="GREEN")
                print()

                app_path = os.path.join(project_path, app_name)
                api_path = os.path.join(app_path, f"api_of_{app_name}")
                templates_path = os.path.join(app_path, "templates", app_name)
                static_path = os.path.join(app_path, "static", app_name)

                os.makedirs(api_path, exist_ok=True)
                os.makedirs(templates_path, exist_ok=True)
                os.makedirs(os.path.join(static_path, "images"), exist_ok=True)
                os.makedirs(os.path.join(static_path, "css"), exist_ok=True)
                os.makedirs(os.path.join(static_path, "js"), exist_ok=True)

                with open(os.path.join(api_path, "serializers.py"), "w") as f:
                    f.write("# serializers.py\n\n")

                with open(os.path.join(api_path, "views.py"), "w") as f:
                    f.write(
                        f"""# views.py
from django.shortcuts import render
from django.http import HttpResponse
"""
                    )

                with open(os.path.join(api_path, "urls.py"), "w") as f:
                    f.write(
                        f"""# urls.py
from django.urls import path
from . import views

urlpatterns = [

]
"""
                    )

                allowed_files = {
                    "__init__.py",
                    "admin.py",
                    "apps.py",
                    "models.py",
                    f"api_of_{app_name}",
                    "templates",
                    "static"
                }

                for item in os.listdir(app_path):
                    if item not in allowed_files:
                        item_path = os.path.join(app_path, item)
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)

                status_tag(f"APP '{app_name}' RESTRUCTURED", symbol="✅", color="GREEN")
                print()

            except subprocess.CalledProcessError:
                status_tag(f"ERROR CREATING APP '{app_name}'", symbol="❌", color="RED")
                raise
