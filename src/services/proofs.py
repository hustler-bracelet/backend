
from sqlalchemy.orm import selectinload

from src.repos import Repository
from src.repos.proofs import ProofsRepository
from src.database.models import TaskCompletionProof, TaskCompletionStatus, ActivityTaskCompletion

from src.api.schemas.proofs import ProofCreate

from .base import BaseDatabaseService


class ProofsService(BaseDatabaseService):
    def post_init(self):
        self._repo = ProofsRepository(self._session)
        self._task_complete_repo = Repository(ActivityTaskCompletion, self._session)

    async def create_new_proof(self, proof: ProofCreate):
        return await self._repo.create(
            TaskCompletionProof(
            telegram_id=proof.user_id,
            activity_task_id=proof.task_id,
            photo_ids=proof.photo_ids,
            caption=proof.caption
        ))

    async def get_wainting_proofs(self, activity_id: int):
        return await self._repo.get_all_by_activity(activity_id=activity_id)

    async def get_by_id(self, proof_id: int) -> TaskCompletionProof:
        return await self._repo.get_by_pk(proof_id)

    async def proof_accept(self, proof_id: int):
        proof = await self.get_by_id(proof_id)
        proof.status = TaskCompletionStatus.VERIFIED
        await self._repo.update(proof, with_commit=False)

        task = ActivityTaskCompletion(
            telegram_id=proof.telegram_id,
            activity_task_id=proof.activity_task_id,
            proof_id=proof.id,
            points=proof.task.points,
        )
        await self._task_complete_repo.create(task, with_commit=False)
        await self._session.commit()

    async def proof_decline(self, proof_id: int):
        proof = await self.get_by_id(proof_id)
        proof.status = TaskCompletionStatus.REJECTED
        await self._repo.update(proof)
