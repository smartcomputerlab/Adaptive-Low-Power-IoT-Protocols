# espnow.adaptive_sender.py
import network, esp
from machine import Pin, deepsleep, freq
import espnow
import utime, ustruct
from sensors import *
from rtc_tools import *
from nvs_tools import *
nvs_key="param"                            # key to NVS records
led = Pin(3, Pin.OUT) 

def connect_send_espnow(chan,wkey,lumi,temp,humi):
    freq(160000000)        # maximum frequency
    sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
    #sta.disconnect()
    sta.active(True)
    sta.config(txpower=5.0)
    sta.config(channel=11) # must be provide from gateway channel
    sta.disconnect()      # For ESP8266
    esp = espnow.ESPNow()
    esp.active(True); print("now active")
    peer= b'\xFF\xFF\xFF\xFF\xFF\xFF'  #  broadcast MAC address
    esp.add_peer(peer)
    data=ustruct.pack('i16s3f',chan,wkey,lumi,temp,humi)
    esp.send(peer,data)
    freq(20000000)

def main():
    freq(20000000)         # setting min frequency
    print("Reading ts from internal EEPROM...")
    len,ts_rparam = read_nvs_ts(nvs_key)
    if len:
        ts_chan,ts_wkey=ustruct.unpack("i16s",ts_rparam)
        print("len:",len,"ts_chan:",ts_chan,"ts_wkey:",ts_wkey.decode())
    len,pow_rparam = read_nvs_power(nvs_key)
    if len:
        cdef,cmax,dmin,dmax,tlow,thigh=ustruct.unpack("2i4f",pow_rparam)
        print("len:",len,", cdef:",cdef,", cmax:",cmax,", dmin:",dmin,", dmax:",dmax,", tlow:",tlow,", thigh:",thigh) 

    ncycle,npos,nneg= rtc_load_param()
    ssens= rtc_load_sensor(); sdelta= rtc_load_delta()
    print("ncycle:" +str(ncycle));
    lumi, temp, humi = sensors(sda=8, scl=9)
    print("Luminosity:",lumi,"lux");print("Temperature:",temp,"C");print("Humidity:",humi,"%")
    print("current: "+str(temp)+" saved: "+str(ssens));   # sensor is temperature
    print(dmin,dmax,sdelta)

    if temp>thigh or temp<tlow :              # testing thresholds - urgent packet
        print("send urgent packet");  
        ncycle=1; npos=0; nneg=0; rtc_store_param(ncycle,npos,nneg)  # back to shoirtes cycle
        sdelta = dmin; rtc_store(sdelta)
        connect_send_espnow(ts_chan,ts_wkey,lumi,temp,humi)
    
    elif abs(ssens-temp)>sdelta or (thigh-temp)<sdelta or (temp-tlow)<sdelta: # testing delta
        print("send normal packet")
        rtc_store_sensor(temp) ; led.on()
        if npos :
            if ncycle > 2:
                ncycle= int(ncycle/2)
            else:
                if sdelta< dmax:
                    sdelta = sdelta+0.1*sdelta         # new delta
                    rtc_store_delta(sdelta)      
        npos=npos+1; nneg=0  # positive and negative counters
        rtc_store_param(ncycle,npos,nneg)
        connect_send_espnow(ts_chan,ts_wkey,lumi,temp,humi)

    else:
        print("data packet NOT sent")
        if nneg :
            if ncycle < cmax:
                ncycle = int(ncycle*2)           # maximum factor 64 (64*15sec)
            else :
                if sdelta> dmin:
                    sdelta = sdelta-0.1*sdelta
                    rtc_store_delta(sdelta)
                
        npos=0; nneg=nneg+1
        rtc_store_param(ncycle,npos,nneg)  
        
    time.sleep(0.5)
    print(ncycle*cdef);print(sdelta)
    deepsleep(ncycle*cdef*1000)
    
main()
