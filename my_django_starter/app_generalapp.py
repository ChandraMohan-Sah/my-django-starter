import os
from my_django_starter.modules.os_detector.os_detector import OSDetector
from my_django_starter.modules.app_creator.app_creator import AppCreator
from my_django_starter.modules.banner.banner import Banner
from my_django_starter.modules.settings_modifier.settings_modifier import SettingsModifier
from my_django_starter.builder.pipeline import Pipeline
from my_django_starter.modules.win_path_helper.win_path_helper import ensure_cli_works
from my_django_starter.animations.terminal_fx import status_tag, type_writer

def add_general_app():
    """Add a single Django app to an existing project."""
    ensure_cli_works()  # Fixes PATH automatically (Windows only)

    # Initialize context
    project_path = os.getcwd()  # Assume current directory is the project root
    context = {
        'project_path': project_path,
        'project_name': os.path.basename(project_path),  # Infer project name from directory
        'app_names': [],  # Will be populated with a single app name
        'os': '',  # Will be set by OSDetector
        'venv_path': '',  # Will be set if virtual environment is active
        'python_cmd': '',  # Will be set if virtual environment is active
        'pip_cmd': ''  # Will be set if virtual environment is active
    }

    # Check if a virtual environment is active
    venv_path = os.environ.get('VIRTUAL_ENV')
    if not venv_path:
        # Use OSDetector to set context['os'] and get OS name
        OSDetector().execute(context)
        os_name = context['os'].lower()
        activation_example = "venv\\Scripts\\activate" if os_name == 'windows' else "source venv/bin/activate"
        status_tag("No active virtual environment detected. Please activate your virtual environment and try again.", symbol="⚠️", color="YELLOW")
        print()
        type_writer(f"Example: {activation_example}", color="CYAN")
        return

    # Set virtual environment paths
    context['venv_path'] = venv_path
    context['os'] = OSDetector().execute(context) or context['os']  # Ensure os is set
    os_name = context['os'].lower()
    context['python_cmd'] = os.path.join(venv_path, "Scripts", "python.exe" if os_name == 'windows' else "bin", "python")
    context['pip_cmd'] = os.path.join(venv_path, "Scripts", "pip.exe" if os_name == 'windows' else "bin", "pip")

    # Check for manage.py to ensure we're in a Django project root
    if not os.path.isfile(os.path.join(project_path, 'manage.py')):
        status_tag("No manage.py found. Please run this command from the Django project root.", symbol="❌", color="RED")
        return

    # Create pipeline with app creation and settings modification
    pipeline = Pipeline([
        Banner(),  # Display banner
        AppCreator(),  # Create and structure the new app
        SettingsModifier()  # Update settings.py and urls.py
    ])

    # Execute pipeline
    pipeline.build_all(context)

if __name__ == "__main__":
    add_general_app()



