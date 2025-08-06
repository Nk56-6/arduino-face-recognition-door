# Face-Recognition Door Lock

This was a group project, I worked with two of my coworkers for the creation of this project. This project uses **Python** and **C++** code to make a door lock/unlock when a face is detected. When an authorized face is detected the system will run the ***handlePass()*** function. When an unauthorized face is detected the system will run the ***handleFail()*** function, which then runs the ***intruder()*** function.

---

## Components Used

| Component               | Quantity |
|------------------------|----------|
| Arduino Uno R3         | 1        |
| Breadboard             | 1        |
| Green LED                | 1        |
| Red LED                | 1         |
| 220Ω Resistors          | 2        |
| Jumper Wires           | 15      |
| Servo Motor           | 1   |
| Piezo Buzzer         | 1   |
| Raspberry Pi             | 1  |
| Microsoft Webcam              | 1  |

---

## Installation & Setup

### Raspberry Pi (Face Recognition)

> Install [Cyberduck](https://cyberduck.io/)

> Use the tutorial from [Core Electronics Face Recognition Guide](https://core-electronics.com.au/guides/raspberry-pi/face-recognition-with-raspberry-pi-and-opencv/) to set up the Raspberry Pi. Add the Python code in this Repo to the Raspberry Pi.

### Arduino (Main Circuit)

1. **Connect Power to the Bread Board**
   - 5V → Bread Board positive strip (+)
   - GND → Bread Board negative strip (-)
   
2. **Connect the LEDs**  
   - Green LED anode (+) → Digital Pin 9  
   - Green LED cathode (–) → 220Ω Resistor → GND
   - Red LED anode (+) → Digital Pin 11 
   - Red LED cathode (–) → 220Ω Resistor → GND

3. **Connect the Piezo Buzzer**  
   - Positive → Digital Pin 12  
   - Negative → GND

4. **Connect the Servo Motor**  
   - Signal(Yellow) → Digital Pin 7  
   - Power(Red) → 5V  
   - GND(brown or black) → GND

5. **Connect the TM1637 display**
   - VCC → 5V  
   - GND → GND  
   - DIO → 5
   - CLK → 6

6. **Upload the Code**:
   - Open [Arduino IDE](https://www.arduino.cc/en/software/).
   - *Install the program if you don't already have it.*
   - Connect your Arduino Uno via USB.
   - Upload your `.ino` sketch.
   
7. **Connect the Arduino to the Raspberry Pi**
   - Plug one end of the USB into one of the Raspberry Pi USB ports
   - Plug the other end into the Arduino

8. **Connect the Webcam**
   - Plug the webcam into one of the USB ports on the Raspberry Pi

## How It Works

1.  The AI that the python script makes gets trained to recognize the faces of the other people in my group, listing them as "authorized".
    
2.  The webcam is connected to the raspberry pi so the AI can use it to detect those authorized faces.
    
3.  If an authorized face is detected by the AI, the handlePass() function activates. This function opens the door for a period of time, then locks it again. The 7-segment display will display a "hello" and "goodbye" message.
    

4. If an unknown face is detected, the handleFail() function activates. This function then calls upon the intruder() function, which displays a different message on the 7-segment display.

## Images / Videos

- ![Project Setup](images/project-setup.jpg)

## Simulation

> Use an online simulator like [Tinkercad](https://www.tinkercad.com/) to view or simulate the main circuit of the project.

- [Tinkercad Simulation Link](https://www.tinkercad.com/things/3U5mjMHGdw5-temperature-fan-with-display-nat?sharecode=d1k_oRAmztpzLEHx-oRXd9poU2PdSio1NQsSGfVgCGE)

> Use an online simulator like [Wokwi](https://wokwi.com/) to view or simulate how the **Seven Segment Display** gets connected to the project.

- [Wokwi Simulation Link](https://wokwi.com/projects/436555416015897601)

## Credits
- Project by: *Nat King*
- Inspired by: Face recognition technologies
- Libraries used:
  - `Arduino.h`
  - `TM1637Display.h`

---
