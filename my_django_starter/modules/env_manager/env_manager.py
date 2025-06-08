import os
import subprocess
import re
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer
from .gitignore_template import GITIGNORE_TEMPLATE

class EnvManager(Step):

    def _validate_context(self):
        self.venv_path = self.context.get('venv_path')
        self.project_path = self.context.get('project_path')
        self.project_name = self.context.get('project_name')

        if not self.venv_path or not self.project_path or not self.project_name:
            raise ValueError("Missing venv_path, project_path, or project_name in context")

    def _determine_pip_path(self):
        os_name = self.context.get('os', '').lower()
        self.pip_cmd = f"{self.venv_path}/Scripts/pip" if "windows" in os_name else f"{self.venv_path}/bin/pip"

    def _install_dependencies(self):
        try:
            subprocess.run([self.pip_cmd, "install", "python-decouple"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Failed to install python-decouple") from e

    def _extract_secret_key(self):
        settings_path = os.path.join(self.project_path, self.project_name, "settings.py")
        try:
            with open(settings_path, "r") as f:
                self.settings_content = f.readlines()
        except IOError as e:
            raise RuntimeError("Unable to read settings.py") from e

        self.secret_key = None
        self.secret_key_line = None
        for i, line in enumerate(self.settings_content):
            if line.strip().startswith("SECRET_KEY"):
                match = re.match(r"SECRET_KEY\s*=\s*['\"](.*?)['\"]", line.strip())
                if match:
                    self.secret_key = match.group(1)
                    self.secret_key_line = i
                break

        if not self.secret_key:
            raise ValueError("SECRET_KEY not found in settings.py")

    def _update_settings_py(self):
        self.settings_content[self.secret_key_line] = "SECRET_KEY = config('SECRET_KEY')\n"
        if "from decouple import config\n" not in self.settings_content:
            self.settings_content.insert(0, "from decouple import config\n")

        settings_path = os.path.join(self.project_path, self.project_name, "settings.py")
        try:
            with open(settings_path, "w") as f:
                f.writelines(self.settings_content)
        except IOError as e:
            raise RuntimeError("Failed to update settings.py") from e

    def _create_env_file(self):
        env_path = os.path.join(self.project_path, ".env")
        try:
            with open(env_path, "w") as f:
                f.write(f"SECRET_KEY={self.secret_key}\n")
        except IOError as e:
            raise RuntimeError("Failed to create .env file") from e

    def _create_gitignore(self):
        gitignore_path = os.path.join(self.project_path, ".gitignore")
        venv_name = os.path.basename(self.venv_path)
        try:
            with open(gitignore_path, "w") as f:
                f.write(self._generate_gitignore_content(venv_name))
        except IOError as e:
            raise RuntimeError("Failed to create .gitignore") from e

    def _generate_gitignore_content(self, venv_name: str) -> str:
        return GITIGNORE_TEMPLATE.format(venv_name=venv_name)

    def execute(self, context: dict):
        type_writer("[🔧 MANAGING ENVIRONMENT VARIABLE ...]", color="CYAN")
        self.context = context
        self._validate_context()
        self._determine_pip_path()
        self._install_dependencies()
        self._extract_secret_key()
        self._update_settings_py()
        self._create_env_file()
        self._create_gitignore()
        