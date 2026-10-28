
#include <SoftwareSerial.h>

// Bluetooth: Arduino RX, TX
// HC-05/HC-06 TXD -> D2
// HC-05/HC-06 RXD <- D7
SoftwareSerial BT(2, 7);

// Shield L298P
const int DIR_A = 12;
const int PWM_A = 10;

const int DIR_B = 13;
const int PWM_B = 11;

const int BUZZER = 4;

const int VELOCIDAD = 180;

char comando = 'S';

void setup() {
  pinMode(DIR_A, OUTPUT);
  pinMode(PWM_A, OUTPUT);
  pinMode(DIR_B, OUTPUT);
  pinMode(PWM_B, OUTPUT);

  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);

  detenerMotores();

  // Bluetooth independiente del puerto USB
  BT.begin(9600);
}

void loop() {
  while (BT.available() > 0) {
    char recibido = BT.read();

    if (recibido >= 'a' && recibido <= 'z') {
      recibido = recibido - 'a' + 'A';
    }

    switch (recibido) {
      case 'F':
        comando = 'F';
        avanzar();
        break;

      case 'B':
        comando = 'B';
        retroceder();
        break;

      case 'L':
        comando = 'L';
        girarIzquierda();
        break;

      case 'R':
        comando = 'R';
        girarDerecha();
        break;

      case 'S':
        comando = 'S';
        detenerMotores();
        break;
    }
  }
}

void avanzar() {
  motorA(-VELOCIDAD);
  motorB(-VELOCIDAD);
}

void retroceder() {
  motorA(VELOCIDAD);
  motorB(VELOCIDAD);
}

void girarIzquierda() {
  motorA(-VELOCIDAD);
  motorB(VELOCIDAD);
}

void girarDerecha() {
  motorA(VELOCIDAD);
  motorB(-VELOCIDAD);
}

void detenerMotores() {
  analogWrite(PWM_A, 0);
  analogWrite(PWM_B, 0);
}

void motorA(int velocidad) {
  digitalWrite(DIR_A, velocidad > 0 ? HIGH : LOW);
  analogWrite(PWM_A, abs(velocidad));
}

void motorB(int velocidad) {
  digitalWrite(DIR_B, velocidad > 0 ? HIGH : LOW);
  analogWrite(PWM_B, abs(velocidad));
}

