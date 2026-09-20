import enum, uuid
from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.enrollment import EnrollmentTier
class SessionMode(str,enum.Enum): ONLINE="ONLINE"; IN_PERSON="IN_PERSON"
class SessionStatus(str,enum.Enum): SCHEDULED="SCHEDULED"; CANCELLED="CANCELLED"; COMPLETED="COMPLETED"
class Session(Base):
    __tablename__="sessions"
    __table_args__=(CheckConstraint("end_at > start_at",name="sessions_time_check"),CheckConstraint("(tier='GROUP' and enrollment_id is null) or (tier='ONE_ON_ONE' and enrollment_id is not null)",name="sessions_one_on_one_check"))
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4); module_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("modules.id",ondelete="CASCADE"))
    tier:Mapped[EnrollmentTier]=mapped_column(Enum(EnrollmentTier,name="enrollment_tier",create_type=False)); enrollment_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),ForeignKey("enrollments.id",ondelete="CASCADE"))
    title:Mapped[str]=mapped_column(String(180)); notes:Mapped[str|None]=mapped_column(Text); start_at:Mapped[datetime]=mapped_column(DateTime(timezone=True)); end_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
    mode:Mapped[SessionMode]=mapped_column(Enum(SessionMode,name="session_mode")); location:Mapped[str|None]=mapped_column(String(255)); meeting_link:Mapped[str|None]=mapped_column(String(500)); status:Mapped[SessionStatus]=mapped_column(Enum(SessionStatus,name="session_status"),default=SessionStatus.SCHEDULED)
    created_by:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id")); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now()); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
