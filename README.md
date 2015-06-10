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
      
- Contacts:
    
    - def contact(input, var):                    
    
      --| |--
      
      Function contact where var is the variable that activate the contact (input, mark, timer, counter)
      
    - def contactNot(input, var):                   
    
      --|/|--
    
      Normaly closed contact
    
    - def contactPos(input, var, imtc):   
    
      --|P|--
    
      Return 1 with a positive flank, 0 in other case. imtc sets the tipe of var value: i(input), m(mark), t(timer), c(counter)

    - def contactNeg(input, var, imtc):   
    
      --|N|--      
    
      Return 1 with a negative flank, 0 in other case
      
- Logic

    - def nott (input):
      
      -|NOT|-
      
      Logic NOT
      
    - def orr (input1, input2):
      
      Logic OR 
      
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
        input-|   tON|
              |      |
           pt-|______|
      

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
    # --| |--------------( S )
    #
    ####################################################

    # Its the same as --ton(contact(1,marks[0]),1,0)-- but if the contact input is 1 always, you can skip it
    ton(marks[0],1,0)

    # To do the fork, there are 2 options. This is the first:
    # Set the timer with: input = value of timer 0, pt = 1 second, number of this thimer = 1
    ton(timers[0],1,1) 
    # Set the coil with: input = value of timer 0, number of output/mark = 0, type = output
    coil(timers[0],0,"q")

    # And this is the second (this is better if you have more logic before the fork):
    # aux = timers[0]
    # ton(aux,1,1)
    # coil(aux,0,"q")

    # Set the mark 0 allwais (input is 1)
    coilSet(1,0,"m") 
    # Reset the mark 0 when timer1 = 1
    coilReset(timers[1],0,"m") 






Notes
- The number of inputs and outputs must be the same in the .py file and .ino file load in arduino
- Serial file (/dev/ttyXXX) must have permissions to read and write
- You can edit the serial config in the 3rd line: ser = serial.Serial('/dev/ttyACM0', 9600)


