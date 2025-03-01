from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app import db
from app.models import Answer, User
from app.forms.evaluator_forms import EvaluationForm
from functools import wraps
from datetime import datetime

bp = Blueprint('evaluator', __name__, url_prefix='/evaluator')

# Decorator para verificar se o usuário é avaliador
def evaluator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'evaluator':
            flash('Acesso negado. Você precisa ser um avaliador.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@evaluator_required
def dashboard():
    """Dashboard do avaliador"""
    # Consultar respostas pendentes de avaliação
    pending_answers = Answer.query.filter(Answer.evaluator_id.is_(None)).all()
    return render_template('evaluator/dashboard.html', pending_answers=pending_answers)

@bp.route('/answers')
@evaluator_required
def list_answers():
    """Listar todas as respostas para avaliação"""
    pending_answers = Answer.query.filter(Answer.evaluator_id.is_(None)).all()
    return render_template('evaluator/answers.html', answers=pending_answers)

@bp.route('/answers/<int:id>/evaluate', methods=['GET', 'POST'])
@evaluator_required
def evaluate_answer(id):
    """Avaliar uma resposta"""
    answer = Answer.query.get_or_404(id)
    
    # Verificar se a resposta já foi avaliada
    if answer.is_evaluated:
        flash('Esta resposta já foi avaliada.', 'info')
        return redirect(url_for('evaluator.list_answers'))
    
    form = EvaluationForm()
    if form.validate_on_submit():
        answer.score = form.score.data
        answer.feedback = form.feedback.data
        answer.evaluator_id = 2  # Por enquanto, hardcoded (usuário avaliador)
        answer.evaluated_at = datetime.utcnow()
        db.session.commit()
        flash('Resposta avaliada com sucesso!', 'success')
        return redirect(url_for('evaluator.list_answers'))
    
    return render_template('evaluator/evaluate_form.html', form=form, answer=answer) 