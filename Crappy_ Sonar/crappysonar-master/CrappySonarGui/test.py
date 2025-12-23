import tkinter as tk
import math
import random
import serial

class SonarGUI:
    
    def __init__(self, master):
        self.master = master
        master.title("Sonar GUI")

        # Configure the serial port
        self.ser = serial.Serial(
            port='COM4',    # Update this with your COM port
            baudrate=115200,  # Update this with the baud rate of your UART device
            timeout=1       # Timeout for read operation
        )

        # Open the serial port
        #self.ser.open()

        self.canvas = tk.Canvas(master, width=800, height=800)  # Scale canvas size
        self.canvas.pack()

        self.turret = self.canvas.create_rectangle(370, 370, 430, 430, fill="gray")  # Turret base, scaled
        self.sonar1 = self.canvas.create_line(400, 400, 400, 200, fill="blue", width=4)  # Sonar 1, scaled
        self.sonar2 = self.canvas.create_line(400, 400, 400, 600, fill="red", width=4)   # Sonar 2, scaled

        self.draw_polar_grid()

        self.angle = 0
        self.rotation_direction = 1  # Initially rotate forward
        self.update_turret()        

        # Create a label to display received data
        self.received_data_label = tk.Label(master, text="Received Data: ")
        self.received_data_label.pack()

    def main(self):
        cock, balls, torture = self.read_serial_data()
        self.draw_polar_grid()
        self.plot_points(cock, balls, torture)  # Plot points based on the received data
        self.update_turret()
        # Schedule the main method to run again after a delay
        self.master.after(100, self.main)

    def draw_polar_grid(self):
        self.canvas.delete("grid")  # Clear existing grid
        for angle in range(0, 360, 15):
            angle_radians = math.radians(-angle + 90)  # Adjust the angle to start from the top and go clockwise
            x1 = 400 + 200 * math.sin(angle_radians)  # Scale coordinates
            y1 = 400 - 200 * math.cos(angle_radians)  # Scale coordinates
            x2 = 400 - 200 * math.sin(angle_radians)  # Scale coordinates
            y2 = 400 + 200 * math.cos(angle_radians)  # Scale coordinates
            self.canvas.create_line(x1, y1, x2, y2, fill="black", dash=(3, 3), tags="grid")

            # Add degree labels
            label_x = 400 + 220 * math.sin(angle_radians)
            label_y = 400 - 220 * math.cos(angle_radians)
            self.canvas.create_text(label_x, label_y, text=str(angle) + "°", fill="black", tags="grid")

        # Add circles expanding from the center
        for r in range(50, 201, 50):
            self.canvas.create_oval(400 - r, 400 - r, 400 + r, 400 + r, outline="black", dash=(3, 3), tags="grid")

    def update_turret(self):
        # Check if the turret reached its maximum angle, if so, start rotating back
        if self.angle >= 180:
            self.rotation_direction = -1
        # Check if the turret reached its minimum angle, if so, start rotating forward
        elif self.angle <= 0:
            self.rotation_direction = 1
        
        # Update the angle based on the rotation direction
        self.angle += self.rotation_direction  # Constant rotation rate
        
        angle_radians = math.radians(self.angle)
        x1 = 400 + 200 * math.sin(angle_radians)  # Scale coordinates
        y1 = 400 - 200 * math.cos(angle_radians)  # Scale coordinates
        x2 = 400 - 200 * math.sin(angle_radians)  # Scale coordinates
        y2 = 400 + 200 * math.cos(angle_radians)  # Scale coordinates

        self.canvas.coords(self.sonar1, 400, 400, x1, y1)  # Scale coordinates
        self.canvas.coords(self.sonar2, 400, 400, x2, y2)  # Scale coordinates

    def read_serial_data(self):
        try:
            # Read a line from the serial port
            line = self.ser.readline().decode('utf-8').strip()
                    
            # Split the line into individual values
            values = line.split(',')
                    
            if len(values) == 3:
                # Extract distance values and servo angle
                distance1 = int(values[0])
                distance2 = int(values[1])
                servo_angle = int(values[2])

                # Update the label with received data
                self.received_data_label.config(text="Received Data: " + line)

        except KeyboardInterrupt:
            # Close the serial port when the program is interrupted
            self.ser.close()

        return distance1, distance2, servo_angle

    def plot_points(self, distance1, distance2, servo_angle):
        # Calculate coordinates based on servo angle and distance
        x_center, y_center = 400, 400  # Center coordinates
        scale_factor = 5  # Adjust this factor for appropriate scaling

        # Calculate coordinates for distance1
        if 25 < distance1 < 1000:
            x1 = x_center + (distance1 / scale_factor) * math.cos(math.radians(servo_angle))
            y1 = y_center - (distance1 / scale_factor) * math.sin(math.radians(servo_angle))
            # Plot a green point
            self.canvas.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill="green")

        # Calculate coordinates for distance2
        if 25 < distance2 < 1000:
            x2 = x_center + (distance2 / scale_factor) * math.cos(math.radians(servo_angle))
            y2 = y_center - (distance2 / scale_factor) * math.sin(math.radians(servo_angle))
            # Plot a red point
            self.canvas.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill="red")

    def clear_points(self):
        self.canvas.delete("points")  # Delete all objects with tag "points"

    def start_action(self):
        self.ser.write(b'Start\n')

    def stop_action(self):
        self.ser.write(b'Stop\n')


root = tk.Tk()
gui = SonarGUI(root)
gui.main()  # Start the main loop

# Create Start Button
start_button = tk.Button(root, text="Start", command=gui.start_action)
start_button.pack()

# Create Stop Button
stop_button = tk.Button(root, text="Stop", command=gui.stop_action)
stop_button.pack()

root.mainloop()
