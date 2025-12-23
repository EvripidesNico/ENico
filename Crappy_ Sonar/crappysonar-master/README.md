-------
README
-------
Authors:
- Abhishek Vijayakumar
- Evripides Nicolaides
- Jerek Cheung

--------------------------
||Flashing code to pic32||
--------------------------
1.To run this project, you must first open up CrappySonar.X as a project in MPLABX.
2.Next, you need to flash the code to the pic32
3.You need to disconnect the JTAG programmer once downloaded. 
4.Leave the pic32 wire connected to the computer


----------------------------
||Project Optional Compiles||
----------------------------
Both ping.c and main.c posses a series of #defines in the beginning which are used to enable or disable test cases at compilation.
This section describes the use of these defines.

MAIN.C

1. MAIN_ACTIVE: 1 or 0

This toggles the __main function in main.c. This is used for test cases in other files, pleasure ensure they are disabled before compiling this main 

2. SERVO_TEST_BUTTONS: 1 or 0

This toggles the button code in the primary operation loop, enabling this will disable the devices state machine, leaving only manual servo control.

3. SERVO_DEBUG: 0 or 1

This toggles optional prints at the beginning of the sweeping states in the state machine. Used for debuging the state machine.


PING.C

1. PING_TEST_MAIN: 1 or 0

This toggles the __main function in ping.c used for testing and calibration. Ensure that no other main is active for proper compilation.

--------------------------------
||Connecting to CrappySonarGUI||
--------------------------------
1.Open up Idle(any computer with python should have this)
2.Install requisite library pyserial to read serial data coming from the pic32
3.Next open up your Device Manager 
4.Go to the COM ports tab and identify the COM port that is being utilized by the pic32's USB (example: COM12)
5.In the init, find the comment "Configure the serial port" and alter the port variable to match the COM port that was identified in Device Manager
6.Lastly, you open up the CrappySonarGUI file and run CrappySonarGUI.py
7.From here you can watch the sonar map points around it.


----------------------------------
||Common Problem and Resolutions||
----------------------------------
- If the servo is stuttering, ensure that the JTAG programmer is disconnected after flashing the pic32
- If the GUI is not picking up distances (distance values will be stuck)
	- Then close the GUI and the shell in IDLE and run the code again
	- This might take a couple trys but it seems to be a sure fire fix

