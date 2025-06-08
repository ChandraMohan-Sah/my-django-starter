import os
import subprocess
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

 
class RequirementsGenerator(Step):

    def _extract_context(self, context):
        pip_cmd = context.get("pip_cmd")
        project_path = context.get("project_path")
        if not pip_cmd or not project_path:
            status_tag("Required context data (pip_cmd or project_path) missing!", symbol="❌", color="RED")
            raise ValueError("Missing 'pip_cmd' or 'project_path' in context")
        return pip_cmd, project_path

    def _generate_requirements(self, pip_cmd, requirements_path):
        try:
            with open(requirements_path, "w") as f:
                subprocess.run([pip_cmd, "freeze"], stdout=f, check=True)
        except (subprocess.CalledProcessError, IOError):
            status_tag("ERROR GENERATING requirements.txt", symbol="❌", color="RED")
            raise

    def execute(self, context: dict):
        type_writer("[🔧 GENERATING REQUIREMENTS.TXT ...]", color="CYAN")
        print()
        pip_cmd, project_path = self._extract_context(context)
        requirements_path = os.path.join(project_path, "requirements.txt")
        self._generate_requirements(pip_cmd, requirements_path)