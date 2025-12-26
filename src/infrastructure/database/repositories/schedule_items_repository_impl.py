from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.domain.repositories.schedule_items import ScheduleItemsRepository
from src.domain.entities.schedule_items import ScheduleItems

from src.infrastructure.database.models.schedule_items import ScheduleItemsModel
from src.infrastructure.database.mappers.schedule_items_mapper import (
    ScheduleItemsMapper
)
from src.infrastructure.exceptions.infrastructure_error import (
    InfrastructureError
)

from src.common.logging.logger_main import logger

from typing import List


class ScheduleItemsRepositoryImpl(ScheduleItemsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def add(self, schedule_items: List[ScheduleItems], user_id: int) -> List[ScheduleItems]:
        try:
            orm_items = [
                ScheduleItemsMapper.to_orm(item, user_id=user_id)
                for item in schedule_items
            ]

            self.session.add_all(orm_items)
            await self.session.commit()

            for item in orm_items:
                await self.session.refresh(item)

            logger.info(f"Schedule item(s) {orm_items} were successfully created")

            return [ScheduleItemsMapper.to_domain(item) for item in orm_items]
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Integrity error while creating schedule item(s): {schedule_items}")
            raise InfrastructureError("Integrity error in database") from e

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"An unknown error occurred in add with schedule_item(s): {schedule_items}")
            raise InfrastructureError("Database error") from e
