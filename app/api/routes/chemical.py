"""
o POST /chemicals/ → Create a new chemical (ORM)
o GET /chemicals/ → Read all chemicals (ORM)
o GET /chemicals/{id} → Read chemical by id (asyncpg)
o PUT /chemicals/{id} → Update a chemical (ORM)
o DELETE /chemicals/{id} → Delete a chemical (ORM)
"""

from app.models.inventory import Chemical
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import asyncpg
from app.models.inventory import ChemicalUpdate, ChemicalCreate
from app.db.postgresql import get_db, get_pool
from datetime import datetime


router = APIRouter(prefix="/chemicals", tags=["chemical"])


@router.post("/")
async def create_chemical(chemical: ChemicalCreate, db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()

    new_chem = Chemical(
        name=chemical.name,
        cas_number=chemical.cas_number,
        quantity=chemical.quantity,
        unit=chemical.unit,
        created_at=now,
        updated_at=now,
    )
    db.add(new_chem)
    await db.commit()
    await db.refresh(new_chem)
    return {
        "id": new_chem.id,
        "name": new_chem.name,
        "cas_number": new_chem.cas_number,
        "quantity": new_chem.quantity,
        "unit": new_chem.unit,
    }


# --- ORM Example: List chemicals ---
@router.get("/")
async def list_chemicals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Chemical))
    chemicals = result.scalars().all()
    return chemicals


@router.get("/{chem_id}")
async def get_stock(chem_id: int, conn: asyncpg.Connection = Depends(get_pool)):
    row = await conn.fetchrow("SELECT * FROM chemicals WHERE id = $1", chem_id)
    if row:
        return {
            "name": row["name"],
            "cas_number": row["cas_number"],
            "quantity": row["quantity"],
            "unit": row["unit"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
    return {"error": "Chemical not found"}


from fastapi import HTTPException


@router.put("/{chem_id}")
async def update_chemical(
    chem_id: int, chem_update: ChemicalUpdate, db: AsyncSession = Depends(get_db)
):
    # Fetch chemical
    chem = await db.get(Chemical, chem_id)
    if not chem:
        raise HTTPException(status_code=404, detail="Chemical not found")

    # Update fields if provided
    for field, value in chem_update.dict(exclude_unset=True).items():
        setattr(chem, field, value)

    await db.commit()
    await db.refresh(chem)
    return chem


@router.delete("/{chem_id}")
async def delete_chemical(chem_id: int, db: AsyncSession = Depends(get_db)):
    chem = await db.get(Chemical, chem_id)
    if not chem:
        raise HTTPException(status_code=404, detail="Chemical not found")

    await db.delete(chem)
    await db.commit()
    return {"detail": f"Chemical {chem_id} deleted successfully"}
