from src.infrastructure.database.table_manager import ModelsInspector


def test_table_names_contains_models():
    tables = ModelsInspector.table_names()

    assert "users" in tables
    assert "schedules" in tables
    assert "schedule_items" in tables