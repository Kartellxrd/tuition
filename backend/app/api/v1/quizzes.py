from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.api.dependencies import get_current_user, require_tutor
from app.core.database import get_db
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.quiz import Quiz, QuizQuestion, QuestionOption, QuizAttempt, QuizAttemptAnswer
from app.models.user import User
router=APIRouter()
def can_access(db,user,module_id):
    return db.scalar(select(Enrollment.id).where(Enrollment.student_id==user.id,Enrollment.module_id==module_id,Enrollment.status==EnrollmentStatus.ACTIVE)) is not None
class AnswerIn(BaseModel):
    question_id:UUID; option_id:UUID
class SubmitIn(BaseModel):
    answers:list[AnswerIn]
@router.get("/module/{module_id}")
def list_quizzes(module_id:UUID,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if user.role.value!="TUTOR" and not can_access(db,user,module_id): raise HTTPException(403,"Active enrollment required.")
    q=select(Quiz).where(Quiz.module_id==module_id)
    if user.role.value!="TUTOR": q=q.where(Quiz.published.is_(True))
    return list(db.scalars(q.order_by(Quiz.created_at.desc())))
class OptionCreate(BaseModel):
    text:str
    is_correct:bool=False
class QuestionCreate(BaseModel):
    prompt:str
    marks:int=1
    options:list[OptionCreate]
class QuizCreate(BaseModel):
    module_id:UUID
    title:str
    instructions:str|None=None
    questions:list[QuestionCreate]

@router.post("/admin/create")
def create_quiz(payload:QuizCreate,tutor:User=Depends(require_tutor),db:Session=Depends(get_db)):
    if not payload.questions: raise HTTPException(400,"Quiz requires at least one question.")
    quiz=Quiz(module_id=payload.module_id,title=payload.title.strip(),instructions=payload.instructions,created_by=tutor.id,published=False)
    db.add(quiz);db.flush()
    for qi,q in enumerate(payload.questions,1):
        if len(q.options)<2 or sum(1 for o in q.options if o.is_correct)!=1 or q.marks<1: raise HTTPException(400,"Each question needs at least two options, exactly one correct answer, and positive marks.")
        question=QuizQuestion(quiz_id=quiz.id,prompt=q.prompt.strip(),marks=q.marks,position=qi);db.add(question);db.flush()
        for oi,o in enumerate(q.options,1): db.add(QuestionOption(question_id=question.id,text=o.text.strip(),is_correct=o.is_correct,position=oi))
    db.commit();db.refresh(quiz);return {"id":quiz.id,"title":quiz.title,"published":quiz.published}

@router.post("/admin/{quiz_id}/publish")
def publish_quiz(quiz_id:UUID,tutor:User=Depends(require_tutor),db:Session=Depends(get_db)):
    quiz=db.scalar(select(Quiz).options(selectinload(Quiz.questions).selectinload(QuizQuestion.options)).where(Quiz.id==quiz_id))
    if not quiz: raise HTTPException(404,"Quiz not found.")
    if not quiz.questions or any(len(q.options)<2 or sum(1 for o in q.options if o.is_correct)!=1 for q in quiz.questions): raise HTTPException(400,"Quiz is incomplete.")
    quiz.published=True;db.commit();db.refresh(quiz);return {"id":quiz.id,"published":True}

@router.post("/admin/{quiz_id}/unpublish")
def unpublish_quiz(quiz_id:UUID,tutor:User=Depends(require_tutor),db:Session=Depends(get_db)):
    quiz=db.get(Quiz,quiz_id)
    if not quiz: raise HTTPException(404,"Quiz not found.")
    quiz.published=False;db.commit();return {"id":quiz.id,"published":False}

@router.get("/admin/{quiz_id}/results")
def quiz_results(quiz_id:UUID,_:User=Depends(require_tutor),db:Session=Depends(get_db)):
    quiz=db.get(Quiz,quiz_id)
    if not quiz: raise HTTPException(404,"Quiz not found.")
    rows=db.execute(select(QuizAttempt,User).join(User,User.id==QuizAttempt.student_id).where(QuizAttempt.quiz_id==quiz_id).order_by(QuizAttempt.submitted_at.desc())).all()
    return [{"attempt_id":a.id,"student_id":u.id,"student_name":u.name,"student_email":u.email,"score":a.score,"total":a.total,"percentage":a.percentage,"submitted_at":a.submitted_at} for a,u in rows]

@router.get("/{quiz_id}/attempts/me")
def my_attempts(quiz_id:UUID,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return list(db.scalars(select(QuizAttempt).where(QuizAttempt.quiz_id==quiz_id,QuizAttempt.student_id==user.id).order_by(QuizAttempt.submitted_at.desc())))

@router.get("/{quiz_id}")
def load_quiz(quiz_id:UUID,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    quiz=db.scalar(select(Quiz).options(selectinload(Quiz.questions).selectinload(QuizQuestion.options)).where(Quiz.id==quiz_id))
    if not quiz or (user.role.value!="TUTOR" and not quiz.published): raise HTTPException(404,"Quiz not found.")
    if user.role.value!="TUTOR" and not can_access(db,user,quiz.module_id): raise HTTPException(403,"Active enrollment required.")
    return {"id":quiz.id,"module_id":quiz.module_id,"title":quiz.title,"instructions":quiz.instructions,"questions":[{"id":q.id,"prompt":q.prompt,"marks":q.marks,"position":q.position,"options":[{"id":o.id,"text":o.text,"position":o.position} for o in q.options]} for q in quiz.questions]}
@router.post("/{quiz_id}/submit")
def submit(quiz_id:UUID,payload:SubmitIn,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    quiz=db.scalar(select(Quiz).options(selectinload(Quiz.questions).selectinload(QuizQuestion.options)).where(Quiz.id==quiz_id,Quiz.published.is_(True)))
    if not quiz: raise HTTPException(404,"Quiz not found.")
    if not can_access(db,user,quiz.module_id): raise HTTPException(403,"Active enrollment required.")
    supplied={a.question_id:a.option_id for a in payload.answers}; score=0; total=sum(q.marks for q in quiz.questions); rows=[]
    for q in quiz.questions:
        selected=supplied.get(q.id); valid={o.id:o for o in q.options}
        if selected is not None and selected not in valid: raise HTTPException(400,"An answer option does not belong to its question.")
        awarded=q.marks if selected is not None and valid[selected].is_correct else 0; score+=awarded; rows.append((q,selected,awarded))
    percentage=Decimal("0.00") if total==0 else (Decimal(score)*Decimal(100)/Decimal(total)).quantize(Decimal("0.01"))
    attempt=QuizAttempt(quiz_id=quiz.id,student_id=user.id,score=score,total=total,percentage=percentage); db.add(attempt); db.flush()
    for q,selected,awarded in rows: db.add(QuizAttemptAnswer(attempt_id=attempt.id,question_id=q.id,selected_option_id=selected,awarded_marks=awarded))
    db.commit();db.refresh(attempt);return {"attempt_id":attempt.id,"score":score,"total":total,"percentage":percentage,"submitted_at":attempt.submitted_at}

