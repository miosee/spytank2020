#include "motor.h"


Motor moteurGauche(9, 8, 7);
Motor moteurDroit(10, 11, 12);


#define CMD_PIN_MODE      1
#define CMD_DIGITAL_READ  2
#define CMD_DIGITAL_WRITE 3
#define CMD_ANALOG_READ   4
#define CMD_ANALOG_WRITE  5
#define CMD_MOTEURS       6
#define CMD_DISTANCE      7


void setup() {
  // Initialisation des moteurs
  moteurGauche.begin();
  moteurDroit.begin();
  // Initialisation de la communication
  Serial.begin(9600);
}

uint8_t distanceRead(uint8_t trigger, uint8_t echo, uint8_t maxCm);

void loop() {
  uint8_t cmd, pin, value, trigger, echo;
  int8_t gauche, droit;
  uint8_t analogOutValue;
  uint16_t analogInValue;
  uint8_t tmp;

  if (Serial.available() > 0) {   // Si on a reçu un octet par le posrt serie
    cmd = Serial.read();          // on le lit
    Serial.write(cmd);            // on le renvoit pour indiquer qu'on l'a bien reçu
    if (cmd == CMD_PIN_MODE) {
      while (Serial.available() == 0) {}              // On attend de recevoir le 1er parametre
      pin = Serial.read();                            // On le lit
      Serial.write(pin);                              // On le renvoit pour indiquer qu'on l'a bien reçu
      if ((pin >= 2) && (pin <= 21)) {                // on vérifie sa valeur. Si elle est correcte,
        while (Serial.available() == 0) {}            // On attend le 2ème parametre
        value = Serial.read();                        // on le lit
        Serial.write(value);                          // On le renvoit pour indiquer qu'on l'a bien reçu
        if ((value == INPUT) || (value == OUTPUT)) {  // on vérifie sa valeur. Si elle est correcte,
          pinMode(pin, value);                        // on exécute la commande
        }
      }
    }
    else if (cmd == CMD_DIGITAL_WRITE) {
      while (Serial.available() == 0) {}              // On attend de recevoir le 1er parametre
      pin = Serial.read();                            // On le lit
      Serial.write(pin);                              // On le renvoit pour indiquer qu'on l'a bien reçu
      if ((pin >= 2) && (pin <= 21)) {                // on vérifie sa valeur. Si elle est correcte,
        while (Serial.available() == 0) {}            // On attend le 2ème parametre
        value = Serial.read();                        // On le lit
        Serial.write(value);                          // On le renvoit pour indiquer qu'on l'a bien reçu
        if ((value == LOW) || (value == HIGH)) {      // on vérifie sa valeur. Si elle est correcte,
          digitalWrite(pin, value);                   // on exécute la commande
        }
      }
    }
    else if (cmd == CMD_DIGITAL_READ) {
      while (Serial.available() == 0) {}              // On attend de recevoir le parametre
      pin = Serial.read();                            // On le lit
      Serial.write(pin);                              // On le renvoit pour indiquer qu'on l'a bien reçu
      if ((pin >= 2) && (pin <= 21)) {                // on vérifie sa valeur. Si elle est correcte,
        Serial.write(digitalRead(pin));               // on exécute la commande
      }
    }
    else if (cmd == CMD_ANALOG_WRITE) {
      while (Serial.available() == 0) {}              // On attend de recevoir le 1er parametre
      pin = Serial.read();                            // On le lit
      Serial.write(pin);                              // On le renvoit pour indiquer qu'on l'a bien reçu
      if ((pin >= 0) && (pin <= 7)) {                 // si elle est correcte,
        analogOutValue = Serial.read();               // on lit le 2ème paramètre 
        Serial.write(analogOutValue);                 // On le renvoit pour indiquer qu'on l'a bien reçu
        analogWrite(pin, analogOutValue);             // on exécute la commande (Pas besoin de tester la valeur, elles sont toutes valides)
      }
    }
    else if (cmd == CMD_ANALOG_READ) {
      while (Serial.available() == 0) {}              // On attend de recevoir le parametre
      pin = Serial.read();                            // On le lit
      Serial.write(pin);                              // On le renvoit pour indiquer qu'on l'a bien reçu
      if ((pin >= 2) && (pin <= 21)) {                // on vérifie sa valeur. Si elle est correcte,
        analogInValue = analogRead(pin);              // on exécute la commande
        tmp = (uint8_t)(analogInValue & 0x00FF);
        Serial.write(tmp);                
        tmp = (uint8_t)(analogInValue >> 8);
        Serial.write(tmp);                
      }
    }
    else if(cmd == CMD_MOTEURS) {
      while (Serial.available() == 0) {}
      gauche = Serial.read();                     // On lit le 1er paramètre et on vérifie sa valeur
      Serial.write(gauche);
      if ((gauche >= -100) && (gauche <= 100)) {  // si elle est correcte,
        while (Serial.available() == 0) {}
        droit = Serial.read();                    // on lit le 2ème paramètre et on vérifie sa valeur
        Serial.write(droit);
        if ((droit >= -100) || (droit <= 100)) {  // si elle est correcte,
          digitalWrite(13, 1);
          moteurGauche.changeVitesse(gauche*2.55);     // on exécute la commande
          moteurDroit.changeVitesse(droit*2.55);
        }
      }
    }
    else if(cmd == CMD_DISTANCE) {
      while (Serial.available() == 0) {}              // On attend de recevoir le 1er parametre
      trigger = Serial.read();                        // On le lit
      Serial.write(trigger);                          // On le renvoit pour indiquer qu'on l'a bien reçu
      if ((trigger >= 2) && (trigger <= 21)) {                // on vérifie sa valeur. Si elle est correcte,
        while (Serial.available() == 0) {}            // On attend de recevoir le 1er parametre
        echo = Serial.read();                         // On le lit
        Serial.write(echo);                           // On le renvoit pour indiquer qu'on l'a bien reçu
        if ((echo >= 2) && (echo <= 21)) {              // on vérifie sa valeur. Si elle est correcte,
          Serial.write(distanceRead(trigger, echo, 250));          // on exécute la commande
        }
      }
    }
  }
}


uint32_t lastEnterTime = 0;
uint32_t _measureValue = 0;

uint32_t measure(uint8_t trigger, uint8_t echo, uint32_t timeout) {
  uint32_t duration;
  
  if(millis() - lastEnterTime > 60) {
    lastEnterTime = millis();

    digitalWrite(trigger, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigger, LOW);
    duration = pulseIn(echo, HIGH, timeout);
    _measureValue = duration;
  }
  else {
    duration = _measureValue;
  }
  return(duration);
}


uint8_t distanceRead(uint8_t trigger, uint8_t echo, uint8_t maxCm) {
  uint32_t distance;
  
  distance = measure(trigger, echo, maxCm * 55 + 200);
  if (distance == 0) {
    distance = 255 * 58;
  }
  return( (uint8_t)(distance / 58));
}
