"""
AVISO: ESTE CÓDIGO FOI GERADO POR INTELIGÊNCIA ARTIFICIAL (Claude 3.7 Sonnet)
NÃO FOI ESCRITO MANUALMENTE PELO AUTOR DO REPOSITÓRIO
"""

from app import create_app
import logging

# Configuração de logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    logger.info("Iniciando a aplicação CELPIP Trainer...")
    # Host 0.0.0.0 para permitir acesso externo ao contêiner
    app.run(host='0.0.0.0', port=5000, debug=True)
    logger.info("Aplicação encerrada.") 