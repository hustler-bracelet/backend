
from enum import Enum

class CompletionStatus(str, Enum):
    PENDING = 'PENDING'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'