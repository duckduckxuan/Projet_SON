#include <Audio.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>
#include "Vinyl.h"

#define SDCARD_CS_PIN 10
#define PLAY_BUTTON_PIN 0

bool isPlaying = false;

Vinyl vinyl;

AudioOutputI2S out;
AudioPlaySdWav audioSD;
AudioControlSGTL5000 audioShield;
AudioMixer4 mix;

AudioConnection patchCord0(vinyl, 0, mix, 0);
AudioConnection patchCord1(audioSD, 0, mix, 1);
AudioConnection patchCord2;
AudioConnection patchCord3;

void setup() {
  Serial.begin(9600);
  audioShield.enable();
  audioShield.volume(2);
  AudioMemory(4);
  pinMode(PLAY_BUTTON_PIN, INPUT);
  mix.gain(0, 5);
  mix.gain(1, 0.15);

  Serial.println("Initializing SD card...");

  if (!(SD.begin(SDCARD_CS_PIN))) {
    while (1) {
      Serial.println("Unable to access the SD card");
      delay(500);
    }
  }
  else {
    Serial.println("Initialize successfully");
  }
}

void loop() {
  int knobValue = analogRead(A4);
  int playButtonState = digitalRead(PLAY_BUTTON_PIN);
  float gain = map(knobValue, 0, 1023, 0, 7);
  mix.gain(0, gain);

  static float previousGainValue = -1.0;
  float gainValue = knobValue / 102.3;
  if (fabs(gainValue - previousGainValue) > 0.1) {
    Serial.printf("%.1f, 'gain'\n", gainValue);
    previousGainValue = gainValue;
  }


  if (playButtonState && !isPlaying) {
    Serial.println("Start playing");
    isPlaying = true;
    Serial.printf("%d, 'play'\n", isPlaying);
    delay(800);
    audioSD.play("song.WAV");
    patchCord2.connect(mix, 0, out, 0);
    patchCord3.connect(mix, 0, out, 1);
    delay(500);
  }


  else if (playButtonState && isPlaying) {
    Serial.println("Stop playing");
    isPlaying = false;
    Serial.printf("%d, 'play'\n", isPlaying);
    delay(100);
    audioSD.stop();
    patchCord2.disconnect();
    patchCord3.disconnect();
    delay(500);
  }

  delay(100);
}
