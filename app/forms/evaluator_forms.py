from flask_wtf import FlaskForm
from wtforms import TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class EvaluationForm(FlaskForm):
    """Formulário para avaliar respostas"""
    score = DecimalField('Pontuação (0-10)', validators=[
        DataRequired(),
        NumberRange(min=0, max=10, message='A pontuação deve estar entre 0 e 10')
    ])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Enviar Avaliação') 