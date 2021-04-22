  #define trigPin 7
  #define echoPin 5
  #define led 8

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

int i = 0;
int stones = 0;
bool finish = false;

void loop() {
  // put your main code here, to run repeatedly:
  long duration, distance;
  long vec[5] = {0, 0, 0, 0, 0};

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;

  vec[i] = distance;

  if ((vec[1]+vec[2]+vec[3]+vec[4]+vec[0])/5 < 7) {
    digitalWrite(led, HIGH);
    stones++;
    delay(1000);
  }
  else {
    digitalWrite(led, LOW);
  }

  i++;

  if (i == 5) {
    i = 0;
  }

  if (stones == 16) {
    stones = 0;
    finish = true;
  }
  else {
    finish = false;
  }

  Serial.print(stones);
  //Serial.println(" cm");
  Serial.println();
  delay(10);
}
