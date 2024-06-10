
from enum import Enum

class ActivityUserEventType(str, Enum):
    JOIN = 'JOIN'
    LEAVE = 'LEAVE'


class TaskCompletionStatus(str, Enum):
    PENDING = 'PENDING'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'
