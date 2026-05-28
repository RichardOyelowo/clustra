from sqlalchemy.ext.asyncio import AsyncSession
from ..models import ActivityType, ModelType
from ..models import Activity
from uuid import UUID


async def log_activity(
    user_id: UUID,
    action: ActivityType,
    model_type: ModelType,
    model_id: UUID,
    org_id: UUID,
    db: AsyncSession
):
    activity = Activity(
        user_id=user_id,
        action=action,
        model_type=model_type,
        model_id=model_id,
        org_id=org_id,
    )
    db.add(activity)
    await db.flush()
