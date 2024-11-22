from machine import Pin, PWM
import time
import sys

class Servo:
    """Controls an individual servo motor."""

    def __init__(self, pin_number, min_pulse=1000, max_pulse=2000):
        """Initialises the servo with a GPIO pin and pulse range."""
        self.pwm = PWM(Pin(pin_number))
        self.pwm.freq(50)
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.current_position = 0

    def degrees_to_duty(self, degrees):
        """Converts angle (0-180) to a duty cycle value."""
        pulse_width = self.min_pulse + (degrees / 180.0) * (self.max_pulse - self.min_pulse)
        return int((pulse_width / 20000.0) * 65535)

    def set_position(self, degrees):
        """Sets the servo to the specified angle (0-180)."""
        if not 0 <= degrees <= 180:
            raise ValueError("Degrees must be within 0 to 180.")
        duty = self.degrees_to_duty(degrees)
        self.pwm.duty_u16(duty)
        self.current_position = degrees

    def get_position(self):
        """Returns the current servo angle."""
        return self.current_position

class QuadrupedController:
    """Manages the quadruped's servos."""

    def __init__(self):
        """Initialises servos on predefined GPIO pins."""
        self.servo_pins = [0, 1, 2, 3, 15, 14, 13, 12]
        self.servos = []
        self.setup_servos()

    def setup_servos(self):
        """Initialises each servo."""
        for pin in self.servo_pins:
            self.servos.append(Servo(pin))

    def update_servos(self, positions):
        """Updates servos to the specified angles."""
        if len(positions) != len(self.servos):
            raise ValueError("Number of positions must match the servos.")
        for servo, position in zip(self.servos, positions):
            servo.set_position(position)
            time.sleep(0.1)
            servo.pwm.duty_u16(0)

    def get_servo_positions(self):
        """Returns the current angles of all servos."""
        return [servo.get_position() for servo in self.servos]

class SerialHandler:
    """Handles serial communication with the PC."""

    def receive_command(self):
        """Reads a command string from serial input."""
        if sys.stdin:
            try:
                raw_command = sys.stdin.readline().strip()
                if raw_command:
                    print(f"Received command: {raw_command}")
                    return raw_command
            except Exception as e:
                print(f"Error receiving command: {e}")
        return None

def start():
    """Main loop for controlling the quadruped."""
    controller = QuadrupedController()
    serial_handler = SerialHandler()
    print("Starting main loop...")
    while True:
        time.sleep(1)
        raw_command = serial_handler.receive_command()

        if raw_command:
            command = raw_command.strip("[]'")
            positions = command.split(",")
            print(f"Parsed positions: {positions}")
            try:
                positions = [int(pos.strip()) for pos in positions]
                controller.update_servos(positions)
            except ValueError:
                print("Invalid position values received.")