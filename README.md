# Sistema de Gestão de Consultas Médicas - Hospital E.A

Um sistema simples para gerenciar consultas médicas, desenvolvido em Python com interface gráfica.

## Funcionalidades

- Cadastro de pacientes
- Cadastro de médicos 
- Agendamento de consultas
- Geração de relatórios em PDF
- Sistema de login para controle de acesso

## Como usar

1. Clone o repositorio usando
```
git clone https://github.com/Gui0r/JogoMisterioso.git
```

2. Instale as dependências:
 pip install -r requirements.txt


3. Configure o banco de dados MySQL:
    - Baixe o xampp
    - Execute o Apache e o MySQL
    - Clique no botão Admin no MySQL, ele ira abrir um phpmyadmin
    - Execute o arquivo banco_de_dados.sql na aba sql que ele criara o banco sozinho
    - Ajuste as credenciais em config.py se necessário
    - Crie um usuario admin
```
USE sistema_consultas;
INSERT INTO usuarios (nome, senha, tipo) 
VALUES ('admin', 'admin123', 'admin');

ou coloque as credenciais que você quiser
```

4. Execute o sistema:
    - No terminal da IDE que você estiver execute o arquivo app.py


5. Faça login com as credenciais:
    - Usuário: admin
    - Senha: admin123

## Tecnologias

- Python 3
- Tkinter para interface gráfica
- MySQL para banco de dados
- ReportLab para geração de PDFs

## Observações

- O sistema foi desenvolvido simulando o sistema Hospital Estadual Sapiranguense
- Horários de consulta são gerados automaticamente baseados na disponibilidade do médico
- Os relatórios podem ser filtrados por período, medicos e atendimentos e pacientes cadastrados 
