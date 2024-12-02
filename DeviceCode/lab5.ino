#include "Adafruit_GPS.h"
#include "PulseOximeter.h"
#include "MQ135.h"

//Initialize Pulse Oxi Variables
#define PULSE_OXI_PIN 2

//Initialize Temperature Sensor Variables
const int lm35_pin = A1;
int temp_adc_val;
float temp_val;

//Initialize Air Quality Sensor Variables
const int air_quality_pin = A0;
float ppm;

//Initialize GPS Variables
string gpsResult;



PulseOximeter pox;
Adafruit_GPS GPS;
MQ135 gasSensor = MQ135(air_quality_pin);


void setup() {
    Serial.begin(9600);
    pinMode(PULSE_OXI_PIN, INPUT);
}


void loop() {
    temp_adc_val = analogRead(lm35_pin);	/* Read Temperature */
    temp_val = (temp_adc_val * 4.88);	/* Convert adc value to equivalent voltage */
    temp_val = (temp_val/10);	/* LM35 gives output of 10mv/°C */
    Serial.print("Temperature = ");
    Serial.print(temp_val);
    Serial.println(" Degree Celsius");

    ppm = gasSensor.getPPM();
    Serial.print("C02 in air: ");
    Serial.print(ppm);
    Serial.println("ppm");

    if (Serial.available() > 0) {	
        gpsResult = GPS.read();
        Serial.print("GPS Result: ");
        Serial.println(gpsResult);
    } 
    else {
        Serial.println("GPS Not Available");
    }

    if (pox.begin()) {
        string oximeterResult = pox.getHeartRate();
        Serial.print("Poximeter Heartrate: ");
        Serial.println(oximeterResult);

        Serial.print("Poximeter SpO2: ");
        Serial.println(pox.getSpO2());
    } 
    else { 
        Serial.println("Poximeter Reading Not Available");
    }
    
    
    delay(1000);

}

