import machine, ustruct
import esp32

# Function to write data to internal flash memory using NVS (Non-Volatile Storage)
def write_nvs_ts(key, value):
    nvs_key = esp32.NVS("thingspeak")  # Open the NVS namespace "thingspeak"
    nvs_key.set_blob(key, value)  # Store a byte array (blob) with a key
    nvs_key.commit()  # Commit the changes

# Function to read data from internal flash memory using NVS
def read_nvs_ts(key):
    nvs_key = esp32.NVS("thingspeak")  # Open the NVS namespace "thingspeak"
    try:
        buff = bytearray(32)
        value = nvs_key.get_blob(key,buff)  # Retrieve the byte array (blob) using the key
        return value,buff
    except OSError:
        print(f"Key '{key}' not found in EEPROM.")
        return None
    
# Function to write data to internal flash memory using NVS (Non-Volatile Storage)
def write_nvs_power(key, value):
    nvs_key = esp32.NVS("power")  # Open the NVS namespace "thingspeak"
    nvs_key.set_blob(key, value)  # Store a byte array (blob) with a key
    nvs_key.commit()  # Commit the changes

# Function to read data from internal flash memory using NVS
def read_nvs_power(key):
    nvs_key = esp32.NVS("power")  # Open the NVS namespace "thingspeak"
    try:
        buff = bytearray(32)
        value = nvs_key.get_blob(key,buff)  # Retrieve the byte array (blob) using the key
        return value,buff
    except OSError:
        print(f"Key '{key}' not found in EEPROM.")
        return None


# Main program to demonstrate write and read functionality
def main():
    nvs_key = "param"  # Key for the thing speak channel
    ts_wkey = "YOX31M0EDKO0JATK"  # Data to write
    ts_chan =1234
    ts_wparam = ustruct.pack("i16s",ts_chan,ts_wkey)
    print("Writing ts to internal EEPROM...")
    write_nvs_ts(nvs_key, ts_wparam)
    print("Reading ts from internal EEPROM...")
    len,ts_rparam = read_nvs_ts(nvs_key)
    if len:
        chan,wkey=ustruct.unpack("i16s",ts_rparam)
        print("len:",len,"ts_chan:",chan,"ts_wkey:",wkey.decode())
        

    c_def = 1; c_max=64        # cycle duration and max limit - cdef = 1 for test only, put 15
    d_min = 0.01; d_max=0.2     # dalta limits
    t_low = 16.0; t_high=26.0   # Data to write
    pow_wparam = ustruct.pack("2i4f",c_def,c_max,d_min,d_max,t_low,t_high)
    print("Writing pow to internal EEPROM...")
    write_nvs_power(nvs_key, pow_wparam)
    print("Reading pow from internal EEPROM...")
    len,pow_rparam = read_nvs_power(nvs_key)
    if len:
        cdef,cmax,dmin,dmax,tlow,thigh=ustruct.unpack("2i4f",pow_rparam)
        print("len:",len,", cdef:",cdef,", cmax:",cmax,", dmin:",dmin,", dmax:",dmax,", tlow:",tlow,", thigh:",thigh)

if __name__ == "__main__":
    main()
    