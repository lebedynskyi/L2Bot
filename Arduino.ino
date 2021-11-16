#include <Mouse.h>
#include <Keyboard.h>
#include <stdlib.h>

int KEYBOARD_DELAY = 20;
int MOUSE_DELAY = 20;
int MOUSE_MOVE_DELAY = 0;
int MOUSE_MOVE_OFFSET = 5;
int RANDOM_KEY = 0;
int RANDOM_MOUSE = 0;
const int SERIAL_PORT = 9600;
const int SERIAL_DELAY = 100;
#define MAX_BUFFER_SIZE 64
#define led 13

#define SET_DELAY '0'
#define SET_KEYBOARD_DELAY '0'
#define SET_MOUSE_DELAY '1'
#define SET_MOUSE_MOVE_DELAY '2'
#define SET_MOUSE_MOVE_OFFSET '3'
#define SET_RANDOM_KEY '4'
#define SET_RANDOM_MOUSE '5'


#define PRESS_KEY '1'
#define PRINT_STRING '2'
#define KEY_DOWN '3'
#define KEY_UP '4'
#define MOUSE_MOVE '5'
#define MOUSE_CLICK '6'
#define MOUSE_DOWN '7'
#define MOUSE_UP '8'
#define MOUSE_SCROLL '9'




void setup() {
  Serial.begin(SERIAL_PORT);
  Mouse.begin();
  Keyboard.begin();
  pinMode(led, OUTPUT);
}

void loop()
{
  char buffer[MAX_BUFFER_SIZE];
  int buffPos = 0;

  while (Serial.available() == 0) {
    delayMicroseconds(SERIAL_DELAY);
  }

  while (Serial.available()) {
    if (buffPos < MAX_BUFFER_SIZE - 1) {
      buffer[buffPos++] = Serial.read();
      buffer[buffPos] = '\0';
    }
    else   //  Buffer overflow
    {
      while (Serial.available()) {
        int temp = Serial.read();
      }
      digitalWrite(led, HIGH);
      delay(3000); // 3 секунды будет включен светодиод L
      digitalWrite(led, LOW);
    }
  }

  switch (buffer[0]) {
    case SET_DELAY:  // Setup delays for Mouse and Keyboards
      {
        switch (buffer[1]) {
          case SET_KEYBOARD_DELAY:
            KEYBOARD_DELAY = atoi(&buffer[2]);
            break;
          case SET_MOUSE_DELAY:
            MOUSE_DELAY = atoi(&buffer[2]);
            break;
          case SET_MOUSE_MOVE_DELAY:
            MOUSE_MOVE_DELAY = atoi(&buffer[2]);
            break;
          case SET_MOUSE_MOVE_OFFSET:
            MOUSE_MOVE_OFFSET = atoi(&buffer[2]);
            break;
          case SET_RANDOM_KEY:
            RANDOM_KEY = atoi(&buffer[2]);
            break;
          case SET_RANDOM_MOUSE:
            RANDOM_MOUSE = atoi(&buffer[2]);
        }
        break;
      }
    case PRESS_KEY:  // Button actions
      {
        char key = atoi(&buffer[1]);
        Keyboard.press(key);
        delay(KEYBOARD_DELAY + random(RANDOM_KEY));
        Keyboard.release(key);
        delay(KEYBOARD_DELAY);
        break;
      }
    case PRINT_STRING:  // Write string
      {
        for (int i = 1; i < buffPos; i++) {
          Keyboard.write(buffer[i]);
          delay(KEYBOARD_DELAY + random(RANDOM_KEY));
        }
        break;
      }
    case KEY_DOWN:  // Press key
      {
        Keyboard.press(atoi(&buffer[1]));
        delay(KEYBOARD_DELAY + random(RANDOM_KEY));
        break;
      }
    case KEY_UP:  // Release key
      {
        Keyboard.release(atoi(&buffer[1]));
        delay(KEYBOARD_DELAY);
        break;
      }
    case MOUSE_MOVE:  // Move mouse to x y positions
      {
        long coordinate = atol(&buffer[3]);
        
        // x and y length we need to move mouse. Not final points.
        long x = coordinate / 65535;
        long y = coordinate % 65535;

        // The way where we need to move
        if (buffer[1] == '-')
          x = -x;
        if (buffer[2] == '-')
          y = -y;


        // The number of steps
        int count_step;
        float stepX = MOUSE_MOVE_OFFSET, stepY = MOUSE_MOVE_OFFSET;   
        int remainsX = 0, remainsY = 0; // How much left in the end

        if (abs(x) > abs(y))  // If length in X axis is more than y axis
        {
          count_step = abs(x) / MOUSE_MOVE_OFFSET;
          if (count_step > 0)
          {
            if (x < 0)stepX = -MOUSE_MOVE_OFFSET;

            if (y > 0)stepY = abs(y) / float(count_step);
            else stepY = y / float(count_step);

            if (abs(stepY) > MOUSE_MOVE_OFFSET)
            {
              if (stepY > 0)stepY = MOUSE_MOVE_OFFSET;
              else stepY = -MOUSE_MOVE_OFFSET;
            }
          }
        }
        else
        {
          count_step = abs(y) / MOUSE_MOVE_OFFSET;
          if (count_step > 0)
          {
            if (y < 0)stepY = -MOUSE_MOVE_OFFSET;
            if (x > 0)stepX = abs(x) / float(count_step);
            else stepX = x / float(count_step);

            if (abs(stepX) > MOUSE_MOVE_OFFSET)
            {
              if (stepX > 0)stepX = MOUSE_MOVE_OFFSET;
              else stepX = -MOUSE_MOVE_OFFSET;
            }
          }
        }

        float temp = 0.0;
        for (int i = 0; i < count_step; i++)  // moving of mouse coursor
        {
          if (abs(x) > abs(y))  
          {
            int stepY2 = trunc(stepY);
            temp = temp + (abs(stepY) - trunc(abs(stepY)));
            if (temp >= 1.0)
            {
              if (y > 0)stepY2 = stepY2 + 1.0;
              else stepY2 = stepY2 - 1.0;
              temp = temp - 1.0;
            }
            remainsX += trunc(abs(stepX));
            remainsY += abs(stepY2);
            Mouse.move(trunc(stepX), stepY2, 0);
            delay(MOUSE_MOVE_DELAY);
          }
          else
          {
            int stepX2 = trunc(stepX);
            temp = temp + (abs(stepX) - trunc(abs(stepX)));
            if (temp >= 1.0)
            {
              if (x > 0)stepX2 = stepX2 + 1.0;
              else stepX2 = stepX2 - 1.0;
              temp = temp - 1.0;
            }
            remainsX += abs(stepX2);
            remainsY += trunc(abs(stepY));
            Mouse.move(stepX2, trunc(stepY), 0);
            delay(MOUSE_MOVE_DELAY);
          }
        }
        
        remainsX = abs(x) - remainsX;
        remainsY = abs(y) - remainsY;        
        if (x < 0)remainsX = -remainsX;
        if (y < 0)remainsY = -remainsY;
        Mouse.move(remainsX, remainsY, 0);  // перемещение в конечную точку
        delay(MOUSE_MOVE_DELAY);
        break;
      }
    case MOUSE_CLICK:  // клик кнопкой мыши
      {
        Mouse.click(buffer[1]);
        delay(MOUSE_DELAY + random(RANDOM_MOUSE));
        break;
      }
    case MOUSE_DOWN:  // зажать кнопку мыши
      {
        Mouse.press(buffer[1]);
        delay(MOUSE_DELAY + random(RANDOM_MOUSE));
        break;
      }
    case MOUSE_UP:  // отпустить кнопку мыши
      {
        Mouse.release(buffer[1]);
        delay(MOUSE_DELAY);
        break;
      }
    case MOUSE_SCROLL:  // скролл мыши
      {
        char wheel = atoi(&buffer[1]);
        Mouse.move(0, 0, wheel);
        delay(MOUSE_DELAY);
        break;
      }
    default:
      break;
  }
  Serial.print(buffer);
}