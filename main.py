#!/usr/bin/env python3

"""
Usage: python3 main.py length opcode (in hexa)

Examples:

    # vendor name
    $ sudo python3 main.py 03 99
    hello RM650i
    raw bytearray(b'CORSAIR\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    stp bytearray(b'CORSAIR')
    dec 23161493009878851
    lin failed big number
    str CORSAIR <= string

    # temp1
    $ sudo python3 main.py 03 8D
    hello RM650i
    raw bytearray(b'\xb7\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    stp bytearray(b'\xb7\xf0')
    dec 61623
    lin 45.75 <= degrees (non-freedom/Celsius ones)
    str failed 'utf-8' codec can't decode byte 0xb7 in position 0: invalid start byte

    # total uptime
    $ sudo python3 main.py 03 D1
    hello RM650i
    raw bytearray(b'\xa1:b\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    stp bytearray(b'\xa1:b\x01')
    dec 23214753 <= seconds
    lin failed big number
    str failed 'utf-8' codec can't decode byte 0xa1 in position 0: invalid start byte
"""

import usb
import logging
import sys

def is_corsair_rmi_hxi_psu(device):
    return device.idVendor == 0x1b1c and device.idProduct in [
        0x1c0a,  # RM650i
        0x1c0b,  # RM750i
        0x1c0c,  # RM850i
        0x1c0d,  # RM1000i
        0x1c04,  # HX650i
        0x1c05,  # HX750i
        0x1c06,  # HX850i
        0x1c07,  # HX1000i
        0x1c08,  # HX1200i
    ]

dev = usb.core.find(custom_match=is_corsair_rmi_hxi_psu)
if dev is None:
    raise ValueError('No Corsair RMi/HXi Series PSU found')

# grab the device from the kernel's claws
ifaceid = 0
if dev.is_kernel_driver_active(ifaceid):
    dev.detach_kernel_driver(ifaceid)
    usb.util.claim_interface(dev, ifaceid)

try:
    cfg = dev.get_active_configuration()
    (reader, writer) = cfg[(0,0)].endpoints()

    # data is an array of ints
    def write(data):
        padding = [0x0]*(64 - len(data))
        writer.write(data + padding, timeout=100)

    def read():
        data = reader.read(64, timeout=100)
        return bytearray(data)[2:]

    # saying hello is required, just do it
    write([0xfe, 0x03])
    name = read().decode()
    print('hello', name)

    # send user-provided length+opcode
    write([int(b, 16) for b in sys.argv[1:3]])

    # get data back and print in it various encoding
    data = read()
    print('raw', data)

    try:
        print('stp', data.strip(b'\x00'))
    except Exception as e:
        print('stp failed', e )

    try:
        print('dec', int.from_bytes(data, byteorder='little'))
    except Exception as e:
        print('dec failed', e)

    try:
        tmp = int.from_bytes(data, byteorder='little')
        exp = tmp >> 11
        fra = tmp & 0x7ff
        if fra > 1023:
            fra = fra - 2048
        if exp > 15:
            exp = exp - 32
        if exp > 15:
            raise ValueError('big number')
        print('lin', fra * 2**exp)
    except Exception as e:
        print('lin failed', e)

    try:
        print('str', data.decode())
    except Exception as e:
        print('str failed', e)
finally:
    # always say goodbye
    usb.util.release_interface(dev, ifaceid)
    dev.attach_kernel_driver(ifaceid)