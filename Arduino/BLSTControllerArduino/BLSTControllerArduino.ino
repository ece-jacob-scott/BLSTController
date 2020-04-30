//Defines the pins for each of the axis

#define LPITCH A2
#define LYAW A1
#define LROLL A0
#define RPITCH A6
#define RYAW A5
#define RROLL A4


//reserves space for a message
char message[40];

//sets up the pins and starts the serial
void setup() {
  pinMode(LPITCH, INPUT);
  pinMode(LYAW, INPUT);
  pinMode(LROLL, INPUT);
  pinMode(RPITCH, INPUT);
  pinMode(RYAW, INPUT);
  pinMode(RROLL, INPUT);
  Serial.begin(115200);
}

//reads the angles, generates a packet, sends the packet and then waits 25 ms to send the next one
void loop() {
  sprintf(message, "%d %d %d %d %d %d\n", analogRead(LPITCH), analogRead(LYAW), analogRead(LROLL), analogRead(RPITCH), analogRead(RYAW), analogRead(RROLL));
  Serial.write(message);
  delay(25);
}
