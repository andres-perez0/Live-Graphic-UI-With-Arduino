'''
    This file was made to test out talking to an arduino;
    Serial communication was something I am still learning with this project
    But it has been fun
'''

import serial
import time

## Port Infomartion
SERIAL_PORT="COM3"
BAUD_RATE=115200
TIMEOUT=0.1

## Serial Communication Statements
SYNC_REQUEST = "#?#\n"
SYNC_OK_PREFIX = "#!#"
START_STREAM = "#A#\n"
STOP_STREAM = "#S#\n"

def main():
    # try-except statements are key
    try: 
        # Connects to the arduino serial port and waits until the arduino sends the ready message
        arduino=serial.Serial(port=SERIAL_PORT,baudrate=BAUD_RATE,timeout=TIMEOUT)
        while True:
            line=arduino.readline().decode('utf-8').strip()
            if line == "Arduino Ready":
                print(f"Arduino says: {line}")
                break
            elif line:
                print(f"Arduino says: {line}")
            else:
                pass
            time.sleep(0.1)

        print(f"Sending START_STREAM command: {START_STREAM.strip()}")
        arduino.write(START_STREAM.encode('utf-8'))

        output_line = arduino.readline().decode('utf-8').strip()

        print(f"Arduino says: {output_line}")

        while True:
            try:
                output_line = arduino.readline().decode('utf-8').strip()
                if output_line:
                    print(f"Arduino says: {output_line}")
            except KeyboardInterrupt:
                print(f"User Stopped. Sending STOP_STREAM command: {START_STREAM.strip()}")
                arduino.write(STOP_STREAM.encode('utf-8'))
                print("Steam Stopped")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
    except serial.SerialException as e:
        print(f"Error connecting to serial port: {e}")
        print("Please ensure the Arduino is connected and the correct COM port is selected.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
   

if __name__ == "__main__":
    main()