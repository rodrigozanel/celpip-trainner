"""
AVISO: ESTE CÓDIGO FOI GERADO POR INTELIGÊNCIA ARTIFICIAL (Claude 3.7 Sonnet)
NÃO FOI ESCRITO MANUALMENTE PELO AUTOR DO REPOSITÓRIO
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import TestType, Question

class QuestionForm(FlaskForm):
    """Formulário para criar/editar questões"""
    content = TextAreaField('Conteúdo da Questão', validators=[DataRequired()])
    instructions = TextAreaField('Instruções', validators=[DataRequired()])
    test_type_id = SelectField('Tipo de Teste', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')
    
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.test_type_id.choices = [(t.id, t.name) for t in TestType.query.all()]

class TestForm(FlaskForm):
    """Formulário para criar/editar testes"""
    title = StringField('Título', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descrição')
    test_type_id = SelectField('Tipo de Teste', coerce=int, validators=[DataRequired()])
    questions = SelectMultipleField('Questões', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')
    
    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.test_type_id.choices = [(t.id, t.name) for t in TestType.query.all()]
        
        # Carregar todas as questões disponíveis por padrão
        self.questions.choices = [(q.id, f"{q.content[:50]}... (Tipo: {q.test_type.name if q.test_type else 'N/A'})") 
                                 for q in Question.query.all()]
        
        # Atualizar com questões específicas se um tipo for fornecido
        if 'test_type_id' in kwargs and kwargs['test_type_id']:
            test_type_id = kwargs['test_type_id']
            self.questions.choices = [(q.id, q.content[:50] + '...') 
                                      for q in Question.query.filter_by(test_type_id=test_type_id).all()] 