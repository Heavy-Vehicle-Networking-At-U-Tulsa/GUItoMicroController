/*
  Blink
  Turns on an LED on and off repeatedly.
  Written for a Teensy 3 USB development board
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led_pin = 13;
int blink_pause;

//create a varaible to adjust the milliseconds between flashes.
String commandVal;
bool led_state = 0;
bool LEDEnabled = true;

elapsedMillis blink_timer;
elapsedMillis report_timer;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(led_pin, OUTPUT);  
  Serial.setTimeout(10); //reduce the timeout from the normal 1000 milliseconds
}

// the loop routine runs over and over again forever:
void loop() {
  while (Serial.available() > 0) {
    // look for the next valid integer in the incoming serial stream:
    commandVal = Serial.readStringUntil('\n');
    if (commandVal == "OFF") {
      LEDEnabled = false;
      digitalWrite(led_pin, LEDEnabled);
    }
    else if (commandVal == "ON"){
      LEDEnabled = true;
      digitalWrite(led_pin, LEDEnabled);
    }
    else {
      blink_pause = commandVal.toInt();
      blink_pause = constrain(blink_pause,20,2000);
    }
    while (Serial.available()) Serial.read(); //clear out the commands
  } 
  if ((blink_timer >= blink_pause) && LEDEnabled){
    blink_timer = 0;
    led_state = !led_state; //Change the State of the LED
    digitalWrite(led_pin, led_state); //Write the new state 
  }

  if (report_timer >= 200){
    report_timer = 0;
    Serial.println(blink_pause);
  }
}
