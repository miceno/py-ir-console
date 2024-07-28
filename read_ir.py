import argparse
import ast
import cmd
from time import sleep
import datetime

from serial import Serial
from serial.serialutil import SerialException

retry_timeout = 2


class SerialConsole(cmd.Cmd):
    intro = 'Welcome to the serial console shell. Type help or ? to list commands.\n'
    prompt = '(serial) '
    params = dict(show_timestamp=True, delimiter=":")

    def _print(self, msg):
        if self.params['show_timestamp']:
            print(datetime.datetime.now(), self.params['delimiter'], end='', sep='')
        print(msg)

    # READ: Read summarized sensor data
    # IR: Return IR data as a stream of float values
    # IRX: Return IR data as a base64 stream
    # IRB: Return IR data as a base64 lzw-compressed stream
    # IRBT: Test IR data as a base64 lzw-compressed stream
    # IRT: Test IR binary encoding and decoding
    # PING: Echo current version
    # START: Start data collection
    # STOP: Stop data collection
    # HELP: Show available commands
    # IRCAL: Set calibration values as floats.

    # ----- basic turtle commands -----
    def do_read(self, arg):
        'Read data from the serial: READ'
        self._print("READ")
        serial.write("READ\n".encode('ascii'))
        serial.flush()
        result = serial.readline()
        self._print(result)

    def do_ir(self, arg):
        'Get IR data in ascii format: IR'
        self._print("IR")
        self.send_command("IR")
        self.print_while_not_empty_line()

    def send_command(self, command):
        serial.write(f"{command}\n".encode('ascii'))
        serial.flush()

    def do_irx(self, arg):
        'Get IRX data in base64 format: IRX'
        self._print("IRX")
        self.send_command("IRX")
        result = serial.readline()
        self._print(result)

    def do_ping(self, arg):
        'Ping the serial port: PING'
        self.send_command("PING")
        result = serial.readline()
        self._print(result)

    def do_commands(self, arg):
        'Get list of available commands: HELP'
        self.send_command("HELP")
        self.print_while_not_empty_line()

    def do_reset(self, arg):
        'Reset input line'
        self._print('Reset input line')
        serial.reset_input_buffer()

    def do_status(self, arg):
        'Show serial port status'
        self._print('Serial port status:', end='')
        self._print(serial.get_settings())

    def do_bye(self, arg):
        'Stop, close the serial window, and exit:  BYE'
        self._print('Thank you for using Serial')
        return True

    def do_set(self, arg):
        'Set param to a value'
        (param, value) = arg.split(" ")
        self.params[param] = ast.literal_eval(value)
        self._print(self.params)

    def print_while_not_empty_line(self):
        result = ""
        while result != b"\r\n":
            result = serial.readline()
            self._print(result)


if __name__ == '__main__':
    # Initialize parser
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Adding optional argument
    parser.add_argument("-p", "--port", help="Serial port path")
    parser.add_argument("-b", "--baud-rate", default=74880, help="Serial port baud rate")
    parser.add_argument("-t", "--timeout", type=float, default=5.0,
                        help="Serial port read timeout in seconds")

    # Read arguments from command line
    args = parser.parse_args()

    while True:
        try:
            with Serial(args.port, args.baud_rate, timeout=args.timeout) as serial:
                SerialConsole().cmdloop()
                exit()
        except SerialException as e:
            print(f"error {e}")
            print(f"Retrying in {retry_timeout} seconds...")
            sleep(retry_timeout)
            pass
