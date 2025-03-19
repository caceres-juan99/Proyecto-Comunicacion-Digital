#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <DallasTemperature.h>
#include <OneWire.h>
#include <RF24.h>

RF24 radio(8, 10); // CE, CSN
const byte address[6] = "00001";

Adafruit_BMP280 bmp;

float ALTITUD, P0;

const int MPU_addr=0x68;  // Direccion del sensor MPU6050 en el bus I2C
int16_t AcX, AcY, AcZ, GyX, GyY, GyZ, temperatura;

#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

float datos[8] = {0}; // Arreglo para almacenar los datos

void setup()
{
  Serial.begin(115200);  // Inicializar la comunicación serial a 9600 baudios
  Serial.println("Enviando...");
  Wire.begin();        // Inicializar el bus I2C
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);     // PWR_MGMT_1 register
  Wire.write(0);        // Setear en 0 para activar el sensor
  Wire.endTransmission(true);

  radio.begin();
  radio.openWritingPipe(address);
  radio.setChannel(90);
  radio.setDataRate(RF24_2MBPS);
  radio.setPALevel(RF24_PA_MAX);


  if (!bmp.begin()){
    Serial.println("BMP280 no encontrado !");
    while (1);
  }
  P0 = bmp.readPressure()/100;
}

void loop()
{
  Wire.beginTransmission(MPU_addr); // Iniciar la comunicación con el MPU6050
  Wire.write(0x3B);                 // Direccion del registro donde comienza la lectura
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr, 14, true); // Leer 14 bytes de datos

  AcX = Wire.read()<<8 | Wire.read();   // Leer los valores del acelerometro
  AcY = Wire.read()<<8 | Wire.read();
  AcZ = Wire.read()<<8 | Wire.read();
  GyX = Wire.read()<<8 | Wire.read();   // Leer los valores del giroscopio
  GyY = Wire.read()<<8 | Wire.read();
  GyZ = Wire.read()<<8 | Wire.read();

  ALTITUD = bmp.readAltitude(P0);

  sensors.requestTemperatures();  // Solicitar la temperatura al sensor DS18B20
  float temperatura = sensors.getTempCByIndex(0);  // Obtener la temperatura en grados Celsius

  datos[0] = AcX;
  datos[1] = AcY;
  datos[2] = AcZ;
  datos[3] = GyX;
  datos[4] = GyY;
  datos[5] = GyZ;
  datos[6] = ALTITUD;
  datos[7] = temperatura;

  radio.write(datos, sizeof(datos));

  delay(10); // Esperar 10 milisegundos antes de tomar otra muestra
}