PLCino simulate a simple PLC with an arduino driving digital (analog not yet) inputs and outputs 

PLCino implements the following functions:

- Set functions:

    - def setPLC (nInputs,nOutputs,nMarks,nTimers,nCounts):
    
      Set the number of inputs, outputs, marks, timers and counters
      
    - def addMark ():
    
      Add a new mark and return the position in the array of marks
      
    - def addTimer():
    
      Add a new timer and return the position in the array of timers
    
    - def addCount():
    
      Add a new counter and return the position in the array of counters
      
    - def setInputs(newInputs):
    
        Set the inputs like the given in newInputs with this structure: ";0,1;2,0;3,1;" where ;Number of input, value; Number of input, value; ......
      
- Contacts:
    
    - def contact(input, var, imtcq):
    
      --| |--
      
      Function contact where var is the number of the imput, mark, timer or counter that activate the contact.
      imtcq sets the tipe of var value: i(input), m(mark), t(timer), c(counter), q(input)
      
    - def contactNot(input, var, imtcq):
    
      --|/|--
    
      Normaly closed contact
    
    - def contactPos(input, var, imtcq):   
    
      --|P|--
    
      Return 1 with a positive flank, 0 in other case.

    - def contactNeg(input, var, imtcq):   
    
      --|N|--      
    
      Return 1 with a negative flank, 0 in other case
      
- Logic

    - def nott (input):
      
      -|NOT|-
      
      Logic NOT
      
- Coils

    - def coil(input, var, qm):
    
      --(  )--
      
      Asign the imput to output or mark value. qm sets the tipe of the imput: q (output), m (mark)
      
    - def coilInv(input, var, qm):
    
      --(/)--
      
    - def coilSet(input, var, qm):
    
      --(S)--
    
      Set the output or mark value
      
    - def coilReset(input, var, qm):
    
      --(R)--
      
      Reset the coil value
      
- Timers

    - def ton(input, pt, var):
    
#
            ___var_
     input-|   tON|
           |      |
        pt-|______|
    
ON Timer block. pt = number of seconds. var = number of the timer
      
- 
    - def toff(input, pt, var):
      
         OFF Timer block
        
- Counters
    
    - def counter(cu, cd, r, pv, var):

#
              ___var_
           cu-|      |
              |      |
           cd-|      |
              |      |
            r-|      |
              |      |
           pv-|______|
      

Counter block. CU: increment, CD: decrease, R: reset, PV: target, VAR: counter number

- Comunication:

    - def get():
        
        Read the input pins state
            
    - def set(pinstring):
            
        Write the output pins

      







# Blinked led example
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
    # --| |--------------( R )
    #
    ####################################################

    # Starts the timer 0 with mark 0
    ton(contact(1,0,"m"),1,0)

    # To do the fork, there are 2 options. This is the first:
    # Set the timer with: input = value of timer 0, pt = 1 second, number of this thimer = 1
    ton(contact(1,0,"t"),1,1) 
    # Set the coil with: input = value of timer 0, number of output/mark = 0, type = output
    coil(contact(1,0,"t"),0,"q")

    # And this is the second (this is better if you have more logic before the fork):
    # aux = contact(1,0,"t")
    # ton(aux,1,1)
    # coil(aux,0,"q")

    # Set the mark with 0 always (input is 1)
    coilSet(1,0,"m") 
    # Reset the mark 0 when timer1 = 1
    coilReset(contact(1,1,"t"),0,"m") 






Notes
- The number of inputs and outputs must be the same in the .py file and .ino file load in arduino
- Serial file (/dev/ttyXXX) must have permissions to read and write
- You can edit the serial config in the 3rd line: ser = serial.Serial('/dev/ttyACM0', 9600)


