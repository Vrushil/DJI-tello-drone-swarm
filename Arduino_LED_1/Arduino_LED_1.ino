/*
  UDPSendReceive.pde:
  This sketch receives UDP message strings, prints them to the serial port
  and sends an "acknowledge" string back to the sender

  A Processing sketch is included at the end of file that can be used to send
  and received messages for testing with a computer.

  created 21 Aug 2010
  by Michael Margolis

  This code is in the public domain.

  adapted from Ethernet library examples
*/

#include <FastLED.h>

#include <WiFiUdp.h>
#include <ESP8266WiFi.h>
#define DATA_PIN 2
#define NUM_LEDS 4
CRGB leds[NUM_LEDS];
#define FRAMES_PER_SECOND  70

int flag = 0;
int x;
uint8_t gHue = 0;

uint8_t fps;

#ifndef STASSID
#define STASSID "fly"
#define STAPSK  "6666666666"
#endif

unsigned int localPort = 8090;      // local port to listen on

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE + 1]; //buffer to hold incoming packet,
char  ReplyBuffer[] = "acknowledged\r\n";       // a string to send back
String param_1, param_2, param_3, param_4, param_5, param_6;
String res;
WiFiUDP Udp;

void setup() {
  Serial.begin(115200);
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(250);

  for (int i = 0; i <= NUM_LEDS; i++) {
    leds[i] = CRGB::Green;
    FastLED.show();
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(STASSID, STAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("UDP server on port %d\n", localPort);
  Udp.begin(localPort);
}

void loop() {
  // if there's data available, read a packet
  //delay(10);
  int packetSize = Udp.parsePacket();
  if (packetSize) {
   //Serial.printf("Received packet of size %d from %s:%d\n    (to %s:%d, free heap = %d B)\n",
     //             packetSize,
       //           Udp.remoteIP().toString().c_str(), Udp.remotePort(),
         //         Udp.destinationIP().toString().c_str(), Udp.localPort(),
           //       ESP.getFreeHeap());
  
    // read the packet into packetBufffer
    int n = Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    packetBuffer[n] = 0;

    res = packetBuffer;
    res.trim();

     Serial.println("Contents:");
     Serial.println(packetBuffer);
    int z = sscanf(packetBuffer, "%s %s %s %s %s %s", &param_1, &param_2, &param_3, &param_4, &param_5, &param_6);
    param_1.trim();
    param_2.trim();
    param_3.trim();
    param_4.trim();
    param_5.trim();
    param_6.trim();
  }
    //String param_1,param_2,param_3,param_4,param_5,param_6;
    //  packetBuffer[n+1]=0;
    //      packetBuffer.replace(" ","");
   



      fps = (uint8_t)param_2.toInt();
if (fps==0){fps==120;}















    
    //Serial.print(F("z="));
    //Serial.println(n);
    //Serial.print(F("Drones="));
    // Serial.print(dronenum);
   // Serial.println();
    //Serial.print(F("Command="));
    //Serial.println(param_1);
    //Serial.println(F("RGB value="));
    //Serial.print(param_2);
    //Serial.print(F(","));

    //Serial.print(param_3);
//    Serial.print(F(","));

  //  Serial.println(param_4);
   // Serial.print(F("Param 5 and 6"));
    //Serial.print(param_5);
    //Serial.print(F(""));
    //Serial.println(param_6);


   // Serial.println(packetBuffer);
  
    //  Serial.println(TYPE_NAME(packetBuffer));
    if (param_1 == "a")
    {

      for (int i = 0; i <= NUM_LEDS; i++)
      {
        leds[i] = CRGB::Blue;
      }
      FastLED.show();
    }
    else if (param_1 == "fill") {
      //Serial.println("in Fill command");

      uint8_t x, y, z;
      x = (uint8_t)param_2.toInt();
      y = (uint8_t)param_3.toInt();
      z = (uint8_t)param_4.toInt();

      //  fill_solid(leds,NUM_LEDS,CRGB((x,y,z)));
      for (int i = 0; i <= NUM_LEDS; i++)
      {
        fill_solid( &(leds[i]), 1 /*number of leds*/, CRGB( x, y, z) );
        FastLED.show();
      }

    }

    else if (param_1 == "ab")
    {
      for (int i = 0; i <= NUM_LEDS; i++)
      {
        leds[i] = CRGB::Green;
        FastLED.show();
      }
    }
    else if (param_1 == "dot") {
      uint8_t secs;
      secs = (uint8_t)param_2.toInt();
    if (secs==0){secs==100;}
      for (int whiteLed = 0; whiteLed < NUM_LEDS; whiteLed = whiteLed + 1) {
        // Turn our current led on to white, then show the leds
        leds[whiteLed] = CRGB::White;

        // Show the leds (only one of which is set to white, from above)
        FastLED.show();

        // Wait a little bit
        delay(secs);

        // Turn our current led back to black for the next loop around
        leds[whiteLed] = CRGB::Black;
      }

    }

    else if (param_1 == "fade")

    {
     
      
       uint8_t secs;
      secs = (uint8_t)param_2.toInt();
    if (secs==0){secs==10;}
      static uint8_t hue = 0;
   
 //     for (int i = 0; i < NUM_LEDS; i++) {
        // Set the i'th led to red
   //     leds[i] = CHSV(hue++, 255, 255);  
      for (int i = (NUM_LEDS) - 1; i >= 0; i--) {
        // Set the i'th led to red
        leds[i] = CHSV(hue++, 255, 255);
       // Show the leds
        FastLED.show();
       
        
        fadeall();
         delay(secs);
      }
  }
   else if(param_1=="rainbow")
    {       
      
      rainbow();
      FastLED.show();  
  // insert a delay to keep the framerate modest
  FastLED.delay(1000/fps); 
EVERY_N_MILLISECONDS( 10 ) { gHue=gHue +1; }
      }

      else if(param_1 =="rainbowg"){

rainbowWithGlitter() ;

        FastLED.show();  
  // insert a delay to keep the framerate modest
  FastLED.delay(1000/fps); 
EVERY_N_MILLISECONDS( 10 ) { gHue=gHue +1; }
        
        
        }

        else if(param_1 =="confetti")
        {
          confetti() ;

              FastLED.show();  
  // insert a delay to keep the framerate modest
  FastLED.delay(1000/FRAMES_PER_SECOND); 
EVERY_N_MILLISECONDS( 10 ) { gHue=gHue +1; }
        
        }

        else if(param_1 =="sinelon")
        {
          sinelon();
          FastLED.show();  
  // insert a delay to keep the framerate modest
  FastLED.delay(1000/fps); 
EVERY_N_MILLISECONDS( 10 ) { gHue=gHue +1; }
          }

          else if(param_1 =="bpm")
          {bpm();

           FastLED.show();  
  // insert a delay to keep the framerate modest
  FastLED.delay(1000/fps); 
EVERY_N_MILLISECONDS( 10 ) { gHue=gHue +1; }
            
            }

            else if(param_1 =="juggle")
            {
              juggle();
               FastLED.show();  
  // insert a delay to keep the framerate modest
  FastLED.delay(1000/fps); 
EVERY_N_MILLISECONDS( 10 ) { gHue=gHue +1; }
              }
 // else
 // {
  //  Serial.println(F("invalid request"));
 // }
  // send a reply, to the IP address and port that sent us the packet we received
 // Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  //Udp.write(ReplyBuffer);
packetSize=0;

}


void SetupStripedPalette()
{
  uint8_t r, g, b;
  r = (uint8_t)param_2.toInt();
  g = (uint8_t)param_3.toInt();
  b = (uint8_t)param_4.toInt();

  // 'black out' all 16 palette entries...
  for (int i = 0; i <= NUM_LEDS; i++)
  {
    fill_solid( &(leds[i]), 1 /*number of leds*/, CRGB::Black );

    // and set every fourth one to white.
    leds[0] = CRGB(r, g, b);
    leds[2] = CRGB(r, g, b);
    FastLED.show();
  }
  //currentPalette[8] = CRGB(r,g,b);
  //currentPalette[12] = CRGB(r,g,b);

}



void fadeall()
{
  for (int i = 0; i < NUM_LEDS; i++)
  {
    leds[i].nscale8(250);
  }
}





void rainbow() 
{
  
  // FastLED's built-in rainbow generator
  fill_rainbow( leds, NUM_LEDS, gHue, 7);
}


void rainbowWithGlitter() 
{
  // built-in FastLED rainbow, plus some random sparkly glitter
  rainbow();
  addGlitter(80);
}



void addGlitter( fract8 chanceOfGlitter) 
{
  if( random8() < chanceOfGlitter) {
    leds[ random16(NUM_LEDS) ] += CRGB::White;
  }
}



void confetti() 
{
  // random colored speckles that blink in and fade smoothly
  fadeToBlackBy( leds, NUM_LEDS, 10);
  int pos = random16(NUM_LEDS);
  leds[pos] += CHSV( gHue + random8(64), 200, 255);
}




void sinelon()
{
  // a colored dot sweeping back and forth, with fading trails
  fadeToBlackBy( leds, NUM_LEDS, 20);
  int pos = beatsin16( 13, 0, NUM_LEDS-1 );
  leds[pos] += CHSV( gHue, 255, 192);
}




void bpm()
{
  // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
  uint8_t BeatsPerMinute = 62;
  CRGBPalette16 palette = PartyColors_p;
  uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
  for( int i = 0; i < NUM_LEDS; i++) { //9948
    leds[i] = ColorFromPalette(palette, gHue+(i*2), beat-gHue+(i*10));
  }
}



void juggle() {
  // eight colored dots, weaving in and out of sync with each other
  fadeToBlackBy( leds, NUM_LEDS, 20);
  byte dothue = 0;
  for( int i = 0; i < 8; i++) {
    leds[beatsin16( i+7, 0, NUM_LEDS-1 )] |= CHSV(dothue, 200, 255);
    dothue += 32;
  }
}



/*
  test (shell/netcat):
  --------------------
	  nc -u 192.168.esp.address 8888
*/
