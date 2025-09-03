"""
o POST /chemicals/{id}/log → Create a log entry (ORM)
o GET /chemicals/{id}/logs → Read all logs for a chemical (asyncpg)
"""

from app.models.inventory import Chemical
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
import asyncpg
from app.db.postgresql import get_db, get_pool

router = APIRouter(prefix="/chemicals", tags=["chemical"])


@router.post("/chemicals/{chemi_id}/log")
async def create_chemica_log(
    name: str, cas_number: str, unit: str, db: AsyncSession = Depends(get_db)
):
    new_chem = Chemical(name=name, cas_number=cas_number, quantity=0, unit=unit)
    db.add(new_chem)
    await db.commit()
    await db.refresh(new_chem)
    return {"id": new_chem.id, "name": new_chem.name}


@router.get("/chemicals/{chem_id}/logs")
async def get_stock(conn: asyncpg.Connection = Depends(get_pool)):
    row = await conn.fetchrow("SELECT * FROM inventory_logs")
    if row:
        return [dict(r) for r in row]
    return {"error": "Chemical not found"}
