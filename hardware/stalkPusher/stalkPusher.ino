#include "ADS1115.h"
#include "SFE_LSM9DS0.h"
#include "Adafruit_GPS.h"

#include <SoftwareSerial.h>
#include <Wire.h>
#include "Adafruit_AM2315.h"
//#include <Adafruit_ADS1015.h>
//#include <Adafruit_LSM9DS0.h>
//#include <Adafruit_Sensor.h>

SoftwareSerial mySerial(3, 2);

Adafruit_GPS GPS(&mySerial);
Adafruit_AM2315 am2315;
ADS1115 adsLoadXPot(0x48);
ADS1115 adsLoadY(0x4A);
//Adafruit_LSM9DS0 lsm(1000);

#define LSM9DS0_XM  0x1D // Would be 0x1E if SDO_XM is LOW
#define LSM9DS0_G   0x6B 
LSM9DS0 lsm(MODE_I2C, LSM9DS0_G, LSM9DS0_XM);

#define GPSECHO false
#define GRAVITY (9.80665F)
//#define LSM9DS0_ACCEL_MG_LSB_2G (0.061F)
//#define LSM9DS0_GYRO_DPS_DIGIT_245DPS (0.00875F)
//#define LSM9DS0_GYRO_DPS_DIGIT_245DPS      (0.00875F)


boolean single = false;
boolean usingInterrupt = true;
//boolean streaming = false;
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy
void getGPS(boolean GPSLocation = true, boolean GPSTime = true);
void getAM2315TempHumidity(boolean AM2315Temperature = true, boolean AM2315Humidity = true);
float kalmanCalculate(float, float, double, float);
//const int MPU = 0x68; // I2C address of the MPU-6050
float AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
char inByte;
float temperature;
float humidity;
float QAngle  =  0.001;
float QGyro   =  0.003;
float RAngle  =  0.03;
float xBias = 0;
float P0 = 0;
float P1 = 0;
float P2 = 0;
float P3 = 0;
float y, S;
float K0, K1;
float xAngle = 0;
float yAngle = 0;
float pi = 3.141696;
uint32_t timer;
uint32_t streamTimer;

int dataIndex = 0;
char dataInputBuffer[10];
bool start;
bool parse;
bool readCommand;
bool toStream;
bool toPerCall;
bool sendTime;
bool sendTimeStamp;
bool sendAngle;
bool sendForce;
bool sendTemp;
bool sendHumidity;
bool sendLocation;
bool sendAll;
bool liveFeed;

String command;
int stringLength;
String value;

void reader (bool, bool, char, const char);
void parser (String, String, char, int);
void prepareData (const String&, const char[], String&, int&);
void sendData (const String&, int&);

void setup() {
  Serial.begin(19200);
  
  //initialize boolean variables
  readCommand = false;
  start = false;
  parse = false;
  toStream = false;
  
  GPS.begin(9600);
  if (! am2315.begin()) {
    Serial.println("Temperature and Humidity Sensor not Found");
  }
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);

  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

  useInterrupt(true);

  //delay(1000);
  // Ask for firmware version
  mySerial.println(PMTK_Q_RELEASE);
//  Wire.begin();
//  Wire.beginTransmission(MPU);
//  Wire.write(0x6B); // PWR_MGMT_1 register
//  Wire.write(0); // set to zero (wakes up the MPU-6050)
//  Wire.endTransmission(true);
  timer = micros();
  streamTimer = millis();
//  ads.setGain(GAIN_TWO);
  adsLoadXPot.initialize();
  adsLoadXPot.setGain(ADS1115_PGA_6P144);
  adsLoadXPot.setRate(ADS1115_RATE_860);
//  adsLoadXPot.begin();
//  adsPot.setGain(GAIN_ONE);
//  adsLoadY.begin();
  adsLoadY.initialize();
  adsLoadY.setGain(ADS1115_PGA_6P144);
  adsLoadY.setRate(ADS1115_RATE_860);
//  lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_2G);
//  lsm.setupMag(lsm.LSM9DS0_MAGGAIN_2GAUSS);
//  lsm.setupGyro(lsm.LSM9DS0_GYROSCALE_245DPS);
  if(! lsm.begin()){
    Serial.println("IMU not Found");
  }
  delay(100);
  Serial.println("%RDDYRECE$");
}

void loop() {
  // put your main code here, to run repeatedly:
  char theChar;
  command = ""; //reset command
  value = ""; //reset value of command
  if (Serial.available()) {
    theChar = Serial.read();
    reader(start, parse, dataInputBuffer, theChar);
    if (parse) {
      parser(command, value, dataInputBuffer, dataIndex);
      parse = false;
      readCommand = true;
    }
  }
  if (readCommand) {
    Serial.println("%" + command + "RECE" + "$");
    if (command == "PCLL") {
      if (value == "0000") {
        sendTimeStamp = true;
        sendTemp = true;
        sendLocation = true;
        sendHumidity = true;
      }
      if (value.charAt(3) == '1') {
        sendTemp = true;
      }
      if (value.charAt(2) == '1') {
        sendHumidity = true;
      }
      if (value.charAt(1) == '1') {
        sendLocation = true;
      }
      if (value.charAt(0) == '1') {
        sendTimeStamp = true;
      }
      toPerCall = true;
    }
    if (command == "LIVE"){
      liveFeed = true;
    }
    if (command == "STRM") {
      toStream = true;
      GPS.standby();
      if (value == "0000") {
        sendForce = true;
        sendAngle = true;
        sendTime = true;
      }
      if (value.charAt(3) == '1') {
        sendForce = true;
      }
      if (value.charAt(2) == '1') {
        sendAngle = true;
      }
      if (value.charAt(1) == '1') {
        sendTime = true;
      }
    }
    if (command == "STOP") {
      toStream = false;
      liveFeed = false;
      GPS.wakeup();
    }
    readCommand = false;
  }
  if (toStream) {
    streaming();
  }
  else {
    resetStreamBool();
  }
  if (toPerCall) {
    perCall();
  }
  if (liveFeed){
    streamFeed();
  }
  updateAngleKalman();
}
