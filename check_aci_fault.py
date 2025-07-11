#!/usr/bin/python3

import sys
import getopt
from ACI import ACI


def main(argv):
    try:
        if len(argv) == 0:
            raise ValueError
        opts, args = getopt.getopt(argv, 'H:u:p:f:', ['hostname', 'username', 'password', 'fault'])
    except (getopt.GetoptError, ValueError):
        print('check_aci_fault.py -H hostname -u username -p password -f fault')
        sys.exit(3)
    fault = None
    for opt, arg in opts:
        if opt == '-H':
            hostname = arg
        elif opt == '-u':
            username = arg
        elif opt == '-p':
            password = arg
        elif opt == '-f':
            fault = arg

    aci = ACI()
    result = aci.connect(hostname=hostname, username=username, password=password)
    if not result:
        aci.disconnect()
        sys.exit(3)
    if fault:
        url = '/api/node/class/faultInst.json?query-target-filter=and(eq(faultInfo.code,"{}"),ne(faultInfo.severity,"cleared"))'
        url = url.format(fault)
    else:
        url = '/api/node/class/faultInst.json?query-target-filter=and(ne(faultInfo.severity,"cleared"))'
    faults = aci.method_get(url=url)
    aci.disconnect()
    print('Faults count: ' + faults['totalCount'])
    if int(faults['totalCount']) == 0:
        sys.exit(0)
    faults = faults['imdata']
    for fault in faults:
        print()
        fault = fault['faultInst']['attributes']
        print('Type: ' + fault['type'])
        print('Severity: ' + fault['severity'])
        print('Cause: ' + fault['cause'])
        print('Created: ' + fault['created'])
        print('Last Transition: ' + fault['lastTransition'])
        print('Description: ' + fault['descr'])
        print('DN: ' + fault['dn'])
    sys.exit(2)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        exit()


