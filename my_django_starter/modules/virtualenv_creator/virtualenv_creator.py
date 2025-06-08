import os
import sys 
import subprocess
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer
from abc import ABC, abstractmethod 


# ---------------- Environment Creation Strategies ----------------
class EnvCreationStrategy(ABC):
    @abstractmethod
    def create_env(self, env_name: str):
        pass


class PythonVenvStrategy(EnvCreationStrategy):
    def create_env(self, env_name: str):
        try:
            subprocess.run([sys.executable, "-m", "venv", env_name], check=True)
        except subprocess.CalledProcessError:
            status_tag("ERROR CREATING VIRTUAL ENVIRONMENT WITH python3 -m venv", symbol="❌", color="RED")
            raise


class VirtualenvStrategy(EnvCreationStrategy):
    def create_env(self, env_name: str):
        try:
            subprocess.run(["virtualenv", env_name], check=True)
        except subprocess.CalledProcessError:
            status_tag("ERROR CREATING VIRTUAL ENVIRONMENT WITH virtualenv", symbol="❌", color="RED")
            raise


class FallbackEnvStrategy(EnvCreationStrategy):
    def create_env(self, env_name: str):
        try:
            PythonVenvStrategy().create_env(env_name)
        except Exception:
            status_tag("FALLING BACK TO virtualenv...", symbol="⚠️", color="YELLOW")
            VirtualenvStrategy().create_env(env_name)


# ---------------- Activation Command Strategies ----------------
class ActivationCommandStrategy(ABC):
    @abstractmethod
    def get_python_cmd(self, venv_path: str) -> str:
        pass

    @abstractmethod
    def get_pip_cmd(self, venv_path: str) -> str:
        pass


class WindowsActivationStrategy(ActivationCommandStrategy):
    def get_python_cmd(self, venv_path: str) -> str:
        return os.path.join(venv_path, "Scripts", "python.exe")

    def get_pip_cmd(self, venv_path: str) -> str:
        return os.path.join(venv_path, "Scripts", "pip.exe")


class PosixActivationStrategy(ActivationCommandStrategy):
    def get_python_cmd(self, venv_path: str) -> str:
        return os.path.join(venv_path, "bin", "python")

    def get_pip_cmd(self, venv_path: str) -> str:
        return os.path.join(venv_path, "bin", "pip")


# ---------------- Main Virtual Environment Creator ----------------
class VirtualEnvCreator(Step):
    def __init__(
        self,
        creation_strategy: EnvCreationStrategy = None,
        activation_strategy: ActivationCommandStrategy = None,
    ):
        self.creation_strategy = creation_strategy or FallbackEnvStrategy()
        self.activation_strategy = activation_strategy

    def _prompt_for_env_name(self) -> str:
        env_name = input("\n2) NAME OF YOUR VIRTUAL ENVIRONMENT: ").strip()
        if not env_name:
            raise ValueError("❌ Virtual environment name cannot be empty!")
        return env_name

    def _display_creation_banner(self):
        print()
        type_writer("[🔧 Creating virtual environment...]", color="CYAN")
        print()

    def _create_environment(self, env_name: str):
        self.creation_strategy.create_env(env_name)

    def _initialize_activation_strategy_if_needed(self, context: dict):
        if self.activation_strategy is None:
            os_name = context.get('os', '').lower()
            if "windows" in os_name:
                self.activation_strategy = WindowsActivationStrategy()
            else:
                self.activation_strategy = PosixActivationStrategy()

    def _set_env_commands(self, context: dict, venv_path: str):
        context['python_cmd'] = self.activation_strategy.get_python_cmd(venv_path)
        context['pip_cmd'] = self.activation_strategy.get_pip_cmd(venv_path)

    # Main method to execute creation
    def execute(self, context: dict):
        env_name = self._prompt_for_env_name()
        self._display_creation_banner()
        self._create_environment(env_name)

        venv_path = os.path.abspath(env_name)
        context['venv_path'] = venv_path

        self._initialize_activation_strategy_if_needed(context)
        self._set_env_commands(context, venv_path)

        status_tag(f"VIRTUAL ENV CREATED AT: {venv_path}", symbol="✅", color="GREEN")
        print()