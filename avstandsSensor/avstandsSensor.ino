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
  long average = (vec[1]+vec[2]+vec[3]+vec[4]+vec[0])/5;

  if (average < 7) {
    //digitalWrite(led, HIGH);
    int counter = 0;
    while(counter < 50) {
      Serial.print(1);
      delay(5);
      counter++;
    }
    delay(1000);
    for(int i = 0; i < 6; i++){
      vec[i] = 100;
    }
  }
  else {
    //digitalWrite(led, LOW);
  }

  i++;

  if (i == 5) {
    i = 0;
  }
}
