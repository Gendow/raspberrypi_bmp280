
This repository contains the steps I took to connect the raspberryPi with a bmp280 temperature and barometric sensor. 

- RaspberryP 3 Model B+ with latest Raspbian isntalle d
- [Adafruit bmp280](https://www.adafruit.com/product/2651) temperature and barometric pressure sensor
- 4 GPIO [jumper wires](https://www.kiwi-electronics.nl/jumperwires-10-stuks-15-cm-femafe-female?search=gpio%20kabels&description=true) female to female

It is a common practice to use a breadboard for connecting sensors to the RaspberryPi. In that case the GPIO jumper wires should be female to male
  

#### Set up 
-----------
enable I2C

`run sudo raspi-config` 


Check if the sensor has been detected

`sudo i2cdetect -y 1` 

The output should look something like this:

`put overview of output here`

If the overview only shows zero's, then your raspberrypi did not detect the sensor. Check whether jumper wires have been installed correctly. 


1. enable I2C (https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)
I installed latest version of raspbian. Required libraries are already installed
`sudo apt-get install -y python-smbus`
`sudo apt-get install -y i2c-tools`

Check if the I2C is enabled: 
`ls /dev/i2c` 

`/dev/i2c-0`

2. Installing Kernel Support (with Raspi-Config) / enable the i2c controlers


select interface optoins --> I2C --> enable I2C interface (yes) reboot system, verify acitivation by ls /dev/i2c*, the files should be listed

install python libraries:

run sudo pip3 install adafruit-circuitpython-bmp280

 Connect BMP280 according to layout
 pip3 install board

#### Assembly
The sensor has the following pins: 	
For a better understanding of the different pins, check out [this](https://learn.adafruit.com/assets/58619)

<img src="https://cdn-learn.adafruit.com/assets/assets/000/058/619/original/adafruit_products_raspi_bmp280_i2c_bb.png?1533324749" alt="drawing" width="450"/>

- Raspberrypi 3V3 to sensor VIN
- Raspberrypi GND to sensor GND
- Raspberrypi SCL to sensor SCK
- Raspberrypi SDA to sensor SDI

<img src="http://www.raspberrypirobotics.com/wp-content/uploads/2018/01/Raspberry-GPIO.jpg" width="450"/>

The sensor pins are written on the board itself. The pins of the raspberryPi are mapped below
Overview of the 

## Reading sensor data
---
Install the python library for reading out the sensor

`pip3 install adafruit-circuitpython-bmp280` 



### Calibrating altitude calculations with from a weather station
The altitude calculations provided by the sensor need to be calibrated, otherwise the altitude will be incorrect intime. These calculations are made based on the measured barometric pressure by the sensor, measured temperature and the Mean Sea Level Pressure (MSLP) at the location of the sensor. The MSLP is the local pressure adjusted for the sea level and is typically the pressure that is shown in the weather reports online. We can calibrate the sensor by looking up de MSLP at our location in the weather and setting the calibration variable to that pressure:

`sensor.sea_level_pressure = 1012.2` 

As simple as that. However, the pressure is not constant. It changes over time just like the weather does. We don't want to manually calibrate the sensor every now and then, we can do that programmaticaly by connecting to an API of the nearest weather station. In The Netherlands the Dutch Meteological Instute provides real time weather data via  [weerlive](http://weerlive.nl). The service requires an API key which you can get with a free subcriptions. To get a request we need to install the following package

```
pip3 install request` 
pip3 install json
``` 

ipi3 install request
pip3 install josn
threading ---> used for executing the request function. 

