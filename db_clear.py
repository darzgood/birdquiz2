from app import db, models

quizzes = models.Quiz.query.all()
for q in quizzes:
    db.session.delete(q)

db.session.commit()
