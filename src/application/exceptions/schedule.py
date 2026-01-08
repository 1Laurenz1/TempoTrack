class ScheduleNotFoundError(Exception):
    """Called when the chart is not found"""
    ...
    
    
class MainScheduleNotSetError(Exception):
    """Called if the user has not selected a main_schedule"""
    ...