import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
InputPins = 0
OutputPins = 0
#The array with the inputs. From 0 to nInputs-1
inputs = []
#Auxiliary array with the previous scan inputs
inputsPrev = []
#The array with the outputs
outputs = []
outputsPrev = []
#The array with the marks values
marks = []
#Aux array that contain the last mark values
marksPrev = []
#Array with the timers values
timers = []
#Array with the target time of the timer
timerAux = []
#Aux array that contain the last timers values
timersPrev = []
#Array with the counters values
counts = []
#Aux arrays for the counters
countAux = []
countPrevCU = []
countPrevCD = []
countPrevR = []
countsPrev = []
# Aux var to read and write
s = ""

############################# SET FUNCTIONS ###################################
# Set the number of inputs, outputs, marks, timers and counters
# INPUTS AND OUTPUTS MUST BE SET IN .INO FILE WITH THE SAME VALUES
def setPLC (nInputs,nOutputs,nMarks,nTimers,nCounts):

    global InputPins
    InputPins = nInputs
    global OutputPins
    OutputPins = nOutputs

    for i in range(0,nInputs):
        inputs.append(0)
        inputsPrev.append(0)

    for i in range(0,nOutputs):
        outputs.append(0)

    for i in range(0,nMarks):
        marks.append(0)
        marksPrev.append(0)

    for i in range(0,nTimers):
        timers.append(0)
        timerAux.append(0)
        timersPrev.append(0)

    for i in range(0,nCounts):
        counts.append(0)
        countAux.append(0)
        countPrevCU.append(0)
        countPrevCD.append(0)
        countPrevR.append(0)
        countsPrev.append(0)

# Add a new mark and return the position in the array of marks
def addMark ():
    marks.append(0)
    marksPrev.append(0)
    return marks.__len__()-1

# Add a new timer and return the position in the array of timers
def addTimer():
    timers.append(0)
    timerAux.append(0)
    return timers.__len__()-1

# Add a new counter and return the position in the array of counters
def addCount():
    counts.append(0)
    countAux.append(0)
    countPrevCU.append(0)
    countPrevCD.append(0)
    countPrevR.append(0)
    return counts.__len__()-1

def getPLC():
    return OutputPins,InputPins

############################# CONTACTS ###################################

def contact(input, var, imtcq):
    if (imtcq == "i")|(imtcq == "I"):
        if (inputs[var] == 1):
            return inputs[var]
        else:
            return 0

    if (imtcq == "m")|(imtcq == "M"):
        if (marks[var] == 1):
            return marks[var]
        else:
            return 0

    if (imtcq == "t")|(imtcq == "T"):
        if (timers[var] == 1):
            return timers[var]
        else:
            return 0

    if (imtcq == "c")|(imtcq == "C"):
        if counts[var] == 1:
            return counts[var]
        else:
            return 0

    if (imtcq == "q")|(imtcq == "Q"):
        if counts[var] == 1:
            return outputs[var]
        else:
            return 0

def contactNot(input, var, imtcq):
    if (imtcq == "i")|(imtcq == "I"):
        if (inputs[var] == 0):
            return inputs[var]
        else:
            return 0

    if (imtcq == "m")|(imtcq == "M"):
        if (marks[var] == 0):
            return marks[var]
        else:
            return 0

    if (imtcq == "t")|(imtcq == "T"):
        if (timers[var] == 0):
            return timers[var]
        else:
            return 0

    if (imtcq == "c")|(imtcq == "C"):
        if (counts[var] == 0):
            return counts[var]
        else:
            return 0

    if (imtcq == "q")|(imtcq == "Q"):
        if counts[var] == 0:
            return outputs[var]
        else:
            return 0

#Return 1 with a positive flank, 0 in other case. imtc sets the tipe of var value: i(input), m(mark), t(timer), c(counter)
def contactPos(input, var, imtcq):
    if (imtcq == "i")|(imtcq == "I"):
        if (inputs[var] == 1)&(inputsPrev[var] == 0):
            inputsPrev[var] = inputs[var]
            return input
        else:
            inputsPrev[var] = inputs[var]
            return 0

    if (imtcq == "m")|(imtcq == "M"):
        if (marks[var] == 1)&(marksPrev[var] == 0):
            marksPrev[var] = marks[var]
            return input
        else:
            marksPrev[var] = marks[var]
            return 0

    if (imtcq == "t")|(imtcq == "T"):
        if (timers[var] == 1)&(timersPrev[var] == 0):
            timersPrev[var] = timers[var]
            return input
        else:
            timersPrev[var] = timers[var]
            return 0

    if (imtcq == "c")|(imtcq == "C"):
        if (counts[var] == 1)&(countsPrev[var] == 0):
            countsPrev[var] = counts[var]
            return input
        else:
            countsPrev[var] = counts[var]
            return 0

    if (imtcq == "q")|(imtcq == "Q"):
        if (inputs[var] == 1)&(inputsPrev[var] == 0):
            inputsPrev[var] = inputs[var]
            return input
        else:
            inputsPrev[var] = inputs[var]
            return 0

#Return 1 with a negative flank, 0 in other case
def contactNeg(input, var, imtcq):
    if (imtcq == "i")|(imtcq == "I"):
        if (inputs[var] == 0)&(inputsPrev[var] == 1):
            inputsPrev[var] = inputs[var]
            return input
        else:
            inputsPrev[var] = inputs[var]
            return 0

    if (imtcq == "m")|(imtcq == "M"):
        if (marks[var] == 0)&(marksPrev[var] == 1):
            marksPrev[var] = marks[var]
            return input
        else:
            marksPrev[var] = marks[var]
            return 0

    if (imtcq == "t")|(imtcq == "T"):
        if (timers[var] == 0)&(timersPrev[var] == 1):
            timersPrev[var] = timers[var]
            return input
        else:
            timersPrev[var] = timers[var]
            return 0

    if (imtcq == "c")|(imtcq == "C"):
        if (counts[var] == 0)&(countsPrev[var] == 1):
            countsPrev[var] = counts[var]
            return input
        else:
            countsPrev[var] = counts[var]
            return 0

    if (imtcq == "q")|(imtcq == "Q"):
        if (inputs[var] == 0)&(inputsPrev[var] == 1):
            inputsPrev[var] = inputs[var]
            return input
        else:
            inputsPrev[var] = inputs[var]
            return 0

############################# LOGIC ###################################
# Needed because logical not return true or false
def nott (input):
    if (input == 0):
        return 1
    else:
        return 0

############################# COILS ###################################
#Asign the imput to output or mark value
def coil(input, var, qm):
    if (qm == "q")|(qm == "Q"):
        outputs[var] = input
    if (qm == "m")|(qm == "M"):
        marks[var] = input

def coilInv(input, var, qm):
    if (qm == "q")|(qm == "Q"):
        outputs[var] = nott(input)
    if (qm == "m")|(qm == "M"):
        marks[var] = nott(input)

#Set the output or mark value
def coilSet(input, var, qm):
    if (qm == "q")|(qm == "Q"):
        if (input == 1):
            outputs[var] = 1
    if (qm == "m")|(qm == "M"):
        if (input == 1):
            marks[var] = 1

#Reset the coil value
def coilReset(input, var, qm):
    if (qm == "q")|(qm == "Q"):
        if (input == 1):
            outputs[var] = 0
    if (qm == "m")|(qm == "M"):
        if (input == 1):
            marks[var] = 0

############################# TIMERS ###################################
# ON Timer block. pt = number of seconds. var = number of the timer
def ton(input, pt, var):
    if (input == 1):
        if (timerAux[var] == 0):
            timerAux[var] = time.time()+pt
        elif(timerAux[var] <= time.time()):
            timers[var] = 1
    else:
        timerAux[var] = 0
        timers[var] = 0

# OFF Timer block.
def toff(input, pt, var):
    if (input == 1):
        if (timerAux[var] == 0):
            timerAux[var] = time.time()+pt
            timers[var] = 1
        elif(timerAux[var] <= time.time()):
            timers[var] = 0
    else:
        timerAux[var] = 0
        timers[var] = 0

############################# COUNTERS ###################################
# Counter block. CU: increment, CD: decrease, R: reset, PV: target, VAR: counter number
def counter(cu, cd, r, pv, var):
    if (r == 1)&(countPrevR[var]!= 1):
        countAux[var] = 0
    else:
        if (cu == 1)&(countPrevCU[var]!= 1):
            countAux[var] = countAux[var] +1

        if (cd == 1)&(countPrevCD[var]!= 1):
            countAux[var] = countAux[var] - 1

        if (countAux[var] >= pv):
            counts[var] = 1
        else:
            counts[var] = 0

    countPrevCU[var]= cu
    countPrevCD[var]= cd
    countPrevR[var]= r

############################# COMUNICATION FUNCTIONS ###################################
# Read the input pins state
def get():
    ser.write("0")
    return ser.readline()

# Write the output pins
def set(pinstring):
    # INPUT EXAMPLE >> "1000000000000000000" >> "1" + 18 pins
    ser.write(pinstring)
