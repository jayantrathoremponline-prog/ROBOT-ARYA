#include <QTRSensors.h>
#define rpi_LF A0
#define rpi_turn_360 A1

QTRSensors qtr;

const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];

//const int sensorPins[num_sensor] = {2, 3, 8, 9, 10, 11, 12, 13};

const int sensorPins[SensorCount] = {13, 12, 11, 10, 9, 8, 3, 2};

const int dir1 = 4;
const int pwm1 = 5;
const int pwm2 = 6;
const int dir2 = 7;

float Kp = 0.05; // ex: 0.07
float Ki = 0.0005; // ex: 0.0008
float Kd = 0.1; // ex: 0.6

int P;
int I;
int D;

int lastError = 0;

boolean onoff = false;

const uint8_t max_speed = 180;
const uint8_t min_speed = 150;

void motor_control(int pwma, int pwmb) {
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, HIGH);
  analogWrite(pwm1, pwma);
  analogWrite(pwm2, pwmb);
}

void turn_360(int a_dir, int b_dir) {
  digitalWrite(dir1, a_dir);
  digitalWrite(dir2, b_dir);
  analogWrite(pwm1, 255);
  analogWrite(pwm2, 255);
}

bool chk_all_white(int sensor_val[]) {
  for (int i = 0; i < SensorCount; i++) {
    if (sensor_val[i] == HIGH) {
      return false;
    }
  }
  return true;
}

void PID_control() {
  uint16_t position = qtr.readLineBlack(sensorValues);
  int error = 3500 - position;

  P = error;
  I = I + error;
  D = error - lastError;
  lastError = error;

  int motorspeed = P * Kp + I * Ki + D * Kd;

  int leftSpeed = constrain(min_speed + motorspeed, 0, max_speed);
  int rightSpeed = constrain(min_speed - motorspeed, 0, max_speed);

  motor_control(leftSpeed, rightSpeed);

  // All white
  //  pos = 0 && error = 3500 || pos = 7000 && error = -3500

  // All black
  //  pos = 3500 && error = 0

  int sensor_val[SensorCount];

  for (int i = 0; i < SensorCount; i++) {
    sensor_val[i] = digitalRead(sensorPins[i]);
    //    Serial.print(sensor_val[i]);
    //    Serial.print(" || ");
  }
  //  Serial.print("\n");

  // mid --> Error = 0, pos = 3500
  // left --> Error < 0, pos > 3500
  // right --> Error > 0, pos < 3500

  while (chk_all_white(sensor_val)) {
    //    Left
    if (error < 0 && position > 3500) {
      turn_360(0, 1);
      Serial.println("Turning Left 360");
    }
    //    Right
    if (error > 0 && position < 3500) {
      turn_360(1, 0);
      Serial.println("Turning Right 360");
    }

    for (int i = 0; i < SensorCount; i++) {
      sensor_val[i] = digitalRead(sensorPins[i]);
    }
  }

  Serial.println("Pos: " + String(position) + " || Error: " + String(error) + " || LError: " + String(lastError) + " || LSpeed: " + String(leftSpeed) + " || RSpeed: " + String(rightSpeed));
}

void setup() {
  Serial.begin(9600);
  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]) {
    13, 12, 11, 10, 9, 8, 3, 2
    //    2, 3, 8, 9, 10, 11, 12, 13
  }, SensorCount);

  for (int i = 0; i < SensorCount; i++) {
    pinMode(sensorPins[i], INPUT);
  }

  pinMode(dir1, OUTPUT);
  pinMode(pwm1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(rpi_LF, INPUT);
  pinMode(rpi_turn_360, INPUT);

  motor_control(0, 0);

  qtr.calibrate();

  //  for (uint16_t i = 0; i < 400; i++)
  //  {
  //    qtr.calibrate();
  //  }

  for (int i = 0; i < 8; i++)
  {
    qtr.calibrationOn.minimum[i] = 48;
  }
  for (int i = 0; i < 8; i++)
  {
    qtr.calibrationOn.maximum[i] = 2500;
  }
}

void loop() {
  while (digitalRead(rpi_LF) == HIGH) {
//    PID_control();
    Serial.println("Aage Badh");
  }
  motor_control(0, 0);
  Serial.println("Stop");
  
//  while (digitalRead(rpi_turn_360) == HIGH) {
//    turn_360();
//  }
}
