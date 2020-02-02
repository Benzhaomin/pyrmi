# pyrmi

Very simple tool to send commands to a Corsair RMi/HXi PSU over USB and explore its returned values, thoughts, emotions and feelings.

## Install

Quick and dirty

```
sudo pip3 install pyusb
```

or cleanly

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

See [main.py](main.py) or just try various things until you get what you're really looking for. Finding inner peace is one of the hidden features of this script.

```bash
sudo python3 main.py 03 8D
    hello RM650i
    raw bytearray(b'\xb7\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    stp bytearray(b'\xb7\xf0')
    dec 61623
    lin 45.75 <= degrees (non-freedom/Celsius ones)
    str failed 'utf-8' codec can't decode byte 0xb7 in position 0: invalid start byte
```

For more Python+Corsair PSU extravaganza look over there https://github.com/jonasmalacofilho/liquidctl/blob/master/liquidctl/driver/corsair_hid_psu.py
