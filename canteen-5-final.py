try:
    from time import sleep_ms, ticks_ms
    from machine import I2C, Pin, DAC, PWM
    import esp8266_i2c_lcd 
    from hcsr04 import HCSR04
    import network
    import socket
    import urequests
    import machine
    import json
    
    SSID = "your_SSID" 
    PASSWORD = "your_password"  
    port=100
    wlan=None
    s=None
    
    mySensorArray1 = [0,0,0,0,0,0,0,0,0,0]
    mySensorArray2 = [0,0,0,0,0,0,0,0,0,0]
    mySensorArray3 = [0,0,0,0,0,0,0,0,0,0]
    mySensorArray4 = [0,0,0,0,0,0,0,0,0,0]
    mySensorArray5 = [0,0,0,0,0,0,0,0,0,0]

    hitCount1 = 0
    hitCount2 = 0
    hitCount3 = 0
    hitCount4 = 0
    hitCount5 = 0
    
    mySensor1 = HCSR04(trigger_pin = 12, echo_pin = 4)
    mySensor2 = HCSR04(trigger_pin = 14, echo_pin = 16)
    mySensor3 = HCSR04(trigger_pin = 27, echo_pin = 17)
    mySensor4 = HCSR04(trigger_pin = 26, echo_pin = 5)
    mySensor5 = HCSR04(trigger_pin = 25, echo_pin = 18)
    
    mySensorBaseAvg = 270 ##REMEMBER TO SET TO ACTUAL VALUE!
    
    for x in range(9):
        mySensorArray1[x] = mySensorBaseAvg
    for x in range(9):
        mySensorArray2[x] = mySensorBaseAvg 
    for x in range(9):
        mySensorArray3[x] = mySensorBaseAvg
    for x in range(9):
        mySensorArray4[x] = mySensorBaseAvg
    for x in range(9):
        mySensorArray5[x] = mySensorBaseAvg
      
    i2c = I2C(scl=Pin(21), sda=Pin(22), freq=400000)
    lcd = esp8266_i2c_lcd.I2cLcd(i2c, 0x27, 4, 20)
    
    lcd.move_to(0,0)
    lcd.putstr("Base avg:" + str(mySensorBaseAvg))
    sleep_ms(2000)
    
    def cycleValues(pickSensor):
        for x in range(9):
            pickSensor[x] = pickSensor[x+1]
        
        
    def connectWifi(ssid,passwd): #function to connect to the Web
        global wlan #declare a WLAN object
        lcd.move_to(0, 0) #move LCD cursor to top left corner
        lcd.putstr("Connect to WLAN") #write the string to the LCD
        wlan=network.WLAN(network.STA_IF)                     #create a wlan object
        wlan.active(True)                                     #Activate the network interface
        wlan.disconnect()                                     #Disconnect the last connected WiFi
        wlan.connect(ssid,passwd)                             #connect wifi
        while(wlan.ifconfig()[0]=='0.0.0.0'): #wait for connection
          sleep_ms(1)
        sleep_ms(1000) #hold on for 1 second
        lcd.move_to(0, 0) #move cursor to top left corner
        lcd.putstr("Connected      ") #write the string to LCD, note the blanks to erase the previous message
        url = "your_PHP_file_for_handling_input"
        headers = {'content-type': 'application/json'}
        data = {'message': 'Boot sequence complete with canteen-5-final.py'}
        jsonObj = json.dumps(data)
        resp = urequests.post(url, data=jsonObj, headers=headers)
        sleep_ms(1000)  #hold on for 1 second
        lcd.clear() #clear the LCD screen
        return True
        
    
    def main():
      connectWifi(SSID,PASSWORD)
      minuteCounter = 0
      while True:
        hitCount1 = 0
        hitCount2 = 0
        hitCount3 = 0
        hitCount4 = 0
        hitCount5 = 0
        
        cycleValues(mySensorArray1)
        mySensorArray1[9] = mySensor1.distance_cm()
        cycleValues(mySensorArray2)
        mySensorArray2[9] = mySensor2.distance_cm()
        cycleValues(mySensorArray3)
        mySensorArray3[9] = mySensor3.distance_cm()
        cycleValues(mySensorArray4)
        mySensorArray4[9] = mySensor4.distance_cm()
        cycleValues(mySensorArray5)
        mySensorArray5[9] = mySensor5.distance_cm()

        for x in range(9):
          if mySensorArray1[x] < 2 * mySensorBaseAvg / 3:
            hitCount1 += 1
        for x in range(9):
          if mySensorArray2[x] < 2 * mySensorBaseAvg / 3:
            hitCount2 += 1
        for x in range(9):
          if mySensorArray3[x] < 2 * mySensorBaseAvg / 3:
            hitCount3 += 1
        for x in range(9):
          if mySensorArray4[x] < 2 * mySensorBaseAvg / 3:
            hitCount4 += 1
        for x in range(9):
          if mySensorArray5[x] < 2 * mySensorBaseAvg / 3:
            hitCount5 += 1

        lcd.move_to(0,0)
        lcd.putstr("A" + str(hitCount1))
        lcd.move_to(3,0)
        lcd.putstr("B" + str(hitCount2))
        lcd.move_to(6,0)
        lcd.putstr("C" + str(hitCount3))
        lcd.move_to(9,0)
        lcd.putstr("D" + str(hitCount4))
        lcd.move_to(12,0)
        lcd.putstr("E" + str(hitCount5))
        lcd.move_to(0,1)
        
        if (hitCount1 > 6 and hitCount2 > 6 and hitCount3 > 6 and hitCount4 > 6 and hitCount5 > 6 ):
            myQueueStatus = "A massive queue   "
        elif (hitCount1 > 6 and hitCount2 > 6 and hitCount3 > 6 and hitCount4 > 6 ):
            myQueueStatus = "A long queue        "
        elif (hitCount1 > 6 and hitCount2 > 6 and hitCount3 > 6):
            myQueueStatus = "A medium queue      "
        elif (hitCount1 > 6 and hitCount2 > 6):
            myQueueStatus = "A short queue       "
        elif (hitCount1 > 6):
            myQueueStatus = "A minimal queue     "
        else:
            myQueueStatus = "No queue at all     "
        lcd.putstr(myQueueStatus)    
        sleep_ms(1000)

        print("A:" + str(int(mySensor1.distance_cm())) + " " + "B:"+ str(int(mySensor2.distance_cm())) + " " + "C:"+ str(int(mySensor3.distance_cm()))+ " D:"+ str(int(mySensor4.distance_cm()))+ " " + "E:"+ str(int(mySensor5.distance_cm())))
        print("A: " + str(hitCount1) + " " + "B: "+ str(hitCount2) + " " + "C: "+ str(hitCount3) + " " + "D: "+ str(hitCount4) + " " + "E: "+ str(hitCount5))
        myQueueSensorData = "A:" + str(hitCount1) + " " + "B:"+ str(hitCount2) + " " + "C:"+ str(hitCount3) + " " + "D:"+ str(hitCount4) + " " + "E:"+ str(hitCount5)
        myQueueSensorDist = "A:" + str(int(mySensor1.distance_cm())) + " " + "B:"+ str(int(mySensor2.distance_cm())) + " " + "C:"+ str(int(mySensor3.distance_cm()))+ " D:"+ str(int(mySensor4.distance_cm()))+ " " + "E:"+ str(int(mySensor5.distance_cm()))
        minuteCounter += 1
        if (minuteCounter % 60 == 0):
          try:
            url = "your_PHP_file_for_handling_input"
            headers = {'content-type': 'application/json'}
            data = {'message': myQueueStatus + " " + myQueueSensorData + " " +myQueueSensorDist }
            jsonObj = json.dumps(data)
            resp = urequests.post(url, data=jsonObj, headers=headers)
            minuteCounter=0
          except Exception as e:
            connectWifi(SSID,PASSWORD)
            f = open('buglog.txt','a')
            f.write("WLAN issue"+"\n")
            f.close()
        #lcd.clear()
        
    main()
    
except Exception as e:
    url = "your_PHP_file_for_handling_input"
    headers = {'content-type': 'application/json'}
    data = {'message': str(e)}
    jsonObj = json.dumps(data)
    resp = urequests.post(url, data=jsonObj, headers=headers)
    f = open('buglog.txt','a')
    f.write(str(e)+"\n")
    f.close()
    import machine
    machine.reset()    

