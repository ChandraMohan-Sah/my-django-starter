import os
import subprocess
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag

class RequirementsGenerator(Step):
    def execute(self, context: dict):
        # Get pip command and project path from context
        pip_cmd = context.get('pip_cmd')
        project_path = context.get('project_path')
        if not pip_cmd or not project_path:
            status_tag("Required context data (pip_cmd or project_path) missing!", symbol="❌", color="RED")
            raise ValueError("Required context data (pip_cmd or project_path) missing!")

        # Path to requirements.txt
        requirements_path = os.path.join(project_path, "requirements.txt")

        # Run pip freeze and save to requirements.txt
        try:
            with open(requirements_path, "w") as f:
                subprocess.run([pip_cmd, "freeze"], stdout=f, check=True)
            status_tag(f"CREATED REQUIREMENTS PATH", symbol="✅", color="GREEN")
        except (subprocess.CalledProcessError, IOError):
            status_tag("ERROR GENERATING requirements.txt", symbol="❌", color="RED")
            raise