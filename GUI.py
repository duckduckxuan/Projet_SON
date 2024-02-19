import tkinter as tk
from tkinter import Canvas
import math
import serial
from threading import Thread

class ArduinoInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Vinyl Simulator")

        button_frame = tk.Frame(root)
        button_frame.pack()

        self.arm_length = 160
        self.arm_angle = 90
        self.arm_width = 8
        self.playing = False
        self.arm_on_turntable = False
        self.gain = 0

        self.ser = serial.Serial('COM5', 9600, timeout = 0.5)
        self.reading_thread = Thread(target=self.read_data)
        self.reading_thread.start()

        # Use the tag_bind method of Canvas to bind the mouse click event
        self.canvas = Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.canvas.create_oval(320 - 15, 80 - 15, 320 + 15, 80 + 15, fill="silver", outline="dimgrey", tags="turntable")

        self.draw_turntable()

    def read_data(self):
        """Read data from Teensy."""
        while True:
            try:
                # Read data
                data = self.ser.readline().decode().strip()
                if data and data[0].isdigit():
                    # Split data
                    values = data.split(', ')

                    # Get value and label
                    sensor_key = values[0]
                    sensor_label = values[1].strip("'")
                    
                    if sensor_label == 'gain':
                        self.gain = float(sensor_key)
                    elif sensor_label == 'play':
                        begin = int(sensor_key)
                        if begin == 1:
                            self.start_playing()
                        else:
                            self.stop_playing()

            except serial.SerialException as e:
                print(f"Error while reading data：{e}")
                break

    def start_playing(self):
        """Start the playback simulation."""
        self.playing = True
        self.arm_on_turntable = True
        self.draw_turntable()

    def stop_playing(self):
        """Stop the playback simulation."""
        self.playing = False
        self.arm_on_turntable = False
        self.draw_turntable()

    def draw_turntable(self):
        """Draw the vinyl turntable, tonearm, and knobs."""
        self.canvas.delete("all")

        # Draw the turntable body
        self.canvas.create_rectangle(50, 50, 350, 350, fill="darkred")

        # Draw the vinyl record
        vinyl_radius = 100
        center_x = 200
        center_y = 200
        self.canvas.create_oval(center_x - vinyl_radius, center_y - vinyl_radius, center_x + vinyl_radius, center_y + vinyl_radius, fill="black", outline="black")
        while vinyl_radius > 45:
            vinyl_radius -= 7
            self.canvas.create_oval(center_x - vinyl_radius, center_y - vinyl_radius, center_x + vinyl_radius, center_y + vinyl_radius, fill="black", outline="dimgray")

        # Draw the center hole of the vinyl record
        hole_radius = 45
        self.canvas.create_oval(center_x - hole_radius, center_y - hole_radius, center_x + hole_radius, center_y + hole_radius, fill="gold", outline="black")

        # Draw the tonearm
        rayon = 15
        arm_x = 320 + self.arm_length * math.cos(math.radians(self.arm_angle))
        arm_y = 80 + self.arm_length * math.sin(math.radians(self.arm_angle))
        needle_x = 320 + (self.arm_length + 25) * math.cos(math.radians(self.arm_angle + 5))
        needle_y = 80 + (self.arm_length + 25) * math.sin(math.radians(self.arm_angle + 5))
        self.canvas.create_line(arm_x, arm_y, needle_x, needle_y, width=self.arm_width, fill="white")
        self.canvas.create_line(320, 80, arm_x, arm_y, width=self.arm_width, fill="white")
        self.canvas.create_oval(320 - rayon, 80 - rayon, 320 + rayon, 80 + rayon, fill="silver", outline="dimgrey", tags="turntable")

        # Draw the Gain and Speed knobs with pointers
        self.create_knob(80, 320, 15, "#ADD8E6", "gain", self.gain)

        # Update the tonearm angle
        if self.arm_on_turntable and self.arm_angle < 110:
            self.arm_angle += 1
            self.canvas.create_line(arm_x, arm_y, needle_x, needle_y, width=self.arm_width, fill="white")
            self.canvas.create_line(320, 80, arm_x, arm_y, width=self.arm_width, fill="white")
            self.canvas.create_oval(320 - rayon, 80 - rayon, 320 + rayon, 80 + rayon, fill="silver", outline="dimgrey", tags="turntable")

        if not self.arm_on_turntable and self.arm_angle >90:
            self.arm_angle -= 1
            self.canvas.create_line(arm_x, arm_y, needle_x, needle_y, width=self.arm_width, fill="white")
            self.canvas.create_line(320, 80, arm_x, arm_y, width=self.arm_width, fill="white")
            self.canvas.create_oval(320 - rayon, 80 - rayon, 320 + rayon, 80 + rayon, fill="silver", outline="dimgrey", tags="turntable")

        # Update the display
        self.root.update()

        # If playing, call itself to create a rotating effect
        if self.playing:
            self.root.after(60, self.draw_turntable)
        # If stopped, rotate the tonearm back to the original position
        elif not self.playing:
            self.root.after(60, self.draw_turntable)

        # Rotate the knobs based on slider values
        self.rotate_knob("gain")

    def create_knob(self, x, y, radius, color_outer, tag, variable):
        """Create a knob Gain with a pointer."""
        pointer_x = x + radius * math.cos(math.radians(180+float(variable)/10*180))
        pointer_y = y + radius * math.sin(math.radians(180+float(variable)/10*180))
        gradient_color, highlight_color = self.calculate_metal_gradient(color_outer)
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=gradient_color, outline=highlight_color, tags=tag)
        self.canvas.create_line(x, y, pointer_x, pointer_y, width=3, fill=highlight_color, tags=tag)

    def hex_to_rgb(self, hex_color):
        """Convert a hexadecimal color to RGB."""
        try:
            hex_color = hex_color.lstrip("#")
            return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            print(f"Invalid color string: {hex_color}")
            return (0, 0, 0)

    def calculate_metal_gradient(self, color):
        """Calculate a gradient color for the metal appearance."""
        # Adjust these values based on your preference
        gradient_factor = 0.1
        highlight_factor = 1.15

        try:
            r, g, b = self.hex_to_rgb(color)
        except ValueError:
            return "black"

        gradient_r = int(r * (1 - gradient_factor))
        gradient_g = int(g * (1 - gradient_factor))
        gradient_b = int(b * (1 - gradient_factor))

        highlight_r = min(255, int(r * highlight_factor))
        highlight_g = min(255, int(g * highlight_factor))
        highlight_b = min(255, int(b * highlight_factor))

        gradient_color = "#{:02X}{:02X}{:02X}".format(gradient_r, gradient_g, gradient_b)
        highlight_color = "#{:02X}{:02X}{:02X}".format(highlight_r, highlight_g, highlight_b)

        # Ensure that gradient_color and highlight_color are not the same
        if gradient_color == highlight_color:
            gradient_color = "#{:02X}{:02X}{:02X}".format(
                int(gradient_r * (1 - gradient_factor)),
                int(gradient_g * (1 - gradient_factor)),
                int(gradient_b * (1 - gradient_factor))
            )

        # Return the gradient and highlight colors as a tuple
        return gradient_color, highlight_color

    def rotate_knob(self,tag):
        """Rotate the knob based on the Teensy value."""
        self.canvas.delete(tag)

        self.create_knob(80, 320, 15, "#ADD8E6", tag, self.gain)

        self.root.after(150, lambda: self.rotate_knob(tag))


if __name__ == "__main__":
    root = tk.Tk()
    app = ArduinoInterface(root)
    root.mainloop()
