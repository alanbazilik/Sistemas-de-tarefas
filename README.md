# Sistema de Gerenciamento de Tarefas

# Este projeto é um Sistema de Gerenciamento de Tarefas que permite adicionar, editar, remover e marcar tarefas como concluídas. Ele utiliza Tkinter para a interface gráfica e MySQL como banco de dados para armazenar as tarefas.

# Funcionalidades
# Adicionar Tarefas: Insira o título, descrição e data limite para cada tarefa.
# Editar Tarefas: Carregue uma tarefa existente, edite suas informações e salve as alterações.
# Remover Tarefas: Exclua tarefas que não são mais necessárias.
# Marcar como Concluída: Marque tarefas como concluídas e filtre tarefas por status (pendente ou concluída).
# Filtros: Visualize todas as tarefas ou filtre apenas as pendentes ou concluídas.

# Tecnologias Utilizadas
# Python 3.x
# Tkinter: Biblioteca padrão para interface gráfica.
# MySQL: Banco de dados relacional para armazenar as tarefas.
# Tkcalendar: Utilizada para selecionar a data de prazo das tarefas.
# Como Executar o Projeto

# 1. Pré-requisitos
# Instalar Python 3.x: Download Python
# Instalar MySQL: Download MySQL
# Instalar os pacotes necessários:
# bash
# Copiar código
# pip install mysql-connector-python tk tkcalendar

# 2. Funcionalidades Futuras
# Notificações de Prazo: Notificar o usuário quando uma tarefa estiver próxima do prazo final.
# Prioridade das Tarefas: Definir níveis de prioridade (baixa, média, alta).
# Melhorias na Interface: Tornar a interface mais moderna e intuitiva.

# 3. Código SQL para o Banco de Dados
# sql
# Copiar código
# CREATE DATABASE tarefas;

# USE tarefas;
# 
# CREATE TABLE tasks (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     description TEXT,
#     status VARCHAR(50) DEFAULT 'Pendente',
#     deadline DATE
# );

# 4. Executando o Programa
# Para executar o programa, utilize o seguinte comando:
# 
# bash
# Copiar código
# python sistema_tarefas.py
# Contribuindo
# Para contribuir com o projeto, por favor, faça um fork deste repositório e envie suas melhorias através de pull requests.
# 
# 5. GitHub
# Você pode encontrar este projeto no GitHub: [alanbazilik](https://github.com/alanbazilik/Sistemas-de-tarefas)