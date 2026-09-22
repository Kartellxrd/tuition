import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Quiz(Base):
    __tablename__="quizzes"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    module_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("modules.id",ondelete="CASCADE"),index=True)
    title:Mapped[str]=mapped_column(String(180)); instructions:Mapped[str|None]=mapped_column(Text); published:Mapped[bool]=mapped_column(Boolean,default=False)
    created_by:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id"))
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now()); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    questions=relationship("QuizQuestion",cascade="all, delete-orphan",order_by="QuizQuestion.position")
class QuizQuestion(Base):
    __tablename__="quiz_questions"; __table_args__=(UniqueConstraint("quiz_id","position"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4); quiz_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("quizzes.id",ondelete="CASCADE"))
    prompt:Mapped[str]=mapped_column(Text); marks:Mapped[int]=mapped_column(Integer,default=1); position:Mapped[int]=mapped_column(Integer)
    options=relationship("QuestionOption",cascade="all, delete-orphan",order_by="QuestionOption.position")
class QuestionOption(Base):
    __tablename__="question_options"; __table_args__=(UniqueConstraint("question_id","position"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4); question_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("quiz_questions.id",ondelete="CASCADE"))
    text:Mapped[str]=mapped_column(Text); is_correct:Mapped[bool]=mapped_column(Boolean,default=False); position:Mapped[int]=mapped_column(Integer)
class QuizAttempt(Base):
    __tablename__="quiz_attempts"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4); quiz_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("quizzes.id",ondelete="CASCADE")); student_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"))
    score:Mapped[int]=mapped_column(Integer); total:Mapped[int]=mapped_column(Integer); percentage:Mapped[Decimal]=mapped_column(Numeric(5,2)); submitted_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class QuizAttemptAnswer(Base):
    __tablename__="quiz_attempt_answers"; __table_args__=(UniqueConstraint("attempt_id","question_id"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4); attempt_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("quiz_attempts.id",ondelete="CASCADE")); question_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("quiz_questions.id",ondelete="CASCADE")); selected_option_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),ForeignKey("question_options.id",ondelete="SET NULL")); awarded_marks:Mapped[int]=mapped_column(Integer,default=0)
