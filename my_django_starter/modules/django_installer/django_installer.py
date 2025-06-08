# django_installer.py
import subprocess
from abc import ABC, abstractmethod
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

# === Strategy Interface ===
class InstallerStrategy(ABC):
    @abstractmethod
    def install(self, context: dict):
        pass

# === Concrete Strategy: Install via PyPI ===
class PyPIInstaller(InstallerStrategy):


    def _get_pip_cmd(self, context: dict) -> str:
        pip_cmd = context.get('pip_cmd')
        if not pip_cmd:
            raise ValueError("❌ Pip command not found in context!")
        return pip_cmd

    def _get_django_package(self) -> tuple[str, str]:
        user_input = input("3) DJANGO VERSION [PRESS ENTER FOR LATEST]: ").strip()
        if user_input == "":
            package_name = "django"
            version = "latest"
        else:
            package_name = f"django=={user_input}"
            version = user_input

        return package_name, version


    def _print_install_start(self, pkg: str):
        print()
        type_writer(f"[🔧 INSTALLING {pkg.upper()}...]", color="CYAN")
        print()

    def _run_install_command(self, pip_cmd: str, pkg: str) -> bool:
        try:
            subprocess.run([pip_cmd, "install", pkg], check=True)
            return True
        except subprocess.CalledProcessError:
            return False 

    def _print_success(self, pkg: str):
        print()
        status_tag(f"{pkg.upper()} INSTALLED", symbol="✅", color="GREEN")

    def _print_failure(self, pkg: str):
        status_tag(f"ERROR INSTALLING {pkg}", symbol="❌", color="RED")



    def install(self, context: dict):
        pip_cmd = self._get_pip_cmd(context)
        django_pkg, version = self._get_django_package()
        
        self._print_install_start(django_pkg)

        success = self._run_install_command(pip_cmd, django_pkg)

        if success:
            context['django_version'] = version
            self._print_success(django_pkg)
        else:
            self._print_failure(django_pkg)
            raise RuntimeError(f"Installation failed for package: {django_pkg}")


# === Context Class ===
class DjangoInstaller(Step):
    def __init__(self):
        self.strategy = PyPIInstaller()  # Default strategy

    def execute(self, context: dict):
        print()
        self.strategy.install(context)
        print()
