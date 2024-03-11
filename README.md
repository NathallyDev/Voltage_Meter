# Voltimeter Sensor - Sistema de Aquisição e Plotagem de Dados

Este projeto consiste em um sistema para medir e registrar dados de tensão DC de 0-28V utilizando um microcontrolador ARDUINO UNO. O script em Python recebe os dados, realiza a plotagem de gráficos e gera um PDF com as informações relevantes.

## Progresso

- Início: 07/03/24 
- Status: Em andamento

## Requisitos

- Arduino 1.8.19
- Python 3.x
- Bibliotecas Python: pyserial, matplotlib, reportlab

## Configuração e Uso

1. **Instalação de Dependências:**
   Certifique-se de ter as bibliotecas necessárias instaladas. Execute o seguinte comando para instalá-las:

   ```bash
   pip install pyserial matplotlib reportlab

2. **Circuito**
   Certifica-se de possuir os componentes:

   - Arduino UNO
   - Sensor de tensão DC (Modelo )
   - Resistores em série (1x de ohm e 1x de ohm)
