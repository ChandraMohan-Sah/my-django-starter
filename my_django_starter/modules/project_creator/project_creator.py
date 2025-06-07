import os
import subprocess
import re
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

class ProjectCreator(Step):

    def is_valid_identifier(self, name: str) -> bool:
        return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))

    def suggest_name(self, name: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_]', '_', name).strip('_')

    def get_valid_project_name(self) -> str:
        while True:
            project_name = input("4) ROOT FOLDER NAME OF DJANGO PROJECT : ").strip()

            if not project_name:
                status_tag("ERROR: Project name cannot be empty!", symbol="❌", color="RED")
                continue

            if self.is_valid_identifier(project_name):
                return project_name

            suggested_name = self.suggest_name(project_name)
            status_tag(f"'{project_name}' is NOT a valid Python identifier", symbol="❌", color="RED")
            type_writer(f"[💡 SUGGESTION]: Try '{suggested_name}' or enter a new name.", color="YELLOW")

            retry = input("Use suggested name? (y/n, or press enter for new input): ").strip().lower()
            if retry == 'y' and suggested_name:
                return suggested_name 

    def create_django_project(self, python_cmd: str, project_name: str, context: dict): 
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


    def execute(self, context: dict):
        python_cmd = context.get('python_cmd')
        if not python_cmd:
            raise ValueError("❌ Python command not found in context!")

        project_name = self.get_valid_project_name()
        self.create_django_project(python_cmd, project_name, context)