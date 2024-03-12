#
# Código Python para plotagem de gráficos e geração de PDF
# Atualização: 12/03/2024
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
from serial.tools import list_ports

def auto_select_serial_port():
    # Função para selecionar automaticamente a porta serial
    ports = serial.tools.list_ports.comports()

    print("Portas seriais disponíveis: ")
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")

    # Espera 3s para o usuário visualizar a lista de portas
    time.sleep(3)

    # Seleciona automaticamente a primeira porta serial disponível
    if ports:
        selected_port = ports[0].device
        print(f"Porta selecionada automaticamente: {selected_port}")
        return selected_port
    else:
        print("Não foi possível detectar uma porta corretamente")
        return None

def read_and_plot_data(modelo, tempo_total_segundos, com_port):
    # Função para ler e plotar dados
    tempo_total = []
    tensao_total = []
    intervalo_leitura = 30

    try:
        ser = serial.Serial(com_port, 9600, timeout=1)
        start_time = time.time()

        while time.time() - start_time < tempo_total_segundos:
            data = ser.readline().decode('utf-8').strip()
            tempo_atual, tensao_atual = map(float, data.split(','))

            tempo_total.append(tempo_atual / 60)  # Converter para minutos
            tensao_total.append(tensao_atual)

            time.sleep(intervalo_leitura)

    except KeyboardInterrupt:
        pass

    finally:
        ser.close()
        plot_graph(tempo_total, tensao_total, f'Gráfico - Tensão ao Longo do Tempo ({modelo})')
        return tempo_total, tensao_total

def plot_graph(tempo, tensao, title):
    # Função para plotar o gráfico
    plt.plot(tempo, tensao)
    plt.xlabel('Tempo (minutos)')  # Alteração para minutos
    plt.ylabel('Tensão')
    plt.title(title)
    plt.savefig("temp_plot.png", format="png")  # Salvar como figura
    plt.show()

def run_experiment():
    # Função para executar o experimento
    com_port = auto_select_serial_port()

    nome = input("Digite o nome do equipamento: ")
    fabricante = input("Digite o fabricante: ")
    p_n = input("Digite o P/N: ")
    s_n = input("Digite o S/N: ")

    modelo = input("Informe se o PS-835 é modelo A/B/C/D/E/F/G: ")
    if modelo in ["A", "B", "C", "D", "E", "F", "G"]:
        tempo_total_segundos = 45 * 60 if modelo in ["A", "C", "E"] else 90 * 60
        tempo_total, tensao_total = read_and_plot_data(modelo, tempo_total_segundos, com_port)
    else:
        print("Modelo inválido. Escolha entre PS-835A, C/E ou PS-835B, D, F & G.")
        return

    titulo = f"Tensão ao Longo do Tempo ({modelo})"
    observacao = input("O.B.S: ")

    # Gera o PDF
    generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo_total, tensao_total, observacao)

def generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo, tensao, observacao):
    # Função para gerar o PDF
    pdf_filename = f"Relatorio_1.pdf"

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

    plt.plot(tempo, tensao)
    plt.xlabel('Tempo (minutos)')
    plt.ylabel('Tensão')
    plt.title(titulo)
    plt.savefig("temp_plot.png", format="png")
    plt.close()  # Fechar o gráfico após salvar a figura

    pdf.drawInlineImage("temp_plot.png", 72, 400, width=400, height=300)

    pdf.save()

# Chama a função para iniciar o experimento
run_experiment()


{time.strftime('%Y%m%d_%H%M%S')}