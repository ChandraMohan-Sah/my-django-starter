import os
import subprocess
import shutil
from abc import ABC, abstractmethod
from my_django_starter.builder.base import Step
from .html_content import HOME_HTML , VIEWS_CONTENT , URLS_CONTENT
from my_django_starter.animations.terminal_fx import status_tag, type_writer


# Strategy: File Creation
class FileCreationStrategy(ABC):
    @abstractmethod
    def create_file(self, path: str):
        pass


class SerializerFileStrategy(FileCreationStrategy):
    def create_file(self, path: str):
        with open(path, "w") as f:
            f.write("# serializers.py\n\n")


class ViewsFileStrategy(FileCreationStrategy):
    def create_file(self, path: str):
        with open(path, "w") as f:
            f.write(VIEWS_CONTENT)



class UrlsFileStrategy(FileCreationStrategy):
    def create_file(self, path: str):
        with open(path, "w") as f:
            f.write(URLS_CONTENT)

class HtmlFileStrategy(FileCreationStrategy):
    def create_file(self, path: str):
        with open(path, "w") as f:
            f.write(HOME_HTML)





# Strategy: Settings Update
class SettingsUpdateStrategy(ABC):
    @abstractmethod
    def update(self, settings_path: str, app_name: str):
        pass

class AddAppToSettingsStrategy(SettingsUpdateStrategy):
    def update(self, settings_path: str, app_name: str):
        with open(settings_path, "r") as f:
            settings_content = f.readlines()

        installed_apps_line = None
        for i, line in enumerate(settings_content):
            if line.strip().startswith("INSTALLED_APPS"):
                installed_apps_line = i
                break

        if installed_apps_line is None:
            raise ValueError("INSTALLED_APPS not found in settings.py!")

        for i, line in enumerate(settings_content[installed_apps_line:]):
            if ']' in line:
                settings_content[installed_apps_line + i:installed_apps_line + i] = [f"    '{app_name}',\n"]
                break

        with open(settings_path, "w") as f:
            f.writelines(settings_content)




# Strategy: URLs Update
class UrlsUpdateStrategy(ABC):
    @abstractmethod
    def update(self, urls_path: str, app_name: str):
        pass

class AddHomeUrlsStrategy(UrlsUpdateStrategy):
    def update(self, urls_path: str, app_name: str):
        with open(urls_path, "r") as f:
            urls_content = f.readlines()

        for i, line in enumerate(urls_content):
            if line.strip().startswith("urlpatterns"):
                for j, subline in enumerate(urls_content[i:]):
                    if "[" in subline:
                        urls_content[i + j + 1:i + j + 1] = [f"    path('', include('{app_name}.api_of_{app_name}.urls')),\n"]
                        break
                break

        with open(urls_path, "w") as f:
            f.writelines(urls_content)





# Main HomePageRenderer Class
class HomePageRenderer(Step):

    def _create_home_app(self, python_cmd: str, project_path: str, home_app_name: str):
        manage_py = os.path.join(project_path, "manage.py")
        try:
            subprocess.run([python_cmd, manage_py, "startapp", home_app_name], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create home app: {e}")

    def _setup_app_structure(self, project_path: str, home_app_name: str):
        app_path = os.path.join(project_path, home_app_name)
        api_path = os.path.join(app_path, f"api_of_{home_app_name}")
        templates_path = os.path.join(app_path, "templates", home_app_name)
        static_path = os.path.join(app_path, "static", home_app_name)

        try:
            os.makedirs(api_path, exist_ok=True)
            os.makedirs(templates_path, exist_ok=True)
            os.makedirs(os.path.join(static_path, "images"), exist_ok=True)
            os.makedirs(os.path.join(static_path, "css"), exist_ok=True)
            os.makedirs(os.path.join(static_path, "js"), exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create directories: {e}")

    def _create_api_files(self, project_path: str, home_app_name: str):
        api_path = os.path.join(project_path, home_app_name, f"api_of_{home_app_name}")
        try:
            for file_name, strategy in self.file_strategies.items():
                if file_name != "home.html":
                    strategy.create_file(os.path.join(api_path, file_name))
        except IOError as e:
            raise RuntimeError(f"Failed to create API files: {e}")

    def _create_templates(self, project_path: str, home_app_name: str):
        templates_path = os.path.join(project_path, home_app_name, "templates", home_app_name)
        try:
            self.file_strategies["home.html"].create_file(os.path.join(templates_path, "home.html"))
        except IOError as e:
            raise RuntimeError(f"Failed to create home.html: {e}")

    def _create_static_files(self, project_path: str, home_app_name: str):
        static_path = os.path.join(project_path, home_app_name, "static", home_app_name)
        try:
            for folder in ["images", "css", "js"]:
                open(os.path.join(static_path, folder, f".gitkeep"), "a").close()
        except IOError as e:
            raise RuntimeError(f"Failed to create static files: {e}")

    def _clean_unnecessary_files(self, project_path: str, home_app_name: str):
        app_path = os.path.join(project_path, home_app_name)
        allowed_files = {
            "__init__.py",
            "admin.py",
            "apps.py",
            "models.py",
            f"api_of_{home_app_name}",
            "templates",
            "static"
        }
        try:
            for item in os.listdir(app_path):
                item_path = os.path.join(app_path, item)
                if item not in allowed_files:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
        except (OSError, IOError) as e:
            raise RuntimeError(f"Failed to clean unnecessary files: {e}")

    def _update_settings(self, project_path: str, project_name: str, home_app_name: str):
        settings_path = os.path.join(project_path, project_name, "settings.py")
        try:
            self.settings_strategy.update(settings_path, home_app_name)
        except (IOError, ValueError) as e:
            raise RuntimeError(f"Failed to update settings.py: {e}")

    def _update_urls(self, project_path: str, project_name: str, home_app_name: str):
        urls_path = os.path.join(project_path, project_name, "urls.py")
        try:
            self.urls_strategy.update(urls_path, home_app_name)
        except IOError as e:
            raise RuntimeError(f"Failed to update urls.py: {e}")



    def __init__(self):
        self.file_strategies = {
            "serializers.py": SerializerFileStrategy(),
            "views.py": ViewsFileStrategy(),
            "urls.py": UrlsFileStrategy(),
            "home.html": HtmlFileStrategy()
        }
        self.settings_strategy = AddAppToSettingsStrategy()
        self.urls_strategy = AddHomeUrlsStrategy()



    def execute(self, context: dict):
        type_writer("[🔧 CREATING HOME PAGE ...]", color="CYAN")
        print()

        """Template Method: Defines the skeleton of the algorithm."""
        python_cmd = context.get('python_cmd')
        project_path = context.get('project_path')
        project_name = context.get('project_name')
        app_names = context.get('app_names', [])

        if not python_cmd or not project_path or not project_name:
            raise ValueError("Required context data (python_cmd, project_path, or project_name) missing!")

        home_app_name = "home"
        self._create_home_app(python_cmd, project_path, home_app_name)
        self._setup_app_structure(project_path, home_app_name)
        self._create_api_files(project_path, home_app_name)
        self._create_templates(project_path, home_app_name)
        self._create_static_files(project_path, home_app_name)
        self._clean_unnecessary_files(project_path, home_app_name)
        self._update_settings(project_path, project_name, home_app_name)
        self._update_urls(project_path, project_name, home_app_name)
        context['apps'] = app_names
