from machine import Pin, PWM
import time
import sys


class Servo:
    def __init__(self, pin_number, min_pulse=500, max_pulse=2500):
        self.pwm = PWM(Pin(pin_number))
        self.pwm.freq(50)
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.current_position = 0

    def degrees_to_duty(self, degrees):
        pulse_width = self.min_pulse + (degrees / 180.0) * (self.max_pulse - self.min_pulse)
        return int((pulse_width / 20000.0) * 65535)

    def set_position(self, degrees):
        if not 0 <= degrees <= 180:
            raise ValueError("Degrees must be within 0 to 180.")
        duty = self.degrees_to_duty(degrees)
        self.pwm.duty_u16(duty)
        self.current_position = degrees

    def get_position(self):
        return self.current_position


class QuadrupedController:
    def __init__(self):
        self.servo_pins = [0, 1, 2, 3, 4, 5, 6, 7]
        self.servos = []
        self.setup_servos()

    def setup_servos(self):
        for pin in self.servo_pins:
            self.servos.append(Servo(pin))

    def update_servos(self, positions):
        if len(positions) != len(self.servos):
            raise ValueError("Number of positions must match the servos.")
        for servo, position in zip(self.servos, positions):
            servo.set_position(position)
            time.sleep(0.1)  # Adjust the delay to 0.1 seconds for continuous update
            servo.pwm.duty_u16(0)

    def get_servo_positions(self):
        return [servo.get_position() for servo in self.servos]


class SerialHandler:
    def receive_command(self):
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
    controller = QuadrupedController()
    serial_handler = SerialHandler()
    print("Starting main loop...")

    # Flag to control continuous updates
    should_update = False
    last_received_positions = []

    while True:
        time.sleep(0.1)  # Main loop sleep time (100ms)

        raw_command = serial_handler.receive_command()
        if raw_command:
            # Process commands and break out of the circle wave loop if needed
            command = raw_command.strip("[]'")
            if command == "circle_wave":
                print("Starting circle wave...")
                circle_wave(controller)
            else:
                try:
                    positions = [int(pos.strip()) for pos in command.split(",")]
                    last_received_positions = positions
                    should_update = True
                except ValueError:
                    print("Invalid position values received.")

        # Regular position updates if `circle_wave` isn't active
        if should_update:
            controller.update_servos(last_received_positions)


if __name__ == "__main__":
    start()