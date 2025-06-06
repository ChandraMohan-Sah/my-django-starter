class Step:
    def execute(self):
        pass

class StepA(Step):
    def execute(self):
        print("Step A")

class StepB(Step):
    def execute(self):
        print("Step B")

class Pipeline:
    def __init__(self, steps: list):
        self.steps = steps  # store the list of steps


pipeline = Pipeline([StepA(), StepB()])
print(pipeline.steps)  # This will print a list of Step objects


