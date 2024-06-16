import random

from sqlalchemy import ForeignKey, Enum, BigInteger, DateTime, Text, Sequence
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from datetime import datetime, date

from src.enums import (
    TaskCompletionStatus, 
    PayoutReason, 
    PaymentReason,
    ActivityUserEventType,
    ActivityTaskUserEventType,
    TaskCompletionStatus,
    TransactionType,
    TransactionStatus,
    NotificationType,
)


def create_int_uid() -> int:
    return int(''.join([str(random.randint(0, 9)) for _ in range(9)]))


class BaseModel(AsyncAttrs, DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = 'user'

    telegram_id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=False)
    telegram_name: Mapped[str] = mapped_column()

    current_balance: Mapped[float] = mapped_column(default=0.0)
    referred_by: Mapped[int | None] = mapped_column(ForeignKey('user.telegram_id'), nullable=True)
    is_participating_in_activity: Mapped[bool] = mapped_column(default=False)
    selected_niche_id: Mapped[int | None] = mapped_column(ForeignKey('niche.id'), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    activity_tasks: Mapped[list['ActivityTaskCompletion']] = relationship('ActivityTaskCompletion', back_populates='user')
    proofs: Mapped[list['TaskCompletionProof']] = relationship('TaskCompletionProof', back_populates='user')


class ActivityTaskCompletion(BaseModel):
    __tablename__ = 'activity_task_completions'

    id: Mapped[int] = mapped_column(primary_key=True, default=create_int_uid)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    activity_task_id: Mapped[int] = mapped_column(ForeignKey('activity_task.id'))
    proof_id: Mapped[int] = mapped_column(ForeignKey('task_completion_proof.id'))
    sent_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    points: Mapped[int]

    is_hidden: Mapped[bool] = mapped_column(default=False, server_default='false')

    activity_task = relationship('ActivityTask', back_populates='completions')
    user: Mapped['User'] = relationship('User', back_populates='activity_tasks')


class ActivityTask(BaseModel):
    __tablename__ = 'activity_task'

    id: Mapped[int] = mapped_column(primary_key=True, default=create_int_uid)
    niche_id: Mapped[int] = mapped_column(ForeignKey('niche.id'), nullable=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey('activity.id'), nullable=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    points: Mapped[int]
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_running: Mapped[bool] = mapped_column(default=True)

    niche: Mapped['Niche'] = relationship('Niche', back_populates='tasks')
    completions: Mapped[list['ActivityTaskCompletion']] = relationship('ActivityTaskCompletion', back_populates='activity_task')
    proofs: Mapped[list['TaskCompletionProof']] = relationship('TaskCompletionProof', back_populates='task')


class Activity(BaseModel):
    __tablename__ = 'activity'

    id: Mapped[int] = mapped_column(primary_key=True, default=create_int_uid)
    name: Mapped[str] = mapped_column(Text)
    emoji: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    fund: Mapped[int]
    total_places: Mapped[int]
    occupied_places: Mapped[int] = mapped_column(default=0)
    started_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now())
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_running: Mapped[bool] = mapped_column(default=False)

    niches: Mapped[list['Niche']] = relationship('Niche', back_populates='activity')


class Asset(BaseModel):
    __tablename__ = 'asset'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=create_int_uid)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    name: Mapped[str] = mapped_column(Text)
    interest_rate: Mapped[float] = mapped_column(default=0.0)
    base_amount: Mapped[float]
    current_amount: Mapped[float]


class Category(BaseModel):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=create_int_uid)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    name: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(Text)


class FinanceTransaction(BaseModel):
    __tablename__ = 'financetransaction'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=create_int_uid)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    type: Mapped[str] = mapped_column(Text)
    category: Mapped[int] = mapped_column(ForeignKey('category.id'))
    value: Mapped[float]
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    transaction_date: Mapped[date]


class InvestmentTransaction(BaseModel):
    __tablename__ = 'investmenttransaction'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=create_int_uid)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    type: Mapped[str | None] = mapped_column(Text, default=None, nullable=True)
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    asset_id: Mapped[int] = mapped_column(ForeignKey('asset.id'))
    value: Mapped[float]


class Niche(BaseModel):
    __tablename__ = 'niche'

    id: Mapped[int] = mapped_column(primary_key=True, default=create_int_uid)
    activity_id: Mapped[int] = mapped_column(ForeignKey('activity.id'))
    name: Mapped[str] = mapped_column(Text)
    emoji: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)

    activity: Mapped['Activity'] = relationship("Activity", back_populates="niches")
    tasks: Mapped[list['ActivityTask']] = relationship("ActivityTask", back_populates="niche")


class Payment(BaseModel):
    __tablename__ = 'user_payment'

    id: Mapped[int] = mapped_column(primary_key=True, default=create_int_uid)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    yookassa_payment_info: Mapped[str | None]
    payment_reason: Mapped[PaymentReason] = mapped_column(Enum(PaymentReason))
    amount_rub: Mapped[float]
    paid_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Payout(BaseModel):
    __tablename__ = 'user_payout'

    id: Mapped[int] = mapped_column(primary_key=True, default=create_int_uid)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    reason: Mapped[PayoutReason] = mapped_column(Enum(PayoutReason))
    amount_rub: Mapped[float]
    paid_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TaskCompletionProof(BaseModel):
    __tablename__ = 'task_completion_proof'

    id: Mapped[int] = mapped_column(primary_key=True, default=create_int_uid)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    status: Mapped[TaskCompletionStatus] = mapped_column(Enum(TaskCompletionStatus), default=TaskCompletionStatus.PENDING, server_default='PENDING')
    activity_task_id: Mapped[int] = mapped_column(ForeignKey('activity_task.id'))
    photo_ids: Mapped[list[int]] = mapped_column(JSONB(), default=[])
    caption: Mapped[str | None] = mapped_column(Text, default=None, nullable=True)
    sent_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    checked_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, nullable=True)

    user: Mapped['User'] = relationship("User", back_populates='proofs')
    task: Mapped['ActivityTask'] = relationship("ActivityTask", back_populates='proofs')


class Task(BaseModel):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, default=create_int_uid)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    name: Mapped[str] = mapped_column(Text)
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    planned_complete_date: Mapped[date]
    is_completed: Mapped[bool] = mapped_column(default=False)


class ActivityUserEvent(BaseModel):
    __tablename__ = "activity_user_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[ActivityUserEventType] = mapped_column(Enum(ActivityUserEventType))
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    activity_id: Mapped[int] = mapped_column(ForeignKey('activity.id'))
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ActivityTaskUserEvent(BaseModel):
    __tablename__ = "activity_task_user_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[ActivityTaskUserEventType] = mapped_column(Enum(ActivityTaskUserEventType))
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    activity_task_id: Mapped[int] = mapped_column(ForeignKey('activity_task.id'))
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BraceletTransaction(BaseModel):
    __tablename__ = "bracelet_transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus))
    amount: Mapped[float]
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, server_default=None)


class BraceletSubscription(BaseModel):
    __tablename__ = "bracelet_subscription"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    transaction_id: Mapped[int] = mapped_column(ForeignKey('bracelet_transaction.id'))
    started_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    will_end_on: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class NotificationRecords(BaseModel):
    __tablename__ = "notification_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
