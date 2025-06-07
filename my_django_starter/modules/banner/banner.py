# modules/banner.py
import shutil
from pyfiglet import Figlet
from my_django_starter.builder.base import Step
from abc import ABC, abstractmethod


# Strategy Interface 
class BannerStrategy(ABC):
    @abstractmethod
    def render(self, text: str) -> str:
        pass


# Concrete Strategy
class SlantBannerStrategy(BannerStrategy):
    def render(self, text: str) -> str:
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        figlet = Figlet(font="slant", width=terminal_width)
        banner = figlet.renderText(text)
        return f"\033[1;36m{banner}\033[0m"
        

# Banner Step Class : Client 
class Banner(Step):
    def __init__(self, strategy: BannerStrategy = SlantBannerStrategy()):
        self.strategy = strategy

    def execute(self, context: dict):
        text = "my-django-starter"
        banner = self.strategy.render(text)
        print(banner)


