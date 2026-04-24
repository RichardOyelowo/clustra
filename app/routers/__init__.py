"""
Router module exports for the Clustra application.

This module provides convenient imports for all router classes.
"""

from .milestones import milestone_router
from .activity import activity_router
from .projects import proj_router
from .labels import label_router
from .tasks import task_router
from .teams import team_router
from .auth import auth_router
from .user import user_router
from .orgs import org_router


__all__ = [
    "milestone_router",
    "activity_router",
    "label_router",
    "task_router",
    "team_router",
    "user_router",
    "auth_router",
    "proj_router",
    "org_router"
]