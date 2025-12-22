"""
Database schema management utilities.

This module provides simple helpers for:
- inspecting registered SQLAlchemy models
- creating, dropping and recreating database tables

⚠️ Intended for development, testing and local tooling.
⚠️ DO NOT use destructive methods in a production environment without explicit permission.
"""

from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.database.session import Base, engine
from src.common.logging.logger_main import logger

import asyncio
from typing import List


class ModelsInspector:
    """
    Utility class for inspecting SQLAlchemy metadata.

    Allows checking which tables are currently registered
    in Base.metadata (i.e. imported ORM models).
    """

    @staticmethod
    def table_names() -> List[str]:
        tables = list(Base.metadata.tables.keys())

        if tables:
            logger.info(f"Tables found: {tables}")
        else:
            logger.warning("No tables found")

        return tables


class TableManager:
    """
    Helper for managing database tables using SQLAlchemy metadata.

    Provides methods to:
    - create all tables
    - drop all tables (with explicit confirmation)
    - recreate all tables (with explicit confirmation)

    Uses SQLAlchemy AsyncEngine.
    """

    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def create_tables(self) -> None:
        """
        Create all tables defined in SQLAlchemy metadata.
        """
        async with self.engine.begin() as conn:
            logger.info("Creating tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created successfully!")

    async def drop_tables(self, force: bool = False) -> None:
        """
        Drop all tables defined in SQLAlchemy metadata.

        Args:
            force:
                If False (default) — operation is skipped.
                If True — ALL tables will be permanently deleted.

        ⚠️ Destructive operation. Use with caution.
        """
        if not force:
            logger.warning("Drop tables skipped: force=False")
            return

        async with self.engine.begin() as conn:
            logger.info("Dropping all tables...")
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Tables dropped successfully!")

    async def recreate_tables(self, force: bool = False) -> None:
        """
        Drop all tables and recreate them.

        Args:
            force:
                If False (default) — operation is skipped.
                If True — tables will be dropped and created again.

        ⚠️ Destructive operation. Useful for tests and local development.
        """
        if not force:
            logger.warning("Recreate tables skipped: force=False")
            return

        async with self.engine.begin() as conn:
            logger.info("Dropping all tables before creation...")
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Tables dropped successfully, creating tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created successfully!")


if __name__ == "__main__":
    # Import models to ensure they are registered in SQLAlchemy metadata
    from src.infrastructure.database.models.user import UserModel
    from src.infrastructure.database.models.schedule import ScheduleModel
    from src.infrastructure.database.models.schedule_items import ScheduleItemsModel
    from src.infrastructure.database.models.refresh_token import RefreshTokenModel

    inspector = ModelsInspector()
    inspector.table_names()

    manager = TableManager(engine)

    asyncio.run(manager.create_tables())
    # asyncio.run(manager.drop_tables(force=True))
    # asyncio.run(manager.recreate_tables(force=True))
