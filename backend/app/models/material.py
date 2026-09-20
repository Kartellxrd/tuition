import enum, uuid
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
class MaterialCategory(str, enum.Enum):
    LECTURE_NOTES="LECTURE_NOTES"; TUTORIAL="TUTORIAL"; REVISION="REVISION"; PAST_PAPER="PAST_PAPER"; OTHER="OTHER"
class Material(Base):
    __tablename__="materials"
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    module_id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("modules.id",ondelete="CASCADE"),index=True)
    title: Mapped[str]=mapped_column(String(180)); description: Mapped[str|None]=mapped_column(Text)
    category: Mapped[MaterialCategory]=mapped_column(Enum(MaterialCategory,name="material_category"))
    storage_path: Mapped[str]=mapped_column(String(500)); original_filename: Mapped[str]=mapped_column(String(255)); mime_type: Mapped[str]=mapped_column(String(120))
    uploaded_by: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id"))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now()); updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
