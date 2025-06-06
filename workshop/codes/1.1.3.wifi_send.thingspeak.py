# wifi_send_ts.py
from machine import Pin, I2C, deepsleep
import machine, ubinascii, urequests
from wifi_tools import *
from sensors import sensors
import time
# WiFi credentials
SSID = 'Livebox-08B0'
PASSWORD = 'G79ji6dtEptVTPWmZP'

rtc = machine.RTC()
# Function to send data to ThingSpeak
def send_data_to_thingspeak(lumi, temp, humi):
    try:
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi)
        url = "https://api.thingspeak.com/update?key=YOX31M0EDKO0JATK"+sf1+sf2+sf3
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi)
    except Exception as e:
        print("Failed to send data:", e)       

def main():
    delta=0.01
    rtc_mem = rtc.memory()
    if len(rtc_mem) == 0:
        stemp = 20.0
    else:
        stemp = float(rtc_mem.decode())
     
    lumi, temp, humi = sensors(sda=8, scl=9)
    print(temp,stemp,delta)
    if (abs(stemp-temp)> delta):
        rtc.memory(str(temp).encode())
        connect_WiFi(SSID, PASSWORD)
        print("WiFi connected")
        send_data_to_thingspeak(lumi, temp, humi)
        time.sleep(1)
        disconnect_WiFi()
        
    print("goes to deepsleep")
    deepsleep(15*1000)   # wait 15 seconds
    
main()
