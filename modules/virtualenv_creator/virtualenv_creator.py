from abc import ABC, abstractmethod
import os
import subprocess
from builder.base import Step
from animations.terminal_fx import status_tag, type_writer

# Strategy for environment creation
class EnvCreationStrategy(ABC):
    @abstractmethod
    def create_env(self, env_name: str):
        pass

class PythonVenvStrategy(EnvCreationStrategy):
    def create_env(self, env_name: str):
        try:
            subprocess.run(["python3", "-m", "venv", env_name], check=True)
        except subprocess.CalledProcessError:
            status_tag("ERROR CREATING VIRTUAL ENVIRONMENT", symbol="❌", color="RED")
            raise

class VirtualenvStrategy(EnvCreationStrategy):
    def create_env(self, env_name: str):
        try:
            subprocess.run(["virtualenv", env_name], check=True)
        except subprocess.CalledProcessError:
            status_tag("ERROR CREATING VIRTUAL ENVIRONMENT WITH virtualenv", symbol="❌", color="RED")
            raise




# Strategy for command setup
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




# Main VirtualEnvCreator with composition of multiple strategies
class VirtualEnvCreator(Step):
    def __init__(
        self,
        creation_strategy: EnvCreationStrategy = None,
        activation_strategy: ActivationCommandStrategy = None,
    ):
        self.creation_strategy = creation_strategy or PythonVenvStrategy()
        self.activation_strategy = activation_strategy

    def execute(self, context: dict):
        env_name = input("\n2) NAME OF YOUR VIRTUAL ENVIRONMENT: ").strip()
        if not env_name:
            raise ValueError("❌ Virtual environment name cannot be empty!")

        print()
        type_writer("[🔧 Creating virtual environment...]", color="CYAN")
        print()

        # Create virtual environment using chosen strategy
        self.creation_strategy.create_env(env_name)

        venv_path = os.path.abspath(env_name)
        context['venv_path'] = venv_path

        # Choose activation strategy based on OS if not given
        if not self.activation_strategy:
            os_name = context.get('os', '').lower()
            if "windows" in os_name:
                self.activation_strategy = WindowsActivationStrategy()
            else:
                self.activation_strategy = PosixActivationStrategy()

        # Set python and pip command paths using activation strategy
        context['python_cmd'] = self.activation_strategy.get_python_cmd(venv_path)
        context['pip_cmd'] = self.activation_strategy.get_pip_cmd(venv_path)

        status_tag(f"VIRTUAL ENV CREATED AT: {venv_path}", symbol="✅", color="GREEN")
        print()
