//
// Código Arduino para ler dados de um sensor de tensão a cada 30 segundos e enviar pela porta serial
// Data: 11/03/2024
//
// Dev: Náthally Lima Arruda 
// e-mail: nathallylym@gmail.com
//
//
//

//Possível alteração: alterar o circuito para um divisor de tensão
void setup() {
  Serial.begin(9600); // Configuração da porta serial com taxa de 9600 bps
}

void loop() {
  // Lê o valor do sensor de tensão (entrada A1)
  int valorSensor = analogRead(A1);

  // Converte o valor para a faixa de tensão (0-5V)
  float tensao = valorSensor * (5.0 / 1023.0);

  // Envio dos dados pela porta serial
  Serial.print(millis()); // Tempo
  Serial.print(",");
  Serial.println(tensao); // Tensão

  delay(30000); // Aguarda 30 segundos antes da próxima leitura
}
