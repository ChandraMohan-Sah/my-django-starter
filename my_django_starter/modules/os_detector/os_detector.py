# modules/os_detector.py
import platform
from my_django_starter.builder.base import Step
from my_django_starter.animations.terminal_fx import status_tag

class OSDetector(Step):
    def execute(self, context: dict):
        os_name = platform.system()
        context['os'] = os_name
        status_tag(f"OS DETECTED: {os_name}")
