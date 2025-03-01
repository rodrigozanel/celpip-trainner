from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.models import User

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Página inicial com informações sobre o simulador"""
    return render_template('index.html')

@bp.route('/select_role/<user_type>')
def select_role(user_type):
    """Selecionar o tipo de usuário (admin, evaluator, applicant)"""
    if user_type not in ['admin', 'evaluator', 'applicant']:
        flash('Tipo de usuário inválido', 'error')
        return redirect(url_for('main.index'))
    
    session['user_type'] = user_type
    
    if user_type == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif user_type == 'evaluator':
        return redirect(url_for('evaluator.dashboard'))
    else:
        return redirect(url_for('applicant.dashboard'))

@bp.route('/about')
def about():
    """Página sobre o simulador"""
    return render_template('about.html') 