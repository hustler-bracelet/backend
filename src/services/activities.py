from datetime import datetime
import logging

from src.database.models import Activity, Niche, ActivityTask, create_int_uid

from src.repos import Repository
from src.api.schemas.activities import ActivityData, ActivityStartRequestData
from src.common.emoji import EmojiParser, EmojiName
from src.common.exceptions import InvalidNameError, InvalidDeadlineError

from .base import BaseDatabaseService
from .niches import NichesService
from .activity_tasks import ActivityTasksService


log = logging.getLogger(__name__)


class ActivitiesService(BaseDatabaseService):
    def post_init(self):
        self._repo = Repository(Activity, self._session)

    async def create_new(self, activity: ActivityData) -> Activity:
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


class ActivityEventsService(BaseDatabaseService):
    def post_init(self):
        self._activities_service = ActivitiesService(self._session)
        self._niches_service = NichesService(self._session)
        self._tasks_service = ActivityTasksService(self._session)

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

        return activity
