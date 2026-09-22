import enum, uuid
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class AssignmentStatus(str,enum.Enum):
    DRAFT="DRAFT"
    PUBLISHED="PUBLISHED"
    CLOSED="CLOSED"

class Assignment(Base):
    __tablename__="assignments"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    module_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("modules.id",ondelete="CASCADE"),index=True)
    title:Mapped[str]=mapped_column(String(180),nullable=False)
    instructions:Mapped[str|None]=mapped_column(Text)
    due_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),index=True)
    status:Mapped[AssignmentStatus]=mapped_column(Enum(AssignmentStatus,name="assignment_status",create_type=False),default=AssignmentStatus.DRAFT)
    created_by:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id"))
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

class AssignmentSubmission(Base):
    __tablename__="assignment_submissions"
    __table_args__=(UniqueConstraint("assignment_id","student_id"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    assignment_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("assignments.id",ondelete="CASCADE"))
    student_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),index=True)
    submitted_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    notes:Mapped[str|None]=mapped_column(Text)
