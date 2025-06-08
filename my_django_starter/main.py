import os
import json
from my_django_starter.modules.banner.banner import Banner
from my_django_starter.modules.os_detector.os_detector import OSDetector

from my_django_starter.modules.virtualenv_creator.virtualenv_creator import VirtualEnvCreator
from my_django_starter.modules.django_installer.django_installer import DjangoInstaller
from my_django_starter.modules.project_creator.project_creator import ProjectCreator
from my_django_starter.modules.app_creator.app_creator import AppCreator
from my_django_starter.modules.settings_modifier.settings_modifier import SettingsModifier
from my_django_starter.modules.env_manager.env_manager import EnvManager
from my_django_starter.modules.migration_manager.migration_manager import MigrationManager
from my_django_starter.modules.requirements_generator.requirements_generator import RequirementsGenerator
from my_django_starter.modules.home_page_renderer.home_page_renderer import HomePageRenderer
from my_django_starter.modules.media_file_handler.media_file_handler import MediaFileHandler
from my_django_starter.modules.create_superuser.create_superuser import  AdminSetup
from my_django_starter.modules.server_runner.server_runner import ServerRunner
 
from my_django_starter.builder.pipeline import Pipeline
from my_django_starter.modules.win_path_helper.win_path_helper import ensure_cli_works

def main():
    ensure_cli_works()  # Fixes PATH automatically (Windows only)
    
    # Initialize context with default project name and no apps
    context = {
        'project_name': 'testproject',
        'app_names': [],
    }

    # Create pipeline
    pipeline = Pipeline([
        Banner(),
        OSDetector(),
        VirtualEnvCreator(),
        DjangoInstaller(),
        ProjectCreator(),
        AppCreator(),
        SettingsModifier(),
        EnvManager(),
        RequirementsGenerator(),
        HomePageRenderer(),
        MediaFileHandler(),
        MigrationManager(),
        AdminSetup(),
        ServerRunner()
    ])

    # Execute pipeline
    pipeline.build_all(context)



if __name__ == "__main__":
    main()
