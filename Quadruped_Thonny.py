from machine import Pin, PWM
import time
import sys


class Servo:
    """Represents and controls individual servos.

    Attributes:
        pwm (PWM): PWM instance for controlling servo pulse width.
        min_pulse (int): Minimum pulse width in microseconds for controlling
          the servo.
        max_pulse (int): Maximum pulse width in microseconds for controlling
          the servo.
        current_position (int): Current position of the servo in degrees.
    """
    def __init__(self, pin_number, min_pulse=1000, max_pulse=2000):
        """Initialises the servo with a min and max pulse range.

        Args:
            pin_number (int): GPIO pin number used for PWM output.
            min_pulse (int, optional): Minimum pulse width in microseconds,
              default is 1000.
            max_pulse (int, optional): Maximum pulse width in microseconds,
              default is 2000.
        """
        self.pwm = PWM(Pin(pin_number))
        self.pwm.freq(50)
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.current_position = 0

    def degrees_to_duty(self, degrees):
        """Convert a degree value to the corresponding duty cycle.

        Args:
            degrees (float): Desired angle in degrees, ranging from 0 to 180.

        Returns:
            int: Duty cycle value corresponding to the input angle.
        """
        pulse_width = self.min_pulse + (degrees / 180.0) *\
            (self.max_pulse - self.min_pulse)
        return int((pulse_width / 20000.0) * 65535)

    def set_position(self, degrees):
        """Sets the position of a servo.

        Args:
            degrees (float): Desired angle in degrees, ranging from 0 to 180.

        Raises:
            ValueError: If degrees is not within 0 to 180.
        """
        if not 0 <= degrees <= 180:
            raise ValueError("Degrees must be within 0 to 180.")

        duty = self.degrees_to_duty(degrees)
        self.pwm.duty_u16(duty)
        self.current_position = degrees

    def get_position(self):
        """Return the current position of the servo in degrees"""
        return self.current_position


class QuadrupedController:
    """Main class for managing the quadruped's servo operations.

    Attributes:
        servo_pins (list): List of GPIO pin numbers assigned to servos.
        servos (list): List of Servo instances representing the
        quadruped's servos.
    """

    def __init__(self):
        """Initialise the quadruped controller and its servos.

        Sets up the servos on the specified GPIO pins.
        """
        self.servo_pins = [
            0, 1, 2, 3, 15, 14, 13, 12  # Put in pins for each servo
            ]
        self.servos = []
        self.setup_servos()

    def setup_servos(self):
        """Initialise and configure each servo based on predefined pins."""
        for pin in self.servo_pins:
            self.servos.append(Servo(pin))

    def update_servos(self, positions):
        """Update all servos positions based on a list of positions.

        Args:
            positions (list): List of angles in degrees (0-180) for each servo.

        Raises:
            ValueError: If positions list does not match the number of servos.
            ValueError: If any position is not within the valid range (0-180)
        """
        if len(positions) != len(self.servos):
            raise ValueError("Number of positions must match number\
                             of servos.")

        for servo, position in zip(self.servos, positions):
            servo.set_position(position)
            time.sleep(0.1)
            servo.pwm.duty_u16(0)

    def get_servo_positions(self):
        """Return the current positions of all servos as a list of angles"""
        return [servo.get_position() for servo in self.servos]


class SerialHandler:
    """Manages receiving serial communication with the PC."""

    def receive_command(self):
        """Receive a command using through serial input.

        Returns:
            str: Command string received from the PC, or None if no command
              is received.

        Raises:
            Exception: If there is an error reading from sys.stdin.
        """
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
    """Main loop for controlling the quadruped based on serial commands.

    Continutously listens for commands to update servo positions.

    Raises:
        ValueError: If a command cannot be parsed into servo positions.
    """
    controller = QuadrupedController()
    serial_handler = SerialHandler()
    print("Starting main loop...")
    while True:
        time.sleep(1)
        raw_command = serial_handler.receive_command()

        if raw_command:
            command = raw_command.strip("[]'")
            positions = command.split(",")
            print(f"Parsed positions before conversion: {positions}")
            try:
                positions = [int(pos.strip()) for pos in positions]
                controller.update_servos(positions)
            except ValueError:
                print("Invalud position values received")
