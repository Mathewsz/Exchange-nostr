# Nostr Descentralized Crypto Exchange

## Visão Geral
Uma exchange de criptomoedas totalmente descentralizada utilizando o protocolo Nostr para comunicação segura e distribuída.

## Funcionalidades
- Troca descentralizada de criptomoedas
- Integração nativa com Nostr
- Carteira Bitcoin/Lightning
- Ordens peer-to-peer
- Interface web moderna e responsiva

## Tecnologias
- Backend: Python (FastAPI)
- Frontend: React
- Protocolo: Nostr
- Blockchain: Bitcoin, Lightning Network

## Pré-requisitos
- Python 3.9+
- pip
- git

## Instalação

### Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/nostr-exchange.git
cd nostr-exchange
```

### Configurar Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
# venv\Scripts\activate   # Windows
```

### Instalar Dependências
```bash
pip install -r backend/requirements.txt
```

### Inicializar Banco de Dados
```bash
python -c "from backend.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Iniciar Servidor
```bash
uvicorn backend.main:app --reload
```

## Segurança
Totalmente descentralizado, sem pontos únicos de falha.

## Contribuindo
Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como contribuir.

## Licença
Este projeto está sob a Licença MIT - veja [LICENSE](LICENSE) para detalhes.

## Aviso
Projeto em desenvolvimento. Use por sua conta e risco.
