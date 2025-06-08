# my_django_starter/builder/pipeline.py
from .base import Step
from my_django_starter.animations.terminal_fx import status_tag, type_writer

class Pipeline:
    def __init__(self, steps: list[Step]):
        self.steps = steps

    def build_all(self, context: dict):
        """
        Execute each step in the pipeline, passing the context.
        Stop and report if any step fails.
        """
        for step in self.steps:
            try:
                step.execute(context) # Passes the same context to all steps
            except Exception as e:
                status_tag(f"Pipeline failed at {step.__class__.__name__}: {str(e)}", symbol="❌", color="RED")
                raise
 
