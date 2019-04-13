# Five sensor queue monitor with LCD
This device allows you to monitor five ultrasound sensors and find out the length of the queue. MicroPython, ESP32, HC-SR04, LCD display, and Internet connection.

LCD library from dhylands.

FILES:
canteen.php is the file on the server to which the device sends its measurements once a minute.
canteen-5-final.py is the file that runs on the ESP32 and monitors the five HC-SR04 sensors and measures the distance between the sensor and the ground. There is a variable, BaseAverage, which must be set to the height of the area where the system is installed. Also, you need to give your SSID and password in this file.
Other files are libraries needed for the ESP32 to run the HC-SR04 and the LCD, as well as the MicroPython requests and JSON.

See http://www.sabulo.com/sb/3d-printing-2/low-cost-low-impact-queue-monitoring-system/ for how this thing works. 

Also, many images on Instagram at @isohoo3d
