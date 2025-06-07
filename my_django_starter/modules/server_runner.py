# modules/server_runner.py
import os
import subprocess
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

class ServerRunner(Step):
    def execute(self, context: dict):
        # Get python command and project path from context
        python_cmd = context.get('python_cmd')
        project_path = context.get('project_path')
        if not python_cmd or not project_path:
            status_tag("Required context data (python_cmd or project_path) missing!", symbol="❌", color="RED")
            raise ValueError("Required context data (python_cmd or project_path) missing!")

        print()  # Spacing
        type_writer("[🔧 STARTING DJANGO DEVELOPMENT SERVER...]", color="CYAN")
        print()

        # Ensure we're in the project directory
        try:
            status_tag(f"[🔧 CHANGING TO PROJECT DIRECTORY: {project_path}...]", color="CYAN")
            print()
            os.chdir(project_path)
            status_tag(f"CHANGED TO PROJECT DIRECTORY: {project_path}", symbol="✅", color="GREEN")
            print()
        except OSError:
            status_tag(f"ERROR CHANGING TO PROJECT DIRECTORY: {project_path}", symbol="❌", color="RED")
            raise

        # Determine manage.py path
        manage_py = os.path.join(project_path, "manage.py")

        # Run the development server
        try:
            status_tag(f"[🔧 RUNNING {python_cmd} {manage_py} runserver...]", color="CYAN")
            print()
            # Use Popen to run the server non-blocking, allowing user interaction
            process = subprocess.Popen([python_cmd, manage_py, "runserver"])

            host = os.getenv('DJANGO_HOST', '127.0.0.1')
            port = os.getenv('DJANGO_PORT', '8000')
            status_tag("[✅ DEVELOPMENT SERVER STARTED AT http://{host}:{port}]", color="GREEN")
            print()
            status_tag("[📌 STOP THE SERVER WITH CTRL+C]", color="YELLOW")
            print()

            # Wait for the process to complete (e.g., when user stops the server)
            process.wait()
        except subprocess.CalledProcessError:
            status_tag("ERROR STARTING DEVELOPMENT SERVER", symbol="❌", color="RED")
            raise
        except KeyboardInterrupt:
            status_tag("[✅ DEVELOPMENT SERVER STOPPED]", color="GREEN")
            print()


