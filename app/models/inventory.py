from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, declarative_base
import enum
from typing import Optional
from pydantic import BaseModel
from app.db.postgresql import Base


# Enum for action_type
class ActionType(enum.Enum):
    ADD = "add"
    REMOVE = "remove"
    UPDATE = "update"


class Chemical(Base):
    __tablename__ = "chemicals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    display_name = Column(String(255), nullable=False, unique=True)
    display_name2 = Column(String(255), nullable=False, unique=True)
    cas_number = Column(String(50), nullable=False, unique=True)
    quantity = Column(Float, nullable=False, default=0.0)
    unit = Column(String(50), nullable=False)  # e.g., g, L, ml, kg
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationship to InventoryLog
    logs = relationship("InventoryLog", back_populates="chemical")


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    chemical_id = Column(Integer, ForeignKey("chemicals.id"), nullable=False)
    action_type = Column(Enum(ActionType), nullable=False)
    quantity = Column(Float, nullable=False)  # How much was added/removed/updated
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship back to Chemical
    chemical = relationship("Chemical", back_populates="logs")


class ChemicalUpdate(BaseModel):
    name: Optional[str]
    cas_number: Optional[str]
    quantity: Optional[float]
    unit: Optional[str]
