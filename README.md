# Britô Cell - E-commerce de iPhones

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
