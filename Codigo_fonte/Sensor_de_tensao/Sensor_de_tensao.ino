//
// Código Arduino para ler dados de um sensor de tensão a cada 30 segundos e enviar pela porta serial
// Data: 11/03/2024
//
// Dev: Náthally Lima Arruda 
// e-mail: nathallylym@gmail.com
//
//
//

void setup() {
  Serial.begin(9600); // Configuração da porta serial com taxa de 9600 bps
}

void loop() {
  // Lê o valor do sensor de tensão 
  int valorSensor = analogRead(A11);

  // Converte o valor para a faixa de tensão real usando o divisor de tensão
  // Considerando resistores de 1k ohms para R1 e R2
  // Valor lido * (5V / 1023) = tensão em volts
  float tensao = (float)valorSensor/ 36.53571;
                                                                                                     
  // Envio dos dados pela porta serial
  Serial.print(millis()); // Tempo
  Serial.print(",");
  Serial.println(tensao); // Tensão

  delay(1000); // Aguarda 1 segundos antes da próxima leitura
}
