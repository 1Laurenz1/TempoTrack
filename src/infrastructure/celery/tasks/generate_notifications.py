from celery import shared_task

from src.infrastructure.container import get_generate_schedule_notifications_usecase

from src.common.logging.logger_main import logger

import asyncio


@shared_task(name="tasks.generate_daily_notifications")
def generate_daily_notifications():
    asyncio.run(_run())
    
    
async def _run():
    usecase = await get_generate_schedule_notifications_usecase()
        
    user_ids = await usecase.schedule_repo.get_all_users_with_main_schedule()
    
    for id in user_ids:
        await usecase.execute(id)
        logger.info(f"Generate notification for user_id: {id}")