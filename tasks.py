import mysql.connector
import tkinter as tk
import datetime
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
    deadline_entry.set_date(datetime.date.today())
    hour_combobox.set('')

# Função para adicionar uma nova tarefa ao banco de dados
def add_task():
    title = title_entry.get()
    description = description_entry.get("1.0", tk.END).strip()
    deadline = deadline_entry.get_date()
    hour = hour_combobox.get()

    if not title:
        messagebox.showwarning("Atenção", "O título da tarefa é obrigatório.")
        return

    if not hour:
        messagebox.showwarning("Atenção", "O horário de conclusão é obrigatório.")
        return

    deadline_with_time = f"{deadline} {hour}"

    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO tasks (title, description, status, deadline) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, description, "Pendente", deadline_with_time))
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

    # Usar o objeto datetime diretamente
    deadline_with_time = task[2]  # task[2] já é um objeto datetime
    deadline_entry.set_date(deadline_with_time.date())  # Definir a data
    hour_combobox.set(deadline_with_time.strftime('%H:%M'))  # Definir a hora

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
    hour = hour_combobox.get()

    if not title:
        messagebox.showwarning("Atenção", "O título da tarefa é obrigatório.")
        return

    if not hour:
        messagebox.showwarning("Atenção", "O horário de conclusão é obrigatório.")
        return

    deadline_with_time = f"{deadline} {hour}"

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = %s, description = %s, deadline = %s WHERE id = %s", 
                   (title, description, deadline_with_time, task_id))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso!")

    load_tasks()
    clear_inputs()
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
    load_tasks()
    clear_inputs()

# Função para filtrar tarefas
def filter_tasks(status):
    load_tasks(filter_status=status)

# Interface gráfica com Tkinter e ttk
app = tk.Tk()
app.title("Gerenciador de Tarefas")

# Tema padrão do ttk
style = ttk.Style(app)
style.theme_use("clam")

# Estilo moderno
style.configure("TButton", font=("Helvetica", 10), padding=10)
style.configure("TLabel", font=("Helvetica", 10))
style.configure("TEntry", font=("Helvetica", 10))
style.configure("TText", font=("Helvetica", 10))

# Frames para organizar melhor a interface
main_frame = ttk.Frame(app, padding="10")
main_frame.pack(fill="both", expand=True)

title_frame = ttk.Frame(main_frame)
title_frame.pack(fill="x", pady=10)

description_frame = ttk.Frame(main_frame)
description_frame.pack(fill="x", pady=10)

deadline_frame = ttk.Frame(main_frame)
deadline_frame.pack(fill="x", pady=10)

button_frame = ttk.Frame(main_frame)
button_frame.pack(fill="x", pady=10)

filter_frame = ttk.Frame(main_frame)
filter_frame.pack(fill="x", pady=10)

task_list_frame = ttk.Frame(main_frame)
task_list_frame.pack(fill="both", expand=True, pady=10)

# Campo de título da tarefa
ttk.Label(title_frame, text="Título da Tarefa:").pack(anchor="w")
title_entry = ttk.Entry(title_frame, width=50)
title_entry.pack(fill="x")

# Campo de descrição da tarefa
ttk.Label(description_frame, text="Descrição:").pack(anchor="w")
description_entry = tk.Text(description_frame, height=4, width=50, font=("Helvetica", 10))
description_entry.pack(fill="x")

# Campo para data de conclusão
ttk.Label(deadline_frame, text="Prazo:").pack(anchor="w")
deadline_entry = DateEntry(deadline_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
deadline_entry.pack()

# Campo para hora de conclusão
ttk.Label(deadline_frame, text="Hora:").pack(anchor="w")
hour_combobox = ttk.Combobox(deadline_frame, values=[f"{h:02d}:00" for h in range(24)], width=10)
hour_combobox.pack()

# Botões para adicionar, editar, concluir e remover tarefas
add_button = ttk.Button(button_frame, text="Adicionar Tarefa", command=add_task)
add_button.pack(side="left", padx=5)

edit_button = ttk.Button(button_frame, text="Editar Tarefa", command=load_selected_task)
edit_button.pack(side="left", padx=5)

save_button = ttk.Button(button_frame, text="Salvar Edição", command=save_task, state=tk.DISABLED)
save_button.pack(side="left", padx=5)

complete_button = ttk.Button(button_frame, text="Concluir Tarefa", command=complete_task)
complete_button.pack(side="left", padx=5)

# Botão para remover tarefas
remove_button = ttk.Button(button_frame, text="Remover Tarefa", command=remove_task)
remove_button.pack(side="left", padx=5)

# Filtros de status
ttk.Label(filter_frame, text="Filtrar Tarefas:").pack(side="left", padx=5)
filter_pending_button = ttk.Button(filter_frame, text="Pendentes", command=lambda: filter_tasks("Pendente"))
filter_pending_button.pack(side="left", padx=5)

filter_completed_button = ttk.Button(filter_frame, text="Concluídas", command=lambda: filter_tasks("Concluída"))
filter_completed_button.pack(side="left", padx=5)

filter_all_button = ttk.Button(filter_frame, text="Todas", command=load_tasks)
filter_all_button.pack(side="left", padx=5)

# Lista de tarefas
task_list = tk.Listbox(task_list_frame, height=15, font=("Helvetica", 10))
task_list.pack(fill="both", expand=True)

# Carregar tarefas ao iniciar o aplicativo
load_tasks()

# Iniciar o loop da interface gráfica
app.mainloop()
