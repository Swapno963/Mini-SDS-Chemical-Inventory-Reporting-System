"""
o POST /chemicals/ → Create a new chemical (ORM)
o GET /chemicals/ → Read all chemicals (ORM)
o GET /chemicals/{id} → Read chemical by id (asyncpg)
o PUT /chemicals/{id} → Update a chemical (ORM)
o DELETE /chemicals/{id} → Delete a chemical (ORM)
"""

from app.models.inventory import Chemical
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.postgresql import AsyncSessionLocal, get_asyncpg_pool
from models import Chemical, InventoryLog, ActionType
import asyncpg
from app.models.inventory import ChemicalUpdate

@app.post("/chemicals/")
async def create_chemical(name: str, cas_number: str, unit: str, db: AsyncSession = Depends(get_db)):
    new_chem = Chemical(name=name, cas_number=cas_number, quantity=0, unit=unit)
    db.add(new_chem)
    await db.commit()
    await db.refresh(new_chem)
    return {"id": new_chem.id, "name": new_chem.name}

# --- ORM Example: List chemicals ---
@app.get("/chemicals/")
async def list_chemicals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Chemical))
    chemicals = result.scalars().all()
    return chemicals



@app.get("/chemicals/{chem_id}/")
async def get_stock(chem_id: int, conn: asyncpg.Connection = Depends(get_pool)):
    row = await conn.fetchrow("SELECT * FROM chemicals WHERE id = $1", chem_id)
    if row:
        return {"quantity": row["quantity"], "unit": row["unit"]}
    return {"error": "Chemical not found"}





from fastapi import HTTPException

@app.put("/chemicals/{chem_id}")
async def update_chemical(
    chem_id: int,
    chem_update: ChemicalUpdate,
    db: AsyncSession = Depends(get_db)
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






@app.delete("/chemicals/{chem_id}")
async def delete_chemical(
    chem_id: int,
    db: AsyncSession = Depends(get_db)
):
    chem = await db.get(Chemical, chem_id)
    if not chem:
        raise HTTPException(status_code=404, detail="Chemical not found")

    await db.delete(chem)
    await db.commit()
    return {"detail": f"Chemical {chem_id} deleted successfully"}
