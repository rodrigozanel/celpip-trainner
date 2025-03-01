"""
AVISO: ESTE CÓDIGO FOI GERADO POR INTELIGÊNCIA ARTIFICIAL (Claude 3.7 Sonnet)
NÃO FOI ESCRITO MANUALMENTE PELO AUTOR DO REPOSITÓRIO
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from app import db
from app.models import User, TestType, Test, Question, TestQuestion
from app.forms.admin_forms import QuestionForm, TestForm
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator para verificar se o usuário é administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'admin':
            flash('Acesso negado. Você precisa ser um administrador.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@admin_required
def dashboard():
    """Dashboard do administrador"""
    return render_template('admin/dashboard.html')

@bp.route('/questions')
@admin_required
def list_questions():
    """Listar todas as questões"""
    questions = Question.query.all()
    return render_template('admin/questions.html', questions=questions)

@bp.route('/questions/new', methods=['GET', 'POST'])
@admin_required
def create_question():
    """Criar uma nova questão"""
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            content=form.content.data,
            instructions=form.instructions.data,
            test_type_id=form.test_type_id.data
        )
        db.session.add(question)
        db.session.commit()
        flash('Questão criada com sucesso!', 'success')
        return redirect(url_for('admin.list_questions'))
    return render_template('admin/question_form.html', form=form, title='Nova Questão')

@bp.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_question(id):
    """Editar uma questão existente"""
    question = Question.query.get_or_404(id)
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        question.content = form.content.data
        question.instructions = form.instructions.data
        question.test_type_id = form.test_type_id.data
        db.session.commit()
        flash('Questão atualizada com sucesso!', 'success')
        return redirect(url_for('admin.list_questions'))
    return render_template('admin/question_form.html', form=form, title='Editar Questão')

@bp.route('/tests')
@admin_required
def list_tests():
    """Listar todos os testes"""
    tests = Test.query.all()
    return render_template('admin/list_tests.html', tests=tests)

@bp.route('/tests/new', methods=['GET', 'POST'])
@admin_required
def create_test():
    """Criar um novo teste"""
    # Garantir que todas as questões estão disponíveis no formulário
    form = TestForm()
    
    if form.validate_on_submit():
        test = Test(
            title=form.title.data,
            description=form.description.data,
            test_type_id=form.test_type_id.data,
            creator_id=1  # Por enquanto, hardcoded (usuário admin)
        )
        db.session.add(test)
        db.session.commit()
        
        # Adicionar questões ao teste
        for i, question_id in enumerate(form.questions.data):
            test_question = TestQuestion(
                test_id=test.id,
                question_id=question_id,
                order=i+1
            )
            db.session.add(test_question)
        db.session.commit()
        
        flash('Teste criado com sucesso!', 'success')
        return redirect(url_for('admin.list_tests'))
    
    return render_template('admin/test_form.html', form=form, title='Novo Teste')

@bp.route('/api/questions-by-type/<int:test_type_id>')
@admin_required
def get_questions_by_type(test_type_id):
    """API para obter questões por tipo de teste"""
    questions = Question.query.filter_by(test_type_id=test_type_id).all()
    questions_data = [
        {
            'id': q.id,
            'content': q.content
        }
        for q in questions
    ]
    return jsonify({'questions': questions_data})

@bp.route('/tests/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_test(id):
    """Editar um teste existente"""
    test = Test.query.get_or_404(id)
    # Pré-popular o formulário com dados existentes
    form = TestForm(obj=test)
    
    # Pré-selecionar as questões que já fazem parte do teste
    if request.method == 'GET':
        form.questions.data = [tq.question_id for tq in test.test_questions]
    
    if form.validate_on_submit():
        test.title = form.title.data
        test.description = form.description.data
        test.test_type_id = form.test_type_id.data
        
        # Remover todas as questões atuais
        TestQuestion.query.filter_by(test_id=test.id).delete()
        
        # Adicionar as questões selecionadas
        for i, question_id in enumerate(form.questions.data):
            test_question = TestQuestion(
                test_id=test.id,
                question_id=question_id,
                order=i+1
            )
            db.session.add(test_question)
        
        db.session.commit()
        flash('Teste atualizado com sucesso!', 'success')
        return redirect(url_for('admin.list_tests'))
    
    return render_template('admin/test_form.html', form=form, title='Editar Teste')

@bp.route('/tests/<int:id>/delete', methods=['POST'])
@admin_required
def delete_test(id):
    """Excluir um teste"""
    test = Test.query.get_or_404(id)
    
    # Remover todas as questões do teste
    TestQuestion.query.filter_by(test_id=test.id).delete()
    
    # Remover o teste
    db.session.delete(test)
    db.session.commit()
    
    flash('Teste excluído com sucesso!', 'success')
    return redirect(url_for('admin.list_tests')) 