from db.models.sim import Sim
from dto.sim import SimCreate
from db.models.user import User
from typing import Optional, Union, Dict, Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Row, RowMapping


async def get_all_sims(db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    query = select(Sim)
    result = await db.execute(query)
    return result.scalars().all()


async def get_sim_by_id(db: AsyncSession, sim_id: int) -> Optional[Sim]:
    query = select(Sim).filter(Sim.id == sim_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_sim(db: AsyncSession, sim: SimCreate) -> Union[Sim, Dict[str, str]]:
    query = select(User).filter(User.id == sim.user_id)
    result = await db.execute(query)

    if not result.scalars().first():
        return {'error': 'User Not Found'}

    query = select(Sim).filter(Sim.number == sim.number)
    result = await db.execute(query)

    if result.scalars().first():
        return {'error': 'Number already exists'}

    new_sim = Sim(number=sim.number, user_id=sim.user_id)
    db.add(new_sim)
    await db.commit()
    await db.refresh(new_sim)
    return new_sim
