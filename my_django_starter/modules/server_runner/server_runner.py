import os
import subprocess
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

class ServerRunner(Step):
    def execute(self, context: dict):
        """Template Method: Defines the skeleton of the algorithm."""
        python_cmd, project_path = self._validate_context(context)
        self._change_directory(project_path)
        self._run_server(python_cmd, project_path)

    def _validate_context(self, context: dict) -> tuple[str, str]:
        """Validate required context data."""
        python_cmd = context.get('python_cmd')
        project_path = context.get('project_path')
        if not python_cmd or not project_path:
            status_tag("Required context data (python_cmd or project_path) missing!", symbol="❌", color="RED")
            raise ValueError("Required context data (python_cmd or project_path) missing!")
        return python_cmd, project_path

    def _change_directory(self, project_path: str):
        """Change to the project directory."""
        try:
            os.chdir(project_path)
        except OSError as e:
            status_tag(f"ERROR CHANGING TO PROJECT DIRECTORY: {project_path}", symbol="❌", color="RED")
            raise RuntimeError(f"Failed to change directory: {e}")

    def _run_server(self, python_cmd: str, project_path: str):
        """Run the Django development server."""
        manage_py = os.path.join(project_path, "manage.py")
        try:
            process = subprocess.Popen([python_cmd, manage_py, "runserver"])
            host = os.getenv('DJANGO_HOST', '127.0.0.1')
            port = os.getenv('DJANGO_PORT', '8000')

            status_tag(f"[✅ DEVELOPMENT SERVER STARTED AT http://{host}:{port}]", color="GREEN")
            print()
            status_tag("[📌 STOP THE SERVER WITH CTRL+C]", color="YELLOW")
            print()
            process.wait()
        except subprocess.CalledProcessError as e:
            status_tag("ERROR STARTING DEVELOPMENT SERVER", symbol="❌", color="RED")
            raise RuntimeError(f"Failed to start development server: {e}")
        except KeyboardInterrupt:
            status_tag("[✅ DEVELOPMENT SERVER STOPPED]", color="GREEN")