
from enum import Enum

class PayoutReason(str, Enum):
    REFERRAL = 'REFERRAL'
    ACTIVITY = 'ACTIVITY'
    OTHER = 'OTHER'


class PaymentReason(str, Enum):
    BRACELET = 'BRACELET'
    OTHER = 'OTHER'
