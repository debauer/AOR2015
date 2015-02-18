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
#define COUNT_VALUE 6
#define COUNT_TEXT 7
#define COUNT_MPD 3

struct value_s{
  double v;
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
  int x;
  int y;
  int color;
  int bcolor;
};

struct mpd_s{
  char s[STRING_LENGHT];
  int x;
  int y;
  int color;
  int bcolor;
};

#define VALUES_MARGIN_TOP 100
#define MPD_MARGIN_TOP 30
#define AOR_MARGIN_TOP 0

mpd_s mpd[COUNT_MPD] = {{"Artist + Titel",CENTER,0+MPD_MARGIN_TOP,COLOR_WHITE,COLOR_BLACK},
                            {"Status1",CENTER,25+MPD_MARGIN_TOP,COLOR_GREY,COLOR_BLACK},
                            {"Status2",CENTER,45+MPD_MARGIN_TOP,COLOR_GREY,COLOR_BLACK}};


string_s text[COUNT_TEXT] = {{"ALLGAEU ORIENT 2015",CENTER,3+AOR_MARGIN_TOP,COLOR_BLACK,COLOR_SAND},
                            {"OEL1",35,53+VALUES_MARGIN_TOP,COLOR_BLACK,COLOR_SAND},
                            {"OEL2",170,53+VALUES_MARGIN_TOP,COLOR_BLACK,COLOR_SAND},
                            {"RPI",315,53+VALUES_MARGIN_TOP,COLOR_BLACK,COLOR_SAND},
                            {"Motor",25,123+VALUES_MARGIN_TOP,COLOR_BLACK,COLOR_SAND},
                            {"Aussen",155,123+VALUES_MARGIN_TOP,COLOR_BLACK,COLOR_SAND},
                            {"Innen",295,123+VALUES_MARGIN_TOP,COLOR_BLACK,COLOR_SAND}};

// 4LCD   
//  drawBox(0,0,100,60);
//  drawBox(99,0,100,60);
//  drawBox(199,0,100,60);
//  drawBox(299,0,100,60);

// 3LCD
//  drawBox(0,0,133,60);
//  drawBox(133,0,133,60);
//  drawBox(266,0,133,60);

value_s values[COUNT_VALUE] = { {60.2,-1,500.0,0,VALUES_MARGIN_TOP,13,133,50,COLOR_PURPLE,COLOR_BLACK},
                                {66.5,-1,500.0,133,VALUES_MARGIN_TOP,13,133,50,COLOR_PURPLE,COLOR_BLACK},
                                {62.0,-1,60.0,266,VALUES_MARGIN_TOP,13,133,50,COLOR_PURPLE,COLOR_BLACK},
                                {120.1,-1,500.0,0,70+VALUES_MARGIN_TOP,13,133,50,COLOR_PURPLE,COLOR_BLACK},
                                {27.6,-1,500.0,133,70+VALUES_MARGIN_TOP,13,133,50,COLOR_PURPLE,COLOR_BLACK},
                                {23.4,-1,500.0,266,70+VALUES_MARGIN_TOP,13,133,50,COLOR_PURPLE,COLOR_BLACK}};

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
    while(arg != NULL && nr < COUNT_TEXT){
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

void mpdHandler(){
  int a,b,nr;  
  char *arg; 
  arg = SCmd.next();
  a = 0; 
  if (arg != NULL){
    nr = atoi(arg);
    arg = SCmd.next();
    if(arg != NULL){
      for(b=0;b<STRING_LENGHT;b++){
         mpd[nr].s[b] = 0x00;
      }
    }   
    while(arg != NULL && nr < COUNT_MPD){
      while(*arg != NULL){
        mpd[nr].s[a] = *arg;
        a++;
        arg++;
      }
      mpd[nr].s[a] = ' ';
      a++;
      arg = SCmd.next();
    }
    myGLCD.setColor(mpd[nr].bcolor);
    myGLCD.fillRect( 0, mpd[nr].y, 399, mpd[nr].y+15);
    myGLCD.setColor(mpd[nr].color);
    myGLCD.setBackColor(mpd[nr].bcolor);
    myGLCD.setFont(BigFont);
    myGLCD.print(mpd[nr].s,CENTER, mpd[nr].y); 
    if(a>0)
      mpd[nr].s[a-1] = 0x00;
    mpd[nr].s[a] = 0x00;
    mpd[nr].s[a+1] = 0x00;
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
    if(arg != NULL && nr < COUNT_VALUE){
       values[nr].v = atof(arg);
    }
  }
}

void inputHandler(){
  SCmd.readSerial();
}


void updateValues(){
  static int c;
  char str[10];
  dtostrf(values[c].v, 5, 1, &str[0]);
  if(values[c].v > values[c].alarm)
    myGLCD.setColor(COLOR_RED); 
  else 
    myGLCD.setColor(values[c].color);
  myGLCD.setBackColor(values[c].bcolor);
  myGLCD.setFont(Ubuntu);
  myGLCD.print(str, values[c].x+values[c].padding-5, values[c].y+values[c].padding);
  c++;
  if(c>=COUNT_VALUE)
     c = 0;
}

void updateText(int c){
  myGLCD.setColor(text[c].color);
  myGLCD.setBackColor(text[c].bcolor);
  myGLCD.setFont(BigFont);
  myGLCD.print(text[c].s,text[c].x, text[c].y);        
}

void updateTexte(){
  static int c;
  updateText(c);
  c++;
  if(c>=COUNT_TEXT)
    c = 0;
}

void setup(){

  //randomSeed(analogRead(0));
  
  // Setup the LCD
  myGLCD.InitLCD();
  myGLCD.setFont(Ubuntu);

  Serial.begin(9600);

  SCmd.addCommand("value",valueHandler);       // Turns LED on
  SCmd.addCommand("string",stringHandler);     // Turns LED off
  SCmd.addCommand("mpd",mpdHandler);     // Turns LED off
  SCmd.addDefaultHandler(unrecognized);        // Handler for command that isn't matched  (says "What?") 

  myGLCD.setColor(COLOR_PURPLE);
  myGLCD.setBackColor(COLOR_BLACK);

  for(i=0;i<COUNT_VALUE;i++){
     drawBox(values[i].x,values[i].y,values[i].width,values[i].height);
  }
  myGLCD.setColor(COLOR_SAND);
  myGLCD.fillRect( 0, AOR_MARGIN_TOP, 399, 20+AOR_MARGIN_TOP);
  myGLCD.fillRect( 0, 50+VALUES_MARGIN_TOP, 399, 70+VALUES_MARGIN_TOP);
  myGLCD.fillRect( 0, 120+VALUES_MARGIN_TOP, 399, 140+VALUES_MARGIN_TOP);

  myGLCD.setFont(BigFont);
  for(i=0;i<COUNT_MPD;i++){
    myGLCD.setColor(mpd[i].color);
    myGLCD.setBackColor(mpd[i].bcolor);
    myGLCD.print(mpd[i].s,CENTER, mpd[i].y); 
  }
  updateTexte();
}

void loop(){
  static int g = 0;
  inputHandler();
  updateValues();
  //updateTexte();
}

