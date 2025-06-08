import os
import subprocess
import re
from getpass import getpass
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

class AdminSetup(Step):

    def execute(self, context: dict):
        print()
        type_writer("[🔧 SUPERUSER SETUP - ADMIN PANEL ...]", color="CYAN")
        print()

        """Template Method: Defines the skeleton of the algorithm."""
        python_cmd, project_path = self._validate_context(context)
        username, email, password = self._collect_user_input()
        self._create_superuser(python_cmd, project_path, username, email, password)

    def _validate_context(self, context: dict) -> tuple[str, str]:
        """Validate required context data."""
        python_cmd = context.get('python_cmd')
        project_path = context.get('project_path')
        if not python_cmd or not project_path:
            status_tag("Required context data (python_cmd or project_path) missing!", symbol="❌", color="RED")
            raise ValueError("Required context data (python_cmd or project_path) missing!")
        return python_cmd, project_path

    def _collect_user_input(self) -> tuple[str, str, str]:
        """Collect and validate superuser credentials interactively."""
        # Username with default option
        while True:
            username = input("Enter superuser username [Enter for default 'admin']: ").strip()
            if not username:
                username = "admin"
                break
            if username:
                break
            status_tag("Username cannot be empty!", symbol="❌", color="RED")

        # Email with default option
        while True:
            email = input("Enter superuser email [Enter for default 'admin@example.com']: ").strip()
            if not email:
                email = "admin@example.com"
                break
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                break
            status_tag("Please enter a valid email address!", symbol="❌", color="RED")

        # Password with confirmation
        while True:
            password = getpass("Enter superuser password: ").strip()
            if not password:
                status_tag("Password cannot be empty!", symbol="❌", color="RED")
                continue
            password_confirm = getpass("Confirm superuser password: ").strip()
            if password == password_confirm:
                break
            status_tag("Passwords do not match!", symbol="❌", color="RED")

        return username, email, password

    def _create_superuser(self, python_cmd: str, project_path: str, username: str, email: str, password: str):
        """Create a Django superuser non-interactively using provided credentials."""
        manage_py = os.path.join(project_path, "manage.py")
        try:
            # Set environment variables for non-interactive createsuperuser
            env = os.environ.copy()
            env['DJANGO_SUPERUSER_USERNAME'] = username
            env['DJANGO_SUPERUSER_EMAIL'] = email
            env['DJANGO_SUPERUSER_PASSWORD'] = password

            # Run createsuperuser command
            subprocess.run(
                [python_cmd, manage_py, "createsuperuser", "--noinput"],
                env=env,
                check=True,
                cwd=project_path
            )
            print()
            status_tag(f"[✅ SUPERUSER CREATED ... ]", color="GREEN")
            print()
        except subprocess.CalledProcessError as e:
            status_tag("ERROR CREATING SUPERUSER", symbol="❌", color="RED")
            raise RuntimeError(f"Failed to create superuser: {e}")