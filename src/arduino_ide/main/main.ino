// #include <Arduino.h>
#include "DFRobot_BloodOxygen_S.h"

#define I2C_COMMUNICATION  //use I2C for communication, but use the serial port for communication if the line of codes were masked

#ifdef  I2C_COMMUNICATION
#define I2C_ADDRESS    0x57
  DFRobot_BloodOxygen_S_I2C MAX30102(&Wire ,I2C_ADDRESS);
#else
/* ---------------------------------------------------------------------------------------------------------------
 *    board   |             MCU                | Leonardo/Mega2560/M0 |    UNO    | ESP8266 | ESP32 |  microbit  |
 *     VCC    |            3.3V/5V             |        VCC           |    VCC    |   VCC   |  VCC  |     X      |
 *     GND    |              GND               |        GND           |    GND    |   GND   |  GND  |     X      |
 *     RX     |              TX                |     Serial1 TX1      |     5     |   5/D6  |  D2   |     X      |
 *     TX     |              RX                |     Serial1 RX1      |     4     |   4/D7  |  D3   |     X      |
 * ---------------------------------------------------------------------------------------------------------------*/
#if defined(ARDUINO_AVR_UNO) || defined(ESP8266)
SoftwareSerial mySerial(4, 5);
DFRobot_BloodOxygen_S_SoftWareUart MAX30102(&mySerial, 9600);
#else
DFRobot_BloodOxygen_S_HardWareUart MAX30102(&Serial1, 9600); 
#endif
#endif

const int heartPin = A1;
const int gsrPin = A2;

void setup() {
  Serial.begin(115200);

  while (false == MAX30102.begin())
  {
    Serial.println("init fail!");
    delay(1000);
  }
  Serial.println("init success!");
  Serial.println("start measuring...");
  MAX30102.sensorStartCollect();
}

void loop() {
  /*
  // ECG Readings
  int heartValue = analogRead(heartPin);
  Serial.println(heartValue);
  delay(5);
  */

  // GSR Readings
  /*
  long gsrSensorSum = 0;
  for(int i = 0; i < 10; i++) {          //Average the 10 measurements to remove the glitch
      gsrSensorSum += analogRead(gsrPin);
      delay(5);
  }
  int gsrSensorAverage = gsrSensorSum/10;

  Serial.print(">gsr:");
  Serial.println(gsrSensorAverage);

  float resistance = ((4096+2*gsrSensorAverage)*10000)/(2048-gsrSensorAverage);
  Serial.print(">resistance:");
  Serial.println(resistance);
  */

  // PPG Demo
  MAX30102.getHeartbeatSPO2();
  Serial.print("SPO2 is : ");
  Serial.print(MAX30102._sHeartbeatSPO2.SPO2);
  Serial.println("%");
  Serial.print("heart rate is : ");
  Serial.print(MAX30102._sHeartbeatSPO2.Heartbeat);
  Serial.println("Times/min");
  Serial.print("Temperature value of the board is : ");
  Serial.print(MAX30102.getTemperature_C());
  Serial.println(" ℃");
  //The sensor updates the data every 4 seconds
  delay(1000);
  //Serial.println("stop measuring...");
  //MAX30102.sensorEndCollect();
}
