#include <Servo.h>
#include <TM1637Display.h>
// TM1637 CLK and DIO pins
const byte CLK_PIN = 6;
const byte DIO_PIN = 5;
const int ledRed = 11;
const int ledGreen = 9;
const int buzzerPin = 12;
const int servoPin = 7;

// Create display object
TM1637Display display(CLK_PIN, DIO_PIN);
// Word: "HEy"
const byte word_hey[] = {
  SEG_B | SEG_C | SEG_E | SEG_F | SEG_G,           // H
  SEG_A | SEG_D | SEG_E | SEG_F | SEG_G,           // E
  SEG_B | SEG_C | SEG_D | SEG_F | SEG_G,           // y
  0x00                                             // blank
};
// Word: "byE"
const byte word_bye[] = {
  SEG_C | SEG_D | SEG_E | SEG_F | SEG_G,           // b
  SEG_B | SEG_C | SEG_D | SEG_F | SEG_G,           // y
  SEG_A | SEG_D | SEG_E | SEG_F | SEG_G,           // E
  0x00                                             // blank
};
// Word: "3"
const byte word_three[] = {
  SEG_A | SEG_B | SEG_C | SEG_D | SEG_G,           // 3
  0x00,                                             // blank
  0x00,                                             // blank
  0x00,                                             // blank
};
// Word: "2"
const byte word_two[] = {
  0x00,                                             // blank
  SEG_A | SEG_B | SEG_D | SEG_E | SEG_G,           // 2
  0x00,                                             // blank
  0x00,                                             // blank
};
// Word: "1"
const byte word_one[] = {
  0x00,                                             // blank
  0x00,                                             // blank
  SEG_B | SEG_C,                                   // 1
  0x00,                                             // blank
};
// Word: "run"
const byte word_run[] = {
  SEG_E | SEG_G,                   // r
  SEG_C | SEG_E | SEG_D,           // u
  SEG_C | SEG_E | SEG_G,           // n
  0x00                             // blank
};
// Display a word on the 4-digit display
void showWord(const byte word[]) {
  display.setSegments(word);
}

Servo doorServo;

void setup() {
  display.setBrightness(7);
  Serial.begin(9600);

  pinMode(ledRed, OUTPUT);
  pinMode(ledGreen, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  doorServo.attach(servoPin);
  doorServo.write(0); // Start in locked position
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');

    if (command == "pass") {
      handlePass();
    } 
    else if (command == "fail") {
      handleFail();
    }
  }
}

void handlePass() {
  digitalWrite(ledRed, LOW);
  digitalWrite(ledGreen, HIGH);
  doorServo.write(90);    // Unlock
  playPositiveChime();
  showWord(word_hey);
  delay(5000); 
  display.clear();
  delay(500);
  showWord(word_bye);           
  doorServo.write(0);     // Lock again
  digitalWrite(ledRed, HIGH);
  digitalWrite(ledGreen, LOW);
  delay(3000);
  display.clear();
}

void handleFail() {
  digitalWrite(ledRed, HIGH);
  doorServo.write(0);     // Ensure it's locked
  playNegativeChime();
  intruder();
}

void intruder() {
  showWord(word_three);
  delay(3000);
  display.clear();
  showWord(word_two);
  delay(3000);
  display.clear();
  showWord(word_one);
  delay(3000);
  display.clear();
  delay(500);
  showWord(word_run);
  delay(5000);
  display.clear();
}

void playPositiveChime() {
  tone(buzzerPin, 880, 200);  
  delay(250);
  tone(buzzerPin, 988, 200);  
  delay(250);
  tone(buzzerPin, 1047, 300); 
  delay(350);
  noTone(buzzerPin);
}

void playNegativeChime() {
  tone(buzzerPin, 300, 300);  // Low buzz
  delay(350);
  tone(buzzerPin, 200, 300);  // Lower buzz
  delay(350);
  noTone(buzzerPin);
}
