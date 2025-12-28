from src.domain.entities.schedule_items import ScheduleItems
from src.infrastructure.database.models.schedule_items import ScheduleItemsModel

class ScheduleItemsMapper:
    @staticmethod
    def to_orm(item: ScheduleItems, user_id: int) -> ScheduleItemsModel:
        """
        Converts the domain entity ScheduleItems into the ORM model ScheduleItemsModel.
        """
        return ScheduleItemsModel(
            id=item.id,
            schedule_id=item.schedule_id,
            name=item.name,
            description=item.description or "",
            day_of_week=item.day_of_week,
            time_start=item.time_start,
            time_end=item.time_end,
            user_id=user_id
        )

    @staticmethod
    def to_domain(item_model: ScheduleItemsModel, user_id: int) -> ScheduleItems:
        """
        Converts the ORM model ScheduleItemsModel into the domain entity ScheduleItems.
        """
        return ScheduleItems(
            id=item_model.id,
            user_id=user_id,
            schedule_id=item_model.schedule_id,
            name=item_model.name,
            description=item_model.description if item_model.description else None,
            day_of_week=item_model.day_of_week,
            time_start=item_model.time_start,
            time_end=item_model.time_end,
            created_at=item_model.created_at,
            updated_at=item_model.updated_at
        )
