##boombox
once the below dependencies are installed, clone the repo and run main.py. the script runs a server (UDP by default, although it's possible to change this by passing ```socket_type='tcp'``` when constructing the ReceiveAndPlay class) in a serve_forever loop listening for messages formatted as 'trackname/volume', where volume is a float between 0.0 - 1.0.

sound files should be placed in the sound/ within the repo's directory. you'll have to make the sound/ dir yourself as it is currently in the .gitignore.

###dependencies:
#### *pyyaml*
```
sudo pip3 install pyyaml
```

#### *pygame and dependencies*
```
sudo apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
sudo apt-get install libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev
sudo pip3 install pygame
```
[reference](https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=33157&p=332140&hilit=croston%2bpygame#p284266)

\- or - (untested)

```
sudo apt-get install python3-pygame
```

#### *Adafruit_MAX9744 library (if using)*
[Adafruit's library](https://github.com/adafruit/Adafruit_Python_MAX9744)


#### *set system volume to 97% (0db):*
```
amixer set PCM -- 97%
```
