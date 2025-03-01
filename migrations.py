from app import create_app, db
from app.models import User, TestType, Test, Question, TestQuestion, Answer, SpeakingAnswer
import time
from sqlalchemy import text

app = create_app()

def init_db():
    """Inicializa o banco de dados e cria as tabelas"""
    # Esperar o banco de dados inicializar completamente (útil para Docker)
    max_retries = 30
    retries = 0
    
    while retries < max_retries:
        try:
            with app.app_context():
                # Testar conexão usando o método correto do SQLAlchemy
                with db.engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                    connection.commit()
                break
        except Exception as e:
            retries += 1
            print(f"Tentativa {retries}/{max_retries} de conexão com o banco de dados falhou. Erro: {e}")
            time.sleep(2)
    
    if retries == max_retries:
        print("Não foi possível conectar ao banco de dados após várias tentativas.")
        return
    
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existem tipos de teste
        if TestType.query.count() == 0:
            # Criar tipos de teste
            writing = TestType(name='writing', description='Teste de escrita em inglês')
            speaking = TestType(name='speaking', description='Teste de fala em inglês')
            reading = TestType(name='reading', description='Teste de leitura em inglês')
            listening = TestType(name='listening', description='Teste de compreensão auditiva em inglês')
            
            db.session.add_all([writing, speaking, reading, listening])
            db.session.commit()
            
            print("Tipos de teste criados com sucesso!")
        
        # Verificar se já existem usuários
        if User.query.count() == 0:
            # Criar usuários padrão
            admin = User(name='Administrador', email='admin@example.com', user_type='admin')
            evaluator = User(name='Avaliador', email='evaluator@example.com', user_type='evaluator')
            applicant = User(name='Aplicante', email='applicant@example.com', user_type='applicant')
            
            db.session.add_all([admin, evaluator, applicant])
            db.session.commit()
            
            print("Usuários padrão criados com sucesso!")
        
        print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    init_db() 