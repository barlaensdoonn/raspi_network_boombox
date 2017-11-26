boombox

dependencies:
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

#### *Adafruit_MAX9744 library and wrapper (if using)*
[Adafruit's library](https://github.com/adafruit/Adafruit_Python_MAX9744)
\[wrapper for above library](https://github.com/barlaensdoonn/ampli)

set system volume to 97% (0db):
```
amixer set PCM -- 97%
```
