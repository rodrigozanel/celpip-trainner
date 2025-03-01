from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'admin', 'evaluator', 'applicant'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    created_tests = db.relationship('Test', backref='creator', lazy=True, foreign_keys='Test.creator_id')
    evaluated_answers = db.relationship('Answer', backref='evaluator', lazy=True, foreign_keys='Answer.evaluator_id')
    submitted_answers = db.relationship('Answer', backref='applicant', lazy=True, foreign_keys='Answer.applicant_id')
    
    def __repr__(self):
        return f'<User {self.name}, {self.user_type}>'
    
    def is_admin(self):
        return self.user_type == 'admin'
    
    def is_evaluator(self):
        return self.user_type == 'evaluator'
    
    def is_applicant(self):
        return self.user_type == 'applicant' 