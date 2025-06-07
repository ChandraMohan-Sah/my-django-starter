# modules/media_file_handler.py
import os
from builder.base import Step
from animations.terminal_fx import status_tag, type_writer

class MediaFileHandler(Step):
    def execute(self, context: dict):
        # Get project path and project name from context
        project_path = context.get('project_path')
        project_name = context.get('project_name')
        if not project_path or not project_name:
            status_tag("Required context data (project_path or project_name) missing!", symbol="❌", color="RED")
            raise ValueError("Required context data (project_path or project_name) missing!")

        print()  # Spacing
        type_writer("[🔧 CONFIGURING MEDIA FILE HANDLING...]", color="CYAN")
        print()

        # Define media directory path
        media_path = os.path.join(project_path, "media")

        # Create media directory and .gitkeep
        try:
            type_writer(f"[🔧 CREATING MEDIA DIRECTORY: {media_path}...]", color="CYAN")
            print()
            os.makedirs(media_path, exist_ok=True)
            with open(os.path.join(media_path, ".gitkeep"), "w") as f:
                f.write("")
            status_tag(f"CREATED MEDIA DIRECTORY: {media_path}", symbol="✅", color="GREEN")
            print()
        except (OSError, IOError):
            status_tag(f"ERROR CREATING MEDIA DIRECTORY: {media_path}", symbol="❌", color="RED")
            raise

        # Update settings.py to add os import, MEDIA_URL, and MEDIA_ROOT
        settings_path = os.path.join(project_path, project_name, "settings.py")
        try:
            type_writer(f"[🔧 UPDATING {settings_path} WITH MEDIA SETTINGS...]", color="CYAN")
            print()
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
                status_tag(f"UPDATED {settings_path} WITH MEDIA SETTINGS", symbol="✅", color="GREEN")
            else:
                status_tag(f"MEDIA SETTINGS ALREADY PRESENT IN {settings_path}", symbol="⚠️", color="YELLOW")
            print()
        except IOError:
            status_tag(f"ERROR UPDATING {settings_path}", symbol="❌", color="RED")
            raise

        # Update urls.py to serve media files in development
        urls_path = os.path.join(project_path, project_name, "urls.py")
        try:
            type_writer(f"[🔧 UPDATING {urls_path} TO SERVE MEDIA FILES...]", color="CYAN")
            print()
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
                status_tag(f"UPDATED {urls_path} TO SERVE MEDIA FILES", symbol="✅", color="GREEN")
            else:
                status_tag(f"MEDIA SERVING CONFIGURATION ALREADY PRESENT IN {urls_path}", symbol="⚠️", color="YELLOW")
            print()
        except IOError:
            status_tag(f"ERROR UPDATING {urls_path}", symbol="❌", color="RED")
            raise

        type_writer("[✅ MEDIA FILE HANDLING CONFIGURED]", color="GREEN")
        print()