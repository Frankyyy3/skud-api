from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Direction, PassEvent, User


async def create_user(session: AsyncSession, full_name: str) -> User:
    user = User(full_name=full_name.strip())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_pass_event(
    session: AsyncSession,
    user_id: int,
    direction: Direction,
) -> PassEvent | None:
    user = await get_user(session, user_id)
    if user is None:
        return None

    event = PassEvent(
        user_id=user_id,
        direction=direction,
        timestamp=datetime.now(timezone.utc),
    )
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


async def get_user_history(
    session: AsyncSession,
    user_id: int,
) -> list[PassEvent] | None:
    user = await get_user(session, user_id)
    if user is None:
        return None

    result = await session.scalars(
        select(PassEvent)
        .where(PassEvent.user_id == user_id)
        .order_by(PassEvent.timestamp.desc(), PassEvent.id.desc())
    )
    return list(result.all())
