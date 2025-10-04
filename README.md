# BKV Departure Display

While commuting with BKV (Budapest's transport company), I don't like waiting for the next bus/train/tram to come. 

So I made this counter to show me when is the next departure.

This way, I can leave only, when I know I'll catch the next departure.

## API setup
I used the BKV API. 

Get your api key at https://opendata.bkk.hu/, and set it in `config.json`.

## Stop setup

In `config.json` under `stop_finding`, you can set the name, latitude and longitude of the stop you want to track. You can get the latitude and longitude for example with Google Maps.

## Hardware details
For details about the hardware setup, see my other project using the same setup: 
https://github.com/LEFTazs/oled-cube-world
