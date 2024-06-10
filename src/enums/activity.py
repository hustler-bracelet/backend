
from enum import StrEnum

class ActivityUserEventType(StrEnum):
    JOIN = 'JOIN'
    LEAVE = 'LEAVE'


class TaskCompletionStatus(StrEnum):
    PENDING = 'PENDING'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'
