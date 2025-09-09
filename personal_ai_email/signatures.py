import dspy
from dspy import Signature
from personal_ai_email.constants import EmailCategory


class EmailClassifierSignature(Signature):
    """
    Chooses one of n email categories.
    """

    email = dspy.InputField(
        type=dict, desc="Dictionary with keys: id, sender, subject, body"
    )
    classification = dspy.OutputField(
        type=EmailCategory,
        desc="Must be exactly one of: spam, work, personal, promotion, other",
    )
