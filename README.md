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