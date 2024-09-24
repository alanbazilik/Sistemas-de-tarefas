import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry

# Função para conectar ao banco de dados MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tarefas"
    )

# Função para limpar os campos de entrada
def clear_inputs():
   title_entry.delete(0, tk.END)
   description_entry.delete("1.0", tk.END)

# Função para adicionar uma nova tarefa ao banco de dados
def add_task():
    title = title_entry.get()
    description = description_entry.get("1.0", tk.END).strip()
    deadline = deadline_entry.get_date()

    if not title:
        messagebox.showwarning("Atenção", "O título da tarefa é obrigatório.")
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO tasks (title, description, status, deadline) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, description, "Pendente", deadline))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
    
    # Limpar campos após adicionar
    load_tasks()
    clear_inputs()
    

# Função para carregar e exibir as tarefas na lista
def load_tasks(filter_status=None):
    task_list.delete(0, tk.END)
    conn = connect_to_db()
    cursor = conn.cursor()

    if filter_status:
        cursor.execute("SELECT id, title, status, deadline FROM tasks WHERE status = %s ORDER BY deadline", (filter_status,))
    else:
        cursor.execute("SELECT id, title, status, deadline FROM tasks ORDER BY deadline")

    for task in cursor.fetchall():
        status_symbol = "✔️" if task[2] == "Concluída" else "❌"
        task_list.insert(tk.END, f"{task[0]} - {task[1]} ({status_symbol}) [Prazo: {task[3]}]")

    cursor.close()
    conn.close()

# Função para remover uma tarefa selecionada
def remove_task():
    selected = task_list.curselection()
    if not selected:
        messagebox.showwarning("Atenção", "Selecione uma tarefa para remover.")
        return

    task_id = task_list.get(selected[0]).split(' ')[0]
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover esta tarefa?"):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Sucesso", "Tarefa removida com sucesso!")
           # Limpar campos após salvar edição
        load_tasks()
        clear_inputs()

# Função para carregar a tarefa selecionada e permitir edição
def load_selected_task():
    selected = task_list.curselection()
    if not selected:
        messagebox.showwarning("Atenção", "Selecione uma tarefa para editar.")
        return

    task_id = task_list.get(selected[0]).split(' ')[0]
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title, description, deadline FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()

    # Preencher os campos de entrada com a tarefa selecionada
    title_entry.delete(0, tk.END)
    title_entry.insert(0, task[0])
    description_entry.delete("1.0", tk.END)
    description_entry.insert(tk.END, task[1])
    deadline_entry.set_date(task[2])

    # Habilitar o botão de salvar a edição
    save_button.config(state=tk.NORMAL)

# Função para salvar alterações de uma tarefa editada
def save_task():
    selected = task_list.curselection()
    if not selected:
        return

    task_id = task_list.get(selected[0]).split(' ')[0]
    title = title_entry.get()
    description = description_entry.get("1.0", tk.END).strip()
    deadline = deadline_entry.get_date()

    if not title:
        messagebox.showwarning("Atenção", "O título da tarefa é obrigatório.")
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = %s, description = %s, deadline = %s WHERE id = %s", 
                   (title, description, deadline, task_id))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso!")

    # Limpar campos após salvar edição
    load_tasks()
    clear_inputs()

    # Desabilitar o botão de salvar até que outra tarefa seja carregada
    save_button.config(state=tk.DISABLED)

# Função para marcar tarefa como concluída
def complete_task():
    selected = task_list.curselection()
    if not selected:
        messagebox.showwarning("Atenção", "Selecione uma tarefa para marcar como concluída.")
        return

    task_id = task_list.get(selected[0]).split(' ')[0]
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'Concluída' WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Tarefa marcada como concluída!")
       # Limpar campos após salvar edição
    load_tasks()
    clear_inputs()

# Função para filtrar tarefas
def filter_tasks(status):
    load_tasks(filter_status=status)

# Interface gráfica com Tkinter
app = tk.Tk()
app.title("Gerenciador de Tarefas")

# Campo de título da tarefa
tk.Label(app, text="Título da Tarefa:").pack(pady=5)
title_entry = tk.Entry(app, width=40)
title_entry.pack(pady=5)

# Campo de descrição da tarefa
tk.Label(app, text="Descrição:").pack(pady=5)
description_entry = tk.Text(app, height=4, width=40)
description_entry.pack(pady=5)

# Campo para data de conclusão
tk.Label(app, text="Prazo:").pack(pady=5)
deadline_entry = DateEntry(app, width=12, background='darkblue', foreground='white', borderwidth=2)
deadline_entry.pack(pady=5)

# Botões para adicionar, editar, concluir e remover tarefas
add_button = tk.Button(app, text="Adicionar Tarefa", command=add_task)
add_button.pack(pady=5)

edit_button = tk.Button(app, text="Carregar Tarefa para Editar", command=load_selected_task)
edit_button.pack(pady=5)

save_button = tk.Button(app, text="Salvar Edição", command=save_task, state=tk.DISABLED)
save_button.pack(pady=5)

complete_button = tk.Button(app, text="Marcar como Concluída", command=complete_task)
complete_button.pack(pady=5)

remove_button = tk.Button(app, text="Remover Tarefa", command=remove_task)
remove_button.pack(pady=5)

# Filtros de tarefas
filter_frame = tk.Frame(app)
filter_frame.pack(pady=5)

pending_button = tk.Button(filter_frame, text="Exibir Pendentes", command=lambda: filter_tasks("Pendente"))
pending_button.pack(side=tk.LEFT, padx=5)

completed_button = tk.Button(filter_frame, text="Exibir Concluídas", command=lambda: filter_tasks("Concluída"))
completed_button.pack(side=tk.LEFT, padx=5)

# Lista de tarefas
task_list = tk.Listbox(app, width=50, height=10)
task_list.pack(pady=5)

# Carregar as tarefas no início
load_tasks()

app.mainloop()
