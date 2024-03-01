#include <Arduino.h>
#include <Wire.h>
#include "MAX30105.h"

// Define constants
int GSR_PIN = A0; // Analog pin for GSR readings
int ECG_PIN = A1; // Analog pin for ECG readings
int TEMP_PIN = A2; // Analog pin for temperature readings
int RECORDING_DELAY_BUFFER = 10; // Delay between each recording in ms
int START_INSTRUCTION = 1; 
int STOP_INSTRUCTION = 2;

int ADC_RESOLUTION = 4095;
int ADC_REF_VOLTAGE = 3300; // in mV

const int SAMPLE_WINDOW_SIZE = 4;

const bool USE_GREEN = true;

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

// Global state
bool isRecording = false;
bool connected = false;
unsigned long startTime = 0;

float ecgReadings[SAMPLE_WINDOW_SIZE];
float gsrReadings[SAMPLE_WINDOW_SIZE];
float ppgInfraredReadings[SAMPLE_WINDOW_SIZE];
float ppgRedReadings[SAMPLE_WINDOW_SIZE];
float ppgGreenReadings[SAMPLE_WINDOW_SIZE];
float temperatureReadings[SAMPLE_WINDOW_SIZE];

float sumECG = 0;
float sumGSR = 0;
float sumPPGInfrared = 0;
float sumPPGRed = 0;
float sumPPGGreen = 0;
float sumTemperature = 0;

int currentIndex = 0;

float ecgAverage = 0;
float gsrAverage = 0;
float ppgInfraredAverage = 0;
float ppgRedAverage = 0;
float ppgGreenAverage = 0;
float temperatureAverage = 0;

float readAdcVoltage(int adcPin) {
  return (analogRead(adcPin) * ADC_REF_VOLTAGE) / ADC_RESOLUTION;
}

int T1 = 0; // C
int T2 = 40; // C
int V1 = 1034; // mV
int V2 = 816; // mV
float toTemp(float voltage) {
  return T1 + ((T2 - T1)/(V2 - V1))*(voltage - V1);
}

void setup() {
  // Initialise Serial
  Serial.begin(115200);
  while (!Serial);
  Serial.println("Initializing...");

  // Initialise PPG
  if (PPG_SENSOR.begin(Wire, I2C_SPEED_FAST) == false) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30102 was not found. Please check wiring/power. ");
    while (1);
  }

  // Initialise window buffers
  for (int i = 0; i < SAMPLE_WINDOW_SIZE; i++) {
    ecgReadings[i] = 0;
    gsrReadings[i] = 0;
    ppgInfraredReadings[i] = 0;
    ppgRedReadings[i] = 0;
    temperatureReadings[i] = 0;
  }

  // PPG_SENSOR.sensorConfiguration();
  // PPG_SENSOR.setup();

  byte LED_BRIGHTNESS = (byte) 60U; //Options: 0=Off to 255=50mA
  byte SAMPLE_AVERAGE = (byte) 4U; //Options: 1, 2, 4, 8, 16, 32
  byte LED_MODE = (byte) 2U; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  byte LED_MODE_GREEN = (byte) 3U; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  int SAMPLE_RATE = 400; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int PULSE_WIDTH = 215; //Options: 69, 118, 215, 411
  int ADC_RANGE = 4096; //Options: 2048, 4096, 8192, 16384
  PPG_SENSOR.setup(LED_BRIGHTNESS, SAMPLE_AVERAGE, USE_GREEN ? LED_MODE_GREEN : LED_MODE, SAMPLE_RATE, PULSE_WIDTH, ADC_RANGE);
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

    sumECG -= ecgReadings[currentIndex];
    sumGSR -= gsrReadings[currentIndex];
    sumTemperature -= temperatureReadings[currentIndex];
    sumPPGInfrared -= ppgInfraredReadings[currentIndex];
    sumPPGRed -= ppgRedReadings[currentIndex];

    ecgReadings[currentIndex] = readAdcVoltage(ECG_PIN);
    gsrReadings[currentIndex] = readAdcVoltage(GSR_PIN);
    temperatureReadings[currentIndex] = toTemp(readAdcVoltage(TEMP_PIN));
    ppgInfraredReadings[currentIndex] = PPG_SENSOR.getIR();
    ppgRedReadings[currentIndex] = PPG_SENSOR.getRed();

    sumECG += ecgReadings[currentIndex];
    sumGSR += gsrReadings[currentIndex];
    sumTemperature += temperatureReadings[currentIndex];
    sumPPGInfrared += ppgInfraredReadings[currentIndex];
    sumPPGRed += ppgRedReadings[currentIndex];

    if (USE_GREEN) {
      sumPPGGreen -= ppgGreenReadings[currentIndex];
      ppgGreenReadings[currentIndex] = PPG_SENSOR.getGreen();
      sumPPGGreen += ppgGreenReadings[currentIndex];
    }

    currentIndex = (currentIndex + 1) % SAMPLE_WINDOW_SIZE;

    ecgAverage = sumECG / SAMPLE_WINDOW_SIZE;
    gsrAverage = sumGSR / SAMPLE_WINDOW_SIZE;
    temperatureAverage = sumTemperature / SAMPLE_WINDOW_SIZE;
    ppgInfraredAverage = sumPPGInfrared / SAMPLE_WINDOW_SIZE;
    ppgRedAverage = sumPPGRed / SAMPLE_WINDOW_SIZE;

    if (USE_GREEN) {
      ppgGreenAverage = sumPPGGreen / SAMPLE_WINDOW_SIZE;
    }

    // // Record relative time (duration)
    // Serial.print(millis() - startTime);
    // Serial.print(" ");
    
    // Record absolute time (end time)
    Serial.print(millis());
    Serial.print(" ");
    // Record ECG
    Serial.print(ecgAverage);
    Serial.print(" ");
    // Record GSR
    Serial.print(gsrAverage);
    Serial.print(" ");
    // Record PPG
    Serial.print(ppgInfraredAverage);
    Serial.print(" ");
    Serial.print(ppgRedAverage);
    Serial.print(" ");

    if (USE_GREEN) {
      Serial.print(ppgGreenAverage);
      Serial.print(" ");
    }

    Serial.print(temperatureReadings[currentIndex]);
    Serial.print("\n");

    PPG_SENSOR.nextSample();
  }

  delay(RECORDING_DELAY_BUFFER);
}

