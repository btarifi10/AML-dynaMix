#include <Arduino.h>
#include <Wire.h>
#include "MAX30105.h"

// Define constants
int ECG_PIN = A1; // Analog pin for ECG readings
int GSR_PIN = A2; // Analog pin for GSR readings
int RECORDING_DELAY_BUFFER = 10; // Delay between each recording in ms
int START_INSTRUCTION = 1; 
int STOP_INSTRUCTION = 2;

/*
PPG Sensor Config
Macro definition opions in sensor configuration 
sampleAverage: SAMPLEAVG_1 SAMPLEAVG_2 SAMPLEAVG_4 
               SAMPLEAVG_8 SAMPLEAVG_16 SAMPLEAVG_32
ledMode:       MODE_REDONLY  MODE_RED_IR  MODE_MULTILED
sampleRate:    SAMPLERATE_50 SAMPLERATE_100 SAMPLERATE_200 SAMPLERATE_400
               SAMPLERATE_800 SAMPLERATE_1000 SAMPLERATE_1600 SAMPLERATE_3200
pulseWidth:    PULSEWIDTH_69 PULSEWIDTH_118 PULSEWIDTH_215 PULSEWIDTH_411
adcRange:      ADCRANGE_2048 ADCRANGE_4096 ADCRANGE_8192 ADCRANGE_16384
*/
// DFRobot_MAX30102 PPG_SENSOR; // Connected via I2C
MAX30105 PPG_SENSOR; // Connected via I2C
byte LED_BRIGHTNESS = 0xFF; //Options: 0=Off to 255=50mA
byte SAMPLE_AVERAGE = 4; //Options: 1, 2, 4, 8, 16, 32
byte LED_MODE = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
int SAMPLE_RATE = 400; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
int PULSE_WIDTH = 411; //Options: 69, 118, 215, 411
int ADC_RANGE = 2048; //Options: 2048, 4096, 8192, 16384

// Global state
bool isRecording = false;
bool connected = false;
unsigned long startTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("Initializing...");

  // Initialise PPG
  if (PPG_SENSOR.begin(Wire, I2C_SPEED_FAST) == false) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30102 was not found. Please check wiring/power. ");
    while (1);
  }
  // PPG_SENSOR.sensorConfiguration();
  // PPG_SENSOR.setup();
  PPG_SENSOR.setup(LED_BRIGHTNESS, SAMPLE_AVERAGE, LED_MODE, SAMPLE_RATE, PULSE_WIDTH, ADC_RANGE);
  PPG_SENSOR.enableDIETEMPRDY();
  PPG_SENSOR.shutDown();

  Serial.println("Ready.");
}

void loop() {
  // Wait for instruction to start recording  
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command.equals("Start")) {
      isRecording = true;
      startTime = millis();
      PPG_SENSOR.wakeUp();
    } else if (command.equals("Stop")) {
      isRecording = false;
      PPG_SENSOR.shutDown();
    }
  }

  PPG_SENSOR.check();
  // Record data
  if (isRecording && PPG_SENSOR.available()) {
    // Record time
    Serial.print(millis() - startTime);
    Serial.print(" ");
    // Record ECG
    Serial.print(analogRead(ECG_PIN));
    Serial.print(" ");
    // Record GSR
    Serial.print(analogRead(GSR_PIN));
    Serial.print(" ");
    // Record PPG
    Serial.print(PPG_SENSOR.getFIFOIR());
    Serial.print(" ");
    Serial.print(PPG_SENSOR.getFIFORed());
    Serial.print(" ");
    // Record temperature from PPG sensor
    Serial.print(PPG_SENSOR.readTemperature());
    Serial.print("\n");

    PPG_SENSOR.nextSample();
  }

  delay(RECORDING_DELAY_BUFFER);
}
