import os
from my_django_starter.builder.base import Step

class MediaFileHandler(Step):
    def execute(self, context: dict):
        # Get project path and project name from context
        project_path = context.get('project_path')
        project_name = context.get('project_name')
        if not project_path or not project_name:
            raise ValueError("Required context data (project_path or project_name) missing!")

        # Define media directory path
        media_path = os.path.join(project_path, "media")

        # Create media directory and .gitkeep
        try:
            os.makedirs(media_path, exist_ok=True)
            with open(os.path.join(media_path, ".gitkeep"), "w") as f:
                f.write("")
        except (OSError, IOError):
            raise

        # Update settings.py to add os import, MEDIA_URL, and MEDIA_ROOT
        settings_path = os.path.join(project_path, project_name, "settings.py")
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
                # Append MEDIA settings at the end of the file
                settings_content.append("\n# Media files configuration\n")
                settings_content.append("MEDIA_URL = '/media/'\n")
                settings_content.append("MEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n")

                with open(settings_path, "w") as f:
                    f.writelines(settings_content)
        except IOError:
            raise

        # Update urls.py to serve media files in development
        urls_path = os.path.join(project_path, project_name, "urls.py")
        try:
            with open(urls_path, "r") as f:
                urls_content = f.readlines()

            # Check if media serving configuration already exists
            media_serving_exists = any("static(settings.MEDIA_URL" in line for line in urls_content)
            if not media_serving_exists:
                # Add necessary imports and media serving configuration
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
                        urls_content.append(f"    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n")
                        break

                with open(urls_path, "w") as f:
                    f.writelines(urls_content)
        except IOError:
            raise