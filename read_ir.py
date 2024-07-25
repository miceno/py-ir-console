import argparse
import cmd
from time import sleep

from serial import Serial
from serial.serialutil import SerialException

retry_timeout = 2


class SerialConsole(cmd.Cmd):
    intro = 'Welcome to the serial console shell. Type help or ? to list commands.\n'
    prompt = '(serial) '

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

    # ----- basic turtle commands -----
    def do_read(self, arg):
        'Read data from the serial: READ'
        serial.write("READ\n".encode('ascii'))
        serial.flush()
        result = serial.readline()
        print(result)

    def do_ir(self, arg):
        'Get IR data in ascii format: IR'
        serial.write("IR\n".encode('ascii'))
        serial.flush()
        result = serial.readline()
        while serial.in_waiting > 0:
            print(result)
            result = serial.readline()

    def do_irx(self, arg):
        'Get IRX data in base64 format: IRX'
        serial.write("IRX\n".encode('ascii'))
        serial.flush()
        result = serial.readline()
        print(result)

    def do_ping(self, arg):
        'Ping the serial port: PING'
        serial.write("PING\n".encode('ascii'))
        serial.flush()
        result = serial.readline()
        print(result)

    def do_commands(self, arg):
        'Get list of available commands: HELP'
        serial.write("HELP\n".encode('ascii'))
        serial.flush()
        result = serial.readline()
        while serial.in_waiting > 0:
            print(result)
            result = serial.readline()

    def do_reset(self, arg):
        'Reset input line'
        print('Reset input line')
        serial.reset_input_buffer()

    def do_status(self, arg):
        'Show serial port status'
        print('Serial port status:', end='')
        print(serial.get_settings())

    def do_bye(self, arg):
        'Stop, close the serial window, and exit:  BYE'
        print('Thank you for using Serial')
        return True

    def precmd(self, line):
        line = line.lower()
        return line

    def close(self):
        pass


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
