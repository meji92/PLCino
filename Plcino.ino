//Constants
//Number of output pins (from 2 to OUT = outputPins = OUT-1) >> TX and RX are busy with the serial comunication
int OUT = 19;
//Number of the input pins (from OUT+1 to ALL) >> the number of pins -1 (0)
int ALL = 53;
//Number of pins of arduino -2
int pin[54];

//MEGA ALL = 53, PIN = 54 // PINS 20, 21 KO
//UNO ALL = 13, PIN = 14


int aux = 0;
int rw = 0;

void setup()
{
   for (int x=2; x<=OUT; x++){
     pinMode(x, OUTPUT);
   }
   for (int x=OUT+1; x<=ALL; x++){
     pinMode(x, INPUT);
   }

   Serial.begin(9600); //iniciando Serial
}

void loop() {

   //Read the operation bit
   rw =  Serial.peek();

   //If rw = 0, read the values of the inputs/////////////////////////////////////
   if (rw == '0'){
     //for (int x=OUT+1; x<=ALL; x++){
     for (int x=OUT+3; x<=ALL; x++){
       aux = digitalRead(x);
       if (aux == HIGH){
         pin[x]= '1';
       }
       if (aux == LOW){
         pin[x]= '0';
       }
     }
     //for (int x=OUT+1; x<=ALL; x++){
     for (int x=OUT+3; x<=ALL; x++){
       Serial.write(pin[x]);
     }
     Serial.write("\n");
     rw = Serial.read();
   }else{
     //If there are the input values in the serial buffer
     if (Serial.available() > OUT-1)
     {
        rw = Serial.read();
        //If rw = 1, write the values of the outputs
        //if (rw == '1'){
          for (int x=2; x<=OUT; x++){
            pin[x]= Serial.read();
          }
          for (int x=2; x<=OUT; x++){
            if (pin[x]== '1'){
              digitalWrite(x, HIGH);
            }else{
              digitalWrite(x, LOW);
            }
          }
          //for (int x=2; x<=OUT; x++){
          //  Serial.write(pin[x]);
          //}
          //Serial.write("1");
          //Serial.write("\n");
        //}
     }
   }
}
