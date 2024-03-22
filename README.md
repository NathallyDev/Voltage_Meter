# Voltimeter Sensor - Sistema de Aquisição e Plotagem de Dados

Este projeto consiste em um sistema para medir e registrar dados de tensão DC de 0-28V utilizando um microcontrolador ARDUINO MEGA 2560. O script em Python recebe os dados, realiza a plotagem de gráficos e gera um PDF com as informações relevantes.

## Progresso

- Início: 07/03/2024 
- Atualização: 21/03/2024
- Status: Em andamento

## Requisitos

- Arduino 1.8.19
- Python 3.x
- Bibliotecas Python: pyserial, matplotlib, reportlab, time, io, tempfile, os, pdfkit

## Configuração e Uso

1. **Instalação de Dependências:**
   Certifique-se de ter as bibliotecas necessárias instaladas. Execute o seguinte comando para instalá-las:

   ```bash
   pip install pyserial matplotlib reportlab winshell

2. **Circuito**
   Certifica-se de possuir os componentes:

   - Arduino MEGA 2560
   - Sensor de tensão DC (Model0: 0V ~ 25V)
   - Resistores em série (1x 10K ohm)