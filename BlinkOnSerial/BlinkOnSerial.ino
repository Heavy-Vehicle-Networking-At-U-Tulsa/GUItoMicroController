/*
  Blink
  Turns on an LED on and off repeatedly.
  Written for a Teensy 3 USB development board
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led_pin = 13;


//create a varaible to adjust the milliseconds between flashes.
int blink_pause = 100;
bool led_state = 0;

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
    blink_pause = Serial.parseInt();
  } 
  if (blink_timer >= blink_pause){
    blink_timer = 0;
    led_state = !led_state; //Change the State of the LED
    digitalWrite(led_pin, led_state); //Write the new state 
  }
  if (report_timer >= 200){
    report_timer = 0;
    Serial.println(blink_pause);
  }
}
