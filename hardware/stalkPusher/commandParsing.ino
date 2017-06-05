
void resetStreamBool() {
  sendTime = false;
  sendAngle = false;
  sendForce = false;
  sendAll = false;
}

//void stopFeed(){
//  
//}

void streamFeed(){
    String dataToSend = "";
    int dataLength = 0;
    prepareData(String(getTime()), "MI", dataToSend, dataLength);
    prepareData(String(getAngleIMU()), "AI", dataToSend, dataLength);
    prepareData(String(getAnglePot()), "AP", dataToSend, dataLength);
    if (single){
      prepareData(String(getForce()), "FO", dataToSend, dataLength);
    }
    else{
      prepareData(String(getForceX()), "FX", dataToSend, dataLength);
      prepareData(String(getForceY()), "FY", dataToSend, dataLength);
    }
    prepareData(String(getTimeStamp()), "TI", dataToSend, dataLength);
    prepareData(String(getLocation()), "LO", dataToSend, dataLength);
    prepareData(String(getTemp()), "TE", dataToSend, dataLength);
    prepareData(String(getHumidity()), "HU", dataToSend, dataLength);
    sendData(dataToSend, dataLength);
    delay(10);
}

void streaming() {
  String dataToSend = "";
  int dataLength = 0;
//  String value = "0000";
//  float start = millis();
  if (sendAll){
    prepareData(String(getTime()), "MI", dataToSend, dataLength);
    prepareData(String(getAngleIMU()), "AI", dataToSend, dataLength);
    prepareData(String(getAnglePot()), "AP", dataToSend, dataLength);
    if (single){
      prepareData(String(getForce()), "FO", dataToSend, dataLength);
    }
    else{
      prepareData(String(getForceX()), "FX", dataToSend, dataLength);
      prepareData(String(getForceY()), "FY", dataToSend, dataLength);
    }
    prepareData(String(getTimeStamp()), "TI", dataToSend, dataLength);
    prepareData(String(getLocation()), "LO", dataToSend, dataLength);
    prepareData(String(getTemp()), "TE", dataToSend, dataLength);
    prepareData(String(getHumidity()), "HU", dataToSend, dataLength);
    delay(10);
  }else{

  if (sendTime) {
    prepareData(String(getTime()), "MI", dataToSend, dataLength);
  }
//  float endTime = millis();
//  Serial.println(start-endTime);
//  start = millis();
  if (sendAngle) {
    prepareData(String(getAngleIMU()), "AI", dataToSend, dataLength);
    prepareData(String(getAnglePot()), "AP", dataToSend, dataLength);
  }
//  endTime = millis();
//  Serial.println(start-endTime);
//  start = millis();
  if (sendForce) {
    if (single){
      prepareData(String(getForce()), "FO", dataToSend, dataLength);
    }
    else{
      prepareData(String(getForceX()), "FX", dataToSend, dataLength);
      prepareData(String(getForceY()), "FY", dataToSend, dataLength);
    }
  }
  }
//  endTime = millis();
//  Serial.println(start-endTime);
  //if (millis() - streamTimer  >= 10){
    sendData(dataToSend, dataLength);
//    streamTimer = millis();
  //}
}

void perCall() {
  String dataToSend = "";
  int dataLength = 0;
  String value = "0000";
  if (sendTimeStamp) {
//    Serial.println("TI");
    prepareData(String(getTimeStamp()), "TI", dataToSend, dataLength);
//    Serial.println(dataToSend);
  }
  if (sendLocation) {
//    Serial.println("LO");
    prepareData(String(getLocation()), "LO", dataToSend, dataLength);
//    Serial.println(dataToSend);
  }
  if (sendTemp) {
//    Serial.println("TE");
//    Serial.println(dataToSend);
    prepareData(String(getTemp()), "TE", dataToSend, dataLength);
//    Serial.println(dataToSend);
  }
  if (sendHumidity) {
//    Serial.println("HU");
    prepareData(String(getHumidity()), "HU", dataToSend, dataLength);
//    Serial.println(dataToSend);
  }
  sendData(dataToSend, dataLength);
  toPerCall = false;
  sendTimeStamp = false;
  sendTemp = false;
  sendHumidity = false;
  sendLocation = false;
}


void prepareData (const String& value, const char valueID[], String& dataToSend, int& dataLength) {
  dataLength = dataLength + value.length() + String(valueID).length() + 1;
  dataToSend = dataToSend + ":" + valueID + value;
}

void sendData (const String& dataToSend, int& dataLength) {
  dataLength = dataLength + 2;
  dataLength = dataLength + String(dataLength + String(dataLength).length()).length();
  Serial.print("%"); Serial.print(String(dataLength)); Serial.print(dataToSend); Serial.println("$");
}

//parser function. Parse the data buffer into command and value
void parser (String &command, String &value, char dataInputBuffer[], int stringLenth) {
  char valueBuffer[4] = {};
  int valueIndex = 0;
  for (int x = 1; x <= stringLength; x++) {
    if (x < 5) {
      command = command + dataInputBuffer[x];
    }
    else {
      valueBuffer[valueIndex] = dataInputBuffer[x];
      valueIndex++;
    }

  }
  //  Serial.println(valueBuffer);
  //  Serial.println(dataInputBuffer);
  for (int c = 0; c < 4; c++) {

    if (valueBuffer[c]) {
      value = value + valueBuffer[c];
    }
    else {
      value = '0' + value;
    }
  }
}

//reader function. Starts appending messages to a data buffer when ':' appears
void reader (bool &start, bool &parse, char dataInputBuffer[], const char &theChar) {
  if (theChar == '%') { //start reading the string if the incoming byte is '%'
    dataIndex = 0;
    start = true;
  }
  if (theChar == '$') { // if incoming byte is '$' then stop reading the string  // null terminate the string
    stringLength = dataIndex;
    if (dataIndex != 0) {
      parse = true;
    }
    dataIndex = 0;
    start = false;
  }
  else if (start) { //theChar >= 0x20 && start) {
    dataInputBuffer[dataIndex] = theChar;
    dataIndex++;
  }
}

