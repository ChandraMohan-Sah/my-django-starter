import os
import subprocess
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer


class MigrationManager(Step):

    def _run_makemigrations(self, python_cmd, manage_py, app_names):
        type_writer("[🔧 DATABASE SETUP  ...]", color="CYAN")
        print()
        type_writer("[🔧 MAKEMIGRATIONS  ...]", color="CYAN")
        print()
        try:
            subprocess.run([python_cmd, manage_py, "makemigrations"] + app_names, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("makemigrations failed") from e

    def _run_migrate(self, python_cmd, manage_py):
        type_writer("[🔧 MIGRATE  ...]", color="CYAN")
        print()
        try:
            subprocess.run([python_cmd, manage_py, "migrate"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("migrate failed") from e

    def execute(self, context: dict):
        python_cmd = context.get("python_cmd")
        project_path = context.get("project_path")
        app_names = context.get("app_names", []) + ["home"]

        if not python_cmd or not project_path:
            raise ValueError("Missing 'python_cmd' or 'project_path' in context")

        manage_py = os.path.join(project_path, "manage.py")

        self._run_makemigrations(python_cmd, manage_py, app_names)
        self._run_migrate(python_cmd, manage_py)
        