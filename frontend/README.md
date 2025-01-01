# Frontend da Exchange Descentralizada com Nostr

## Visão Geral
Frontend construído com React e TypeScript para a Exchange Descentralizada utilizando o protocolo Nostr.

## Tecnologias Principais
- React
- TypeScript
- Axios
- WebSocket
- React Router

## Configuração do Ambiente

### Pré-requisitos
- Node.js (v16+)
- npm ou yarn

### Instalação
1. Clone o repositório
2. Copie `.env.example` para `.env`
3. Instale as dependências:
   ```bash
   npm install
   ```

### Variáveis de Ambiente
- `REACT_APP_API_URL`: URL base da API backend
- `REACT_APP_TRADE_WEBSOCKET_URL`: URL do WebSocket para trades
- `REACT_APP_NOSTR_DEFAULT_RELAYS`: Lista de relays Nostr

### Scripts Disponíveis
- `npm start`: Iniciar servidor de desenvolvimento
- `npm test`: Executar testes
- `npm run build`: Compilar para produção

## Estrutura do Projeto
```
src/
├── components/      # Componentes React
├── contexts/        # Contextos globais
├── hooks/           # Hooks personalizados
├── services/        # Serviços de API e WebSocket
└── styles/          # Estilos globais
```

## Contribuição
1. Faça fork do projeto
2. Crie sua feature branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença
[Especificar licença]
