/*
  Arduino code for UART communication with Python GUI
*/

const String SYNC_REQUEST = "#?#";
const String SYNC_OK="#!#";

const String START_STREAM = "#A#";
const String STOP_STREAM = "#S#";
String command;

const int numChannels=3;
bool isStreaming=false;

void setup() {
  Serial.begin(9600);
  while(!Serial);         // Waits for serial port to connect
}

void loop() {
  if (Serial.available()) {
    command=Serial.readStringUntil('\n'); // Reads Serial port
    command.trim();                        // Elimates white space from Serial Message
    
    if (command==SYNC_REQUEST){
      // Sync Requests
      Serial.print(SYNC_OK);
      Serial.print(numChannels);
      Serial.println("#");
    } else if (command==START_STREAM) {
      // Start Stream
      isStreaming=true;
    } else if (command==STOP_STREAM) {
      // Stop Stream
      isStreaming=false;
    }

    /*
      Insert Body Code
        Implement the MPU9250   
    */

  }
  // put your main code here, to run repeatedly:

}
