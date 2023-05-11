import PySimpleGUI as sg
def is_safe(processes, available, max_resources, allocation_matrix):
    work = available.copy()
    finish = [False] * len(processes)
    safe_sequence = []

    while True:
        for i, process in enumerate(processes):
            if not finish[i] and all(allocation_matrix[i][j] + work[j] >= max_resources[i][j] for j in range(len(work))):
                work = [work[j] + allocation_matrix[i][j] for j in range(len(work))]
                finish[i] = True
                safe_sequence.append(i)
                break
        else:
            break   

    return all(finish), safe_sequence, work

def resource_page():
    layout = [[sg.Text('Enter the process that requests the resource:'), sg.InputText()],[sg.Text('Enter the resource type:'), sg.InputText()],[sg.Text('Enter the number of that resource needed:'), sg.InputText()],[sg.Button('Ok'), sg.Button('Cancel')]]
    window=sg.Window("Calculating if safe or not...",layout)
    while True:             
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Ok':
            process_num = int(values[0])
            resource_num = int(values[1])
            amount= int(values[2])
            window.close()
            break
    return process_num, resource_num, amount

sg.theme('DarkAmber')
layout = [[sg.Text('Enter the number of resources'), sg.InputText()],[sg.Text('Enter the number of processes'), sg.InputText()],[sg.Button('Ok'), sg.Button('Cancel')]]
window=sg.Window("Welcome User!",layout)
while True:             
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'Ok':
        num_processes = int(values[1])
        num_resources = int(values[0])
        window.close()
        break
sg.set_options(font=('Courier New', 12))
layout = [[sg.Text('Enter the available resources:')]]
for i in range(num_resources):
    layout.append([sg.Text('R'+str(i)+':'),sg.InputText()])
layout.append([sg.Button('Ok'), sg.Button('Cancel')])
window=sg.Window("Please enter the information below",layout)
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'Ok':
        available = [int(values[i]) for i in range(num_resources)]
        window.close()
        break

sg.set_options(font=('Courier New', 12))
layout=[[sg.Text('Enter the allocated matrix:')]]
for i in range(num_processes):
    layout.append([sg.Text('Enter the allocated for p'+str(i)+':')])
    for j in range(num_resources):
        layout.append([sg.Text('R'+str(j)+':'),sg.InputText()])
        
layout.append([sg.Button('Ok'), sg.Button('Cancel')])
window=sg.Window("Please enter the information below",layout)
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'Ok':
        allocation_matrix = []
        for i in range(num_processes):
            row = []
            for j in range(num_resources):
                row.append(int(values[i*num_resources+j]))
            allocation_matrix.append(row)
        window.close()
        break

sg.set_options(font=('Courier New', 12))
layout=[[sg.Text('Enter the maximum matrix:')]]
for i in range(num_processes):
    layout.append([sg.Text('Enter the maximum for p'+str(i)+':')])
    for j in range(num_resources):
        layout.append([sg.Text('R'+str(j)+':'),sg.InputText()])
        
layout.append([sg.Button('Ok'), sg.Button('Cancel')])
window=sg.Window("Please enter the information below",layout)
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'Ok':
        max_matrix = []
        for i in range(num_processes):
            row = []
            for j in range(num_resources):
                row.append(int(values[i*num_resources+j]))
            max_matrix.append(row)
        window.close()
        break


process_num, resource_num, amount = resource_page()  
if amount <= available[resource_num]:
    available[resource_num] -= amount
    allocation_matrix[process_num][resource_num] += amount
else:
    while amount > available[resource_num]:
        window=sg.popup_ok_cancel("Not enough resources available. Process p"+str(process_num)+" must wait.")
        process_num, resource_num, amount = resource_page()

safe, safe_sequence, work = is_safe(range(num_processes), available, max_matrix, allocation_matrix)
if safe:
        layout = [[sg.Text('The system is in a safe state!')]]
        layout.append([sg.Text("Safe sequence:")])
        layout.append([sg.Text(" -> ".join(map(str, safe_sequence)))])
        layout.append([sg.Text("Available resources in each iteration:")])
        for i, process in enumerate(safe_sequence):
            for j in range(len(work)):
                available[j]= available[j] + allocation_matrix[process][j] 
            layout.append([sg.Text("After P" + str(process) + ":"+ str(work if i == len(safe_sequence) - 1 else available))])
        layout.append([sg.Button('Ok')])
        window=sg.Window("DONE!",layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Ok'):
                window.close()
                break
else:
    layout=([sg.Text("The system is not in a safe state!")])
    layout.append([sg.Button('Ok')])
    window=sg.Window("DONE!",layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Ok'):
            window.close()
            break