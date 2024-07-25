# py-ir-console
A console to send commands and read data from a IR arm.

# Requirements

Create a fresh new virtual environment, by providing a new path for it:
```shell
python -m venv <path-to-venv-folder> 
```

Activate it:
```shell
source <path-to-venv-folder>
```

Install file `requirements.txt`:
```shell
pip install -r requirements.txt
```

# List serial ports

```shell
python -m serial.tools.list_ports
```

# Usage

```shell
python read_ir.py --help
usage: read_ir.py [-h] [-p PORT] [-b BAUD_RATE] [-t TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Serial port path (default: None)
  -b BAUD_RATE, --baud-rate BAUD_RATE
                        Serial port baud rate (default: 74880)
  -t TIMEOUT, --timeout TIMEOUT
                        Serial port read timeout in seconds (default: 5.0)
```

# Serial console

This app allows sending remote commands to a microcontroller.

In case there is no response from the microcontroller, I recommend you disconnect it from the
USB port and connect it again. Once it is disconnected, the app will try to reconnect to it again
every 2 seconds:
```shell
(cloud-detector)$ python read_ir.py -p /dev/cu.usbserial-110 -b 115200

error [Errno 16] could not open port /dev/cu.usbserial-110: [Errno 16] Resource busy: '/dev/cu.usbserial-110'
Retrying in 2 seconds...
Welcome to the serial console shell. Type help or ? to list commands.

(serial) 
```

In order to exit the console, press `Control+C` or use command `bye`.

Press `?` or send `help` command to get a list of available commands:
```shell
(serial) ?

Documented commands (type help <topic>):
========================================
bye  commands  help  ir  irx  ping  read  reset  status
```