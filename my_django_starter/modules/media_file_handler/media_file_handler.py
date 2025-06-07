import os
from abc import ABC, abstractmethod
from my_django_starter.builder.base import Step

# Strategy: Directory Creation
class DirectoryCreationStrategy(ABC):
    @abstractmethod
    def create_directory(self, path: str):
        pass

class MediaDirectoryStrategy(DirectoryCreationStrategy):
    def create_directory(self, path: str):
        try:
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, ".gitkeep"), "w") as f:
                f.write("")
        except (OSError, IOError) as e:
            raise RuntimeError(f"Failed to create media directory: {e}")


# Strategy: Settings Update
class SettingsUpdateStrategy(ABC):
    @abstractmethod
    def update(self, settings_path: str):
        pass

class MediaSettingsStrategy(SettingsUpdateStrategy):
    def update(self, settings_path: str):
        try:
            with open(settings_path, "r") as f:
                settings_content = f.readlines()

            # Check if os import exists
            os_import_exists = any(line.strip().startswith("import os") for line in settings_content)
            if not os_import_exists:
                settings_content.insert(0, "import os\n")

            # Check if MEDIA settings already exist
            media_settings_exist = any("MEDIA_URL" in line or "MEDIA_ROOT" in line for line in settings_content)
            if not media_settings_exist:
                settings_content.append("\n# Media files configuration\n")
                settings_content.append("MEDIA_URL = '/media/'\n")
                settings_content.append("MEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n")

            with open(settings_path, "w") as f:
                f.writelines(settings_content)
        except IOError as e:
            raise RuntimeError(f"Failed to update settings.py: {e}")


# Strategy: URLs Update
class UrlsUpdateStrategy(ABC):
    @abstractmethod
    def update(self, urls_path: str):
        pass

class MediaUrlsStrategy(UrlsUpdateStrategy):
    def update(self, urls_path: str):
        try:
            with open(urls_path, "r") as f:
                urls_content = f.readlines()

            # Check if media serving configuration already exists
            media_serving_exists = any("static(settings.MEDIA_URL" in line for line in urls_content)
            if not media_serving_exists:
                # Add necessary imports
                for i, line in enumerate(urls_content):
                    if line.strip().startswith("from django.urls"):
                        urls_content[i] = line.rstrip() + ", include\n"
                        break

                # Add static import and media serving configuration
                for i, line in enumerate(urls_content):
                    if line.strip().startswith("urlpatterns"):
                        urls_content.insert(i, "from django.conf import settings\n")
                        urls_content.insert(i + 1, "from django.conf.urls.static import static\n")
                        urls_content.append("\nif settings.DEBUG:\n")
                        urls_content.append("    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n")
                        break

                with open(urls_path, "w") as f:
                    f.writelines(urls_content)
        except IOError as e:
            raise RuntimeError(f"Failed to update urls.py: {e}")

# Main MediaFileHandler Class
class MediaFileHandler(Step):
    def __init__(self):
        self.directory_strategy = MediaDirectoryStrategy()
        self.settings_strategy = MediaSettingsStrategy()
        self.urls_strategy = MediaUrlsStrategy()

    def execute(self, context: dict):
        """Template Method: Defines the skeleton of the algorithm."""
        project_path = context.get('project_path')
        project_name = context.get('project_name')
        if not project_path or not project_name:
            raise ValueError("Required context data (project_path or project_name) missing!")

        media_path = os.path.join(project_path, "media")
        settings_path = os.path.join(project_path, project_name, "settings.py")
        urls_path = os.path.join(project_path, project_name, "urls.py")

        self._create_media_directory(media_path)
        self._update_settings(settings_path)
        self._update_urls(urls_path)

    def _create_media_directory(self, media_path: str):
        self.directory_strategy.create_directory(media_path)

    def _update_settings(self, settings_path: str):
        self.settings_strategy.update(settings_path)

    def _update_urls(self, urls_path: str):
        self.urls_strategy.update(urls_path)