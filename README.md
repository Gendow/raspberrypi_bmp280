### Measuring barometric pressure, temperature and altitude with Adafruit BMP280 sensor and a RaspberryPi

Connect a BMP280 temperature and barometric pressure sensor to your RaspberryPi. This tutorial will go through the necessary steps to wire up the sensor and program your RaspberryPi to show meaningfull measurements from the BMP280 sensor.

- [Components](#components)
- [Wiring to RaspberryPi](#wiring)
- [Detect sensor](#detect-sensor)
- [Reading sensor data with Python](#reading-sensor-data-with-python)
- [Calibrating altitude calculations using weather data](#calibrating-altitude-calculations-using-real-time-weather-data)

If you have any questions, comments or suggestions, please make sure to contact me. 

### Components

- RaspberryP 3 Model B+ with latest Raspbian installed
- [Adafruit bmp280](https://www.adafruit.com/product/2651) temperature and barometric pressure sensor
- 4 GPIO [jumper wires](https://www.kiwi-electronics.nl/jumperwires-10-stuks-15-cm-femafe-female?search=gpio%20kabels&description=true) female to female

It is a common practice to use a breaborad for connecting sensors to a RaspberryPi. I didn't use one. If you do, you will need female to male jumper wires. 

### Wiring
The sensor can be wired to the RaspberryPi with I2C and SPI. In this tutorial we will use the I2C standard. Therefore we need to connect the power supply (3V3), ground (GND) and the I2C (SCL & SDA) pins between both devices. I highly recommened reading the official [pinout documentation](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/pinouts) of the sensor better understand the purpose of the pins.

The image below shows how to do the [wiring](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/circuitpython-test).

<img src="https://cdn-learn.adafruit.com/assets/assets/000/058/619/original/adafruit_products_raspi_bmp280_i2c_bb.png?1533324749" alt="drawing" width="450"/>

- RaspberryPi 3V3 to VIN on sensor (red)
- RaspberryPi GND to GND on sensor (black)
- RaspberryPi SCL to SCK on sensor (orange)
- RaspberryPi SDA to SDI on sensor (blue)

The pins on the sensor are labelled on the board. The pins on the RaspberryPi can be found using the `pinout` command in the terminal. 

<img src="https://github.com/codehub-rony/raspberrypi_bmp280/blob/master/images/pinout.PNG">

Unfortunately the image above does not show where the I2C pins are. To find this, check out the interactive pinout chart on [https://pinout.xyz/](https://pinout.xyz/).

### Detect sensor
Once we have wired the sensor, we need to make sure the RaspberryPi has actually detected it. Otherwise our Python code will throw an error. Detect the sensor:

`sudo i2cdetect -y 1` 

This will return an output similar to the image below. This matrix shows all devices that have been detected on the I2C bus. The multi device support of the I2C standard is one of the reasons for the popularity of the standard. The RaspberryPi will automatically assign each device to a different port number. This allows us to communicate with different devices at the same time. 

<img src="https://github.com/codehub-rony/raspberrypi_bmp280/blob/master/images/i2c_detect.PNG">

We can see that our sensor has been detected on port 77.

If your sensor hasn't been detected; double check the wiring. Also, make sure I2C has been enabled and configured properly. Adafruit has a nice [tutorial](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2) on how to set up the I2C on your RasperryPi. 

### Reading sensor data with Python
Make sure you have installed [Adafruit CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython). This is a python library that adds hardware support to Python.

Assuming CircuitPython is working, we can now move on to installing the specific library for the BMP280 sensor

`pip3 install adafruit-circuitpython-bmp280`

From here on it is super easy to read the measurements of the sensor. First, we will create our bmp280 object to access the sensor:
``` 
# Create sensor object using the I2C port
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
``` 

Now, there is some fake news going on in this sensor. It claims to measure temperature, barometric pressure and altitude. Altitude can't be measured. Instead, the altitude is calculated using the pressure measurements and the Mean Sea Level Pressure (MSRLP). The MSLP is the local pressure adjusted for the sea level. It is typically the pressure  shown in the weather reports online. The sensor has a property for the MSLP, but it has to be set manually. So, find a weather report for your location and set the property:

```
sensor.sea_level_pressure = 991.35 
```
This method is fine for now. However, the weather and pressure are changing constantly. This will also affect the pressure at sea level, which in turn.... Yes, will also affect the accuracy of your altitude readings. So, make sure to update the `sea_level_pressure` property on a regular base. Or - if you are lazy like me - automate this task. More on this in the next section.

Now that we have configured our sensor and the altitude calculations, we can start reading out the sensor. The people at Adafruit are doing an amazing job at simplifying things for us. This is the code to get your first measurements printed to the console:

```
while True:
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Pressure: %0.1f hPa" % sensor.pressure)
    print("Altitude: %0.2f meters" % sensor.altitude)
    print(datetime.datetime.now())
    time.sleep(10)

```

The code above will print the temperature, pressure, altitude and current time every 10 seconds. Run your code and take a moment to enjoy the satisfaction and excitement this small project is currently bringing you. 

### Calibrating altitude calculations using real time weather data
Weather changes, so does the pressure. That's why people are interested in measuring it. As time passes and the pressure changes, your `sensor.sea_level_pressure` will become incorrect. In my case the altitude was 20 meters of. We can update the property manually as mentioned before. OR, we can use actual weather data from weather stations.

In The Netherlands the Dutch Meteorological  Institute provides real time weather data via [weerlive](http://weerlive.nl). The service requires an API key which you can get with a free subscription. To get a request we need to install the `request` package for doing a `get` request, and the `json` package to parse the result.

```
pip3 install request 
pip3 install json
``` 

Now we can define a simple function to get the weather data from the weather stations. We only need to provide two parameters to the request: `key` and `locatie`. The `key` is your API key and the `locatie` is a city in The Netherlands. It will automatically fetch the weather data from the closest weather station. The if statement checks whether the weerlive server is online and if our request is valid. Any errors will be printed to the console. 

```
    req = requests.get('http://weerlive.nl/api/json-data-10min.php?key=YOUR_APIY_KEY&locatie=Amsterdam')

    if req.status_code == 200:
        payload = json.loads(req.text)
        sensor.sea_level_pressure = float(payload["liveweer"][0]["luchtd"])
    else:
        print("error from weather API: %" % req.status-code)
```

If the request is valid, we will receive an response as a `json`, like this [example](http://weerlive.nl/api/json-data-10min.php?key=demo&locatie=Amsterdam). Parse the json using `json.loads` and extract the values of interest. In our case this is the value under the `luchtd` (=luchtdruk = pressure) attribute. Finally, assign the value to the `sensor.sea_level_pressure` to calibrate the sensor. 


##### Dealing with API request limits
The weerlive API has a [request limit](http://weerlive.nl/delen.php) of 300 requests per day. We want to update the MSLP value as often as possible to keep the sensor calibrated, but not more than the API limit. We will create a [thread function](https://realpython.com/intro-to-python-threading/#what-is-a-thread): a function that runs parallel to the readouts of the sensor data, extended with a timer. The timer will ensure the function is being executed (i.e. weather station data is requested), but with a delay/pause. Adding the thread function to the code above results in:

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

If we put all these pieces of code together and run the code, we will see the following result in the terminal:

<img src="https://github.com/codehub-rony/raspberrypi_bmp280/blob/master/images/measurement_example.PNG">

We can see the `temperature`, `pressure` in `hPa` and `altitude` measurements. However, this time, the altitude has been calculated using the actual `sea level pressure`. We have also calculated the pressure in `mmHg`. In this particular case the MSLP and the measured pressure are more or less the same. But I have had days in which there is a significant difference between the two.

