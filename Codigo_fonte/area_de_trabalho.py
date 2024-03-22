#
# Código Python para criar icone na atalho na área de trabalho
# Data: 21/03/2024
#
# Dev: Náthally Lima Arruda 
# e-mail: nathallylym@gmail.com
#
#
#

import os
import shutil
import winshell
import tkinter as tk
from tkinter import messagebox
from win32com.client import Dispatch

def criar_atalho(script_path, target_path):
    # Criar atalho na área de trabalho
    atalho = os.path.join(winshell.desktop(), "Plotagem.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(atalho)
    shortcut.Targetpath = target_path
    shortcut.Arguments = '/K "' + script_path + '"'
    shortcut.save()

def criar_atalho_confirmacao():
    # Callback para criação de atalho
    def criar():
        # Caminho para o diretório onde este script está localizado
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Caminho para o arquivo plotagem.py
        script_path = os.path.join(script_dir, "plotagem.py")

        # Caminho para o diretório de destino onde o arquivo será copiado
        destino_dir = winshell.desktop()
        
        # Copiar o arquivo para o diretório de destino
        shutil.copy(script_path, destino_dir)
        print("Arquivo plotagem.py copiado para a área de trabalho.")

        # Caminho completo do arquivo copiado
        destino_path = os.path.join(destino_dir, "plotagem.py")

        # Caminho para o executável do Python
        python_exe = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'python.exe')

        # Criar o atalho
        criar_atalho(destino_path, python_exe)
        print("Atalho criado com sucesso na área de trabalho.")
        root.destroy()

    # Callback para cancelamento
    def cancelar():
        root.destroy()

    # Criar a janela de confirmação
    root = tk.Tk()
    root.title("Confirmação")
    root.geometry("300x100")

    # Label com a mensagem
    label = tk.Label(root, text="Deseja criar o atalho na área de trabalho?")
    label.pack(pady=10)

    # Botão de "Okay"
    btn_okay = tk.Button(root, text="Okay", width=10, command=criar)
    btn_okay.pack(side=tk.LEFT, padx=10)

    # Botão de "Cancelar"
    btn_cancelar = tk.Button(root, text="Cancelar", width=10, command=cancelar)
    btn_cancelar.pack(side=tk.RIGHT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    criar_atalho_confirmacao()
