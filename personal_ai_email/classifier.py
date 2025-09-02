import dspy


class EmailClassifier:
    def __init__(self, llm_name: str):
        self.model = dspy.LM()
        pass
