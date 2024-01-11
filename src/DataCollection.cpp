#include <Arduino.h>
#include "Wire.h"
#include "DFRobot_MAX30102.h"

// Define constants
const int ECG_PIN = A1; // Analog pin for ECG readings
const int GSR_PIN = A2; // Analog pin for GSR readings
const int RECORDING_DELAY_BUFFER = 10; // Delay between each recording in ms
const String START_INSTRUCTION = "OOGA_BOOGA"; 
const String STOP_INSTRUCTION = "BIG_CHUNGUS";

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
DFRobot_MAX30102 PPG_SENSOR; // Connected via I2C
const byte LED_BRIGHTNESS = 70; //Options: 0=Off to 255=50mA
const byte SAMPLE_AVERAGE = SAMPLEAVG_2;
const byte LED_MODE = MODE_RED_IR;
const int SAMPLE_RATE = SAMPLERATE_1000;
const int PULSE_WIDTH = PULSEWIDTH_118;
const int ADC_RANGE = ADCRANGE_16384;

// Global state
bool isRecording = false;
unsigned long startTime = 0;

void setup() {
  Serial.begin(9600);

  // Initialise PPG
  while (!PPG_SENSOR.begin()) {
    Serial.println("Initialisation of PPG sensor failed...");
    delay(1000);
  }
  Serial.println("Initialisation success!");

  PPG_SENSOR.sensorConfiguration();
  // PPG_SENSOR.sensorConfiguration(LED_BRIGHTNESS, SAMPLE_AVERAGE, LED_MODE, SAMPLE_RATE, PULSE_WIDTH, ADC_RANGE);
}

void loop() {
  // Wait for instruction to start recording
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == START_INSTRUCTION) {
      isRecording = true;
      startTime = millis();
    } else if (command == STOP_INSTRUCTION) {
      isRecording = false;
    }
  }

  // Record data
  if (isRecording) {
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
    Serial.print(PPG_SENSOR.getIR());
    Serial.print(" ");
    Serial.print(PPG_SENSOR.getRed());
    Serial.print(" ");
    // Record temperature from PPG sensor
    Serial.print(PPG_SENSOR.readTemperatureC());
    Serial.print("\n");
  }

  delay(RECORDING_DELAY_BUFFER);
}
