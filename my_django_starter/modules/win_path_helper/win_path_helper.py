import os
import sys
from pathlib import Path

def is_windows():
    return os.name == "nt"

def get_scripts_path():
    """Returns the Python Scripts path (where mydjango.exe is installed)."""
    return str(Path(sys.executable).parent / "Scripts")

def ensure_cli_works():
    """Automatically fixes PATH for Windows so 'mydjango' works."""
    if not is_windows():
        return  # Only needed on Windows
    
    scripts_path = get_scripts_path()
    if scripts_path not in os.environ["PATH"]:
        os.environ["PATH"] = f"{scripts_path}{os.pathsep}{os.environ['PATH']}"