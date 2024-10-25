import serial
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time
from serial.tools.list_ports import comports
from io import BytesIO
import os
from PIL import Image  

def auto_select_serial_port():
    # Função para selecionar a porta serial

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
    # Função para ler e plotar gráficos

    tempo_total = []
    tensao_total = []
    intervalo_leitura = 1

    print("Coletando dados...")
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
# definir o tamanho da figura para garantir clareza
        
    plt.figure(figsize=(10, 6))
    tempo_minutos = [t / 60000 for t in tempo]

# Definindo parametros do gráfico
    plt.plot(tempo_minutos, tensao)
    plt.xlabel('Tempo (min)')
    plt.ylabel('Tensão')
    plt.title(titulo)
    plt.ylim(0, 30)
    plt.xlim(0, t_graph + 0.5)
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

def run_experiment():
# Função para iniciar o experimento e realizar a coleta de dados

    com_port = auto_select_serial_port()
    if com_port is None:
        print("Não foi possível selecionar uma porta serial.")

        return
    
# Coleta de dados para o PDF
    nome = input("Nome do equipamento: ")
    fabricante = input("Nome do fabricante: ")
    p_n = input("P/N: ")
    s_n = input("S/N: ")
    modelo = input("Modelo do equipamento: ")
    t_graph = int(input("Informe o tempo para a realização do teste (em minutos): "))

# Reorganizando o tempo para a plotagem do gráfico
    tempo_total_segundos = t_graph * 60
    tempo_total, tensao_total = read_and_plot_data(modelo, tempo_total_segundos, com_port)
    titulo = f"Tensão ao Longo do Tempo ({modelo})"

# Continuação da coleta de dados do PDF
    ad = input("Houve AD: ")
    num_ad = input("Informe o número da AD: ")
    observacao = input("O.B.S: ")
    graph_buffer = plot_graph(tempo_total, tensao_total, titulo, modelo, t_graph)
    generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo_total, tensao_total, observacao, graph_buffer, ad, num_ad, t_graph)

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import os
import time

def generate_pdf(nome, fabricante, p_n, s_n, modelo, titulo, tempo_total, tensao_total, observacao, graph_buffer, ad, num_ad, t_graph):
    pdf_filename = f"{p_n}_{s_n}_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(72, 750, f"Equipamento: {nome}       Fabricante: {fabricante}      Modelo: {modelo} ")
    pdf.drawString(72, 735, f"P/N: {p_n}    S/N: {s_n}    AD: {ad}       AD NUMBER: {num_ad}")

    # Define o caminho da imagem com base no P/N
    pn_to_image = {
        "501-1228-01": r"C:\xampp\htdocs\GitHub\Voltage_Meter\Codigo_fonte\Imagem_1.png",
        "501-1228-03": r"C:\xampp\htdocs\GitHub\Voltage_Meter\Codigo_fonte\Imagem_1.png",
        "501-1228-05": r"C:\xampp\htdocs\GitHub\Voltage_Meter\Codigo_fonte\Imagem_1.png",
        "501-1228-02": r"C:\xampp\htdocs\GitHub\Voltage_Meter\Codigo_fonte\Imagem_2.png",
        "501-1228-04": r"C:\xampp\htdocs\GitHub\Voltage_Meter\Codigo_fonte\Imagem_2.png",
        "501-1228-06": r"C:\xampp\htdocs\GitHub\Voltage_Meter\Codigo_fonte\Imagem_2.png",
        "501-1228-07": r"C:\xampp\htdocs\GitHub\Voltage_Meter\Codigo_fonte\Imagem_2.png"
    }

    # Salva o buffer de bytes em um arquivo temporário
    temp_filename = f"{p_n}_{s_n}_{time.strftime('%Y%m%d_%H%M%S')}.png"
    with open(temp_filename, 'wb') as f:
        f.write(graph_buffer.getvalue())

    # Adiciona a imagem do gráfico ao PDF
    pdf.drawImage(temp_filename, 100, 400, width=400, height=300)

    # Verifica se o P/N está no dicionário
    if p_n in pn_to_image:
        image_name = pn_to_image[p_n]
        # Verifica se o arquivo de imagem está na mesma pasta do código

        img_height = 0  # Define um valor padrão
        if os.path.exists(image_name):
            img = Image.open(image_name)
            img_width, img_height = img.size  # Atualiza o valor de img_height se a imagem existir
            pdf.drawImage(image_name, 100, 50, width=400, height=300)
            observacao_y = 720
        else:
            print(f"Imagem {image_name} não encontrada na pasta do código.")
    else:
        print(f"P/N {p_n} não encontrado no dicionário de imagens.")
        observacao_y = 390

    # Adiciona as observações ao PDF
    pdf.drawString(72, observacao_y, f"Observações: {observacao}")

    pdf.save()
    print("PDF Gerado.")

    # Remover o arquivo temporário após salvar o PDF
    os.unlink(temp_filename)

run_experiment()




        

            
       
