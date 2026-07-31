import time
import sys
import CONSTS
import colorama

# --
# ... delay
# --

class Delay:
    def __init__(self, delay_):
        colorama.init()
        print(f"{CONSTS.COLORS.DELAY_PROMPT.value}I am waiting for {delay_} milliseconds", end="")
        delay_ /= 1000

        int_delay = int(delay_)
        float_delay = delay_ - int_delay

        sys.stdout.flush()

        for _ in range(int_delay):
            time.sleep(1)
            print(".", end="", flush=True)

        if float_delay > 0:
            time.sleep(float_delay)
            print(".", end="", flush=True)

        print(f"{CONSTS.COLORS.ENDC.value}")
        