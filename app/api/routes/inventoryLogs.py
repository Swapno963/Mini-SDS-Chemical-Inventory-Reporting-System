"""
o POST /chemicals/{id}/log → Create a log entry (ORM)
o GET /chemicals/{id}/logs → Read all logs for a chemical (asyncpg)
"""

from app.models.inventory import InventoryLog, InventoryLogCreate
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
import asyncpg
from app.db.postgresql import get_db, get_pool

router = APIRouter(prefix="/chemicals", tags=["chemical"])


@router.post("/{chemi_id}/log")
async def create_chemica_log(
    chemi_id: int, inventoryLog: InventoryLogCreate, db: AsyncSession = Depends(get_db)
):
    new_chem = InventoryLog(
        chemical_id=chemi_id,
        action_type=inventoryLog.action_type,
        quantity=inventoryLog.quantity,
        timestamp=inventoryLog.timestamp,
    )
    db.add(new_chem)
    await db.commit()
    await db.refresh(new_chem)
    return {
        "id": new_chem.id,
        "name": new_chem.chemical_id,
        "action_type": new_chem.action_type,
        "quantity": new_chem.quantity,
        "timestamp": new_chem.timestamp,
    }


@router.get("/{chem_id}/logs")
async def get_all_log_for_a_chemical(
    chem_id: int, conn: asyncpg.Connection = Depends(get_pool)
):
    row = await conn.fetchrow("SELECT * FROM inventory_logs WHERE id = $1", chem_id)
    if row:
        return [dict(r) for r in row]
    return {"error": "Chemical not found"}
