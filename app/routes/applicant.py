from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app import db
from app.models import Test, Question, Answer, TestType, TestQuestion, SpeakingAnswer
from app.forms.applicant_forms import WritingAnswerForm, SpeakingAnswerForm
from functools import wraps
import os
from werkzeug.utils import secure_filename

bp = Blueprint('applicant', __name__, url_prefix='/applicant')

# Decorator para verificar se o usuário é aplicante
def applicant_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'applicant':
            flash('Acesso negado. Você precisa ser um aplicante.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@applicant_required
def dashboard():
    """Dashboard do aplicante"""
    # Listar todos os tipos de teste
    test_types = TestType.query.all()
    return render_template('applicant/dashboard.html', test_types=test_types)

@bp.route('/tests/<int:test_type_id>')
@applicant_required
def list_tests(test_type_id):
    """Listar testes disponíveis por tipo"""
    test_type = TestType.query.get_or_404(test_type_id)
    tests = Test.query.filter_by(test_type_id=test_type_id).all()
    return render_template('applicant/tests.html', tests=tests, test_type=test_type)

@bp.route('/tests/<int:test_id>/start')
@applicant_required
def start_test(test_id):
    """Iniciar um teste"""
    test = Test.query.get_or_404(test_id)
    
    # Obter a primeira questão do teste
    first_question = TestQuestion.query.filter_by(test_id=test_id).order_by(TestQuestion.order).first()
    
    if not first_question:
        flash('Este teste não possui questões.', 'error')
        return redirect(url_for('applicant.list_tests', test_type_id=test.test_type_id))
    
    # Redirecionar para a primeira questão
    return redirect(url_for('applicant.show_question', test_id=test_id, question_id=first_question.question_id))

@bp.route('/tests/<int:test_id>/questions/<int:question_id>', methods=['GET', 'POST'])
@applicant_required
def show_question(test_id, question_id):
    """Mostrar uma questão para responder"""
    test = Test.query.get_or_404(test_id)
    question = Question.query.get_or_404(question_id)
    test_question = TestQuestion.query.filter_by(test_id=test_id, question_id=question_id).first_or_404()
    
    # Verificar o tipo de teste para usar o formulário correto
    if test.test_type.name == 'writing':
        form = WritingAnswerForm()
        if form.validate_on_submit():
            answer = Answer(
                content=form.content.data,
                question_id=question_id,
                applicant_id=3  # Por enquanto, hardcoded (usuário aplicante)
            )
            db.session.add(answer)
            db.session.commit()
            flash('Resposta enviada com sucesso!', 'success')
            
            # Obter próxima questão, se houver
            next_question = TestQuestion.query.filter(
                TestQuestion.test_id == test_id,
                TestQuestion.order > test_question.order
            ).order_by(TestQuestion.order).first()
            
            if next_question:
                return redirect(url_for('applicant.show_question', test_id=test_id, question_id=next_question.question_id))
            else:
                return redirect(url_for('applicant.test_completed', test_id=test_id))
    
    elif test.test_type.name == 'speaking':
        form = SpeakingAnswerForm()
        if form.validate_on_submit():
            # Processar o arquivo de áudio
            audio_file = form.audio_file.data
            filename = secure_filename(audio_file.filename)
            audio_path = os.path.join('app/static/uploads/audio', filename)
            audio_file.save(audio_path)
            
            # Criar a resposta
            answer = Answer(
                content=form.content.data or 'Resposta de áudio',
                question_id=question_id,
                applicant_id=3  # Por enquanto, hardcoded (usuário aplicante)
            )
            db.session.add(answer)
            db.session.commit()
            
            # Criar a resposta de áudio
            speaking_answer = SpeakingAnswer(
                answer_id=answer.id,
                audio_file_path=audio_path
            )
            db.session.add(speaking_answer)
            db.session.commit()
            
            flash('Resposta enviada com sucesso!', 'success')
            
            # Obter próxima questão, se houver
            next_question = TestQuestion.query.filter(
                TestQuestion.test_id == test_id,
                TestQuestion.order > test_question.order
            ).order_by(TestQuestion.order).first()
            
            if next_question:
                return redirect(url_for('applicant.show_question', test_id=test_id, question_id=next_question.question_id))
            else:
                return redirect(url_for('applicant.test_completed', test_id=test_id))
    else:
        form = None
        flash('Tipo de teste não suportado.', 'error')
        return redirect(url_for('applicant.dashboard'))
    
    return render_template('applicant/question.html', test=test, question=question, form=form)

@bp.route('/tests/<int:test_id>/completed')
@applicant_required
def test_completed(test_id):
    """Página de conclusão do teste"""
    test = Test.query.get_or_404(test_id)
    return render_template('applicant/test_completed.html', test=test)

@bp.route('/answers')
@applicant_required
def list_answers():
    """Listar todas as respostas enviadas pelo aplicante"""
    # Por enquanto, hardcoded (usuário aplicante)
    applicant_id = 3
    answers = Answer.query.filter_by(applicant_id=applicant_id).all()
    return render_template('applicant/answers.html', answers=answers) 