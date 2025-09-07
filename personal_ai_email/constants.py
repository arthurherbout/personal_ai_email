from enum import Enum


class EmailCategory(str, Enum):
    SPAM = "spam"
    WORK = "work"
    PERSONAL = "personal"
    PROMOTION = "promotion"
    OTHER = "other"
