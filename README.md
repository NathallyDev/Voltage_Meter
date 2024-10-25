# Sensor Voltímetro - Sistema de Aquisição e Plotagem de Dados

Este projeto consiste em um sistema para medir e registrar dados de tensão DC de 0-28V utilizando um microcontrolador ARDUINO MEGA 2560. O script Python recebe os dados, traça gráficos e gera um PDF com as informações relevantes.

## Progresso

- Início: 07/03/2024
- Atualização: 28/09/2024
- Status: Concluído

## Requisitos

- Arduino 1.8.19
- Python 3.x
- Bibliotecas Python: pyserial, matplotlib, reportlab, time, io, tempfile, os, pdfkit

## Configuração e uso

1. **Instalando Dependências:**
Certifique-se de ter as bibliotecas necessárias instaladas. Execute o seguinte comando para instalá-los:

```bash
pip instalar pyserial matplotlib reportlab winshell

2. **Circuito**
Certifique-se de ter os seguintes componentes:

-Arduino MEGA 2560
- Sensor de tensão DC (Modelo 0: 0V ~ 25V)
- Resistores em série (1x 10K ohm)
- Diodo 