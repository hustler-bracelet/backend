
from enum import Enum

class TaskCompletionStatus(str, Enum):
    PENDING = 'PENDING'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'

class ActivityTaskUserEventType(str, Enum):
    JOIN = 'JOIN'
    LEAVE = 'LEAVE'
