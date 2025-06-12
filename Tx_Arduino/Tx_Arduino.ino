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
  delay(100); 
  Serial.println("Arduino Ready"); 
  }

void loop() {
  if (Serial.available()) {
    command=Serial.readStringUntil('\n'); 
    command.trim();
    
    if (command==SYNC_REQUEST){
      // Sync Requests
      Serial.print(SYNC_OK);
      Serial.print(numChannels);
      Serial.println("#");
    } else if (command==START_STREAM) {
      // Start Stream
      isStreaming=true;
      Serial.println("Streaming Started");
    } else if (command==STOP_STREAM) {
      // Stop Stream
      isStreaming=false;
      Serial.println("Streaming Stopped");
    }
  }

  // Serial.println(isStreaming);
  
  if (isStreaming) {
    Serial.println("hello world");
    delay(100);
  }
}
