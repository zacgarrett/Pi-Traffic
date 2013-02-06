Pi-Traffic
==========
This is a car monitoring script that runs on a raspberry pi. 

Hardware Requirements
---------------------

* Raspberry pi
* [Raspberry pi proto plate](http://www.adafruit.com/products/801)
* [MCP3008](https://www.adafruit.com/products/856) -- Gives the raspberry pi analog input
* Differential pressure sensor (I used [Freescale MPX5500DP](http://www.digikey.com/scripts/DkSearch/dksus.dll?WT.z_header=search_go&lang=en&keywords=MPX5500DP-ND&x=0&y=0&cur=USD))
* Tubing to fit the pressure sensor

Setting up the Raspberry Pi
---------------------------

    sudo apt-get update
    sudo apt-get install python-dev
    sudo apt-get install python-setuptools
    sudo easy_install rpi.gpio
