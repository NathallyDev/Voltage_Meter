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
        
def plot_graph(tempo, tensao, titulo, modelo):
    # Função para plotar o gráfico
    plt.plot(tempo, tensao)
    plt.xlabel('Tempo (min)')  # Corrigido para definir o rótulo do eixo x como uma string
    plt.ylabel('Tensão')
    plt.title(titulo)

    # Definir os limites do eixo y
    if modelo == "PS-835A, C/E":
        plt.ylim(0, 30)
    else:
        plt.ylim(0, 30)

    # Salvar o gráfico em um buffer de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

def run_experiment():
    # Função para executar o experimento
    com_port = auto_select_serial_port()

    nome = input("Digite o nome do equipamento: ")
    fabricante = input("Digite o fabricante: ")
    p_n = input("Digite o P/N: ")
    s_n = input("Digite o S/N: ")

    modelo = input("Digite o modelo (PS-835A, C/E ou PS-835B, D/F/G): ")
    if modelo in ["PS-835A, C/E", "PS-835B, D/F/G"]:
        tempo_total_segundos = 1 * 60 if modelo == "PS-835A, C/E" else 90 * 60
        tempo_total, tensao_total = read_and_plot_data(modelo, tempo_total_segundos, com_port)
        titulo = f"Tensão ao Longo do Tempo ({modelo})"
        observacao = input("O.B.S: ")

        # Gerar o gráfico
        graph_buffer = plot_graph(tempo_total, tensao_total, titulo, modelo)  # Passar o modelo como argumento

        generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo_total, tensao_total, observacao, graph_buffer)
        
    else:
        print("Modelo inválido. Escolha entre PS-835A, C/E ou PS-835B, D, F & G.")

def generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo, tensao, observacao, graph_buffer):
    # Gerar o nome do arquivo PDF
    pdf_filename = f"Relatorio_{time.strftime('%Y%m%d_%H%M%S')}.pdf"

    # Iniciar o documento PDF
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    # Escrever o cabeçalho
    pdf.drawString(72, 750, f"Equipamento: {nome}       Fabricante: {fabricante}")
    pdf.drawString(72, 735, f"Modelo: {modelo}       P/N: {p_n}    S/N: {s_n}")

    # Adicionar o buffer de bytes do gráfico ao PDF
    temp_filename = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename.write(graph_buffer.getvalue())
    temp_filename.close()
    pdf.drawImage(temp_filename.name, 100, 400, width=400, height=300)
    os.unlink(temp_filename.name)

    # Escrever as observações
    pdf.drawString(72, 350, "Observações:")
    obs_lines = observacao.split('\n')
    y_position = 335
    for line in obs_lines:
        pdf.drawString(72, y_position, line)
        y_position -= 15

    # Salvar o PDF
    pdf.save()
    print("PDF Gerado.")

run_experiment()

