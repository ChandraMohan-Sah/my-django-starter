# modules/requirements_generator.py
import os
import subprocess
from builder.base import Step
from animations.terminal_fx import status_tag, type_writer

class RequirementsGenerator(Step):
    def execute(self, context: dict):
        # Get pip command and project path from context
        pip_cmd = context.get('pip_cmd')
        project_path = context.get('project_path')
        if not pip_cmd or not project_path:
            status_tag("Required context data (pip_cmd or project_path) missing!", symbol="❌", color="RED")
            raise ValueError("Required context data (pip_cmd or project_path) missing!")

        print()  # Spacing
        type_writer("[🔧 GENERATING requirements.txt...]", color="CYAN")
        print()

        # Path to requirements.txt
        requirements_path = os.path.join(project_path, "requirements.txt")

        # Run pip freeze and save to requirements.txt
        try:
            status_tag(f"[🔧 CREATING {requirements_path}...]", color="CYAN")
            print()
            with open(requirements_path, "w") as f:
                subprocess.run([pip_cmd, "freeze"], stdout=f, check=True)
            status_tag(f"CREATED {requirements_path}", symbol="✅", color="GREEN")
            print()
        except (subprocess.CalledProcessError, IOError):
            status_tag("ERROR GENERATING requirements.txt", symbol="❌", color="RED")
            raise

        status_tag("[✅ REQUIREMENTS FILE GENERATED]", color="GREEN")
        print()