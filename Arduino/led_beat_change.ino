#include <IRremote.h>

IRsend irsend;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);

}
int n2 = 20;
int n1 = 60;
bool var = false;
float val;
bool condition = true;
float arr[70] = { };
float mini;
float maxi;
float sensorValue; 
float log_val;
int count = 0;
int color = 0;
void loop() {
  while (condition)
  {
    for (int a = 0; a < n2; a++)
    {
      val = 0;
      for (int b = 0; b < n1; b++)
      {
        sensorValue = pow(400 * (3.3 * analogRead(A0) / 1023) - 440, 2);
        val = val + (sensorValue / n1);
      }
      log_val = log(val) / log(2);
      arr[a] = log_val;
    }
    condition = false;
  }
  maxi = arr[0];
  mini = arr[0];
  float avg = 0;
  for (int a = 0; a < n2; a++)
  {
    avg = avg + (arr[a] / n2);
    if (arr[a] > maxi)
    {
      maxi = arr[a];
    }
    if (arr[a] < mini)
    {
      mini = arr[a];
    }
  }
  for (int a = 0; a < n2; a++)
  {
    val = 0;
    for (int b = 0; b < n1; b++)
    {
      sensorValue = pow(400 * (3.3 * analogRead(A0) / 1023) - 440, 2);
      val = val + (sensorValue / n1);
    }
    log_val = log(val) / log(3);
    int brightness = map(int(24 * log_val), int(30 * mini), int(30 * maxi), 0, 10);
    if (brightness > 10)
    {
      brightness = 10;
    }
    if (brightness < 0)
    {
      brightness = 0;
    }
    if (log_val < 1.4)
    {
      brightness = 0;
    }
    Serial.println(brightness);
    if (brightness  > 4 and count > 22){
      count = 9;
      if (color == 0 or color == 12)
      {
        irsend.sendNEC(16718565, 32);
        delay(100);
        color = 0;
      }
      if (color == 1)
      {
        irsend.sendNEC(16722645, 32);
        delay(100);
      }
      if (color == 2 )
      {
        irsend.sendNEC(16714485, 32);
        delay(100);
      }
      if (color == 3 )
      {
        irsend.sendNEC(16726215, 32);
        delay(100);
      }
      if (color == 4 )
      {
        irsend.sendNEC(16718055, 32);
        delay(100);
      }
      if (color == 5 )
      {
        irsend.sendNEC(16720605, 32);
        delay(100);
      }
      if (color == 6)
      {
        irsend.sendNEC(16751205, 32);
        delay(100);
      }
      if (color == 7)
      {
        irsend.sendNEC(16755285, 32);
        delay(100);
      }
      if (color == 8)
      {
        irsend.sendNEC(16747125, 32);
        delay(100);
      }
      if (color == 9)
      {
        irsend.sendNEC(16758855, 32);
        delay(100);
      }
      if (color == 10)
      {
        irsend.sendNEC(16750695, 32);
        delay(100);
      }
      if (color == 11)
      {
        irsend.sendNEC(16753245, 32);
        delay(100);
      }
    color = color + 1;
    }
    count = count + 1;
    arr[a] = log_val;
  }

}
