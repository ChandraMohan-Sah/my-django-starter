import os
import json

from modules.banner.banner import Banner
from modules.os_detector.os_detector import OSDetector
from modules.virtualenv_creator.virtualenv_creator import VirtualEnvCreator
from modules.django_installer.django_installer import DjangoInstaller
from modules.project_creator.project_creator import ProjectCreator
from modules.app_creator.app_creator import AppCreator
from modules.settings_modifier.settings_modifier import SettingsModifier
from modules.env_manager.env_manager import EnvManager
from modules.migration_manager.migration_manager import MigrationManager
from modules.requirements_generator.requirements_generator import RequirementsGenerator
from modules.home_page_renderer.home_page_renderer import HomePageRenderer
from modules.media_file_handler.media_file_handler import MediaFileHandler
from modules.server_runner.server_runner import ServerRunner

from builder.pipeline import Pipeline

def main():
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
        ServerRunner()
    ])

    # Execute pipeline
    pipeline.build_all(context)



if __name__ == "__main__":
    main()
 