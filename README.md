### Measure barometric pressure, temperature and altitude with a RaspberryPi

Connect a BMP280 temperature and barometric pressure sensor to your RaspberryPi. This tutorial will go through the necessary steps to wire up the sensor and program your RaspberryPi to show meaningfull measurements from the BMP280 sensor.

- [Components](#components)
- [Wiring to RaspberryPi](#wiring)
- [Detect sensor](#detect-sensor)
- [Reading sensor data with Python](#reading-sensor-data-with-python)
- [Calibrating altitude calculations using weather data](#calibrating-altitude-calculations-using-weather-data)

If you have any questions, comments or suggestions, please make sure to contact me. 

### Components

- RaspberryP 3 Model B+ with latest Raspbian installed
- [Adafruit bmp280](https://www.adafruit.com/product/2651) temperature and barometric pressure sensor
- 4 GPIO [jumper wires](https://www.kiwi-electronics.nl/jumperwires-10-stuks-15-cm-femafe-female?search=gpio%20kabels&description=true) female to female

It is a common practice to use a breadboard for connecting sensors to the RaspberryPi. In my set up I connected the sensor directly to the RaspberryPi. If you intend to use a breaboard, you will need female to male jumper wires. 

### Wiring
The sensor can be wired to the RaspberryPi both with I2C and SPI. In this tutorial we will use the I2C standard. We will need to connect the power supply (3V3), ground (GND) and the I2C (SCL & SDA) pins.

The image below shows the [wiring](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/circuitpython-test) of the sensor. For a more in depth explanation of the pins, visit the official [pinout documentation](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/pinouts) of the sensor.

- RaspberryPi 3V3 to VIN on sensor
- RaspberryPi GND to GND on sensor
- RaspberryPi SCL to SCK on sensor
- RaspberryPi SDA to SDI on sensor

<img src="https://cdn-learn.adafruit.com/assets/assets/000/058/619/original/adafruit_products_raspi_bmp280_i2c_bb.png?1533324749" alt="drawing" width="450"/>

The pins on the sensor have been labelled on the board itself. The pins on the RaspberryPi can be found using a pinout chart as shown below. See this [interactive resource](https://pinout.xyz/) for an extensive guide. 

![pi_pinout](https://www.raspberrypi.org/documentation/usage/gpio/images/GPIO-Pinout-Diagram-2.png)


### Detect sensor
Once you have wired the sensor, we need to make sure the RaspberryPi has actually detected it. Otherwise our Python code will throw an error. To check if the device has been detected, we can use:

`sudo i2cdetect -y 1` 

This will return a matrix with all the ports and devices that have been detected. One of the reasons why I2C is a popular standard, is that it supports multiple devices on the same pins. The RaspberryPi will automatically assign each device to a different port. This can also be seen in this matrix. 

<img src="https://github.com/codehub-rony/raspberrypi_bmp280/blob/master/images/i2c_detect.PNG">

We can see that the sensor has been detected on port 77. Continue to the next section of this tutorial if you can see your sensor on any of the ports.

If your sensor hasn't been detected; double check the wiring. Also, make sure to check your I2C has been enabled and configured properly. Adafruit has a nice [tutorial](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2) on how to set up the I2C. 

### Reading sensor data with Python
Install the python library with `pipenv` for reading out the sensor measurements

`pipenv install adafruit-circuitpython-bmp280` 

#### Calibrating altitude calculations using weather data
The altitude calculations provided by the sensor need to be calibrated, otherwise the altitude will be incorrect in time. These calculations are made based on the measured barometric pressure by the sensor, measured temperature and the Mean Sea Level Pressure (MSLP) at the location of the sensor. The MSLP is the local pressure adjusted for the sea level and is typically the pressure that is shown in the weather reports online. We can calibrate the sensor by looking up de MSLP at our location in the weather and setting the calibration variable to that pressure:

`sensor.sea_level_pressure = 1012.2` 

As simple as that. However, the pressure is not constant. It changes over time just like the weather does. We don't want to manually calibrate the sensor every now and then, we can do that programmaticaly by connecting to an API of the nearest weather station. In The Netherlands the Dutch Meteological Instute provides real time weather data via  [weerlive](http://weerlive.nl). The service requires an API key which you can get with a free subcriptions. To get a request we need to install the following package

```
pipenv install request 
pipenv install json
``` 

Now we can define a simple function to get the weather data from the weather stations. We only need to provide two parameters to the get request: `key` and `locatie`. The `key` is your api key and the `locatie` is a city in The Netherlands. It will automatically fetch the weather data from the closest weather station. The if statement checks whather the weerlive server is online and if our request is valid. Any errors will be printed to the console. 

```
    req = requests.get('http://weerlive.nl/api/json-data-10min.php?key=YOUR_APIY_KEY&locatie=Amsterdam')

    if req.status_code == 200:
        payload = json.loads(req.text)
        sensor.sea_level_pressure = float(payload["liveweer"][0]["luchtd"])
    else:
        print("error from weather API: %" % req.status-code)
```

If the request is valid and the server is online, we will receive an response as a `json`, like this [example](http://weerlive.nl/api/json-data-10min.php?key=demo&locatie=Amsterdam). Parse the json using `json.loads` and extract the values of interest. In our case this is the value under the `luchtd` (=luchtdruk = pressure) attribute. In the final step we assign this value to the `sensor.sea_level_pressure` to calibrate the sensor. 


##### Dealing with API request limits
The weerlive API has a [request limit](http://weerlive.nl/delen.php) of 300 requests per day. We want to update the MSLP value as often as possible to keep the sensor calibrated, but not more then 300 times as the API will refuse our requests. We will create a [thread](https://realpython.com/intro-to-python-threading/#what-is-a-thread) function: a function that runs parellel to the readouts of the sensor data, extended with a timer. The timer will ensure the function is being executed (i.e. weather station data is requested), but with a pause. Adding the thread function to the code above results in this:

```
def getSeaLevelPressure():
    threading.Timer(240, getSeaLevelPressure).start()
    req = requests.get('http://weerlive.nl/api/json-data-10min.php?key=%s&locatie=Arnhem' % apikey)

    if req.status_code == 200:
        payload = json.loads(req.text)
        sensor.sea_level_pressure = float(payload["liveweer"][0]["luchtd"])
    else:
        print("error from weather API: %" % req.status-code)
  
getSeaLevelPressure()
```





threading ---> used for executing the request function. 

