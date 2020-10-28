# Screencap: A programme to screencap and rename your file(s)
To use the script, you have to install mss module and pygame. Use this to install necessary modules.
```pip install -r requirements.txt```

There are 2 screenshot modes: single and continuous. 
For single mode: Enter a filename and simply press Screencap.
For continuous mode: First, tick the box and then set an interval. Press Screencap to start capturing screen every set interval. Press Stop to stop the continuous mode.


For Linux user, if you encounter 
`pygame.error: No available audio device`, 
please install the following libraries:
`sudo apt-get install libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev`

