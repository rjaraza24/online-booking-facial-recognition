I. Hardware Raspberry Pi Bootup (2 pieces)

1. Input HDMI cable Monitor, Camera USB(Raspi1)/ PiCamera(Raspi2), Keyboard and Mouse

2. Insert Cables for Output Modules. Pinout Reference: https://community.element14.com/products/raspberry-pi/m/files/17428
   a. Raspi1 Solenoid Lock Relay - Red Cable->5V Power(Pin#02) ; Brown Cable->Ground(Pin#06) ; Brown Cable->GPIO14(Pin#08)
   
   b. Raspi2 Servo Motor - Red Cable->5V Power(Pin#02) ; Brown Cable->Ground(Pin#06) ; Brown Cable->GPIO17(Pin#11)

3. Check again the connections of cables and inputs

4. If okay, insert the Micro USB Power Adapter 5V

5. Raspberry will now boot up, wait for Desktop to display. MAKE SURE WIFI IS STABLE

6. Get Flash Drive (with copied updated files sent from online) then input to raspis1,2

7. In raspi1,2 , open File Manager(folder icon), go to /home/pi/project/face-recognition

8. Copy all the 3 files from Flash Drive to that folder path
  a. API python program - for raspi1(working-api-door1.py) , for raspi2 (working-api-door1.py) 
  
  b. Face Encoder Trainer program - face-encoding.py
  
  c. Face Recognition program - for raspi1(face-working-recog-door1.py) , for raspi2 (face-working-recog-door2.py) 
  
  
  
9. To use the API python program

go to LX Terminal (black CMD icon)
enter "cd project/face-recognition/"  without ("")
"python3 working-api-door1.py "

if no booking, program will train empty dataset/ folder , rendering all faces in camera as "Unknown Person"

if booking is "active" (raspi1- room_id 33 - dataset/door1; raspi2- room_id 34 - dataset/door2)  , program will get photo and save it in the 
specific door folder in dataset, training encode python and face recog python will auto run if booking is active

press key 'q' to end running program

ps. since 1 image only fetch from web, very low accuracy on Face Recognition algorithm,  must train more pictures in folder before running recognizer. 

if face recognized, door1-relay will trigger alongside the solenoid, door2-pwm servo will operate

10. To use Face encode and recognition without web API,

put pictures in dataset/door1 or dataset/door2 as 001.jpg - 002.jpg - etc
go to LX Terminal (black CMD icon)
enter "cd project/face-recognition/"  without ("")

encode first - "python3 face-encoding.py --dataset dataset --encodings encodings.pickle --detection-method hog"

then run recognize - "python3 face-working-recog-door1.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle --door1 14 --door2 17"

press key 'q' to end running program

ps. since 1 image only fetch from web, very low accuracy on Face Recognition algorithm, must train more pictures in folder before running recognizer. 

if face recognized, door1-relay will trigger alongside the solenoid, door2-pwm servo will operate






