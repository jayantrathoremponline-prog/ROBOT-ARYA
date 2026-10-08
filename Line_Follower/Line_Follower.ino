// 6-array IR line follower with PID
// For Arduino Uno/Nano

#define rpi_LF        A0
#define rpi_turn_360  A1

const int SENSOR_COUNT = 6;
const int sensorPins[SENSOR_COUNT] = {13, 12, 11, 10, 9, 8};

const int dir1 = 4;
const int pwm1 = 5;
const int pwm2 = 6;
const int dir2 = 7;

// Change to HIGH if your IR module gives HIGH on black line
#define LINE_STATE LOW

// 6 sensors => positions 0, 1000, 2000, 3000, 4000, 5000
const int CENTER = 2500;

float Kp = 0.05;
float Ki = 0.0005;
float Kd = 0.1;

int P, D;
long I = 0;
int lastError = 0;

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

// Returns 0..5000 if line found, or -1 if line lost
int readLinePosition() {
  long weightedSum = 0;
  int count = 0;

  for (int i = 0; i < SENSOR_COUNT; i++) {
    if (digitalRead(sensorPins[i]) == LINE_STATE) {
      weightedSum += (long)i * 1000;
      count++;
    }
  }

  if (count == 0) return -1;
  return weightedSum / count;
}

void PID_control() {
  int position = readLinePosition();

  // Lost line: spin toward the last known side
  if (position < 0) {
    if (lastError < 0) {
      turn_360(0, 1);
      Serial.println("Lost: turning LEFT");
    } else {
      turn_360(1, 0);
      Serial.println("Lost: turning RIGHT");
    }
    return;
  }

  int error = position - CENTER;

  P = error;
  I = I + error;
  I = constrain(I, -10000, 10000);   // prevent integral windup
  D = error - lastError;
  lastError = error;

  float motorspeed = P * Kp + I * Ki + D * Kd;

  int leftSpeed  = constrain(min_speed + (int)motorspeed, 0, max_speed);
  int rightSpeed = constrain(min_speed - (int)motorspeed, 0, max_speed);

  motor_control(leftSpeed, rightSpeed);

  Serial.print("Pos: ");
  Serial.print(position);
  Serial.print(" | Error: ");
  Serial.print(error);
  Serial.print(" | L: ");
  Serial.print(leftSpeed);
  Serial.print(" | R: ");
  Serial.println(rightSpeed);
}

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < SENSOR_COUNT; i++) {
    pinMode(sensorPins[i], INPUT);
  }

  pinMode(dir1, OUTPUT);
  pinMode(pwm1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(pwm2, OUTPUT);

  pinMode(rpi_LF, INPUT);
  pinMode(rpi_turn_360, INPUT);

  motor_control(0, 0);
}

void loop() {
  if (digitalRead(rpi_LF) == HIGH) {
    PID_control();
  } else {
    motor_control(0, 0);
    Serial.println("Stop");
    delay(100);
  }

  // Optional: Raspberry Pi controlled 360 spin
  // if (digitalRead(rpi_turn_360) == HIGH) {
  //   turn_360(1, 0);
  //   delay(500);
  // }
}
