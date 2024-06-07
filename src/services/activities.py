from datetime import datetime
import logging

from src.database.models import Activity, Niche, User

from sqlalchemy.orm import selectinload

from src.repos import Repository
from src.api.schemas.activities import ActivityDataCreate, ActivityStartRequestData, ActivitySummaryResponse, UserNicheResponse, ActivityTaskDataResponse
from src.common.emoji import EmojiParser, EmojiName
from src.common.exceptions import InvalidNameError, InvalidDeadlineError, CurrentActivityError
from src.jobs.activity_notifications import send_start_activity_notification
from src.services.activity_leaderboard import ActivityLeaderboardService

from .base import BaseDatabaseService
from .niches import NichesService
from .activity_tasks import ActivityTasksService


log = logging.getLogger(__name__)


class ActivitiesService(BaseDatabaseService):
    def post_init(self):
        self._repo = Repository(Activity, self._session)

    async def create_new(self, activity: ActivityDataCreate) -> Activity:
        """
        Create new activity

        :param activity: activity data
        :return: created activity
        """

        emoji_parser = EmojiParser(activity.name)

        if not emoji_parser.contains_emoji:
            raise InvalidNameError(f'Invalid activity name: {activity.emoji} - must contain emoji')

        parsed_name: EmojiName = emoji_parser.parse()

        model = Activity(
            **activity.model_dump(exclude=['name']),
            **parsed_name.model_dump(),
        )

        return await self._repo.create(model)

    async def get_current(self) -> Activity | None:
        """Получить текущую активность"""
        return (await self._repo.filter_by(
            is_running=True,
            options=[
                selectinload(Activity.niches).options(selectinload(Niche.tasks))
            ]
        )).first()

    async def filter(self, is_active: bool = False) -> list[Activity]:
        """Получить все активности"""
        return (await self._repo.filter_by(
                is_running=is_active,
                order_by=[
                    Activity.started_on.desc(),
                ],
                options=[
                    selectinload(Activity.niches).options(selectinload(Niche.tasks))
                ]
            )
        ).all()

    async def get_by_id(self, activity_id: int) -> Activity | None:
        """Получить активность по id"""
        return await self._repo.get_by_pk(activity_id)


class ActivityEventsService(BaseDatabaseService):
    def post_init(self):
        self._repo = Repository(Activity, self._session)

        self._activities_service = ActivitiesService(self._session)
        self._niches_service = NichesService(self._session)
        self._tasks_service = ActivityTasksService(self._session)
        self._leaderboard_service = ActivityLeaderboardService(self._session)

    def validate_deadlines(self, activity_deadline: datetime, task_deadline: datetime) -> bool:
        return task_deadline < activity_deadline

    async def create_event(self, request: ActivityStartRequestData) -> Activity:
        """
        Start activity

        :param request: activity start request data
        :return: started activity
        """
        log.info(f'Starting activity -- {request.activity.name}')

        # NOTE: создаем основную активность
        activity = await self._activities_service.create_new(request.activity)

        # NOTE: создаем ниши для активности
        for niche in request.niches:
            niche_db = await self._niches_service.create_new(niche, activity)

            task = niche.task

            # NOTE: проверяем что дедлайн задачи меньше дедлайна активности
            if not self.validate_deadlines(activity.deadline, task.deadline):
                err_text = f'Invalid deadline for task {task.name}: {task.deadline} > {activity.deadline}'
                log.error(err_text)
                raise InvalidDeadlineError(err_text)

            await self._tasks_service.create_new(task, niche_db)

        log.info(f'Activity started -- id={activity.id}, name={activity.name}')

        # NOTE: запускаем джобу оповещение 
        send_start_activity_notification.send(activity.id)

        return activity

    async def stop_event(self, activity_id: int) -> Activity:
        """
        Stop activity

        :param activity_id: activity id
        :return: stopped activity
        """
        activity = await self._repo.get_by_pk(activity_id)

        if not activity:
            raise CurrentActivityError(f'Activity {activity_id} not found')

        if not activity.is_running:
            raise CurrentActivityError(f'Activity {activity_id} is not running')

        log.info(f'Stopping activity -- id={activity.id}, name={activity.name}')

        activity.is_running = False
        await self._repo.update(activity)

        log.info(f'Activity stopped -- id={activity.id}, name={activity.name}')

        # TODO: добавить notification

        return activity

    async def get_user_event_summary(self, user: User, activity_id: int) -> ActivitySummaryResponse:
        activity: Activity = await self._repo.get_by_pk(activity_id)

        if not activity:
            raise CurrentActivityError(f'Activity {activity_id} not found')

        leaderboard = await self._leaderboard_service.get_leaderboard_item_by_user(user, activity)
        niche = await self._niches_service.get_selected_niche(user.telegram_id)

        if not niche:
            raise CurrentActivityError(f'Niche for user {user.id} not found')

        current_task = None
        for task in niche.tasks:
            if task.is_running:
                current_task = task
                break

        if not current_task:
            raise CurrentActivityError(f'Current task for niche {niche.id} not found')

        return ActivitySummaryResponse(
            id=activity.id,
            emoji=activity.emoji,
            name=activity.name,
            description=activity.description,
            fund=activity.fund,
            total_places=activity.total_places,
            started_on=activity.started_on,
            deadline=activity.deadline,
            leaderboard_data=leaderboard,
            niche=UserNicheResponse(
                id=niche.id,
                emoji=niche.emoji,
                name=niche.name,
                description=niche.description,
                task=ActivityTaskDataResponse(
                    id=current_task.id,
                    name=current_task.name,
                    description=current_task.description,
                    points=current_task.points,
                    added_on=current_task.added_on,
                    deadline=current_task.deadline,
                ),
            )
        )
