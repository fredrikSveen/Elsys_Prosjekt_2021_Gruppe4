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
int numberAverage = 10;
long duration, distance;
//Array of values to average.
long vec[10] = {200, 200, 200, 200, 200, 200, 200, 200, 200, 200}; 

void loop() {

  //Measures the distance
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 10;

  //Make an avegrage to prevent spikes in the sensor data.
  vec[i] = distance;
  long sum = 0;
  for (int j = 0; j < numberAverage; j++){
    sum += vec[j];
  }
  int average = sum/numberAverage;

//Limit value found by testing
  if (average < 100) {
    //Can be used in testing to indicate when something is closer than the border set from the user.
    //digitalWrite(led, HIGH);
    int counter = 0;
    //Loop for sending information to the central computer about a stone that passed.
    while(counter < 70) {
      Serial.print(1);
      delay(5);
      counter++;
    }
    delay(750);
    //Pumps up the average values to prevent really close objects to make the sensor indicate twice.
    for(int k = 0; k < numberAverage; k++){
      vec[k] = 150;
    }
  }
  else {
    //digitalWrite(led, LOW);
  }

  i++;

  if (i == numberAverage) {
    i = 0;
  }
}
