import tkinter as tk
import math
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

        self.canvas = tk.Canvas(master, width=1200, height=1200)  # Scale canvas size
        self.canvas.pack()

        self.turret = self.canvas.create_rectangle(555, 555, 645, 645, fill="gray")  # Turret base, scaled
        self.sonar1 = self.canvas.create_line(600, 600, 600, 300, fill="blue", width=6)  # Sonar 1, scaled
        self.sonar2 = self.canvas.create_line(600, 600, 600, 900, fill="red", width=6)   # Sonar 2, scaled

        self.draw_polar_grid()

        self.angle = 0
        self.rotation_direction = 1  # Initially rotate forward
        #self.update_turret()        

        # Create a label to display received data
        self.received_data_label = tk.Label(master, text="Received Data: ")
        self.received_data_label.pack(anchor=tk.NW)

        # Create labels for displaying distance1, distance2, and servo angle
        self.distance1_label = tk.Label(master, text="Distance 1: ")
        self.distance1_label.pack(anchor=tk.NW)

        self.distance2_label = tk.Label(master, text="Distance 2: ")
        self.distance2_label.pack(anchor=tk.NW)

        self.servo_angle_label = tk.Label(master, text="Servo Angle: ")
        self.servo_angle_label.pack(anchor=tk.NW)

        # Create Start Button
        self.start_button = tk.Button(master, text="Start", command=self.start_action)
        self.start_button.pack(anchor=tk.NW)

        # Create Stop Button
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_action)
        self.stop_button.pack(anchor=tk.NW)

        # Create Clear Button
        self.clear_button = tk.Button(master, text="Clear", command=self.clear_action)
        self.clear_button.pack(anchor=tk.NW)

    def main(self):
        distance1, distance2, servo_angle = self.read_serial_data()
        self.draw_polar_grid()
        self.plot_points(distance1, distance2, servo_angle)  # Plot points based on the received data
        self.update_turret(servo_angle)
        # Update labels with received data
        self.distance1_label.config(text="Distance 1: " + str(distance1))
        self.distance2_label.config(text="Distance 2: " + str(distance2))
        self.servo_angle_label.config(text="Servo Angle: " + str(servo_angle))
        # Schedule the main method to run again after a delay
        self.master.after(100, self.main)

    def draw_polar_grid(self):
        self.canvas.delete("grid")  # Clear existing grid

        # Calculate the coordinates for placing the "6 Feet" label
        label_x = 618  # X-coordinate remains constant
        label_y = 288  # Y-coordinate is the top of the y-axis
        label_text = "6 Feet"  # Text for the label

        # Create the text object
        self.canvas.create_text(label_x, label_y, text=label_text, anchor=tk.E, fill="black")

        for angle in range(0, 360, 15):
            angle_radians = math.radians(-angle + 90)  # Adjust the angle to start from the top and go clockwise
            x1 = 600 + 300 * math.sin(angle_radians)  # Scale coordinates
            y1 = 600 - 300 * math.cos(angle_radians)  # Scale coordinates
            x2 = 600 - 300 * math.sin(angle_radians)  # Scale coordinates
            y2 = 600 + 300 * math.cos(angle_radians)  # Scale coordinates
            self.canvas.create_line(x1, y1, x2, y2, fill="black", dash=(3, 3), tags="grid")

            # Add degree labels
            label_x = 600 + 330 * math.sin(angle_radians)
            label_y = 600 - 330 * math.cos(angle_radians)
            self.canvas.create_text(label_x, label_y, text=str(angle) + "°", fill="black", tags="grid")
            

        # Add circles expanding from the center
        for r in range(75, 301, 75):
            self.canvas.create_oval(600 - r, 600 - r, 600 + r, 600 + r, outline="black", dash=(3, 3), tags="grid")

    def update_turret(self, servo_angle):
        # Convert servo angle to turret angle (adjust if necessary)
        turret_angle = 5 - servo_angle

        # Convert turret angle to radians
        angle_radians = math.radians(turret_angle)

        # Calculate the endpoint coordinates of the sonar beams
        x1 = 600 + 300 * math.cos(angle_radians)  # Calculate x-coordinate for sonar1
        y1 = 600 + 300 * math.sin(angle_radians)  # Calculate y-coordinate for sonar1
        x2 = 600 - 300 * math.cos(angle_radians)  # Calculate x-coordinate for sonar2
        y2 = 600 - 300 * math.sin(angle_radians)  # Calculate y-coordinate for sonar2

        # Update the coordinates of the sonar beams
        self.canvas.coords(self.sonar1, 600, 600, x1, y1)  # Update coordinates for sonar1
        self.canvas.coords(self.sonar2, 600, 600, x2, y2)  # Update coordinates for sonar2


    def read_serial_data(self):
        distance1 = distance2 = servo_angle = 0
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
        x_center, y_center = 600, 600  # Center coordinates
        scale_factor = 6  # Adjust this factor for appropriate scaling

        # Calculate coordinates for distance1
        if 25 < distance1 < 1828:
            x1 = x_center + (distance1 / scale_factor) * math.cos(math.radians(servo_angle))
            y1 = y_center - (distance1 / scale_factor) * math.sin(math.radians(servo_angle))
            # Plot a green point and tag it as "green_points"
            self.canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="green", tags="green_points")

        # Calculate coordinates for distance2
        if 25 < distance2 < 1828:
            x2 = x_center + (distance2 / scale_factor) * -math.cos(math.radians(servo_angle))
            y2 = y_center - (distance2 / scale_factor) * -math.sin(math.radians(servo_angle))
            # Plot a red point and tag it as "red_points"
            self.canvas.create_oval(x2 - 3, y2 - 3, x2 + 3, y2 + 3, fill="red", tags="red_points")


    def clear_points(self):
        self.canvas.delete("green_points")  # Delete all objects with tag "green_points"
        self.canvas.delete("red_points")  # Delete all objects with tag "red_points"

    def start_action(self):
        self.ser.write(b'S')
        print(b'S')
        
    def stop_action(self):
        self.ser.write(b'T')
        print(b'T')

    def clear_action(self):
        self.clear_points()

root = tk.Tk()
gui = SonarGUI(root)
gui.main()  # Start the main loop

root.mainloop()
