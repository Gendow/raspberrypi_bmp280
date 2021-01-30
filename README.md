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
The sensor can be wired to the RaspberryPi both with I2C and SPI. In this tutorial we will use the I2C standard. Therefore we need to connect the power supply (3V3), ground (GND) and the I2C (SCL & SDA) pins between both devices.

The image below shows how to do the [wiring](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/circuitpython-test) of the sensor.

<img src="https://cdn-learn.adafruit.com/assets/assets/000/058/619/original/adafruit_products_raspi_bmp280_i2c_bb.png?1533324749" alt="drawing" width="450"/>

- RaspberryPi 3V3 to VIN on sensor (red)
- RaspberryPi GND to GND on sensor (black)
- RaspberryPi SCL to SCK on sensor (orange)
- RaspberryPi SDA to SDI on sensor (blue)

The pins on the sensor are labelled on the board. The pins on the RaspberryPi can be found using the `pinout` command in the terminal. 

<img src="https://github.com/codehub-rony/raspberrypi_bmp280/blob/master/images/pinout.PNG">

I highly recommened reading the official [pinout documentation](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/pinouts) of the sensor to understand what these pins are acutally for.

### Detect sensor
Once we have wired the sensor, we need to make sure the RaspberryPi has actually detected it. Otherwise our Python code will throw an error. To check if the device has been detected type the following command in the terminal:

`sudo i2cdetect -y 1` 

This will return a matrix showing all devices that have been detected on the I2C bus. Yes, you read it correctly. I2C provides us with the possibility to connect multiple devices on the same pins. This is unique to the I2C standard. The RaspberryPi will automatically assign each device to a different port number. This allows us to communicate with different devices at the same time. 

<img src="https://github.com/codehub-rony/raspberrypi_bmp280/blob/master/images/i2c_detect.PNG">

We can see that our sensor has been detected on port 77. Continue to the next section of this tutorial if your sensor has been assigned to any of the ports.

If your sensor hasn't been detected; double check the wiring. Also, make sure I2C has been enabled and configured properly. Adafruit has a nice [tutorial](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2) on how to set up the I2C on your RasperryPi. 

### Reading sensor data with Python
Make sure you have installed [Adafruit CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython). This is a python library that adds hardware support to Python. It allows us to work microcontrolers in an easy way. 

Assuming CircuitPython is working, we can now move on to installing the specific library for the BMP280 sensor

`pip3 install adafruit-circuitpython-bmp280`

From here on it is super easy to read the measurements of the sensor. First, we will create our bmp280 object to access the sensor:
``` 
# Create sensor object using the I2C port
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
``` 

Now, there is some fakenews going on in this sensor. It isn't actually measuring the altitude. You can't measure altitude with hardware. Instead, the altitude is calculated using the pressure measurements and the sea level pressure. The sea level pressure needs to be set manually in order to get a correct altitude. You can find the sea level pressure in local weather reports. 

```
sensor.sea_level_pressure = 991.35 
```
This method is oke for now. However, the weather is changing constantly. This change will also affect the pressure at sea level, which in turn.... Yes, will also affect the accuracy of your altitude calculations. So, make sure to update the `sea_level_pressure` property on a regular base. Or - if you are lazy like me - automate this task. More on this in the next section.

Now that we have configured our sensor and the altitude calculations, we can start reading out the sensor. The people at Adafruit are doing an amazing job at simplifying things for us. This is the code to get your first measurements printed to the console:

```
while True:
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Pressure: %0.1f hPa" % sensor.pressure)
    print("Altitude: %0.2f meters" % sensor.altitude)
    print(datetime.datetime.now())
    time.sleep(10)

```

The above code will print the temperature, pressure, altitude and current time every 10 seconds. Take a moment to enjoy the satisfaction and excitment this small project is currently bringing you. 


<img src="https://media.giphy.com/media/xUPJPnaANa5SFyTlTi/giphy.gif">


#### Calibrating altitude calculations using weather data
The sensor does not actually measure the altitude. You can't measure altitude using barometric pressure. The altitude is based on a calculation in which the measured 
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

