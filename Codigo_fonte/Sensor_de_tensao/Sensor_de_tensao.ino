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
