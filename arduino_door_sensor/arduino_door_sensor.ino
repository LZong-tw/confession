const int led = 3; 
const int sensor = 4;

int state; // 0 close - 1 open wwitch

void setup()
{
  pinMode(led, OUTPUT);
	pinMode(sensor, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop()
{
	state = digitalRead(sensor);
	
	if (state == LOW){
    // 閉合
    Serial.println("CLOSE");
		digitalWrite(led, HIGH);
    delay(500);
    digitalWrite(led, LOW);
    delay(500);
    Serial.flush();
	}
	else{
    // 開啟
    Serial.println("OPEN");
    digitalWrite(led, LOW);
    delay(200);
    Serial.flush();
	}
}
