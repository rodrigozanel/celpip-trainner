from app import db
from datetime import datetime

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    score = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    evaluated_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Answer {self.id}>'
    
    @property
    def is_evaluated(self):
        return self.evaluator_id is not None and self.score is not None
        
# Modelo específico para respostas de speaking (pode armazenar caminho para arquivo de áudio)
class SpeakingAnswer(db.Model):
    __tablename__ = 'speaking_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False, unique=True)
    audio_file_path = db.Column(db.String(255), nullable=False)
    
    # Relacionamento
    answer = db.relationship('Answer', backref=db.backref('speaking_answer', uselist=False))
    
    def __repr__(self):
        return f'<SpeakingAnswer {self.id}>' 