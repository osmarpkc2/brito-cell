# Brito Cell - E-commerce de Celulares

Este é um site de e-commerce desenvolvido em Flask para venda de celulares, com painel administrativo para gerenciamento de produtos.

## 🚀 Como executar localmente

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Git (opcional, para controle de versão)

### Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/brito-cell.git
   cd brito-cell
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # No Windows
   # ou
   source venv/bin/activate  # No Linux/Mac
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   - Copie o arquivo `.env.example` para `.env`
   - Edite o arquivo `.env` com suas configurações

5. **Crie o arquivo de configuração**
   - Crie um arquivo `config.json` com suas credenciais de administrador
   - Consulte o arquivo `.env.example` para referência

6. **Execute a aplicação**
   ```bash
   flask run
   ```
   - Acesse: http://localhost:5000
   - Painel administrativo: http://localhost:5000/admin

## 🔒 Configuração de Segurança

- O arquivo `config.json` contém credenciais sensíveis e NÃO deve ser compartilhado
- Certifique-se de que o `config.json` está listado no `.gitignore`
- Gere uma chave secreta segura para produção
- Nunca execute com `DEBUG=True` em produção

## 🛠️ Estrutura do Projeto

```
brito-cell/
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── templates/          # Templates HTML
│   ├── admin/         # Painel administrativo
│   └── main/          # Páginas principais
├── api/               # Endpoints da API
├── data/              # Dados da aplicação
├── .env.example       # Exemplo de variáveis de ambiente
├── app.py             # Aplicação principal
├── config.json        # Configurações sensíveis (não versionado)
├── requirements.txt   # Dependências do projeto
└── README.md          # Este arquivo
```

## 🔧 Tecnologias Utilizadas

- Python 3.11+
- Flask
- Bootstrap 5
- SQLAlchemy (para futuras implementações)
- Flask-Login para autenticação

## 📝 Notas Importantes

- Este projeto utiliza armazenamento em memória para os produtos (serão reiniciados a cada reinicialização)
- Para produção, recomenda-se implementar um banco de dados

## 🙌 Contribuição

Contribuições são bem-vindas! Siga estes passos:

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Adicione suas mudanças (`git add .`)
4. Comite suas mudanças (`git commit -m 'Add some AmazingFeature'`)
5. Faça o Push da Branch (`git push origin feature/AmazingFeature`)
6. Abra um Pull Request
