
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from src.services.notifications.proofs import ProofsNotificationService
from src.services.proofs import ProofsService
from src.common.bot import BOT

from src.api.schemas.proofs import ProofResponse, ProofCreate, ProofLoadedReasonse
from src.dependencies.session import get_session


router = APIRouter(
    tags=['proofs'],
)


@router.get('/activities/{activity_id}/proofs/waitlist')
async def get_waitlist(activity_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> list[ProofLoadedReasonse]:
    return await ProofsService(session).get_wainting_proofs(activity_id)


@router.get('/proofs/{proof_id}')
async def get_proof(proof_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> ProofResponse:
    return await ProofsService(session).get_by_id(proof_id)


@router.post('/proofs')
async def create_proof(proof: ProofCreate, session: Annotated[AsyncSession, Depends(get_session)]) -> ProofResponse:
    return await ProofsService(session).create_new_proof(proof)


@router.post('/proofs/{proof_id}/accept')
async def accept_proof(proof_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> ProofResponse:
    proof = await ProofsService(session).get_by_id(proof_id)

    if not proof:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await ProofsService(session).proof_accept(proof)
    await ProofsNotificationService(BOT).send_accept_notification(
        telegram_id=proof.telegram_id,
        task=proof.task,
    )

    return proof


@router.post('/proofs/{proof_id}/reject')
async def reject_proof(proof_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> ProofResponse:
    proof = await ProofsService(session).get_by_id(proof_id)

    if not proof:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await ProofsService(session).proof_decline(proof)
    await ProofsNotificationService(BOT).send_decline_notification(
        telegram_id=proof.telegram_id,
        task=proof.task,
    )

    return proof
