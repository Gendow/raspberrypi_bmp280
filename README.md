
This repository contains the steps I took to connect the raspberryPi with a bmp280 temp, humidity and barometric sensor. 


1. enable I2C (https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)
I installed latest version of raspbian. Required libraries are already installed
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools

2. Installing Kernel Support (with Raspi-Config) / enable the i2c controlers
run sudo raspi-config
select interface optoins --> I2C --> enable I2C interface (yes)
reboot system
verify acitivation by ls /dev/i2c*, the files should be listed

3. install python libraries:
run sudo pip3 install adafruit-circuitpython-bmp280

3. Connect BMP280 according to layout
- test whethrsudo i2cdetect -y 1


4. pip3 install board



#### Assembly
For a better understanding of the different pins, check out [this](https://learn.adafruit.com/assets/58619)

<img src="https://cdn-learn.adafruit.com/assets/assets/000/058/619/original/adafruit_products_raspi_bmp280_i2c_bb.png?1533324749" alt="drawing" width="450"/>


- Pi 3V3 to sensor VIN
- Pi GND to sensor GND
- Pi SCL to sensor SCK
- Pi SDA to sensor SDI

<img src="https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwiGpaWHma_lAhVDK1AKHXE0ApEQjRx6BAgBEAQ&url=http%3A%2F%2Fwww.raspberrypirobotics.com%2Fraspberry-pi-gpio-access%2F&psig=AOvVaw1f3vdjlCFb9pkF0MKLAxyG&ust=1571810559547839" alt="drawing" width="450"/>

The sensor pins are written on the board itself. The pins of the raspberryPi are mapped below
Overview of the 

#### Getting weather data to calibrate altitude meter
ipi3 install request
pip3 install josn
threading ---> used for executing the request function. 
