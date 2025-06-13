/*
  Arduino code for UART communication with Python GUI
*/

#include <MPU9250.h>

const String SYNC_REQUEST = "#?#";
const String SYNC_OK="#!#";

const String START_STREAM = "#A#";
const String STOP_STREAM = "#S#";
const String DATA_STREAM = "#D#";

String command;

const int numChannels=3;
bool isStreaming=false;

MPU9250 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  delay(2000); 

  if (!mpu.setup(0x68)) {
    while (1) {
        Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
        delay(5000);
    }
  }

  Serial.println("Arduino Ready");
}

void loop() {
  // Handle incoming commands from Python
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();

    if (command == SYNC_REQUEST){
      Serial.print(SYNC_OK);
      Serial.print(numChannels);
      Serial.println("#");
    } else if (command == START_STREAM) {
      isStreaming = true;
      Serial.println("Streaming Started");
    } else if (command == STOP_STREAM) {
      isStreaming = false;
      Serial.println("Streaming Stopped");
    }
  }

  // Continuously update MPU data
  if (mpu.update()) {
   
  } else {
    delay(1); // A small delay to prevent busy-waiting
  }

  // Transmit data only if streaming is active
  if (isStreaming) {
    static uint32_t prev_transmit_ms = millis();
    if (millis() - prev_transmit_ms >= 100) {
      transmit_r_p_y();
      prev_transmit_ms = millis();
    }
  }
}

void transmit_r_p_y() {
  int count=0;
  Serial.print(DATA_STREAM);
  count += Serial.print(mpu.getYaw(), 0);
  Serial.print("#");
  count += Serial.print(mpu.getPitch(), 0);
  Serial.print("#");
  count += Serial.print(mpu.getRoll(), 0);
  Serial.print("#");
  Serial.print(count);
  Serial.println("#");
}

