# Sistema de Gerenciamento de Tarefas

Este projeto é um **Sistema de Gerenciamento de Tarefas** que permite adicionar, editar, remover e marcar tarefas como concluídas. Ele utiliza **Tkinter** para a interface gráfica e **MySQL** como banco de dados para armazenar as tarefas.

## Funcionalidades

- **Adicionar Tarefas**: Insira o título, descrição e data limite para cada tarefa.
- **Editar Tarefas**: Carregue uma tarefa existente, edite suas informações e salve as alterações.
- **Remover Tarefas**: Exclua tarefas que não são mais necessárias.
- **Marcar como Concluída**: Marque tarefas como concluídas e filtre tarefas por status (pendente ou concluída).
- **Filtros**: Visualize todas as tarefas ou filtre apenas as pendentes ou concluídas.

## Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter**: Biblioteca padrão para interface gráfica.
- **MySQL**: Banco de dados relacional para armazenar as tarefas.
- **Tkcalendar**: Utilizada para selecionar a data de prazo das tarefas.

## Como Executar o Projeto

### 1. Pré-requisitos

- Instalar Python 3.x: [Download Python](https://www.python.org/downloads/)
- Instalar MySQL: [Download MySQL](https://www.mysql.com/downloads/)
- Instalar os pacotes necessários:

```bash
pip install mysql-connector-python tk tkcalendar
pip install tkinter 
python sistema_tarefas.py

## codigo mysql 
### 2. sql tarefas

-CREATE DATABASE tarefas;

USE tarefas;

- CREATE TABLE tasks (
-     id INT AUTO_INCREMENT PRIMARY KEY,
-     title VARCHAR(255) NOT NULL,
-     description TEXT,
-     status VARCHAR(50) DEFAULT 'Pendente',
-     deadline DATE
- );

## Executando o Programa

### 3. Executando o Programa

- python sistema_tarefas.py
