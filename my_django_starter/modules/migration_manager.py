# modules/migration_manager.py
import os
import subprocess
from builder.base import Step
from animations.terminal_fx import status_tag, type_writer

class MigrationManager(Step):
    def execute(self, context: dict):
        # Get python command and project details from context
        python_cmd = context.get('python_cmd')
        project_path = context.get('project_path')
        app_names = context.get('app_names', []) + ['home']  # Include home app
        if not python_cmd or not project_path or not app_names:
            status_tag("Required context data (python_cmd, project_path, or app_names) missing!", symbol="❌", color="RED")
            raise ValueError("Required context data (python_cmd, project_path, or app_names) missing!")

        print()  # Spacing
        type_writer("[🔧 SETTING UP DATABASE MIGRATIONS...]", color="CYAN")
        print()

        # Determine manage.py path
        manage_py = os.path.join(project_path, "manage.py")

        # Run makemigrations for all apps
        try:
            status_tag("[🔧 RUNNING python manage.py makemigrations...]", color="CYAN")
            print()
            subprocess.run([python_cmd, manage_py, "makemigrations"], check=True)
            status_tag(f"INITIAL MIGRATIONS CREATED FOR APPS: {', '.join(app_names)}", symbol="✅", color="GREEN")
            print()
        except subprocess.CalledProcessError:
            status_tag("ERROR CREATING MIGRATIONS", symbol="❌", color="RED")
            raise

        # Run migrate to apply migrations
        try:
            status_tag("[🔧 RUNNING python manage.py migrate...]", color="CYAN")
            print()
            subprocess.run([python_cmd, manage_py, "migrate"], check=True)
            status_tag("MIGRATIONS APPLIED TO DATABASE", symbol="✅", color="GREEN")
            print()
        except subprocess.CalledProcessError:
            status_tag("ERROR APPLYING MIGRATIONS", symbol="❌", color="RED")
            raise

        type_writer("[✅ DATABASE MIGRATION SETUP COMPLETED]", color="GREEN")
        print()