from machine import Pin, I2C
import time

# Initialize I2C (GPIO21 = SDA, GPIO22 = SCL)
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)

# Common I2C address range for AT24CXX EEPROMs
EEPROM_ADDRESSES = [0x50 + i for i in range(8)]  # 0x50 - 0x57

def check_eeprom():
    print("Scanning I2C bus for AT24CXX EEPROM...")
    devices = i2c.scan()
    if not devices:
        print("No I2C devices found.")
        return False

    found = False
    for addr in EEPROM_ADDRESSES:
        if addr in devices:
            try:
                # Try reading 1 byte from address 0x00
                i2c.writeto(addr, b'\x00')         # Set memory pointer to 0x00
                data = i2c.readfrom(addr, 1)        # Read 1 byte
                print(f"EEPROM found at address 0x{addr:02X}. Data at 0x00: {data[0]:02X}")
                found = True
            except Exception as e:
                print(f"Device at 0x{addr:02X} responded but did not behave like EEPROM. Error: {e}")

    if not found:
        print("No AT24CXX EEPROM found on the I2C bus.")
    return found
