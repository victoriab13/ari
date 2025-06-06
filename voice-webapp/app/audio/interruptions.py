import time

class InterruptionManager:
    def __init__(self, abrupt_interruption_delay=3.0, def_interrupted_vad_pause_length=3):
        self.interrupted = False
        self.last_interruption_time = 0.0
        self.abrupt_interruption_delay = abrupt_interruption_delay  # seconds
        self.def_interrupted_vad_pause_length = def_interrupted_vad_pause_length

    def handle_interruption(self, is_interrupted):
        if is_interrupted:
            print("Interrupted")
            self.interrupted = True
            self.last_interruption_time = time.time()
            print(f"Increase VAD pause length to {self.def_interrupted_vad_pause_length}")
            # Here you would call your VAD adjustment logic
        else:
            print("NOT Interrupted. Restore default VAD pause length.")
            self.interrupted = False
            # Here you would restore your default VAD pause length

    def check_smart_interruption(self):
        now = time.time()
        if self.interrupted and (now - self.last_interruption_time < self.abrupt_interruption_delay):
            print("Abrupt interruption detected. Prompting user to continue.")
            self.interrupted = False
            # Here you could trigger a message: "Sorry, please continue."
            return True
        return False