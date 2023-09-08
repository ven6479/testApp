from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from db.dao.sim import create_sim
from dto.sim import SimCreate

router = APIRouter()


@router.post("/createSim")
async def create_sim_handler(sim: SimCreate, db: AsyncSession = Depends(get_session)):
    response = await create_sim(db, sim)
    return response
