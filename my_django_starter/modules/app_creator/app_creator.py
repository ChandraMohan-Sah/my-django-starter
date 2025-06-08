import os
import re
import shutil
import subprocess
from abc import ABC, abstractmethod
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer
from .constants import SERIALIZERS_PY_CONTENT, VIEWS_PY_CONTENT, URLS_PY_CONTENT, ALLOWED_APP_FILES


# Strategy interface
class AppCreationStrategy(ABC):
    @abstractmethod
    def perform(self, context: dict) -> None:
        pass


# Strategy: Validate inputs for app creation
class InputValidationStrategy(AppCreationStrategy):
    def perform(self, context: dict) -> None:
        total_apps = self._validate_total_apps()
        app_names = self._get_app_names(total_apps)
        context['app_names'] = app_names

    def _validate_total_apps(self) -> int:
        while True:
            total_apps = input("5) TOTAL APPS TO CREATE : ").strip()
            try:
                total_apps = int(total_apps)
                if total_apps <= 0:
                    raise ValueError()
                return total_apps
            except ValueError:
                status_tag("Please enter a valid positive number!", symbol="❌", color="RED")
                print()

    def _validate_app_name(self, app_name, existing_names):
        if not app_name:
            status_tag("App name cannot be empty!", symbol="❌", color="RED")
            print()
            return False, None

        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', app_name):
            suggested_name = re.sub(r'[^a-zA-Z0-9_]', '_', app_name).strip('_')
            status_tag(f"'{app_name}' is NOT a valid Python identifier", symbol="❌", color="RED")
            print()
            type_writer(f"[💡 SUGGESTION]: Try '{suggested_name}' or enter a new name.", color="YELLOW")
            retry = input("Use suggested name? (y/n, or press enter for new input): ").strip().lower()
            print()
            if retry == 'y' and suggested_name:
                return True, suggested_name
            return False, None

        if app_name in existing_names:
            status_tag(f"App name '{app_name}' is already used. Please choose a unique name.", symbol="❌", color="RED")
            print()
            return False, None

        return True, app_name

    def _get_app_names(self, total_apps):
        app_names = []
        for i in range(total_apps):
            print()
            while True:
                app_name = input(f"6) NAME OF APP{i+1}: ").strip()
                print()
                is_valid, validated_name = self._validate_app_name(app_name, app_names)
                if is_valid:
                    app_names.append(validated_name)
                    break
        return app_names


# Strategy: Create Django app using subprocess
class SubprocessAppCreationStrategy(AppCreationStrategy):
    def perform(self, context: dict) -> None:
        venv_path = context.get('venv_path')
        project_path = context.get('project_path')
        app_names = context.get('app_names', [])
        os_name = context.get('os', '').lower()

        if not venv_path or not project_path or not app_names:
            raise ValueError("❌ Required context missing: venv_path, project_path, or app_names!")

        manage_py = os.path.join(project_path, "manage.py")
        python_cmd = f"{venv_path}/Scripts/python" if "windows" in os_name else f"{venv_path}/bin/python"

        for app_name in app_names:
            type_writer(f"[🔧 CREATING APP '{app_name.upper()}'...]", color="CYAN")
            print()

            try:
                subprocess.run([python_cmd, manage_py, "startapp", app_name], check=True)
                status_tag(f"APP '{app_name}' CREATED", symbol="✅", color="GREEN")
                print()
            except subprocess.CalledProcessError:
                status_tag(f"ERROR CREATING APP '{app_name}'", symbol="❌", color="RED")
                raise


# Strategy: Create the app directory structure and initial files
class AppStructureCreationStrategy(AppCreationStrategy):
    def perform(self, context: dict) -> None:
        project_path = context.get('project_path')
        app_names = context.get('app_names', [])

        if not project_path or not app_names:
            raise ValueError("❌ Required context missing: project_path or app_names!")

        for app_name in app_names:
            self._create_app_structure(project_path, app_name)
            status_tag(f"APP '{app_name}' RESTRUCTURED", symbol="✅", color="GREEN")
            print()

    def _create_app_structure(self, project_path, app_name):
        app_path = os.path.join(project_path, app_name)
        api_path = os.path.join(app_path, f"api_of_{app_name}")
        templates_path = os.path.join(app_path, "templates", app_name)
        static_path = os.path.join(app_path, "static", app_name)

        # Create directories
        os.makedirs(api_path, exist_ok=True)
        os.makedirs(templates_path, exist_ok=True)
        os.makedirs(os.path.join(static_path, "images"), exist_ok=True)
        os.makedirs(os.path.join(static_path, "css"), exist_ok=True)
        os.makedirs(os.path.join(static_path, "js"), exist_ok=True)

        # Create initial files
        with open(os.path.join(api_path, "serializers.py"), "w") as f:
            f.write(SERIALIZERS_PY_CONTENT)

        with open(os.path.join(api_path, "views.py"), "w") as f:
            f.write(VIEWS_PY_CONTENT)

        with open(os.path.join(api_path, "urls.py"), "w") as f:
            f.write(URLS_PY_CONTENT)

        # Clean up unwanted files
        allowed_files = ALLOWED_APP_FILES.copy()
        allowed_files.remove("api_of_{app_name}")
        allowed_files.add(f"api_of_{app_name}")

        for item in os.listdir(app_path):
            if item not in allowed_files:
                item_path = os.path.join(app_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)


# Main class coordinating all strategies
class AppCreator(Step):
    def __init__(self):
        self.strategies = [
            InputValidationStrategy(),
            SubprocessAppCreationStrategy(),
            AppStructureCreationStrategy()
        ]

    def execute(self, context: dict):
        """Perform the full app creation process."""
        print()  # Spacing
        for strategy in self.strategies:
            strategy.perform(context)
