#include <SPI.h>
#include <RF24.h>

RF24 radio(8, 10); // CE, CSN
const byte address[6] = "00001";

float datos[8] = {0}; // Arreglo para almacenar los datos

void setup()
{
  Serial.begin(115200);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setChannel(90);
  radio.setDataRate(RF24_2MBPS);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening(); 
  // Limpia el buffer del puerto serie
  Serial.flush();
}

void loop()
{
  if (radio.available())
  {
    radio.read(datos, sizeof(datos));

    for (int i = 0; i < sizeof(datos) / sizeof(datos[0]); i++)
    {
      Serial.print(datos[i]);
      if (i < sizeof(datos) / sizeof(datos[0]) - 1)
      {
        Serial.print(",");
      }
    }

    Serial.println(); // Saltar a la siguiente línea después de imprimir todos los datos
  }
  delay(10);
}