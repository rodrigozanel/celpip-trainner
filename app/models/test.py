from app import db
from datetime import datetime

class TestType(db.Model):
    __tablename__ = 'test_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # 'writing', 'speaking', 'reading', 'listening'
    description = db.Column(db.Text, nullable=True)
    
    # Relacionamentos
    tests = db.relationship('Test', backref='test_type', lazy=True)
    questions = db.relationship('Question', backref='test_type', lazy=True)
    
    def __repr__(self):
        return f'<TestType {self.name}>'

class Test(db.Model):
    __tablename__ = 'tests'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    test_type_id = db.Column(db.Integer, db.ForeignKey('test_types.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    questions = db.relationship('TestQuestion', backref='test', lazy=True)
    
    def __repr__(self):
        return f'<Test {self.title}>'

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    test_type_id = db.Column(db.Integer, db.ForeignKey('test_types.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tests = db.relationship('TestQuestion', backref='question', lazy=True)
    answers = db.relationship('Answer', backref='question', lazy=True)
    
    def __repr__(self):
        return f'<Question {self.id}>'

class TestQuestion(db.Model):
    """Tabela de associação entre testes e questões"""
    __tablename__ = 'test_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<TestQuestion {self.test_id}:{self.question_id}>' 