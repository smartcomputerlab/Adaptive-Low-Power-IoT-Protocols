# lora.receive_aes.py
from machine import Pin, I2C, SPI
import ustruct
from lora_init import *
from display_sensors import *
from aes_tools import *
import time

AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
# Initialize LoRa modem
lora_modem = lora_init()

# --- Receive LoRa Packet ---
def onReceive(lora_modem,payload):
    rssi = lora_modem.packetRssi()
    if len(payload)==32:
        rssi = lora_modem.packetRssi()
        data=aes_decrypt(payload,AES_KEY)
        chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', data)
        print("Received encrypted LoRa packet with RSSI: "+str(rssi))   #, payload.decode())
        print(chan,wkey,lumi,temp,humi)
        display_sensors(8,9,lumi,temp,humi,0)
        ack=ustruct.pack('2i2f',chan,10,0.01,25.1)  # chan, cycle, delta, thold
        enc_ack=aes_encrypt(ack,AES_KEY)
        lora_modem.println(enc_ack)  # sending ACK packet
        print("send encrypted ack AES packet")
        lora_modem.receive()

def main():
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(2)
        print("in the loop")
        
main()