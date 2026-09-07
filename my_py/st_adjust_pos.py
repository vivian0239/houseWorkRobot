#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available ST Servo model on this example : All models using Protocol ST
# This example is tested with a ST Servo(ST3215/ST3020/ST3025), and an URT
#

import sys
import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
        
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

sys.path.append("..")
from scservo_sdk import *                 # Uses SC Servo SDK library

# Default setting
SCS_ID                      = 6                 # SC Servo ID : 1
BAUDRATE                    = 1000000           # SC Servo default baudrate : 1000000
DEVICENAME                  = 'COM3'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
SCS_MINIMUM_POSITION_VALUE  = 446           # SC Servo will rotate between this value
SCS_MAXIMUM_POSITION_VALUE  = -100
SCS_MOVING_SPEED            = 50        # SC Servo moving speed
SCS_MOVING_ACC              = 50          # SC Servo moving acc

EPROM_MAX_TEMPERATURE       = 0x0D
EPROM_MAX_VOLTAGE           = 0x0E
EPROM_MAX_CURRENT           = 0x1C

index = 0
scs_goal_position = [SCS_MINIMUM_POSITION_VALUE, SCS_MAXIMUM_POSITION_VALUE]         # Goal position

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sms_sts(portHandler)
    
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

def ReadOFSValue(scs_id):
    """Read position offset value (0x1F) from EPROM"""
    ofs_value, scs_comm_result, scs_error = packetHandler.read2ByteTxRx(scs_id, SMS_STS_OFS_L)
    if scs_comm_result != COMM_SUCCESS:
        print("Read OFS failed: %s" % packetHandler.getTxRxResult(scs_comm_result))
        return None
    if scs_error != 0:
        print("Read OFS error: %s" % packetHandler.getRxPacketError(scs_error))
        return None
    return ofs_value

def WriteOFSValue(scs_id, ofs_value):
    """Write position offset value (0x1F) to EPROM"""
    scs_comm_result, scs_error = packetHandler.write2ByteTxRx(scs_id, SMS_STS_OFS_L, ofs_value)
    if scs_comm_result != COMM_SUCCESS:
        print("Write OFS failed: %s" % packetHandler.getTxRxResult(scs_comm_result))
        return False
    if scs_error != 0:
        print("Write OFS error: %s" % packetHandler.getRxPacketError(scs_error))
        return False
    return True

def ReadEPROMByte(scs_id, address, name):
    value, scs_comm_result, scs_error = packetHandler.read1ByteTxRx(scs_id, address)
    if scs_comm_result != COMM_SUCCESS:
        print("Read %s failed: %s" % (name, packetHandler.getTxRxResult(scs_comm_result)))
        return None
    if scs_error != 0:
        print("Read %s error: %s" % (name, packetHandler.getRxPacketError(scs_error)))
        return None
    return value

def ReadEPROMWord(scs_id, address, name):
    value, scs_comm_result, scs_error = packetHandler.read2ByteTxRx(scs_id, address)
    if scs_comm_result != COMM_SUCCESS:
        print("Read %s failed: %s" % (name, packetHandler.getTxRxResult(scs_comm_result)))
        return None
    if scs_error != 0:
        print("Read %s error: %s" % (name, packetHandler.getRxPacketError(scs_error)))
        return None
    return value

def WriteMaxCurrent(scs_id, current):
    scs_comm_result, scs_error = packetHandler.write2ByteTxRx(scs_id, EPROM_MAX_CURRENT, current)
    if scs_comm_result != COMM_SUCCESS:
        print("Write maximum current failed: %s" % packetHandler.getTxRxResult(scs_comm_result))
        return False
    if scs_error != 0:
        print("Write maximum current error: %s" % packetHandler.getRxPacketError(scs_error))
        return False
    return True

print("\n=== ST Servo EPROM Adjust ===")
while 1:
    print("\n--- Menu ---")
    print("1. Read OFS value from EPROM (0x1F)")
    print("2. Write OFS value to EPROM (0x1F)")
    print("3. Read maximum voltage from EPROM (0x0E)")
    print("4. Read maximum temperature from EPROM (0x0D)")
    print("5. Read maximum current from EPROM (0x1C)")
    print("6. Write maximum current to EPROM (0x1C)")
    print("7. Move servo (original function)")
    print("0. Exit")
    
    menu_choice = input("Select option (0-7): ").strip()
    
    if menu_choice == '0':
        break
    elif menu_choice == '1':
        # Read OFS value
        ofs_val = ReadOFSValue(SCS_ID)
        if ofs_val is not None:
            print("Successfully read OFS value: %d (0x%04X)" % (ofs_val, ofs_val))
    elif menu_choice == '2':
        # Write OFS value
        try:
            ofs_input = input("Enter OFS value to write (0-65535): ").strip()
            ofs_val = int(ofs_input)
            if 0 <= ofs_val <= 65535:
                if WriteOFSValue(SCS_ID, ofs_val):
                    print("Successfully wrote OFS value: %d (0x%04X)" % (ofs_val, ofs_val))
                    # Read back to verify
                    verify_val = ReadOFSValue(SCS_ID)
                    if verify_val is not None:
                        print("Verification read: %d (0x%04X)" % (verify_val, verify_val))
            else:
                print("Invalid value. Please enter a value between 0 and 65535")
        except ValueError:
            print("Invalid input. Please enter a valid number")
    elif menu_choice == '3':
        max_voltage = ReadEPROMByte(SCS_ID, EPROM_MAX_VOLTAGE, "maximum voltage")
        if max_voltage is not None:
            print("Successfully read maximum voltage: %d (0x%02X)" % (max_voltage, max_voltage))
    elif menu_choice == '4':
        max_temperature = ReadEPROMByte(SCS_ID, EPROM_MAX_TEMPERATURE, "maximum temperature")
        if max_temperature is not None:
            print("Successfully read maximum temperature: %d (0x%02X)" % (max_temperature, max_temperature))
    elif menu_choice == '5':
        max_current = ReadEPROMWord(SCS_ID, EPROM_MAX_CURRENT, "maximum current")
        if max_current is not None:
            print("Successfully read maximum current: %d (0x%04X)" % (max_current, max_current))
    elif menu_choice == '6':
        try:
            current_input = input("Enter maximum current value to write (0-65535): ").strip()
            max_current = int(current_input)
            if 0 <= max_current <= 65535:
                if WriteMaxCurrent(SCS_ID, max_current):
                    print("Successfully wrote maximum current: %d (0x%04X)" % (max_current, max_current))
                    verify_current = ReadEPROMWord(SCS_ID, EPROM_MAX_CURRENT, "maximum current")
                    if verify_current is not None:
                        print("Verification read: %d (0x%04X)" % (verify_current, verify_current))
            else:
                print("Invalid value. Please enter a value between 0 and 65535")
        except ValueError:
            print("Invalid input. Please enter a valid number")
    elif menu_choice == '7':
        # Original move servo function
        print("Press any key to continue! (or press ESC to quit!)")
        if getch() == chr(0x1b):
            continue

        # Write SC Servo goal position/moving speed/moving acc
        scs_comm_result, scs_error = packetHandler.WritePosEx(SCS_ID, scs_goal_position[index], SCS_MOVING_SPEED, SCS_MOVING_ACC)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        if scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

        # Change goal position
        if index == 0:
            index = 1
        else:
            index = 0
    else:
        print("Invalid option. Please try again")

# Close port
portHandler.closePort()
