from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class WritingAnswerForm(FlaskForm):
    """Formulário para respostas de writing"""
    content = TextAreaField('Sua resposta', validators=[DataRequired()])
    submit = SubmitField('Enviar Resposta')

class SpeakingAnswerForm(FlaskForm):
    """Formulário para respostas de speaking"""
    audio_file = FileField('Arquivo de Áudio', validators=[
        FileRequired(), 
        FileAllowed(['mp3', 'wav', 'ogg'], 'Apenas arquivos de áudio são permitidos!')
    ])
    content = TextAreaField('Observações (opcional)')
    submit = SubmitField('Enviar Resposta') 