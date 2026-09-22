import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
class Announcement(Base):
    __tablename__="announcements"
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    module_id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("modules.id",ondelete="CASCADE"),index=True)
    title: Mapped[str]=mapped_column(String(180)); message: Mapped[str]=mapped_column(Text); important: Mapped[bool]=mapped_column(Boolean,default=False)
    created_by: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id"))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now()); updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
