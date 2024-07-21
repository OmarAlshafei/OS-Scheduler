# Omar Alshafei
# Hung Tran
# Marc Palacio
# Gavin Cruz
# Natalya McKay

import sys

# this program implements three CPU scheduling algorithms (FCFS, RR, andd SJF)

# function which implements FIFO CPU scheduling algorithm
# code from chatgpt, modified to fulfill requirements
def fifo_scheduler(processes, runTime):
    # statements to add to outputfile    
    output = ""
    output += f"{len(processes)} processes\n"
    output += "Using First-Come First-Served\n"

    # declaration of variables that will be used
    curTime = 0
    isProcessRunning = False
    originalProcesses = processes[:]
    processes.sort(key=lambda x: x.arrivalTime)
    queue = []

    # modified from ChatGPT so that its iterative instead of from process list
    while curTime < runTime:
        # modified this so that it will run at a specific time instead of the beginning
        for proc in processes:
            if proc.arrivalTime == curTime:
                queue.append(proc)
                output += f"Time {curTime} : {proc.name} arrived\n"
        
        # checks if there are processes in the queue then compares their remaining time
        if queue:
            if queue[0].remainingTime == 0:
                    output += f"Time {curTime} : {queue[0].name} finished\n"
                    queue[0].completionTime = curTime
                    queue[0].turnaround = curTime - queue[0].arrivalTime
                    queue.pop(0)
                    isProcessRunning = False
        
        # this is an added function to ensure a process is selected from the queue
        if isProcessRunning == False:
            if queue:
                queue[0].startTime = curTime
                queue[0].waitTime = curTime - queue[0].arrivalTime
                queue[0].responseTime = curTime - queue[0].arrivalTime
                output += f"Time {curTime} : {queue[0].name} selected (burst   {queue[0].burstTime})\n"
                isProcessRunning = True

        # checks if a process is in the queue
        if queue:            
            queue[0].remainingTime -=  1
        # if there isn't, it will print out idle
        if not queue:
            output += f"Time {curTime} : Idle\n"
        
        # iterate the timer
        curTime += 1

    output += f"Finished at time {curTime}\n\n"

    # uses the original array to metrics of each process in order
    for process in originalProcesses:
        output += f"{process.name} wait Time\t{process.waitTime} turnaround\t{process.turnaround} response\t{process.responseTime}\n"

    return output

# Preemptive Shortest Job First Algorithm
# Remodified and editied from ChatGPT
def preemptive_sjf(runTime, processes):
    finishedProcesses = []
    prevProc = None
    output = ""

    # find all valid process that are less or equal to the arrival time
    for curTime in range(runTime):
        validProcs = [p for p in processes if p.arrivalTime <= curTime]
        if not validProcs:
            output += f"Time {curTime} : Idle\n"
            continue

        # print if a process has arrived at the current time
        for process in processes:
            if process.arrivalTime == curTime:
                output += f"Time {curTime} : {process.name} arrived\n"

        # find the shortest process in the array for all valid ready processes
        shortestProcess = min(validProcs, key=lambda p: p.remainingTime)

        # update response time for the shortest process
        if shortestProcess.responseTime == -1:
            shortestProcess.responseTime = curTime - shortestProcess.arrivalTime

        # checking tsee if a process that has arrived has a shorter process than the curre        
        if prevProc is None or (shortestProcess != prevProc and shortestProcess.remainingTime < prevProc.remainingTime):
            if shortestProcess.responseTime == -1:
                shortestProcess.responseTime = curTime - shortestProcess.arrivalTime
            output += f"Time {curTime} : {shortestProcess.name} selected (burst {shortestProcess.remainingTime})\n"

        for process in processes:
            if process != shortestProcess and process.arrivalTime <= curTime:
                process.waitTime += 1

        shortestProcess.remainingTime -= 1

        if shortestProcess.remainingTime <= 0:
            finishedProcesses.append(shortestProcess)
            processes.remove(shortestProcess)
            shortestProcess.turnaround = curTime + 1 - shortestProcess.arrivalTime
            output += f"Time {curTime + 1} : {shortestProcess.name} finished\n"
            shortestProcess = None

        prevProc = shortestProcess

    output += f"Finished at time {runTime}\n\n"

    finishedProcesses.sort(key=lambda x: x.name)
    for process in finishedProcesses:
        output += f"{process.name} wait Time\t{process.waitTime} turnaround\t{process.turnaround} response\t{process.responseTime}\n"

    return output

# function which implements the round-robin CPU scheduling algorithm
def round_robin_scheduler(processes, runTime, quantum):
    # initialize an empty queue and list to hold finished processes
    queue = []
    finishedProcesses = []
    # initialize quantum remainder, current processes, and current time    
    quantumRemainder = 0
    curProcesses = None
    curTime = 0
    output = ""
    
    # loop until the total runtime is reached
    while runTime > curTime:
            
        # check for processes arriving at current time and add them to the queue
        for process in processes:
            if process.arrivalTime == curTime:
                queue.append(process)
                output += f"Time {curTime} : {process.name} arrived\n"
                
        # given from chatgpt and refactored and edited
        if curProcesses is not None:
            if curProcesses.remainingTime == 0:
                output += f"Time {curTime} : {curProcesses.name} finished\n"
                finishedProcesses.append(curProcesses)
                curProcesses.turnaround = curTime - curProcesses.arrivalTime
                curProcesses.waitTime = curProcesses.turnaround - curProcesses.burstTime
                quantumRemainder = 0
                curProcesses = None
            elif quantumRemainder == 0:
                queue.append(curProcesses)
                
        # given from chatgpt and refactored and edited
        if queue and quantumRemainder == 0:
            quantumRemainder = quantum
            curProcesses = queue.pop(0)
            if curProcesses.responseTime == -1:
                curProcesses.responseTime = curTime - curProcesses.arrivalTime
            output += f"Time {curTime} : {curProcesses.name} selected (burst {curProcesses.remainingTime})\n"
        
        # handle idle time if no processes in queue
        elif len(queue) == 0 and quantumRemainder == 0:
            output += f"Time {curTime} : Idle\n"
            curTime += 1
            continue
        
        # given from chatgpt
        curProcesses.remainingTime -= 1
        curTime += 1
        quantumRemainder -= 1

    output += f"Finished at time {curTime}\n\n"

    finishedProcesses.sort(key=lambda x: x.name)
    for process in finishedProcesses:
        output += f"{process.name} wait\t{process.waitTime} turnaround\t{process.turnaround} response\t{process.responseTime}\n"

    return output

class Process:
    def __init__(self, name, arrivalTime, burstTime):
        self.name = name
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.remainingTime = burstTime
        self.completionTime = 0
        self.startTime = -1
        self.waitTime = 0
        self.responseTime = -1
        self.turnaround = 0

# read the input from file and format tthe processes info
def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Parse directives
        process_count = int(lines[0].split()[1])
        run_for = int(lines[1].split()[1])
        use_algorithm = lines[2].split()[1]

        if use_algorithm == 'rr':
            quantum = int(lines[3].split()[1])
            lines = lines[4:]
        else:
            quantum = None
            lines = lines[3:]

        # Parse processes
        processes = []
        for line in lines:
            if line.strip() == 'end':
                break

            parts = line.split()
            if parts[0] == 'process':
                name = parts[2]
                arrival = int(parts[4])
                burst = int(parts[6])
                processes.append(Process(name, arrival, burst))

        ## human added
        if not process_count: 
            print("Error: Missing parameter processcount")
            exit(1)
        if not run_for:
            print("Error: Missing parameter runfor")
            exit(1)
        if not use_algorithm:
            print("Error: Missing parameter use")
            exit(1)
        if use_algorithm == 'rr' and not quantum:
            print("Error: Missing quantum parameter when use is 'rr'")
            exit(1)

        return processes, use_algorithm, quantum, run_for

    except (IOError, ValueError, IndexError) as e:
        print(f"Usage: scheduler-get.py <input file>")
        sys.exit(1)

def write_output(filename, output):
    with open(filename, 'w') as file:
        file.write(output)

def main(input_filename):
    output_filename = input_filename.replace('.in', '.out')
    processes, algorithm, quantum, runTime = read_input_file(input_filename)
    output = ""

    if algorithm == 'fcfs':
        output = fifo_scheduler(processes, runTime)
    elif algorithm == 'sjf':
        output = preemptive_sjf(runTime, processes)
    elif algorithm == 'rr':
        output = round_robin_scheduler(processes, runTime, quantum)
    else:
        print(f"Error: Invalid algorithm - {algorithm}")
        return

    write_output(output_filename, output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scheduler-gpt.py inputfile.in")
    else:
        input_filename = sys.argv[1]
        main(input_filename)
