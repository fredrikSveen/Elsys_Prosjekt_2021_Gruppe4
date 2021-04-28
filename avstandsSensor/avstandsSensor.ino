#define trigPin 7
#define echoPin 5

//You can use this pin to ignite a LED when the sensor registrate a stone.
//#define led 8 

void setup() {
  Serial.begin(9600); //Open serial communication through the USB cable.
  //Sets the pins for the sensor to send data through.
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);
}

int i = 0;
int numberAverage = 4;

void loop() {
  long duration, distance;
  long vec[numberAverage] = {0, 0, 0, 0};

  //Measures the distance
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 10;

  //Make an avegrage to prevent spikes int the sensor data.
  vec[i] = distance;
  long sum = 0;
  for (int j = 0; j < numberAverage; j++){
    sum += vec[j];
  }
  long average = sum/numberAverage;
  //Serial.print(average);
  //Serial.println(" ");

  if (average < 27) {
    //Can be used in testing to indicate when something is closer than the border set from the user.
    //digitalWrite(led, HIGH);
    int counter = 0;
    //Loop for sending information to the central computer about a stone that passed.
    while(counter < 50) {
      Serial.print(1);
      delay(5);
      counter++;
    }
    delay(1000);
    //Pumps up the average values to prevent really close objects to make the sensor indicate twice.
    for(int i = 0; i < numberAverage; i++){
      vec[i] = 100;
    }
  }
  else {
    //digitalWrite(led, LOW);
  }

  i++;

  if (i == 4) {
    i = 0;
  }
}
