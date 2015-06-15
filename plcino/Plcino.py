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

############################# CONTACTS ###################################

def contact(input, var):
    if (var == 1):
        return input
    else:
        return 0

def contactNot(input, var):
    if (var == 0):
        return input
    else:
        return 0

#Return 1 with a positive flank, 0 in other case. imtc sets the tipe of var value: i(input), m(mark), t(timer), c(counter)
def contactPos(input, var, imtc):
    if (imtc == "i")|(imtc == "I"):
        if (inputs[var] == 1)&(inputsPrev[var] == 0):
            inputsPrev[var] = inputs[var]
            return input
        else:
            inputsPrev[var] = inputs[var]
            return 0

    if (imtc == "m")|(imtc == "M"):
        if (marks[var] == 1)&(marksPrev[var] == 0):
            marksPrev[var] = marks[var]
            return input
        else:
            marksPrev[var] = marks[var]
            return 0

    if (imtc == "t")|(imtc == "T"):
        if (timers[var] == 1)&(timersPrev[var] == 0):
            timersPrev[var] = timers[var]
            return input
        else:
            timersPrev[var] = timers[var]
            return 0

    if (imtc == "c")|(imtc == "C"):
        if (counts[var] == 1)&(countsPrev[var] == 0):
            countsPrev[var] = counts[var]
            return input
        else:
            countsPrev[var] = counts[var]
            return 0

#Return 1 with a negative flank, 0 in other case
def contactNeg(input, var, imtc):
    if (imtc == "i")|(imtc == "I"):
        if (inputs[var] == 0)&(inputsPrev[var] == 1):
            inputsPrev[var] = inputs[var]
            return input
        else:
            inputsPrev[var] = inputs[var]
            return 0

    if (imtc == "m")|(imtc == "M"):
        if (marks[var] == 0)&(marksPrev[var] == 1):
            marksPrev[var] = marks[var]
            return input
        else:
            marksPrev[var] = marks[var]
            return 0

    if (imtc == "t")|(imtc == "T"):
        if (timers[var] == 0)&(timersPrev[var] == 1):
            timersPrev[var] = timers[var]
            return input
        else:
            timersPrev[var] = timers[var]
            return 0

    if (imtc == "c")|(imtc == "C"):
        if (counts[var] == 0)&(countsPrev[var] == 1):
            countsPrev[var] = counts[var]
            return input
        else:
            countsPrev[var] = counts[var]
            return 0

############################# LOGIC ###################################
def nott(input):
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


############################# MAIN PROGRAM ###################################

# Set the configuration of the plc
setPLC(32,18,7000,500,500)
# Time to connect with the arduino
time.sleep(1)

while(1): # RUN STATE
    print "/////////////////////////////////////////////////////////////////////////"
# READ THE INPUTS //////////////////////////////////////////////////////////////
    s = get()
    for i in range(0,InputPins):
        inputs[i] = int(s[i])
    print "Inputs: "+str.__getslice__(s,0,InputPins)
    s = ""

# PROGRAM //////////////////////////////////////////////////////////////////////
    #counter(inputs[31],inputs[30],inputs[29],3,0)
    #ton(inputs[31],3,0)
    #coilSet(contact(1,counts[0]), 0,"o")
    #coilMark(contact(1,temps[0]), 0)
    #coilSet(contact(1,inputs[31]),0,"m")
    #coilReset(contact(1,inputs[30]),0,"m")
    #coil(contactNeg(1,31,"i"),0,"m")
    #coil(nott(contactNeg(1,0,"t")),0, "q")

    ########### Blinked led example ###################
    #
    # In this example, the blinked led is in output[0] = pin 2 in arduino (0 and 1 are tx and rx)

    #
    #   m0      ___t0__
    # --| |-----|   tON|
    #           |      |
    #         1-|______|
    #
    #   t0               ___t1__
    # --| |--------------|   tON|
    #         |          |      |
    #         |        1-|______|
    #         |
    #         |           q0
    #         |----------(  )
    #
    #                     m0
    # -------------------( S )
    #
    #   t1                m0
    # --| |--------------( S )
    #
    ####################################################

    # Its the same as --ton(contact(1,marks[0]),1,0)-- but if the contact input is 1 always, you can skip it
#    ton(marks[0],1,0)

    # To do the fork, there are 2 options. This is the first:
#    ton(timers[0],1,1) # Set the timer with: input = value of timer 0, pt = 1 second, number of this thimer = 1
#    coil(timers[0],0,"q") # Set the coil with: input = value of timer 0, number of output/mark = 0, type = output

    # And this is the second (this is better if you have more logic before the fork):
    #aux = timers[0]
    #ton(aux,1,1)
    #coil(aux,0,"q")

#    coilSet(1,0,"m") # Set the mark 0 allwais (input is 1)
#    coilReset(timers[1],0,"m") # Reset the mark 0 when timer1 = 1

    #####################################################

    print contact((1 or 0),1)
    print"\teee"


# WRITE THE OUTPUTS ///////////////////////////////////////////////////////////
    for i in range(0,OutputPins):
        s = s+ str(outputs[i])
    print "Outputs: "+s
    out = "1"+s
    set(out)
    s = ""

