import subprocess, argparse, serial, re, os
from datetime import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Pump guard")
    parser.add_argument('-p', '--port', type=int, dest='port', help="serial port to the sensor")
    args = parser.parse_args()
    print("listening on port ", args.port)

    serial0= serial.Serial('/dev/ttyUSB0', args.port)
    log_file=os.path.join(os.path.expanduser('~'), '.local/share/qtile/pump_guard.log')
    while True:
        serial_output = serial0.readline().decode("utf-8")
        serial_output = re.match('[^\r]*',serial_output).group()
        time_now=datetime.now()
        dt_string = time_now.strftime("[%Y/%m/%d %H:%M] ")
        with open(log_file, 'a') as f:
            f.write(dt_string+serial_output+'\n')
        if serial_output == 'Critical!':
            subprocess.Popen("sudo poweroff".split())
