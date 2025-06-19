#!/usr/bin/python
import requests
from prettytable import PrettyTable

# DEFINE VARIABLES
controller_ip = '10.20.12.161' # UNCOMMENT AND EDIT THIS
target_api = 'wm/core/controller/switches/json' # UNCOMMENT AND EDIT THIS
headers = {'Content-type': 'application/json','Accept': 'application/json'}
url = f'http://{controller_ip}:8080/{target_api}'
response = requests.get(url=url, headers=headers)

if response.status_code == 200:
    # SUCCESSFUL REQUEST
    print('SUCCESSFUL REQUEST | STATUS: 200')
    data = response.json()
    table = PrettyTable(data[0].keys())
    for row in data:
        table.add_row(row.values())
    print(table)
else:
    # FAILED REQUEST
    print(f'FAILED REQUEST | STATUS: 200 {response.status_code}')

# FOR QUESTION 1h
# COMPLETE FOR PRINT ALL FLOWS PER SWITCH PID
# FIRST YOU NEED TO ASK USER INPUT A SWITCH PID
# AFTERWARD, BY USING THIS SWITCH PID, YOU SHOULD ASK THE PERTINENT API FOR GET ALL FLOWS PER SWITCH PID AND PRINT THEM (AS ABOVE CODE)
dpid = input("\nIngrese el DPID del switch para ver sus Flow Entries:\n> ").strip()
target_api = f'wm/core/switch/{dpid}/flow/json'
url = f'http://{controller_ip}:8080/{target_api}'
response = requests.get(url=url, headers=headers)

if response.status_code == 200:
    print('SUCCESSFUL REQUEST | STATUS: 200')
    data = response.json()

    flows = data.get('flows')
    if not flows:
        print("Este switch no tiene Flow Entries.")
    else:
        table = PrettyTable(['Match', 'Priority', 'Actions', 'Packet Count'])
        for flow in flows:
            # Obtener acciones desde instructions
            actions = 'N/A'
            instructions = flow.get('instructions', {})
            apply_actions = instructions.get('instruction_apply_actions', {})
            if 'actions' in apply_actions:
                actions = apply_actions['actions']

            table.add_row([
                str(flow.get('match', {})),
                flow.get('priority', 'N/A'),
                actions,
                flow.get('packetCount', 0)
            ])
        print("\nFlow Entries para el switch:")
        print(table)
else:
    print(f'FAILED REQUEST | STATUS: {response.status_code}')