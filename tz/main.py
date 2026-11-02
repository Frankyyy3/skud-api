from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from database import Base, engine, get_session
from schemas import PassEventCreate, PassEventRead, UserCreate, UserRead


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="СКУД — журнал проходов", lifespan=lifespan)


@app.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = await crud.create_user(session, user_data.full_name)
    return UserRead.model_validate(user)


@app.post(
    "/events/",
    response_model=PassEventRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    event_data: PassEventCreate,
    session: AsyncSession = Depends(get_session),
) -> PassEventRead:
    event = await crud.create_pass_event(
        session,
        event_data.user_id,
        event_data.direction,
    )
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {event_data.user_id} not found",
        )
    return PassEventRead.model_validate(event)


@app.get(
    "/users/{user_id}/history",
    response_model=list[PassEventRead],
)
async def get_user_history(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> list[PassEventRead]:
    events = await crud.get_user_history(session, user_id)
    if events is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return [PassEventRead.model_validate(event) for event in events]
