#include <FastLED.h>

#define LED_PIN     3   //utgang på ardunio
#define NUM_LEDS    211  //antall LED lys koden skal virke på 
#define BRIGHTNESS  64  
#define LED_TYPE    WS2811 //type led strip 
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

#define UPDATES_PER_SECOND 100

//oppsett for de forskjellige manuelt definerte fargepaletter:
CRGBPalette16 currentPalette; 
TBlendType    currentBlending;

extern CRGBPalette16 myRedWhiteBluePalette;                       
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM; 

extern CRGBPalette16 blueWins;
extern const TProgmemPalette16 blueWins_p PROGMEM;

extern CRGBPalette16 orangeWins;
extern const TProgmemPalette16 orangeWins_p PROGMEM;

extern CRGBPalette16 myWhitePalette;
extern const TProgmemPalette16 myWhitePalette_p PROGMEM;

extern CRGBPalette16 partyArty;
extern const TProgmemPalette16 partyArty_p PROGMEM;


//tellere for å bestemme hvilk fargekombinasjoner som skal vises 
int i = 0;
int k = 8; //gunntilstand, ingen fargekombinasjon vil vises


void setup() {
  
    Serial.begin(9600);

    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    
    currentPalette = myWhitePalette_p; //standardpalett
    currentBlending = NOBLEND;
}

void loop()
{ 

    //mottar nye k-verdier, i henhold til LCD-skjerm, via raspberry pi 
    if (Serial.available() > 0) 
    {
    String data = Serial.readStringUntil('\n');
    k = 6;
    k = data.toInt();
    }
    

    ChangePalettePeriodically(); //funksjon som endrer på fargekombinasjonene
    
    static uint8_t startIndex = 0;
    startIndex = startIndex + 1; /* motion speed */
    
    FillLEDsFromPaletteColors( startIndex);
    FastLED.show();
    FastLED.delay(1000 / UPDATES_PER_SECOND);

}

void FillLEDsFromPaletteColors( uint8_t colorIndex)
{
    uint8_t brightness = 255;
    
    for( int i = 0; i < NUM_LEDS; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        colorIndex += 3;
    }
}

void ChangePalettePeriodically()
{
        uint8_t secondHand = (millis() / 1000) % 60;

              
        
        //bestemmer når de forskjellige fargekombinasjoene skal vises,
        //avhengig av k-verdi sent av raspberry pi
        if(i == 0){
          if(k == 0) //start
            {
              i = 1;
            }
          else if(k == 1) //blå vinner runden  
            {
              i = 2;
            }
          else if(k == 2) //oransje vinner runden
            {
              i = 3;
            }         
          else if(k == 3) //blå vinner spillet
            {
              i = 4;
            }
          else if(k == 4) //oransje vinner spillet
            {
              i = 5;
            }
          else if (k == 8){ //grunntilstand, ingen spiller
             blinkyBlack();
          }
          else{
             currentPalette = myWhitePalette_p; //standard fargepalette
             currentBlending = NOBLEND; 
          } 
        }
        
     
//START
          if(i == 1)
          {
            secondHand = (millis() / 500) % 21; //tidsoppsett
            
            if( secondHand == 5)  { currentPalette = myRedWhiteBluePalette_p; currentBlending = NOBLEND;}
            
            if( secondHand == 20) {i = 0; k = 6;} // går tilbake til standard fargepalett
          }

        
//BLÅ vinner runde
          else if (i == 2)
          {
            secondHand = (millis() / 500) % 13;
          
            if( secondHand == 5) {blinkyBlack(); currentBlending = NOBLEND;}
            if( secondHand == 6) {blinkyBlue(); currentBlending = NOBLEND;}
            if( secondHand == 7) {blinkyBlack(); currentBlending = NOBLEND;}
            if( secondHand == 8) {blinkyBlue(); currentBlending = NOBLEND;}
            if( secondHand == 9) {blinkyBlack(); currentBlending = NOBLEND;}
            if( secondHand == 10) {blinkyBlue(); currentBlending = NOBLEND;}
            if( secondHand == 11) {blinkyBlack(); currentBlending = NOBLEND;}
    
            if( secondHand == 12) { i = 0; k = 6;} 
          }


//ORANSJE vinner runde
          else if(i == 3)
          {
            secondHand = (millis() / 500) % 13;
          
            if( secondHand == 5) {blinkyBlack(); currentBlending = NOBLEND;}
            if( secondHand == 6) {blinkyOrange();currentBlending = NOBLEND;}
            if( secondHand == 7) {blinkyBlack(); currentBlending = NOBLEND;}
            if( secondHand == 8) {blinkyOrange();currentBlending = NOBLEND;}
            if( secondHand == 9) {blinkyBlack(); currentBlending = NOBLEND;}
            if( secondHand == 10) {blinkyOrange();currentBlending = NOBLEND;}
            if( secondHand == 11) {blinkyBlack(); currentBlending = NOBLEND;}

            if( secondHand == 12) {k = 6; i = 0;}  
          }
          

//BLÅ vinner spillet
        else if( i == 4)
        {
          secondHand = (millis() / 500) % 59;
          
          if( secondHand == 5)  {currentPalette = partyArty_p; currentBlending = LINEARBLEND;}
          if( secondHand == 20) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 21) {currentPalette = blueWins_p; currentBlending = NOBLEND;}
          if( secondHand == 36) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 37) {blinkyBlue();currentBlending = NOBLEND;}
          if( secondHand == 38) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 39) {blinkyBlue();currentBlending = NOBLEND;}
          if( secondHand == 40) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 41) {blinkyBlue();currentBlending = NOBLEND;}
          if( secondHand == 42) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 43) {currentPalette = blueWins_p; currentBlending = NOBLEND;}

          if( secondHand == 58) {i = 0; k = 6;}
        }
        
        
//ORANSJE vinner spillet
        else if( i == 5)
        {
          secondHand = (millis() / 500) % 59;
          
          if( secondHand == 5)  {currentPalette = partyArty_p; currentBlending = LINEARBLEND;}
          if( secondHand == 20) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 21) {currentPalette = orangeWins_p; currentBlending = NOBLEND;}
          if( secondHand == 36) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 37) {blinkyOrange();currentBlending = NOBLEND;}
          if( secondHand == 38) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 39) {blinkyOrange();currentBlending = NOBLEND;}
          if( secondHand == 40) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 41) {blinkyOrange();currentBlending = NOBLEND;}
          if( secondHand == 42) {blinkyBlack(); currentBlending = NOBLEND;}
          if( secondHand == 43) {currentPalette = orangeWins_p; currentBlending = NOBLEND;}

          if( secondHand == 58) {i = 0; k = 6;}
        }
}


void blinkyBlack() //viser fargen svart 
{
  fill_solid( currentPalette, 16, CRGB::Black);
}

void blinkyBlue() //viser fargen blå
{
  fill_solid( currentPalette, 16, CRGB::Navy);
}

void blinkyOrange() //viser fargen rød
{
  fill_solid( currentPalette, 16, CRGB::Red);
}


const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM = 
{
    CRGB::Red,
    CRGB::Gray, 
    CRGB::Navy,
    CRGB::Gray,
    
    CRGB::Red,
    CRGB::Gray, 
    CRGB::Navy,
    CRGB::Gray,
    
    CRGB::Red,
    CRGB::Gray,
    CRGB::Navy,
    CRGB::Gray,
};


const TProgmemPalette16 blueWins_p PROGMEM =
{
    CRGB::Navy,
    CRGB::Gray, 
    CRGB::Navy,
    CRGB::Gray,
    
    CRGB::Navy,
    CRGB::Gray, 
    CRGB::Navy,
    CRGB::Gray,
    
    CRGB::Navy,
    CRGB::Gray,
    CRGB::Navy,
    CRGB::Gray,  
};


const TProgmemPalette16 orangeWins_p PROGMEM =
{
    CRGB::Red,
    CRGB::OrangeRed, 
    CRGB::Red,
    CRGB::OrangeRed,
    
    CRGB::Red,
    CRGB::OrangeRed, 
    CRGB::Red,
    CRGB::OrangeRed,
    
    CRGB::Red,
    CRGB::OrangeRed,
    CRGB::Red,
    CRGB::OrangeRed,
};


const TProgmemPalette16 myWhitePalette_p PROGMEM =
{
    CRGB:: Orange,
    CRGB:: Orange, 
    CRGB:: Orange,
    CRGB:: Orange,
    
    CRGB:: Orange,
    CRGB:: Orange, 
    CRGB:: Orange,
    CRGB:: Orange,
    
    CRGB:: Orange,
    CRGB:: Orange,
    CRGB:: Orange,
    CRGB:: Orange,

    CRGB:: Orange,
    CRGB:: Orange,
    CRGB:: Orange,
    CRGB:: Orange,
};


const TProgmemPalette16 partyArty_p PROGMEM =
{
    CRGB:: DeepPink,
    CRGB:: Green, 
    CRGB:: Red,
    CRGB:: Turquoise,
    
    CRGB:: Black,
    CRGB:: Black, 
    CRGB:: Black,
    CRGB:: Black,
    
    CRGB:: DeepPink,
    CRGB:: Green,
    CRGB:: Red,
    CRGB:: Turquoise,
};
