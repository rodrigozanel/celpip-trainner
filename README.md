# CELPIP Trainer

Um simulador de provas de inglês focado em testes como IELTS e CELPIP.

## AVISO IMPORTANTE

**ESTE CÓDIGO FOI GERADO POR INTELIGÊNCIA ARTIFICIAL**

Este projeto, incluindo todo o código-fonte, documentação, configurações e estrutura, foi desenvolvido com o auxílio de ferramentas de IA, especificamente Claude 3.7 Sonnet. O código não foi escrito manualmente pelo autor do repositório.

Este aviso é incluído para total transparência sobre a natureza do conteúdo deste repositório.

## Descrição

O CELPIP Trainer é uma aplicação web desenvolvida para ajudar estudantes a se prepararem para exames de proficiência em inglês, como CELPIP e IELTS. A aplicação permite que os usuários pratiquem diferentes tipos de questões (writing e speaking, com planos para adicionar reading e listening no futuro) e recebam feedback detalhado de avaliadores.

## Funcionalidades

- Três tipos de usuários: administrador, avaliador e aplicante
- Administradores podem criar e gerenciar questões e testes
- Avaliadores podem avaliar as respostas dos aplicantes e fornecer feedback
- Aplicantes podem realizar testes e visualizar suas avaliações
- Suporte para testes de writing (escrita) e speaking (fala)

## Tecnologias Utilizadas

- Python 3.9
- Flask (Framework web)
- SQLAlchemy (ORM)
- MySQL (Banco de dados)
- Bootstrap 5 (Frontend)
- Docker (Containerização)

## Instalação e Execução

### Requisitos

- Python 3.9 ou superior
- MySQL 8.0 ou superior
- Docker e Docker Compose (opcional)

### Instalação Local

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/celpip-trainer.git
   cd celpip-trainer
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o banco de dados MySQL:
   - Crie um banco de dados chamado `celpip_trainer`
   - Ajuste as configurações de conexão no arquivo `.env` se necessário

5. Inicialize o banco de dados:
   ```
   python migrations.py
   ```

6. Execute a aplicação:
   ```
   python run.py
   ```

7. Acesse a aplicação em `http://localhost:5000`

### Execução com Docker

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/celpip-trainer.git
   cd celpip-trainer
   ```

2. Execute com Docker Compose:
   ```
   docker-compose up
   ```

3. A aplicação estará disponível em `http://localhost:5000`

4. O banco de dados MySQL estará disponível em:
   - Host: localhost
   - Porta: 3306
   - Usuário: celpip_user
   - Senha: celpip_password
   - Banco de dados: celpip_trainer

5. Interface de administração do banco de dados (Adminer):
   - Acesse `http://localhost:8080`
   - Sistema: MySQL
   - Servidor: db
   - Usuário: celpip_user
   - Senha: celpip_password
   - Banco de dados: celpip_trainer

## Estrutura do Projeto

```
celpip-trainer/
├── app/                    # Diretório principal da aplicação
│   ├── models/             # Modelos de dados
│   ├── routes/             # Rotas e controladores
│   ├── forms/              # Formulários
│   ├── static/             # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/          # Templates HTML
│   └── __init__.py         # Inicialização da aplicação
├── migrations.py           # Script para inicializar o banco de dados
├── run.py                  # Script para executar a aplicação
├── requirements.txt        # Dependências do projeto
├── Dockerfile              # Configuração do Docker
├── docker-compose.yml      # Configuração do Docker Compose
└── README.md               # Documentação
```

## Desenvolvimento Futuro

- Implementação de testes de reading (leitura)
- Implementação de testes de listening (compreensão auditiva)
- Sistema de autenticação de usuários
- Cronômetro para controle de tempo nas questões
- Relatórios de desempenho para aplicantes
