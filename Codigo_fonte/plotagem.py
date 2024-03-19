#
# Código Python para plotagem de gráficos e geração de PDF
# Data: 19/03/2024
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
            tempo_atual, tensao_atual = map(float, data.split(','))

            tempo_total.append(tempo_atual / 60)  # Converter de segundos para minutos
            tensao_total.append(tensao_atual)

            time.sleep(intervalo_leitura)

    except KeyboardInterrupt:
        pass

    finally:
        ser.close()
        print("Leitura finalizada.")
        return tempo_total, tensao_total

def plot_graph(tempo, tensao, title):
    # Função para plotar o gráfico
    plt.plot(tempo, tensao)
    plt.xlabel('Tempo (min)')
    plt.ylabel('Tensão')
    plt.title(title)

    if tensao:  # Verificar se há dados de tensão
        # Definir os limites do eixo y para cobrir toda a variação dos dados
        plt.ylim(min(tensao), max(tensao))

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
        tempo_total_segundos = 5 * 60 if modelo == "PS-835A, C/E" else 90 * 60
        tempo_total, tensao_total = read_and_plot_data(modelo, tempo_total_segundos, com_port)
        titulo = f"Tensão ao Longo do Tempo ({modelo})"
        observacao = input("O.B.S: ")

        # Gerar o gráfico
        graph_buffer = plot_graph(tempo_total, tensao_total, titulo)

        generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo_total, tensao_total, observacao, graph_buffer)
        
    else:
        print("Modelo inválido. Escolha entre PS-835A, C/E ou PS-835B, D, F & G.")

def generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo, tensao, observacao, graph_buffer):
    # Função para gerar o PDF
    pdf_filename = f"Relatorio_{time.strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    pdf.drawString(72, 750, f"Nome: {nome}")
    pdf.drawString(72, 735, f"Fabricante: {fabricante}")
    pdf.drawString(72, 720, f"P/N: {p_n}")
    pdf.drawString(72, 705, f"S/N: {s_n}") 
    pdf.drawString(72, 690, f"Modelo: {modelo}")

    pdf.drawString(72, 660, f"Gráfico - {titulo}")

    pdf.drawString(72, 630, "Observações:")
    pdf.drawString(72, 615, observacao)

    # Salvar o buffer de bytes em um arquivo temporário
    temp_filename = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename.write(graph_buffer.getvalue())
    temp_filename.close()

    # Adicionar a imagem ao PDF
    pdf.drawImage(temp_filename.name, 100, 400, width=400, height=300)

    # Excluir o arquivo temporário após o uso
    os.unlink(temp_filename.name)

    pdf.save()  # Salvar o PDF
    print("PDF Gerado.")

run_experiment()

