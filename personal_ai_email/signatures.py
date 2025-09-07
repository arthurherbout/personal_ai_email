import dspy
from dspy import Signature
from constants import EmailCategory


class EmailClassifierSignature(Signature):
    """
    Chooses one of n email categories.
    """

    email = dspy.InputField(
        type=dict, desc="Dictionary with keys: id, sender, subject, body"
    )
    classification = dspy.OutputField(type=EmailCategory)
