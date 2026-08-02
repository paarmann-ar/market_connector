import time


class TimerContextManager:
    def __enter__(self):
        self.start = time.perf_counter()
        print("starting timer...")
        return self

    # --
    # ... exit
    # --

    def __exit__(self, exc_type, exe_value, exc_tb):
        self.end = time.perf_counter()
        print(f"Timer stop, Elapses time: {self.end - self.start}")
