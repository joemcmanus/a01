# a01
A collection of programs for the Olympus Air A01 OPC 

The Olympus Air A01 is a unique camera that is designed around an open platform. 
This repo will hold a collection of scripts to run on the device. 
More features will be added as I play with this more. 

All of these programs are writte in python if you need any inspiration for creating your OPC code take a look. 

# a01.py
This program will enable picture taking via command line on python.

    usage: a01.py [-h] [--pid] [--interval INTERVAL] [--count COUNT] [--debug]

    Olympus Air A01 Control Program. (C) Joe McManus 2016

    optional arguments:
      -h, --help           show this help message and exit
      --pid                Create a pid file in /var/run/a01.pid
      --interval INTERVAL  Take pictures at X interval in seconds.
      --count COUNT        Take X pictures
      --getImageList       List images on SD card
      --getImage GETIMAGE  Download image imageName
      --delImage DELIMAGE  Delete image imageName
      --debug              Enable debug messages

To take one photo just run ./a01.py.

     sazed:a01 joe$ ./a01.py 
     Taking 1 photo.

To take 5 photos at 3 seconds each provide the --interval and --count options. 

    sazed:a01 joe$ ./a01.py  --interval 5 --count 3
    Setting Intervalometer to take 5 pictures.
    Taking a total of 3 pictures.
    Taking picture 1 of 3 
    Sleeping for 5 seconds.
    Taking picture 2 of 3 
    Sleeping for 5 seconds.
    Taking picture 3 of 3 

To enable debug messages use the --debug option. 

    http://192.168.0.10/get_connectmode.cgi
    <?xml version="1.0"?>
    <connectmode>OPC</connectmode>
    http://192.168.0.10/switch_cameramode.cgi?mode=rec
    <?xml version="1.0"?><result>OK</result>
    .....


To list images use the --getImageList option.

    sazed:a01 joe$ ./a01.py --getImageList
    PA190001.JPG
    PA190002.JPG
    PA190003.JPG

To delete images use the --delImage imageName option. 

    sazed:a01 joe$ ./a01.py --delImage PA190001.JPG

To download images use the --getImage option.

    sazed:a01 joe$ ./a01.py --getImage PA190001.JPG

# a01-flask.py 

A web based front end to control the Air. 
![alt_tag](https://raw.githubusercontent.com/joemcmanus/a01/master/ao1FrontEnd.png)

To start run ./a01-flask.py . 

Make sure you are connected to the AIR wifi or you will see the error below. 

    sazed:a01 joe$ ./a01-flask.py
    Trying to connect to A01
    ERROR: Unable to reach air at : http://192.168.0.10/
    ERROR: Make sure you are connected to the Air Wifi. 
    ERROR: The SSID is something like AIR-A01-MAC


Currently you can take pictures, view thumbnails, download images and remove files from the SD card. 


Current known issue: 
 Intervalometer not implemented in Web UI

