#include <memorysaver.h>

#include <UTFT.h>
#include <SerialCommand.h>
extern uint8_t SevenSegNumFont[];
extern uint8_t SmallFont[];
extern uint8_t DotMatrix_M_Slash[];
extern uint8_t Ubuntu[];
extern uint8_t BigFont[];

SerialCommand SCmd; 

#define COLOR_PURPLE 0x04DF // 0,153,255 
#define COLOR_BLACK 0x0000 
#define COLOR_WHITE 0xFFFF // 255,255,255
#define COLOR_RED 0xF800 // 255,0,0
#define COLOR_GREEN 0x07E0 //0,255,0
#define COLOR_BLUE 0x001F // 0,0,255
#define COLOR_SAND 0xDD01 // 218,163,8
#define COLOR_GREY 0x94B2

#define BOX_COLOR_RAND COLOR_SAND
#define BOX_COLOR_FILL COLOR_BLACK

UTFT myGLCD(ITDB32WD,38,39,40,41);

#define STRING_LENGHT 50
#define COUNT_VALUE 3
#define COUNT_TEXT 4

struct value_s{
  char str[20];
  int natNumbers;
  int alarm;
  int x;
  int y;
  int padding;
  int width;
  int height;
        int color;
        int bcolor;
};

struct string_s{
  char s[STRING_LENGHT];
        char b[STRING_LENGHT];
  int x;
  int y;
        int color;
        int bcolor;
};

string_s text[COUNT_TEXT] = {{"Die Antwoord - ADSD","Artist + Titel",CENTER,140,COLOR_WHITE,COLOR_BLACK},
                            {"#13/19 1:34/4:31 (34%)","Status1",CENTER,170,COLOR_GREY,COLOR_BLACK},
                            {"V: 51%  RE: off  RA: off","Status2",CENTER,200,COLOR_GREY,COLOR_BLACK},
                            {"ALLGAEU ORIENT 2015","penis",CENTER,3,COLOR_BLACK,COLOR_SAND}};

// 4LCD   
//  drawBox(0,0,100,60);
//  drawBox(99,0,100,60);
//  drawBox(199,0,100,60);
//  drawBox(299,0,100,60);

// 3LCD
//  drawBox(0,0,133,60);
//  drawBox(133,0,133,60);
//  drawBox(266,0,133,60);

#define VALUES_MARGIN_TOP 20

value_s values[COUNT_VALUE] = { {"0123",-1,-99,0,VALUES_MARGIN_TOP,5,133,60,COLOR_PURPLE,COLOR_BLACK},
                                {"0567",-1,-99,133,VALUES_MARGIN_TOP,5,133,60,COLOR_PURPLE,COLOR_BLACK},
                                {"0234",-1,-99,266,VALUES_MARGIN_TOP,5,133,60,COLOR_PURPLE,COLOR_BLACK}};

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

void valueHandler(){
  int a,c,nr;
  double d;  
  char *arg; 
  arg = SCmd.next();
  a = 0; 
  if (arg != NULL){
    nr = atoi(arg);
    arg = SCmd.next();
    if(arg != NULL && nr < 3){
       sprintf(values[nr].str,"%s",arg);
    }
  }
}

void inputHandler(){
  SCmd.readSerial();
}


void updateValues(){
  static int c;
  myGLCD.setColor(values[c].color);
  myGLCD.setBackColor(values[c].bcolor);
  myGLCD.setFont(SevenSegNumFont);
  myGLCD.print(values[c].str, values[c].x+values[c].padding, values[c].y+values[c].padding);
        myGLCD.fillRect( values[c].x+97, values[c].y+50, values[c].x+100, values[c].y+53);
  c++;
  if(c>=COUNT_VALUE)
     c = 0;
}

void updateTexte(){
  static int c;
  myGLCD.setColor(text[c].color);
  myGLCD.setBackColor(text[c].bcolor);
  myGLCD.setFont(BigFont);
        myGLCD.print(text[c].s,text[c].x, text[c].y);
  c++;
  if(c>=COUNT_TEXT)
        c = 0;
        //myGLCD.setColor(COLOR_SAND);
        //myGLCD.fillRect( 0, text[c].y+35, 399, text[c].y+40);
                
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

  myGLCD.setColor(COLOR_PURPLE);
  myGLCD.setBackColor(COLOR_BLACK);

  for(i=0;i<3;i++){
     drawBox(values[i].x,values[i].y,values[i].width,values[i].height);
  }
        myGLCD.setColor(COLOR_SAND);
        myGLCD.fillRect( 0, 0, 399, 20);
        myGLCD.fillRect( 0, 80, 399, 100);
        //GLCD.setColor(COLOR_BLACK);
        //myGLCD.setBackColor(COLOR_SAND);
        //yGLCD.setFont(BigFont);
        //myGLCD.print(aor.s,aor.x, aor.y);
}

void loop(){
  static int g = 0;
  inputHandler();
  updateValues();
  updateTexte();
}

