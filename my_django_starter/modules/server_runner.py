import os
import subprocess
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag
import json

class ServerRunner(Step):
    def execute(self, context: dict):
        # Get python command and project path from context
        python_cmd = context.get('python_cmd')
        project_path = context.get('project_path')
        if not python_cmd or not project_path:
            status_tag("Required context data (python_cmd or project_path) missing!", symbol="❌", color="RED")
            raise ValueError("Required context data (python_cmd or project_path) missing!")

        # Ensure we're in the project directory
        try:
            os.chdir(project_path)
        except OSError:
            status_tag(f"ERROR CHANGING TO PROJECT DIRECTORY: {project_path}", symbol="❌", color="RED")
            raise

        # Determine manage.py path
        manage_py = os.path.join(project_path, "manage.py")

        # Run the development server
        try:
            process = subprocess.Popen([python_cmd, manage_py, "runserver"])
            host = os.getenv('DJANGO_HOST', '127.0.0.1')
            port = os.getenv('DJANGO_PORT', '8000')
            status_tag(f"[✅ DEVELOPMENT SERVER STARTED AT http://{host}:{port}]", color="GREEN")
            status_tag("[📌 STOP THE SERVER WITH CTRL+C]", color="YELLOW")
            process.wait()
        except subprocess.CalledProcessError:
            status_tag("ERROR STARTING DEVELOPMENT SERVER", symbol="❌", color="RED")
            raise
        except KeyboardInterrupt:
            status_tag("[✅ DEVELOPMENT SERVER STOPPED]", color="GREEN")