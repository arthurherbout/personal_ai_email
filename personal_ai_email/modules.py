from dspy import Module
from personal_ai_email import signatures

import dspy


class EmailClassificationModule(Module):
    def __init__(self):
        super().__init__()
        self.classifier = dspy.Predict(signatures.EmailClassifierSignature)

    def forward(self, email: dict):
        result = self.classifier(email=email)
        return result
