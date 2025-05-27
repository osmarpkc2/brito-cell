# Brito Cell - E-commerce de Celulares

Este é um e-commerce desenvolvido em Flask para venda de celulares, com painel administrativo para gerenciamento de produtos.

## 🚀 Como implantar no Vercel

### Pré-requisitos

- Conta no [Vercel](https://vercel.com)
- Conta no [GitHub](https://github.com)
- [Git](https://git-scm.com/) instalado localmente

### Passo a Passo

1. **Faça um fork deste repositório**
   - Clique no botão "Fork" no canto superior direito desta página

2. **Faça o deploy no Vercel**
   - Acesse o [painel do Vercel](https://vercel.com/dashboard)
   - Clique em "Add New" > "Project"
   - Conecte sua conta do GitHub
   - Importe o repositório do fork
   - Nas configurações do projeto:
     - **Framework Preset**: Other
     - **Build Command**: Deixe em branco
     - **Output Directory**: Deixe em branco
     - **Install Command**: `pip install -r requirements.txt`
   - Clique em "Deploy"

3. **Configure as variáveis de ambiente**
   - No painel do Vercel, vá para "Settings" > "Environment Variables"
   - Adicione as seguintes variáveis:
     - `FLASK_APP=app.py`
     - `FLASK_ENV=production`
     - `SECRET_KEY=sua_chave_secreta_muito_segura`
     - `DATABASE_URL=sqlite:///britocell.db` (para SQLite local) ou sua URL de banco de dados

4. **Acesse o site**
   - Após o deploy, o Vercel fornecerá uma URL como `https://seu-projeto.vercel.app`
   - Acesse o painel administrativo em `/admin`
   - Credenciais padrão:
     - Usuário: `admin`
     - Senha: `admin123`

## 🛠️ Desenvolvimento Local

### Pré-requisitos

- Python 3.8+
- pip
- Git

### Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/brito-cell.git
   cd brito-cell
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   Crie um arquivo `.env` na raiz do projeto:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=sua_chave_secreta_local
   DATABASE_URL=sqlite:///britocell.db
   ```

5. **Inicialize o banco de dados**
   ```bash
   flask db upgrade
   ```

6. **Execute o servidor de desenvolvimento**
   ```bash
   flask run
   ```

7. **Acesse o site**
   - Frontend: http://localhost:5000
   - Painel Admin: http://localhost:5000/admin

## 📦 Estrutura do Projeto

```
brito-cell/
├── api/                 # Arquivos da API para o Vercel
├── migrations/          # Migrações do banco de dados
├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   └── images/         # Imagens dos produtos
├── templates/           # Templates HTML
│   ├── admin/          # Painel administrativo
│   └── main/           # Páginas principais
├── .env.example        # Exemplo de variáveis de ambiente
├── .gitignore          # Arquivos ignorados pelo Git
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências do projeto
└── vercel.json         # Configuração do Vercel
```

## 🔒 Segurança

- Altere as credenciais padrão do administrador após o primeiro login
- Nunca exponha informações sensíveis no código-fonte
- Use HTTPS em produção
- Mantenha as dependências atualizadas

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙌 Contribuição

Contribuições são bem-vindas! Siga estes passos:

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Adicione suas mudanças (`git add .`)
4. Comite suas mudanças (`git commit -m 'Add some AmazingFeature'`)
5. Faça o Push da Branch (`git push origin feature/AmazingFeature`)
6. Abra um Pull Requestô Cell - E-commerce de iPhones

Sistema de catálogo de produtos com painel administrativo para gerenciamento de estoque da loja Britô Cell.

## Recursos

- Catálogo de produtos com fotos e descrições
- Painel administrativo protegido por senha
- Gerenciamento de produtos (adicionar, editar, remover)
- Controle de estoque
- Design responsivo e moderno
- Cores temáticas: Dourado, Prata e Azul metalizados

## Requisitos

- Python 3.7+
- pip (gerenciador de pacotes do Python)
- Navegador web moderno

## Instalação (Windows)

1. Clone o repositório:
   ```
   git clone [URL_DO_REPOSITORIO]
   cd brito-cell
   ```

2. Execute o script de configuração:
   ```
   .\setup.bat
   ```

   Isso irá:
   - Criar um ambiente virtual
   - Instalar todas as dependências
   - Criar o arquivo .env a partir do .env.example
   - Configurar o banco de dados
   - Criar o usuário admin

## Configuração

O arquivo `.env` será criado automaticamente durante a instalação. Você pode editá-lo para configurar:
- `SECRET_KEY`: Chave secreta para segurança da aplicação
- `SQLALCHEMY_DATABASE_URI`: URL de conexão com o banco de dados (padrão: SQLite)

## Executando a Aplicação

1. Inicie o servidor Flask:
   ```
   flask run
   ```

2. Acesse o site no navegador:
   - Site principal: http://localhost:5000
   - Painel administrativo: http://localhost:5000/admin
     - Usuário: admin
     - Senha: admin123

## Estrutura do Projeto

```
brito-cell/
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/               
│   ├── js/
│   └── images/
│       └── products/      # Imagens dos produtos
├── templates/              # Templates HTML
│   ├── admin/             # Painel administrativo
│   ├── main/              # Páginas do site principal
│   └── base.html          # Template base
├── app.py                 # Aplicação Flask
├── requirements.txt       # Dependências do Python
└── README.md              # Este arquivo
```

## Primeiros Passos

1. Acesse o painel administrativo
2. Adicione seus produtos usando o formulário
3. Gerencie o estoque conforme necessário
4. Visualize as alterações no site principal

## Personalização

- **Cores**: As cores podem ser alteradas no arquivo `static/css/style.css`
- **Logo**: Substitua o arquivo `static/images/logo.png` pelo seu logotipo
- **Favicon**: Adicione seus próprios arquivos de favicon na pasta `static/`

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais detalhes.

---

Desenvolvido por [Seu Nome] para Britô Cell
