//
// Código Arduino para ler dados de um sensor de tensão a cada 30 segundos e enviar pela porta serial
// Atualização: 12/03/2024
//
// Dev: Náthally Lima Arruda 
// e-mail: nathallylym@gmail.com
//
//
//

void setup() {
  Serial.begin(9600); // Configura;'ao da porta serial com taxa de 9600 bps
}

void loop() {
  // Lê o valor do sensor de tensão
  int valorSensor = analogRead(A1);

  // Converte o valor para a faixa de tensão real usando o divisor de tensão
  // Valor dos resistores: 10K ohms para R1 e R2
  // Valor lido * (5V/1023) = tensão em volts
  float tensao = (float)valorSensor * (5.0/1023.0) * (10000.0 + 10000.o) / 10000.0;

  // Envio de dados pela porta serial
  Serial.print(millis()) // Tempo
  Serial.print (",");
  Serial.println(tensao); // Tensão

  delay(30000; // Espera 30 segundos antes da próxima leitura
}
