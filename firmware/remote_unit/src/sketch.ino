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
};

struct string_s{
	char s[STRING_LENGHT];
	int x;
	int y;
};

string_s text[COUNT_TEXT] = {{"Dateiname",5,100},{"Titel",5,150},{"Album",5,200},{"ALLGÄU ORIENT 2015",CENTER,2}};

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

value_s values[COUNT_VALUE] = {{"0123",-1,-99,0,VALUES_MARGIN_TOP,5,133,60},{"0567",-1,-99,133,VALUES_MARGIN_TOP,5,133,60},{"0234",-1,-99,266,VALUES_MARGIN_TOP,5,133,60}};

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
	myGLCD.setColor(COLOR_PURPLE);
	myGLCD.setBackColor(COLOR_BLACK);
	myGLCD.setFont(SevenSegNumFont);
	myGLCD.print(values[c].str, values[c].x+values[c].padding, values[c].y+values[c].padding);
	c++;
	if(c>=COUNT_VALUE)
		 c = 0;
}

void updateTexte(){
		static int c;
		myGLCD.setColor(COLOR_PURPLE);
		myGLCD.setBackColor(COLOR_BLACK);
		myGLCD.setFont(Ubuntu);
		myGLCD.print(text[c].s,text[c].x, text[c].y);
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
	SCmd.addCommand("string",stringHandler);        // Turns LED off
	SCmd.addDefaultHandler(unrecognized);  // Handler for command that isn't matched  (says "What?") 

	myGLCD.setColor(COLOR_PURPLE);
	myGLCD.setBackColor(COLOR_BLACK);

	for(i=0;i<3;i++){
		 drawBox(values[i].x,values[i].y,values[i].width,values[i].height);
	}

	myGLCD.fillRect( 97, 50, 100, 53);
	myGLCD.fillRect(230, 50, 233, 53);
	myGLCD.fillRect(363, 50, 366, 53);
}

void loop(){
	static int g = 0;
	inputHandler();
	updateValues();
	updateTexte();
}

