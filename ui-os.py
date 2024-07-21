import sys
from tabulate import tabulate

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

# Function which implements FIFO CPU scheduling algorithm
def fifo_scheduler(processes, runTime):
    curTime = 0
    isProcessRunning = False
    originalProcesses = processes[:]
    processes.sort(key=lambda x: x.arrivalTime)
    queue = []
    output = []

    while curTime < runTime:
        for proc in processes:
            if proc.arrivalTime == curTime:
                queue.append(proc)
                output.append([curTime, proc.name, "arrived", proc.burstTime])

        if queue:
            if queue[0].remainingTime == 0:
                    output.append([curTime, queue[0].name, "finished"])
                    queue[0].completionTime = curTime
                    queue[0].turnaround = curTime - queue[0].arrivalTime
                    queue.pop(0)
                    isProcessRunning = False

        if isProcessRunning == False:
            if queue:
                queue[0].startTime = curTime
                queue[0].waitTime = curTime - queue[0].arrivalTime
                queue[0].responseTime = curTime - queue[0].arrivalTime
                output.append([curTime, queue[0].name, "selected", queue[0].burstTime])
                isProcessRunning = True

        if queue:
            queue[0].remainingTime -=  1
        if not queue:
            output.append([curTime, "", "Idle"])

        curTime += 1

    # Print the actions table
    print("Actions Table:")
    print(tabulate(output, headers=["Time", "Process", "Action", "Burst Left"], tablefmt="fancy_grid"))

    # uses the original array to metrics of each process in order
    print("\nProcess Metrics:")
    print(tabulate([(process.name, process.waitTime, process.turnaround, process.responseTime) for process in originalProcesses],
                   headers=["Process", "wait Time", "turnaround", "response"], tablefmt="fancy_grid"))

# Preemptive Shortest Job First Algorithm
def preemptive_sjf(runTime, processes):
    finishedProcesses = []
    prevProc = None
    output = []

    for curTime in range(runTime):
        validProcs = [p for p in processes if p.arrivalTime <= curTime]
        if not validProcs:
            output.append([curTime, "", "Idle"])
            continue

        for process in processes:
            if process.arrivalTime == curTime:
                output.append([curTime, process.name, "arrived", process.burstTime])

        shortestProcess = min(validProcs, key=lambda p: p.remainingTime)

        if shortestProcess.responseTime == -1:
            shortestProcess.responseTime = curTime - shortestProcess.arrivalTime

        if prevProc is None or (shortestProcess != prevProc and shortestProcess.remainingTime < prevProc.remainingTime):
            if shortestProcess.responseTime == -1:
                shortestProcess.responseTime = curTime - shortestProcess.arrivalTime
            output.append([curTime, shortestProcess.name, "selected", shortestProcess.burstTime])

        for process in processes:
            if process != shortestProcess and process.arrivalTime <= curTime:
                process.waitTime += 1

        shortestProcess.remainingTime -= 1

        if shortestProcess.remainingTime <= 0:
            finishedProcesses.append(shortestProcess)
            processes.remove(shortestProcess)
            shortestProcess.turnaround = curTime + 1 - shortestProcess.arrivalTime
            output.append([curTime + 1, shortestProcess.name, "finished"])
            shortestProcess = None

        prevProc = shortestProcess

    # Print the actions table
    print("Actions Table:")
    print(tabulate(output, headers=["Time", "Process", "Action", "Burst Left"], tablefmt="fancy_grid"))

    # Sort the finished processes by name
    finishedProcesses.sort(key=lambda x: x.name)

    # Print process metrics
    print("\nProcess Metrics:")
    print(tabulate([(process.name, process.waitTime, process.turnaround, process.responseTime) for process in finishedProcesses],
                   headers=["Process", "wait Time", "turnaround", "response"], tablefmt="fancy_grid"))

# Function which implements the round-robin CPU scheduling algorithm
def round_robin_scheduler(processes, runTime, quantum):
    queue = []
    finishedProcesses = []
    quantumRemainder = 0
    curProcesses = None
    curTime = 0
    output = []

    while runTime > curTime:
        for process in processes:
            if process.arrivalTime == curTime:
                queue.append(process)
                output.append([curTime, process.name, "arrived", process.burstTime])

        if curProcesses is not None:
            if curProcesses.remainingTime == 0:
                output.append([curTime, curProcesses.name, "finished"])
                finishedProcesses.append(curProcesses)
                curProcesses.turnaround = curTime - curProcesses.arrivalTime
                curProcesses.waitTime = curProcesses.turnaround - curProcesses.burstTime
                quantumRemainder = 0
                curProcesses = None
            elif quantumRemainder == 0:
                queue.append(curProcesses)

        if queue and quantumRemainder == 0:
            quantumRemainder = quantum
            curProcesses = queue.pop(0)
            if curProcesses.responseTime == -1:
                curProcesses.responseTime = curTime - curProcesses.arrivalTime
            output.append([curTime, curProcesses.name, "selected", curProcesses.burstTime])

        elif len(queue) == 0 and quantumRemainder == 0:
            output.append([curTime, "", "Idle"])
            curTime += 1
            continue

        curProcesses.remainingTime -= 1
        curTime += 1
        quantumRemainder -= 1

    # Print the actions table
    print("Actions Table:")
    print(tabulate(output, headers=["Time", "Process", "Action", "Burst Left"], tablefmt="fancy_grid"))

    # Sort the finished processes by name
    finishedProcesses.sort(key=lambda x: x.name)

    # Print process metrics
    print("\nProcess Metrics:")
    print(tabulate([(process.name, process.waitTime, process.turnaround, process.responseTime) for process in finishedProcesses],
                   headers=["Process", "wait Time", "turnaround", "response"], tablefmt="fancy_grid"))

def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        process_count = int(lines[0].split()[1])
        run_for = int(lines[1].split()[1])
        use_algorithm = lines[2].split()[1]

        if use_algorithm == 'rr':
            quantum = int(lines[3].split()[1])
            lines = lines[4:]
        else:
            quantum = None
            lines = lines[3:]

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

def main(input_filename):
    output_filename = input_filename.replace('.in', '.out')
    processes, algorithm, quantum, runTime = read_input_file(input_filename)

    if algorithm == 'fcfs':
        fifo_scheduler(processes, runTime)
    elif algorithm == 'sjf':
        preemptive_sjf(runTime, processes)
    elif algorithm == 'rr':
        round_robin_scheduler(processes, runTime, quantum)
    else:
        print(f"Error: Invalid algorithm - {algorithm}")
        return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scheduler-gpt.py inputfile.in")
    else:
        input_filename = sys.argv[1]
        main(input_filename)
