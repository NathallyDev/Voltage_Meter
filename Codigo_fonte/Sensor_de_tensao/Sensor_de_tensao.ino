//
// Código Arduino para ler dados de um sensor de tensão a cada 1segundos e enviar pela porta serial
// Data: 21/03/2024
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
  // Lê o valor do sensor de tensão do sensor
  int valorSensor = analogRead(A11);

  // Valor lido / Valor de conversão (Valor do arduino convertido para valor real)
  float tensao = (float)valorSensor/ 36.53571;
                                                                                                     
  // Envio dos dados pela porta serial
  Serial.print(millis()); // Tempo
  Serial.print(",");
  Serial.println(tensao); // Tensão

  delay(1000); // Aguarda 1 segundos entre as leituras
}
