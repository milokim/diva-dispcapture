# diva-dispcapture
HDMI display capture from target board and socket communication with the diva-server

## Device
RPi 2 + [PiCapture](https://lintestsystems.com/products/picapture-hd1) board.
This enables recording HDMI signal from diva target device and generating mp4 file.

## Flow chart
 			+---------------------+     +---------------------+
 			|  diva dispcapture   |     |      diva server    |
 			+---------------------+     +---------------------+
  			+----+ systemd +----+
  			|                   | capture:hdmi
  			|    dcthread.py    | <-----
  			|      |    ^       | ------>
  			|      v    |       |  done
  			|    picapture.py   |  scp mp4
  			|                   |
  			+-------------------+
       			raspivid
       			MP4Box

## Files
- systemd: register the display capture service on startup
- dcthread.py: communicate with the diva-server. Call picapture.py on demand
- picapture.py: record display output (h264) from the target device. Convert h264 to mp4.
