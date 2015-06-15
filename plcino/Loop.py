from Plcino import *

############################# MAIN PROGRAM ###################################
InputPins = 0
OutputPins = 0
# Set the configuration of the plc
setPLC(32,18,7000,500,500)
OutputPins,InputPins = getPLC()
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
    ton(marks[0],1,0)

    # To do the fork, there are 2 options. This is the first:
    ton(timers[0],1,1) # Set the timer with: input = value of timer 0, pt = 1 second, number of this timer = 1
    coil(timers[0],0,"q") # Set the coil with: input = value of timer 0, number of output/mark = 0, type = output

    # And this is the second (this is better if you have more logic before the fork):
    #aux = timers[0]
    #ton(aux,1,1)
    #coil(aux,0,"q")

    coilSet(1,0,"m") # Set the mark 0 allwais (input is 1)
    coilReset(timers[1],0,"m") # Reset the mark 0 when timer1 = 1

    #####################################################

# WRITE THE OUTPUTS ///////////////////////////////////////////////////////////
    for i in range(0,OutputPins):
        s = s+ str(outputs[i])
    print "Outputs: "+s
    out = "1"+s
    set(out)
    s = ""


