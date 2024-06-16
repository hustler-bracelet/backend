
from enum import Enum

class PayoutReason(str, Enum):
    REFERRAL = 'REFERRAL'
    ACTIVITY = 'ACTIVITY'
    OTHER = 'OTHER'


class PaymentReason(str, Enum):
    BRACELET = 'BRACELET'
    OTHER = 'OTHER'


class TransactionType(str, Enum):
    INCOME = 'INCOME'
    OUTCOME = 'OUTCOME'


class TransactionStatus(str, Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    DECLINED = 'DECLINED'
