/*
  Button

  Turns on and off a light emitting diode(LED) connected to digital pin 13,
  when pressing a pushbutton attached to pin 2.

  The circuit:
  - LED attached from pin 13 to ground through 220 ohm resistor
  - pushbutton attached to pin 2 from +5V
  - 10K resistor attached to pin 2 from ground

  - Note: on most Arduinos there is already an LED on the board
    attached to pin 13.

  created 2005
  by DojoDave <http://www.0j0.org>
  modified 30 Aug 2011
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Button
*/

// constants won't change. They're used here to set pin numbers:
#import <Keyboard.h>

const int buttonPin = 2;  // the number of the pushbutton pin
const int reedPin = 3;
const int ledPin = 9;
int incomingByte;

// variables will change:
int buttonState = 0;  // variable for reading the pushbutton status
int reedState;
int DL = 300;

void setup() {
  Serial.begin(115200);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  pinMode(reedPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
}
   
void loop() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  reedState = digitalRead(reedPin);
 
  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    Keyboard.press(0x20);
    Serial.println("BUTTON DOWN");
    delay(DL);

  }
  else {
    Keyboard.release(0x20);
  }


  if (reedState == HIGH) {
    Serial.println("TOP OPEN");
    delay(DL);
  } 

  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    if (incomingByte == '1') {
      digitalWrite(ledPin, HIGH);
    }
    if (incomingByte == '0') {
      digitalWrite(ledPin, LOW);
    }
  }
}