#
# Código Python para plotagem de gráficos e geração de PDF
# Data: 21/03/2024
#
# Dev: Náthally Lima Arruda 
# e-mail: nathallylym@gmail.com
#
#
#

import serial
import matplotlib.pyplot as plt  # Adicionando importação do módulo matplotlib.pyplot
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time
from serial.tools.list_ports import comports
from io import BytesIO
import tempfile
import os
import pdfkit
import numpy as np

def auto_select_serial_port():
    # Função para selecionar automaticamente a porta serial
    ports = comports()

    for port, desc, hwid in sorted(ports):
        pass

    time.sleep(2)

    if ports:
        selected_port = ports[0].device
        return selected_port
    else:
        return None

def read_and_plot_data(modelo, tempo_total_segundos, com_port):
    # Função para ler e plotar dados
    tempo_total = []
    tensao_total = []
    intervalo_leitura = 1

    print("Iniciando coleta de dados...")

    ser = None
    try:
        ser = serial.Serial(com_port, 9600, timeout=1)

        start_time = time.time()

        while time.time() - start_time < tempo_total_segundos:
            data = ser.readline().decode('utf-8').strip()
            if data:
                tempo_atual, tensao_atual = map(float, data.split(','))
                tempo_total.append(tempo_atual)
                tensao_total.append(tensao_atual)

            time.sleep(intervalo_leitura)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Erro ao ler da porta serial: {e}")

    finally:
        if ser:
            ser.close()
        print("Fim da coleta de dados.")

    if not tempo_total or not tensao_total:
        print("Nenhum dado lido.")
        return None, None

    return tempo_total, tensao_total

def plot_graph(tempo, tensao, titulo, modelo, t_graph):
    # Definir o tamanho da figura para garantir clareza
    plt.figure(figsize=(10, 6))
    tempo_minutos = [t / 60000 for t in tempo]  # Converter milissegundos para minutos

    # Plotar o gráfico
    plt.plot(tempo_minutos, tensao)
    plt.xlabel('Tempo (min)')
    plt.ylabel('Tensão')
    plt.title(titulo)
    plt.ylim(0, 30)
    plt.xlim(0, t_graph + 1)  # Adiciona uma unidade extra ao limite máximo do eixo x

    # Adicionar grade ao gráfico
    plt.grid(True)

    # Salvar o gráfico em um buffer de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

def run_experiment():
    # Função para executar o experimento
    com_port = auto_select_serial_port()

    if com_port is None:
        print("Não foi possível selecionar uma porta serial.")
        return

    nome = input("Nome do equipamento: ")
    fabricante = input("Nome do fabricante: ")
    p_n = input("P/N: ")
    s_n = input("S/N: ")
    modelo = input("Modelo do equipamento: ")
    t_graph = int(input("Informe o tempo para a realização do teste (em minutos): "))

    tempo_total_segundos = t_graph * 60
    tempo_total, tensao_total = read_and_plot_data(modelo, tempo_total_segundos, com_port)
    titulo = f"Tensão ao Longo do Tempo ({modelo})"
    
    ad = input("Houve AD: ")
    num_ad = input("Informe o número da AD: ")
    observacao = input("O.B.S: ")

    graph_buffer = plot_graph(tempo_total, tensao_total, titulo, modelo, t_graph)

    generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo_total, tensao_total, observacao, graph_buffer, ad, num_ad)

def generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo_total, tensao_total, observacao, graph_buffer, ad, num_ad):
    pdf_filename = f"{p_n}_{s_n}_{time.strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    pdf.drawString(72, 750, f"Equipamento: {nome}       Fabricante: {fabricante}")
    pdf.drawString(72, 735, f"Modelo: {modelo}       P/N: {p_n}    S/N: {s_n}    AD: {ad}       AD NUMBER: {num_ad}")

    # Salvar o buffer de bytes em um arquivo temporário
    temp_filename = f"{p_n}_{s_n}_{time.strftime('%Y%m%d_%H%M%S')}.png"
    with open(temp_filename, 'wb') as f:
        f.write(graph_buffer.getvalue())

    # Adiciona a imagem do gráfico ao PDF
    pdf.drawImage(temp_filename, 100, 400, width=400, height=300)

    # Escreve as observações abaixo do gráfico
    pdf.drawString(72, 350, f"Observações: {observacao}")

    # Salva o PDF
    pdf.save()
    print("PDF Gerado.")

    # Remover o arquivo temporário após salvar o PDF
    os.unlink(temp_filename)

run_experiment()
