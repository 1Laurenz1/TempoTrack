import pytest
from sqlalchemy import text

from src.infrastructure.database.table_manager import TableManager
from src.infrastructure.database.session import Base


@pytest.mark.asyncio
async def test_create_tables(test_engine):
    manager = TableManager(test_engine)
    
    await manager.create_tables()
    
    async with test_engine.begin() as conn:
        result = await conn.execute(
            text(
                "SELECT tablename FROM pg_tables WHERE schemaname='public';"
            )
        )
        
        tables = {row[0] for row in result.fetchall()}
        
    assert "users" in tables
    assert "schedules" in tables
    assert "schedule_items" in tables
    
    
@pytest.mark.asyncio
async def test_drop_tables_without_force_does_nothing(test_engine):
    manager = TableManager(test_engine)
    
    await manager.drop_tables(force=False)
    
    async with test_engine.begin() as conn:
        result = await conn.execute(
            text(
                "SELECT tablename FROM pg_tables WHERE schemaname='public';"
            )
        )
        
        tables = {row[0] for row in result.fetchall()}

    assert "users" in tables
    assert "schedules" in tables
    assert "schedule_items" in tables
    
    
@pytest.mark.asyncio
async def test_drop_tables(test_engine):
    manager = TableManager(test_engine)
    
    await manager.drop_tables(force=True)
    
    async with test_engine.begin() as conn:
        result = await conn.execute(
            text(
                "SELECT tablename FROM pg_tables WHERE schemaname='public';"
            )
        )
        
        tables = result.fetchall()
        
    assert tables == []