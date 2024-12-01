#include "Adafruit_GPS.h"
#include "PulseOximeter.h"

#define PULSE_OXI_PIN 2
PulseOximeter pox;


Adafruit_GPS GPS;


void setup() {
  Serial.begin(9600);

  pinMode(PULSE_OXI_PIN, INPUT);

}
void loop() {
  if (Serial.available() > 0) {	
    string gpsResult = GPS.read();
    Serial.println("gps result");
    Serial.print(gpsResult);

    

  } else {
      Serial.print("not available");
  }

  if (pox.begin()) {
        // get the readings and print them out
      string oximeterResult = pox.getHeartRate();
      Serial.println("poximeter heartrate");
      Serial.print(oximeterResult);

      Serial.println("poximeter spO2");
      Serial.print(pox.getSpO2());
    } else { 
        // do something. Hint: you can print some messages
    }


  delay(1000);
}

