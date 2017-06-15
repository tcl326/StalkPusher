/*
  StalkPusherHAL.h - Hardware Abstraction Layer of StalkPusher.
  Created by Ting-Che, Lin, June 06, 2017.
*/

#ifndef StalkPusherHAL_h
#define StalkPusherHAL_h

#include "Arduino.h"

class StalkPStalkPusherHAL
{
  public:
    StalkPStalkPusherHAL(int pin);
    void getTemperature();
    void getHumidity();
    void getIMUAngle();
    void 
  private:
    int _pin;
};

#endif
