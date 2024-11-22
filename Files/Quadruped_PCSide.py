import tkinter as tk
from tkinter import messagebox, Label, Scale, StringVar, Button, Entry, HORIZONTAL
import json
import serial
import time 
from threading import Thread

class Servo:
    def __init__(self, parent, servo_id, name: str, x: int, y: int, min_val=0, max_val=180):
        self.parent = parent
        self.servo_id = servo_id
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.value = StringVar()
        self.label = Label(parent, text=self.name)
        self.label.grid(row=y, column=x, padx=10, pady=10)
        self.scale = Scale(parent, variable=self.value, from_=self.min_val, to=self.max_val, orient=HORIZONTAL, length=200)
        self.scale.grid(row=y, column=x + 1, padx=10, pady=10)
        self.entry_var = StringVar()
        self.entry = tk.Entry(parent, textvariable=self.entry_var, width=5)
        self.entry.grid(row=y, column=x + 2, padx=10, pady=10)
        self.entry.bind("<Return>", self.update_from_textbox)
        self.scale.bind("<ButtonRelease-1>", self.update_textbox)

    def update_from_textbox(self, event):
        try:
            value = int(self.entry_var.get())
            if self.min_val <= value <= self.max_val:
                self.scale.set(value)
            else:
                self.entry_var.set("")
        except ValueError:
            self.entry_var.set("")

    def update_textbox(self, event):
        self.entry_var.set(self.get_value())
    
    def get_value(self):
        return self.value.get()
    
    def set_value(self, value):
        self.scale.set(value)
        self.entry_var.set(value)

class Leg:
    def __init__(self, parent, leg_id, base_x, base_y):
        self.parent = parent
        self.leg_id = leg_id
        self.servos = []

        if leg_id == 1:
            labels = ["Front Left Ankle", "Front Left Hip"]
        elif leg_id == 2:
            labels = ["Back Left Ankle", "Back Left Hip"]
        elif leg_id == 3:
            labels = ["Front Right Ankle", "Front Right Hip"]
        elif leg_id == 4:
            labels = ["Back Right Ankle", "Back Right Hip"]
        
        for servo_id in range(1, 3):
            servo_name = labels[servo_id - 1]
            servo = Servo(parent, servo_id, servo_name, base_x, base_y + (servo_id - 1))
            self.servos.append(servo)

class Quadruped:
    def __init__(self, parent):
        self.parent = parent
        self.legs = []
        for leg_id in range(1, 5):
            if leg_id <= 2:
                base_x = 0
            base_y = (leg_id - 1) * 2
            leg = Leg(parent, leg_id, base_x, base_y)
            self.legs.append(leg)

class StateManager:
    def __init__(self, quadruped):
        self.filename = "states.json"
        self.states_dict = {}
        self.quadruped = quadruped

    def load_states(self):
        try:
            with open(self.filename, "r") as file:
                self.states_dict = json.load(file)
        except FileNotFoundError:
            print("States file not found, creating file with empty states...")
            self.save_states({})
        except TypeError:
            print("There was an issue with the deserialising of the dictionary.")

    def save_states(self, states_dict):
        self.states_dict.update(states_dict)
        try:
            with open(self.filename, "w") as outfile:
                json.dump(self.states_dict, outfile)
        except TypeError:
            print("There was an issue with serialising the dictionary.")

    def get_state(self):
        if self.states_dict:
            return self.states_dict.get("default")
        return

    def set_state(self, state):
        if state is None:
            print("State does not exist")
            return
        for leg in self.quadruped.legs:
            for servo in leg.servos:
                if servo.name in state:
                    servo.set_value(state[servo.name])
                else:
                    print(f"No value found for {servo.name} in loaded state")

class SerialCommunicator:
    def __init__(self, port="COM6", baud_rate=115200):
        try:
            self.s = serial.Serial(port, baud_rate)
            print(f"Connected to {port} at {baud_rate} baud")
        except serial.SerialException:
            print("Couldn't find COM port")

    def send_command(self, value_list):
        try:
            command = ",".join(map(str, value_list))
            commandbytes = bytes(f"{command}\n", encoding="utf-8")
            self.s.write(commandbytes)
            print(f"Command sent: {commandbytes}")
        except AttributeError:
            print("The COM port was already occupied")

    def receive_data(self):
        while True:
            if self.s.in_waiting > 0:
                message = self.s.readline().decode("utf-8").strip()
                return message
            return None

class QuadrupedGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.geometry("400x700")
        self.parent.title("Quadruped GUI")
        self.quadruped = Quadruped(root)
        self.state_manager = StateManager(self.quadruped)
        self.serial_communicator = SerialCommunicator()
        self.state_name_var = StringVar()  # Variable to hold the state name
        self.create_gui()

    def create_gui(self):
        Label(self.parent, text="State Name:").grid(row=9, column=0, padx=10, pady=10)
        Entry(self.parent, textvariable=self.state_name_var).grid(row=9, column=1, padx=10, pady=10)

        Button(self.parent, text="Save State", command=self.save_state).grid(row=8, column=0, padx=0, pady=20)
        Button(self.parent, text="Load State", command=self.load_state).grid(row=8, column=1, padx=0, pady=20)
        Button(self.parent, text="Update Pico", command=self.update_pico).grid(row=10, column=0, padx=(0, 0), pady=20)
        Button(self.parent, text="Stand", command=self.stand).grid(row=10, column=1, padx=0, pady=20)
        Button(self.parent, text="Wave", command=self.wave).grid(row=10, column=2, padx=0, pady=20)

        self.parent.grid_columnconfigure(0, weight=1, uniform="equal")
        self.parent.grid_columnconfigure(1, weight=1, uniform="equal")
        self.parent.grid_columnconfigure(2, weight=1, uniform="equal")

    def stand(self):
        stand_positions = [0, 55, 0, 139, 0, 142, 0, 55]
        index = 0
        for leg in self.quadruped.legs:
            for servo in leg.servos:
                servo.set_value(stand_positions[index])
                index += 1

    def wave(self):
        def perform_wave():
            # Initial standing position
            self.values = [0, 113, 0, 139, 90, 170, 0, 55]
            self.update_pico()
            time.sleep(0.1)

            for _ in range(5):
                wave_pos1 = [0, 113, 0, 139, 170, 142, 0, 55]
                index = 0
                for leg in self.quadruped.legs:
                    for servo in leg.servos:
                        servo.set_value(wave_pos1[index])
                        index += 1
                self.update_pico()  # Send wave position 1 to the servos
                time.sleep(0.1) 

                wave_pos2 = [0, 113, 0, 139, 170, 102, 0, 55]
                index = 0
                for leg in self.quadruped.legs:
                    for servo in leg.servos:
                        servo.set_value(wave_pos2[index])
                        index += 1
                self.update_pico()  # Send wave position 2 to the servos
                time.sleep(0.1) 
            self.stand()
        perform_wave()

    def save_state(self):
        state_name = self.state_name_var.get().strip()
        if not state_name:
            messagebox.showerror("Error", "Please enter a name for the state before saving.")
            return
        
        states = {}
        for leg in self.quadruped.legs:
            for servo in leg.servos:
                states[servo.name] = servo.get_value()

        # Save the state under the provided name
        self.state_manager.save_states({state_name: states})
        messagebox.showinfo("Success", f"State '{state_name}' saved successfully!")

    def load_state(self):
        self.state_manager.load_states()
        state_name = self.state_name_var.get().strip()
        if not state_name:
            messagebox.showerror("Error", "Please enter the name of the state to load.")
            return
        
        state = self.state_manager.states_dict.get(state_name)
        if state is None:
            messagebox.showerror("Error", f"No saved state found for '{state_name}'")
        else:
            self.state_manager.set_state(state)

    def update_pico(self):
        value_list = []
        for leg in self.quadruped.legs:
            for servo in leg.servos:
                value = servo.get_value()
                value_list.append(value)
        self.serial_communicator.send_command(value_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrupedGUI(root)
    root.mainloop()