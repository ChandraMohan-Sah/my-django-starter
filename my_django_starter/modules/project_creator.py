import os
import subprocess
import re
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

class ProjectCreator(Step):
    def execute(self, context: dict):
        python_cmd = context.get('python_cmd')
        if not python_cmd:
            raise ValueError("❌ Python command not found in context!")

        while True:
            project_name = input("4) ROOT FOLDER NAME OF DJANGO PROJECT : ").strip()

            if not project_name:
                status_tag("ERROR: Project name cannot be empty!", symbol="❌", color="RED")
                continue

            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', project_name):
                suggested_name = re.sub(r'[^a-zA-Z0-9_]', '_', project_name).strip('_')
                status_tag(f"'{project_name}' is NOT a valid Python identifier", symbol="❌", color="RED")
                type_writer(f"[💡 SUGGESTION]: Try '{suggested_name}' or enter a new name.", color="YELLOW")
                retry = input("Use suggested name? (y/n, or press enter for new input): ").strip().lower()
                if retry == 'y' and suggested_name:
                    project_name = suggested_name
                    break
                continue
            break

        try:
            subprocess.run([python_cmd, "-m", "django", "startproject", project_name], check=True)
            status_tag(f"DJANGO PROJECT '{project_name}' CREATED", symbol="✅", color="GREEN")

            project_path = os.path.abspath(project_name)
            context['project_path'] = project_path
            context['project_name'] = project_name

            os.chdir(project_path)
            context['current_dir'] = os.getcwd()

        except subprocess.CalledProcessError:
            status_tag(f"ERROR CREATING PROJECT '{project_name}'", symbol="❌", color="RED")
            raise