import os
from abc import ABC, abstractmethod
from my_django_starter.builder.base import Step
from .constants import BASE_HTML_CONTENT, NOT_FOUND_HTML_CONTENT, STATIC_SETTINGS, URL_IMPORTS

# Strategy interface
class ModificationStrategy(ABC):
    @abstractmethod
    def apply(self, context: dict) -> None:
        pass
 
# ---------------------- Helper Functions ---------------------- #

def create_directory(path: str) -> None:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create directory '{path}': {e}")

def write_file(path: str, content: str) -> None:
    try:
        with open(path, "w") as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Failed to write file '{path}': {e}")

def read_lines(path: str) -> list:
    try:
        with open(path, "r") as f:
            return f.readlines()
    except IOError as e:
        raise IOError(f"Failed to read file '{path}': {e}")

def write_lines(path: str, lines: list) -> None:
    try:
        with open(path, "w") as f:
            f.writelines(lines)
    except IOError as e:
        raise IOError(f"Failed to write file '{path}': {e}")

# ---------------------- Concrete Strategies ---------------------- #

class GlobalFileCreationStrategy(ModificationStrategy):
    def apply(self, context: dict) -> None:
        project_path = context.get('project_path')
        if not project_path:
            raise ValueError("project_path missing in context!")

        static_dir = os.path.join(project_path, "static")
        templates_dir = os.path.join(project_path, "templates")

        create_directory(static_dir)
        create_directory(templates_dir)
        write_file(os.path.join(templates_dir, "base.html"), BASE_HTML_CONTENT)
        write_file(os.path.join(templates_dir, "404.html"), NOT_FOUND_HTML_CONTENT)

class SettingsUpdateStrategy(ModificationStrategy):
    def apply(self, context: dict) -> None:
        project_path = context.get('project_path')
        project_name = context.get('project_name')
        app_names = context.get('app_names', [])
        if not project_path or not project_name or not app_names:
            raise ValueError("Required context data (project_path, project_name, or app_names) missing!")

        settings_path = os.path.join(project_path, project_name, "settings.py")
        lines = read_lines(settings_path)

        # Update INSTALLED_APPS
        for i, line in enumerate(lines):
            if line.strip().startswith("INSTALLED_APPS"):
                for j in range(i, len(lines)):
                    if ']' in lines[j]:
                        insertion = [f"    '{app}',\n" for app in app_names]
                        lines[j:j] = insertion
                        break
                break

        # Update TEMPLATES['DIRS']
        for i, line in enumerate(lines):
            if line.strip().startswith("TEMPLATES"):
                for j in range(i, len(lines)):
                    if "'DIRS'" in lines[j]:
                        lines[j] = "        'DIRS': [BASE_DIR / 'templates'],\n"
                        break
                    elif ']' in lines[j]:
                        lines[j:j] = ["        'DIRS': [BASE_DIR / 'templates'],\n"]
                        break
                break

        lines.extend(STATIC_SETTINGS)
        write_lines(settings_path, lines)

class UrlsUpdateStrategy(ModificationStrategy):
    def apply(self, context: dict) -> None:
        project_path = context.get('project_path')
        project_name = context.get('project_name')
        app_names = context.get('app_names', [])
        if not project_path or not project_name or not app_names:
            raise ValueError("Required context data (project_path, project_name, or app_names) missing!")

        urls_path = os.path.join(project_path, project_name, "urls.py")
        url_patterns = ["    path('admin/', admin.site.urls),\n"]
        url_patterns += [
            f"    path('{app}/', include('{app}.api_of_{app}.urls')),\n"
            for app in app_names
        ]

        content = URL_IMPORTS.copy()
        content.append("urlpatterns = [\n")
        content.extend(url_patterns)
        content.append("]\n")

        write_lines(urls_path, content)

# ---------------------- Context Runner : Client ---------------------- #

class SettingsModifier(Step):
    def __init__(self):
        self.strategies = [
            GlobalFileCreationStrategy(),
            SettingsUpdateStrategy(),
            UrlsUpdateStrategy()
        ]

    def execute(self, context: dict):
        for strategy in self.strategies:
            strategy.apply(context)
