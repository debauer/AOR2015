#include <memorysaver.h>

#include <UTFT.h>
#include <SerialCommand.h>
extern uint8_t SevenSegNumFont[];
//extern uint8_t SmallFont[];
extern uint8_t DotMatrix_M_Slash[];
extern uint8_t Ubuntu[];
//extern uint8_t BigFont[];

SerialCommand SCmd; 

#define COLOR_PURPLE 0,153,255 
#define COLOR_BLACK 0,0,0 
#define COLOR_WHITE 255,255,255
#define COLOR_RED 255,0,0
#define COLOR_GREEN 0,255,0
#define COLOR_BLUE 0,0,255

#define BOX_COLOR_RAND COLOR_PURPLE
#define BOX_COLOR_FILL COLOR_BLACK

UTFT myGLCD(ITDB32WD,38,39,40,41);

struct value_s{
  char strRaw[20];
  char str[20];
  int natNumbers;
  int alarm;
  int x;
  int y;
};

#define STRING_LENGHT 50

struct string_s{
  char s[STRING_LENGHT];
  int x;
  int y;
};

string_s text[3] = {{"Dateiname",5,100},{"Titel",5,150},{"Album",5,200}};

value_s values[5];

int i,k;

void drawBox(int x, int y, int width, int height){
  myGLCD.setColor(BOX_COLOR_RAND);
  myGLCD.drawRect(x, y, x+width, y+height);
  myGLCD.setColor(BOX_COLOR_FILL);
  myGLCD.fillRect(x+1, y+1, x+width-1, y+height-1);
}

void stringHandler(){
  int a,nr;  
  char *arg; 
  arg = SCmd.next();
  a = 0; 
  if (arg != NULL){
    nr = atoi(arg);
    arg = SCmd.next();
    while(arg != NULL && nr < 3){
      while(*arg != NULL){
        text[nr].s[a] = *arg;
        a++;
        arg++;
      }
      text[nr].s[a] = ' ';
      a++;
      arg = SCmd.next();
    }
    text[nr].s[a] = 0x00;
  }
}

void unrecognized(){
}

void valueHandler()    {
  //int aNumber;  
  //char *arg; 
//
  //arg = SCmd.next(); 
  //if (arg != NULL) 
  //{
  //  aNumber=atoi(arg);    // Converts a char string to an integer
  //  Serial.print("First argument was: "); 
  //  Serial.println(aNumber); 
  //} 
  //else {
  //  Serial.println("No arguments"); 
  //}
//
  //arg = SCmd.next(); 
  //if (arg != NULL) 
  //{
  //  aNumber=atol(arg); 
  //  Serial.print("Second argument was: "); 
  //  Serial.println(aNumber); 
  //} 
  //else {
  //  Serial.println("No second argument"); 
  //}

}

void updateSegments(){
  myGLCD.setColor(COLOR_PURPLE);
  myGLCD.setBackColor(COLOR_BLACK);
  myGLCD.setFont(SevenSegNumFont);
  //for(i=0;i<3;i++){
  //  if(values[i].str[0] != 0x00){
  //    myGLCD.print(values[i].str,values[i].x, values[i].y); 
  //  }else{
  //    for(k=0;k<20;k++){
  //      if(values[i].str[k] == '.')
  //        values[i].natNumbers = -1;
  //    }
  //    myGLCD.print(values[i].str,values[i].x, values[i].y); 
  //  }
  //}
}

void setup(){

  //randomSeed(analogRead(0));
  
// Setup the LCD
  myGLCD.InitLCD();
  myGLCD.setFont(Ubuntu);

  Serial.begin(9600);

  SCmd.addCommand("value",valueHandler);       // Turns LED on
  SCmd.addCommand("string",stringHandler);        // Turns LED off
  SCmd.addDefaultHandler(unrecognized);  // Handler for command that isn't matched  (says "What?") 

  drawBox(0,0,133,60);
  drawBox(133,0,133,60);
  drawBox(266,0,133,60);

  for(i=0;i<5;i++){
    values[i].natNumbers = -1;
    values[i].strRaw[0] = '1';
    values[i].strRaw[1] = '1';
    values[i].strRaw[2] = '.';
    values[i].strRaw[3] = '3';
  }
  values[0].strRaw[0] = '0';

  values[0].x = 5;
  values[0].y = 5;
  values[1].x = 138;
  values[1].y = 5;
  values[2].x = 269;
  values[2].y = 5;

  myGLCD.setColor(COLOR_PURPLE);
  myGLCD.setBackColor(COLOR_BLACK);
  myGLCD.setFont(SevenSegNumFont);

  myGLCD.print("0123", 5, 5);
  myGLCD.print("1337", 138, 5);
  myGLCD.print("0678", 269, 5);

  myGLCD.fillRect( 97, 50, 100, 53);
  myGLCD.fillRect(230, 50, 233, 53);
  myGLCD.fillRect(363, 50, 366, 53);
}


void loop(){
  static int g = 0;
  SCmd.readSerial();     // We don't do much, just process serial commands

  updateSegments();
  if(g){
    g = 0;
    myGLCD.setColor(COLOR_RED);
  }else{
    g = 1;
    myGLCD.setColor(COLOR_PURPLE);
  }
  myGLCD.setBackColor(COLOR_BLACK);
  myGLCD.setFont(Ubuntu);
  for(i=0;i<3;i++;){
    myGLCD.print(text[i].s,text[i].x, text[i].y);
  }

// 4LCD   
//  drawBox(0,0,100,60);
//  drawBox(99,0,100,60);
//  drawBox(199,0,100,60);
//  drawBox(299,0,100,60);

// 3LCD
//  drawBox(0,0,133,60);
//  drawBox(133,0,133,60);
//  drawBox(266,0,133,60);
//
//  myGLCD.setColor(COLOR_PURPLE);
//  myGLCD.setBackColor(COLOR_BLACK);
//  myGLCD.setFont(SevenSegNumFont);

// 4 LCD
//  myGLCD.print("123", 2, 5);
//  myGLCD.print("456", 102, 5);
//  myGLCD.print("678", 202, 5);
//  myGLCD.print("231", 302, 5);
//  myGLCD.fillRect( 64, 50,  67, 53);
//  myGLCD.fillRect(164, 50, 167, 53);
//  myGLCD.fillRect(264, 50, 267, 53);
//  myGLCD.fillRect(364, 50, 367, 53);

 // 3 LCD
//  myGLCD.print("0123", 5, 5);
//  myGLCD.print("1337", 138, 5);
//  myGLCD.print("0678", 269, 5);
//
//  myGLCD.fillRect( 97, 50, 100, 53);
//  myGLCD.fillRect(230, 50, 233, 53);
//  myGLCD.fillRect(363, 50, 366, 53);
//
//  while(1);

//  myGLCD.setColor(COLOR_BLACK);
//  myGLCD.fillRect(0, 0, 59, 79);
//  myGLCD.setBackColor(0, 255, 0);
//  myGLCD.setFont(Ubuntu);
//  myGLCD.print("Gogo Powerrangers!", LEFT, 1);
//  myGLCD.setFont(DotMatrix_M_Slash);
//  myGLCD.print("1238.23", LEFT, 100);
}

