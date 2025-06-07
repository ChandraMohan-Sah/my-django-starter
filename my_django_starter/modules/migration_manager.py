import os
import subprocess
from my_django_starter.builder.base import Step

class MigrationManager(Step):
    def execute(self, context: dict):
        # Get python command and project details from context
        python_cmd = context.get('python_cmd')
        project_path = context.get('project_path')
        app_names = context.get('app_names', []) + ['home']  # Include home app
        if not python_cmd or not project_path or not app_names:
            raise ValueError("Required context data (python_cmd, project_path, or app_names) missing!")

        # Determine manage.py path
        manage_py = os.path.join(project_path, "manage.py")

        # Run makemigrations for all apps
        try:
            subprocess.run([python_cmd, manage_py, "makemigrations"], check=True)
        except subprocess.CalledProcessError:
            raise

        # Run migrate to apply migrations
        try:
            subprocess.run([python_cmd, manage_py, "migrate"], check=True)
        except subprocess.CalledProcessError:
            raise