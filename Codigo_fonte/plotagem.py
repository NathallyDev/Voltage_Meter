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
import matplotlib.pyplot as plt
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

    print("Portas seriais disponíveis:")
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")

    # Espera 2 segundos para o usuário visualizar a lista de portas
    time.sleep(2)

    # Seleciona automaticamente a primeira porta serial disponível
    if ports:
        selected_port = ports[0].device
        print(f"Porta serial selecionada automaticamente: {selected_port}")
        return selected_port
    else:
        print("Nenhuma porta serial disponível.")
        return None

def read_and_plot_data(modelo, tempo_total_segundos, com_port):
    # Função para ler e plotar dados
    tempo_total = []
    tensao_total = []
    intervalo_leitura = 1

    print("Leitura em processamento...")

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

    finally:
        ser.close()
        print("Leitura finalizada.")

    # Verifica se houve leitura de dados
    if not tempo_total or not tensao_total:
        print("Nenhum dado lido.")
        return None, None

    return tempo_total, tensao_total

def plot_graph(tempo, tensao, titulo, modelo, t_graph, tempo_total_segundos):
    # Definir o tamanho da figura para garantir clareza
    plt.figure(figsize=(10, 6))
    tempo = [i for i in range(tempo_total_segundos + 1)]
    tempo = tempo /

    # Plotar o gráfico
    plt.plot(tempo, tensao)
    plt.xlabel('Tempo (min)')
    plt.ylabel('Tensão')
    plt.title(titulo)
    plt.ylim(0, 30)

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

    # Dados que serão inseridos pelo usuário
    nome = input("Nome do equipamento: ")
    fabricante = input("Nome do fabricante: ")
    p_n = input("P/N: ")
    s_n = input("S/N: ")
    modelo = input("Modelo do equipamento: ")
    t_graph = int(input("Informe o tempo para a realização do teste (em minutos): "))  # Convertendo para inteiro

    tempo_total_segundos = t_graph * 60
    tempo_total, tensao_total = read_and_plot_data(modelo, tempo_total_segundos, com_port)
    titulo = f"Tensão ao Longo do Tempo ({modelo})"
    
    ad = input("Houve AD: ")
    num_ad = input("Informe o número da AD: ")
    observacao = input("O.B.S: ")

    # Gera o gráfico
    graph_buffer = plot_graph(tempo_total, tensao_total, titulo, modelo, t_graph)  # Passa o valor de t_graph como argumento

    generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo_total, tensao_total, observacao, graph_buffer, ad, num_ad)

def generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo_total, tensao_total, observacao, graph_buffer, ad, num_ad):
    # Gera o nome do arquivo PDF
    pdf_filename = f"{p_n}_{s_n}_{time.strftime('%Y%m%d_%H%M%S')}.pdf"

    # Inicia o documento PDF
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    # Escreve o cabeçalho
    pdf.drawString(72, 750, f"Equipamento: {nome}       Fabricante: {fabricante}")
    pdf.drawString(72, 735, f"Modelo: {modelo}       P/N: {p_n}    S/N: {s_n}    AD: {ad}       AD NUMBER: {num_ad}")

    # Adiciona o buffer de bytes do gráfico ao PDF
    temp_filename = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename.write(graph_buffer.getvalue())
    temp_filename.close()
    pdf.drawImage(temp_filename.name, 100, 400, width=400, height=300)
    os.unlink(temp_filename.name)

    # Escreve as observações abaixo do grafico
    pdf.drawString(72, 350, f"Observações: {observacao}")


    # Salva o PDF
    pdf.save()
    print("PDF Gerado.")

run_experiment()