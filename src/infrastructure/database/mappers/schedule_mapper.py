from src.domain.entities.schedule import Schedule
from src.infrastructure.database.models.schedule import ScheduleModel


class ScheduleMapper:
    @staticmethod
    def to_orm(schedule: Schedule) -> ScheduleModel:
        return ScheduleModel(
            id=schedule.id,
            user_id=schedule.user_id,
            name=schedule.name,
            description=schedule.description,
            type_schedule=schedule.type_schedule,
        )

    @staticmethod
    def to_domain(schedule_model: ScheduleModel) -> Schedule:
        return Schedule(
            id=schedule_model.id,
            user_id=schedule_model.user_id,
            name=schedule_model.name,
            description=schedule_model.description,
            type_schedule=schedule_model.type_schedule,
            created_at=schedule_model.created_at,
            updated_at=schedule_model.updated_at,
        )
