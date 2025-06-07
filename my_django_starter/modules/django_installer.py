# modules/django_installer.py
import subprocess
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

class DjangoInstaller(Step):
    def execute(self, context: dict):
        print()  # spacing

        pip_cmd = context.get('pip_cmd')
        if not pip_cmd:
            raise ValueError("❌ Pip command not found in context!")

        django_version = input("3) DJANGO VERSION [PRESS ENTER FOR LATEST]: ").strip()
        django_pkg = "django" if not django_version else f"django=={django_version}"

        print()  # spacing
        type_writer(f"[🔧 INSTALLING {django_pkg.upper()}...]", color="CYAN")
        print()  # spacing

        try:
            subprocess.run([pip_cmd, "install", django_pkg], check=True)
            print("\n")
            status_tag(f"{django_pkg.upper()} INSTALLED", symbol="✅", color="GREEN")
            context['django_version'] = django_version or "latest"
        except subprocess.CalledProcessError:
            status_tag(f"ERROR INSTALLING {django_pkg}", symbol="❌", color="RED")
            raise

        print()  # final spacing
