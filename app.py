import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime, timedelta
import json
import os

ARQUIVO = "tarefas.json"

tarefas = []



def salvar_tarefas():
    with open(ARQUIVO, "w") as f:
        json.dump(tarefas, f, indent=4)

def carregar_tarefas():
    global tarefas
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            tarefas = json.load(f)



def atualizar_lista():
    lista.delete(0, tk.END)
    tarefas_ordenadas = sorted(tarefas, key=lambda x: x["prioridade"])
    for t in tarefas_ordenadas:
        status = "✔" if t["concluida"] else "⏳"
        texto = f"{status} {t['titulo']} | Prioridade: {t['prioridade']} | Entrega: {t['data']}"
        lista.insert(tk.END, texto)

def adicionar_tarefa():
    titulo = entrada_titulo.get()
    prioridade = entrada_prioridade.get()
    data = entrada_data.get()

    if not titulo or not prioridade or not data:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return

    try:
        datetime.strptime(data, "%d/%m/%Y")
        prioridade = int(prioridade)
    except:
        messagebox.showwarning("Erro", "Data ou prioridade inválida!")
        return

    tarefas.append({
        "titulo": titulo,
        "prioridade": prioridade,
        "data": data,
        "concluida": False
    })

    salvar_tarefas()
    atualizar_lista()
    entrada_titulo.delete(0, tk.END)
    entrada_prioridade.delete(0, tk.END)
    entrada_data.delete(0, tk.END)

def remover_tarefa():
    selecionado = lista.curselection()
    if not selecionado:
        return

    tarefas_ordenadas = sorted(tarefas, key=lambda x: x["prioridade"])
    tarefa = tarefas_ordenadas[selecionado[0]]
    tarefas.remove(tarefa)

    salvar_tarefas()
    atualizar_lista()

def concluir_tarefa():
    selecionado = lista.curselection()
    if not selecionado:
        return

    tarefas_ordenadas = sorted(tarefas, key=lambda x: x["prioridade"])
    tarefas_ordenadas[selecionado[0]]["concluida"] = True

    salvar_tarefas()
    atualizar_lista()

def adiar_tarefa():
    selecionado = lista.curselection()
    if not selecionado:
        return

    dias = simpledialog.askinteger("Adiar", "Quantos dias deseja adiar?")
    if dias is None:
        return

    tarefas_ordenadas = sorted(tarefas, key=lambda x: x["prioridade"])
    tarefa = tarefas_ordenadas[selecionado[0]]

    data_atual = datetime.strptime(tarefa["data"], "%d/%m/%Y")
    nova_data = data_atual + timedelta(days=dias)
    tarefa["data"] = nova_data.strftime("%d/%m/%Y")

    salvar_tarefas()
    atualizar_lista()




janela = tk.Tk()
janela.title("Lista de Afazeres")
janela.geometry("600x500")
janela.config(bg="#2c3e50")

tk.Label(janela, text="Título", bg="#2c3e50", fg="white").pack()
entrada_titulo = tk.Entry(janela, width=40)
entrada_titulo.pack()

tk.Label(janela, text="Prioridade (número)", bg="#2c3e50", fg="white").pack()
entrada_prioridade = tk.Entry(janela, width=10)
entrada_prioridade.pack()

tk.Label(janela, text="Data (dd/mm/aaaa)", bg="#2c3e50", fg="white").pack()
entrada_data = tk.Entry(janela, width=15)
entrada_data.pack()

tk.Button(janela, text="Adicionar", command=adicionar_tarefa, bg="#27ae60", fg="white").pack(pady=5)
tk.Button(janela, text="Concluir", command=concluir_tarefa, bg="#2980b9", fg="white").pack(pady=5)
tk.Button(janela, text="Adiar", command=adiar_tarefa, bg="#f39c12", fg="white").pack(pady=5)
tk.Button(janela, text="Remover", command=remover_tarefa, bg="#c0392b", fg="white").pack(pady=5)

lista = tk.Listbox(janela, width=80, height=12)
lista.pack(pady=10)

carregar_tarefas()
atualizar_lista()

janela.mainloop()
