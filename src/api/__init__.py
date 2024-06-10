
from .endpoints.activities import router as activities_router
from .endpoints.activity_tasks import router as activity_tasks_router
from .endpoints.niches import router as niches_router
from .endpoints.leaderboard import router as leaderboard_router
from .endpoints.proofs import router as proofs_router

__all__ = [
    'activities_router',
    'activity_tasks_router',
    'niches_router',
    'leaderboard_router',
    'proofs_router',
]
