from app.api.v1.quizzes import QuizCreate,QuestionCreate,OptionCreate

def test_quiz_payload_supports_multiple_questions():
    quiz=QuizCreate(module_id="00000000-0000-0000-0000-000000000001",title="Practice",questions=[
        QuestionCreate(prompt="Q1",marks=1,options=[OptionCreate(text="A",is_correct=True),OptionCreate(text="B")]),
        QuestionCreate(prompt="Q2",marks=2,options=[OptionCreate(text="A"),OptionCreate(text="B",is_correct=True)])
    ])
    assert len(quiz.questions)==2
    assert sum(q.marks for q in quiz.questions)==3
