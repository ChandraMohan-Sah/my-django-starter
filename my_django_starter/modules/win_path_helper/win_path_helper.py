import os
import sys
import ctypes
from pathlib import Path

def is_windows():
    return os.name == "nt"

def get_scripts_path():
    """Returns the Python Scripts path (where mydjango.exe is installed)."""
    return str(Path(sys.executable).parent / "Scripts")

def is_admin():
    """Check if running as admin (required for permanent PATH changes)."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_to_path_permanently(scripts_path):
    """Add directory to system PATH permanently (requires admin)."""
    import winreg
    
    # Open the environment key
    with winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        0, winreg.KEY_ALL_ACCESS
    ) as key:
        # Get current PATH
        current_path = winreg.QueryValueEx(key, "Path")[0]
        
        # Add if not already present
        if scripts_path not in current_path:
            new_path = f"{scripts_path};{current_path}"
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            
            # Broadcast the change to all processes
            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x1A, 0, "Environment", 0x02, 5000, None
            )
            return True
    return False

def ensure_cli_works():
    """Ensures mydjango works by fixing PATH (tries permanent then temporary)."""
    if not is_windows():
        return
    
    scripts_path = get_scripts_path()
    
    # First try permanent solution (requires admin)
    if is_admin():
        if add_to_path_permanently(scripts_path):
            print(f"✓ Added {scripts_path} to system PATH permanently")
            return
    
    # Fallback to temporary solution
    if scripts_path not in os.environ["PATH"]:
        os.environ["PATH"] = f"{scripts_path};{os.environ['PATH']}"
        print(f"⚠ Temporarily added {scripts_path} to PATH (restart terminal to make permanent)")