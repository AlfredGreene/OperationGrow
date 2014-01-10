/*
 * Arduino code for a single capacitance sensor.
 * Send data over serial to initiate a read.
 * Arduino will reply with sensed value as an ASCII number followed by a CR + LF.
 * The onboard LED will blink to show that it is working.
 * 
 * Connect pin 4 through a resistor to a bolt embedded in the soil.
 * Connect pin 8 through a resistor to foil wrapped around the planter.
 * The soil between the bolt and foil provide a capacitance that we measure.
 * You may add a stabalization capacitor between the foil and ground. (100 pF)
 * 
 * Use a high value resistor e.g. 10 megohm between send pin and receive pin.
 * Resistor effects sensitivity, experiment with values, 50 kilohm - 50 megohm.
 * Larger resistor values yield larger sensor values.
 */
 
#include <CapacitiveSensor.h>

// Pin 4 is the send pin and pin 8 is the receive pin
CapacitiveSensor cs_4_8 = CapacitiveSensor(4,8);
// Combine 30 readings
#define CAP_READ_COUNT 30

// Wait before communicating over serial or we can confuse the host
#define SERIAL_INIT_DELAY 2000 

// Onboard LED
#define LED_PIN 13

void setup()                    
{
    delay(SERIAL_INIT_DELAY);
    Serial.begin(9600);
    pinMode(LED_PIN, OUTPUT);
}

void loop()                    
{
    digitalWrite(LED_PIN, LOW);
    delay(1000);
    digitalWrite(LED_PIN, HIGH);
    delay(1000);
}

void serialEvent() {
    byte command = Serial.read();
    long result =  cs_4_8.capacitiveSensorRaw(CAP_READ_COUNT);
    Serial.println(result);
}