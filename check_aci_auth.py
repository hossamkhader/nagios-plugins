#!/usr/bin/python3

import sys
import getopt
from ACI import ACI

NAGIOS_EXIT_CODE = {'OK': 0, 'WARNING': 1, 'CRITICAL': 2, 'UNKNOWN': 3}
NAGIOS_OUTPUT = {'EXIT_CODE': NAGIOS_EXIT_CODE['UNKNOWN'], 'OUTPUT': '', 'PERFDATA': [], 'LONGOUTPUT': []}


def print_output():
    print(NAGIOS_OUTPUT['OUTPUT'])
    if NAGIOS_OUTPUT['LONGOUTPUT']:
        print()
    for line in NAGIOS_OUTPUT['LONGOUTPUT']:
        print(line)

    if NAGIOS_OUTPUT['PERFDATA']:
        print('|')
    for line in NAGIOS_OUTPUT['PERFDATA']:
        print(line.replace(' ', ''))
    sys.exit(NAGIOS_OUTPUT['EXIT_CODE'])


def main(argv):
    try:
        if len(argv) == 0:
            raise ValueError
        opts, args = getopt.getopt(argv, 'H:u:p:', ['hostname', 'username', 'password'])
    except (getopt.GetoptError, ValueError):
        print('check_aci_switch_login.py -H hostname -u username -p password')
        sys.exit(3)
    for opt, arg in opts:
        if opt == '-H':
            hostname = arg
        elif opt == '-u':
            username = arg
        elif opt == '-p':
            password = arg

    aci = ACI()
    result = aci.connect(hostname=hostname, username=username, password=password)
    aci.disconnect()
    if result:
        NAGIOS_OUTPUT['OUTPUT'] = 'TRUE'
        NAGIOS_OUTPUT['EXIT_CODE'] = NAGIOS_EXIT_CODE['OK']
    else:
        NAGIOS_OUTPUT['OUTPUT'] = 'FALSE'
        NAGIOS_OUTPUT['EXIT_CODE'] = NAGIOS_EXIT_CODE['CRITICAL']


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
        print_output()
    except KeyboardInterrupt:
        exit()


