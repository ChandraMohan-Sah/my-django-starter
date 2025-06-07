# modules/env_manager.py
import os
import subprocess
import re
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

class EnvManager(Step):
    def execute(self, context: dict):
        # Get virtual environment and project details from context
        venv_path = context.get('venv_path')
        project_path = context.get('project_path')
        project_name = context.get('project_name')
        if not venv_path or not project_path or not project_name:
            status_tag("Required context data (venv_path, project_path, or project_name) missing!", symbol="❌", color="RED")
            raise ValueError("Required context data (venv_path, project_path, or project_name) missing!")

        print()  # Spacing
        status_tag("[🔧 CONFIGURING ENVIRONMENT AND SECRET KEY...]", color="CYAN")
        print()

        # Determine pip path based on OS
        os_name = context.get('os', '').lower()
        pip_cmd = f"{venv_path}/Scripts/pip" if "windows" in os_name else f"{venv_path}/bin/pip"

        # Install python-decouple
        try:
            status_tag("[🔧 INSTALLING python-decouple...]", color="CYAN")
            print()
            subprocess.run([pip_cmd, "install", "python-decouple"], check=True)
            status_tag("python-decouple INSTALLED", symbol="✅", color="GREEN")
            print()
        except subprocess.CalledProcessError:
            status_tag("ERROR INSTALLING python-decouple", symbol="❌", color="RED")
            raise

        # Paths to settings.py and .env
        settings_path = os.path.join(project_path, project_name, "settings.py")
        env_path = os.path.join(project_path, ".env")

        # Extract SECRET_KEY from settings.py
        try:
            status_tag(f"[🔧 READING {settings_path} FOR SECRET_KEY...]", color="CYAN")
            print()
            with open(settings_path, "r") as f:
                settings_content = f.readlines()

            secret_key = None
            secret_key_line = None
            for i, line in enumerate(settings_content):
                if line.strip().startswith("SECRET_KEY"):
                    match = re.match(r"SECRET_KEY\s*=\s*['\"](.*?)['\"]", line.strip())
                    if match:
                        secret_key = match.group(1)
                        secret_key_line = i
                    break

            if secret_key is None or secret_key_line is None:
                status_tag("SECRET_KEY not found in settings.py!", symbol="❌", color="RED")
                raise ValueError("SECRET_KEY not found in settings.py!")
        except IOError:
            status_tag(f"ERROR READING {settings_path}", symbol="❌", color="RED")
            raise

        # Update settings.py to use python-decouple
        try:
            status_tag(f"[🔧 UPDATING {settings_path} WITH python-decouple...]", color="CYAN")
            print()
            settings_content[secret_key_line] = "SECRET_KEY = config('SECRET_KEY')\n"
            settings_content.insert(0, "from decouple import config\n")

            with open(settings_path, "w") as f:
                f.writelines(settings_content)
            status_tag(f"UPDATED {settings_path} WITH python-decouple", symbol="✅", color="GREEN")
            print()
        except IOError:
            status_tag(f"ERROR UPDATING {settings_path}", symbol="❌", color="RED")
            raise

        # Create .env file with SECRET_KEY
        try:
            status_tag(f"[🔧 CREATING {env_path} WITH SECRET_KEY...]", color="CYAN")
            print()
            with open(env_path, "w") as f:
                f.write(f"SECRET_KEY={secret_key}\n")
            status_tag(f"CREATED {env_path} WITH SECRET_KEY", symbol="✅", color="GREEN")
            print()
        except IOError:
            status_tag(f"ERROR CREATING {env_path}", symbol="❌", color="RED")
            raise

        # Create .gitignore file
        gitignore_path = os.path.join(project_path, ".gitignore")
        try:
            status_tag(f"[🔧 CREATING {gitignore_path}...]", color="CYAN")
            print()
            venv_name = os.path.basename(venv_path)
            gitignore_content = f"""# Virtual environment
{venv_name}/
.env

db.sqlite3

#All that developer ignores
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
# .python-version

# pipenv
#Pipfile.lock

# poetry
#poetry.lock

# pdm
#pdm.lock
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#.idea/
"""
            with open(gitignore_path, "w") as f:
                f.write(gitignore_content)
            status_tag(f"CREATED {gitignore_path}", symbol="✅", color="GREEN")
            print()
        except IOError:
            status_tag(f"ERROR CREATING {gitignore_path}", symbol="❌", color="RED")
            raise

        type_writer("[✅ ENVIRONMENT AND SECRET KEY CONFIGURED]", color="GREEN")
        print()