import math

from queues.schemas.s_general import TypeRepeat


class ToRepeat:

    manual_delay_default = (100, 100, 200, 300, 400, 500,
                            1*1000, 2*1000, 3*1000, 5*1000, 10*1000, 15*1000,
                            30*1000, 45*1000, 60*1000, 60*1000*2, 60*1000*3,
                            60*1000*5, 60*1000*10, 60*1000*15, 60*1000*24,
                            60*1000*30, 60*1000*45, 60*1000*60)
    max_ms_delay = 1000*3600
    min_ms_delay = 1

    def __init__(self,
                 type_delay: str = TypeRepeat.linear.value,
                 counter: int = 0,
                 k: int = 1,
                 b: int = 0,
                 n: int = 2,
                 manual_delay: tuple = manual_delay_default,
                 evenly_delay: int = 500,
                 max_ms_delay: int = max_ms_delay,
                 min_ms_delay: int = min_ms_delay):
        # Required
        self.type_delay = type_delay
        self.counter = counter

        # Optional
        self.max_ms_delay = max_ms_delay
        self.min_ms_delay = min_ms_delay
        self.k = k
        self.b = b
        self.n = n
        self.manual_delay = manual_delay
        self.evenly_delay = evenly_delay

    def set_counter(self, value):
        self.counter = value

    def get_counter(self):
        return self.counter

    def inc_counter(self):
        self.counter += 1

    def get_delay(self) -> int:
        delay_repeat = {
            "linear": self.linear(),
            "manual": self.manual(),
            "expo": self.exponent(),
            "log": self.logn(),
            "fibo": self.fibo(),
            "evenly": self.evenly()
        }
        delay_ms = int(delay_repeat.get(self.type_delay, self.evenly()))
        delay_ms = delay_ms if delay_ms > 0 else 1
        delay_ms = self.max_ms_delay if delay_ms >= self.max_ms_delay else delay_ms
        delay_ms = self.min_ms_delay if delay_ms < self.min_ms_delay else delay_ms
        return delay_ms

    def linear(self):
        return int(self.k * self.counter + self.b)

    def manual(self):
        if self.counter < len(self.manual_delay):
            return int(self.manual_delay[self.counter])
        return int(self.manual_delay[len(self.manual_delay)-1])

    def exponent(self):
        return int(math.exp(self.counter))

    def logn(self):
        if self.counter == 0:
            self.counter = 1
        return int(math.log2(self.counter)*1000)

    def fibo(self):
        def fibonacci_of(n):
            if n in {0, 1}:
                return 1
            return n
        return int(fibonacci_of(self.counter - 1) +
                   fibonacci_of(self.counter - 2))*1000

    def evenly(self):
        return int(self.evenly_delay)


if __name__ == "__main__":
    delay = ToRepeat(type_delay=str(TypeRepeat.fibo.value))
    for i in range(30):
        delay.set_counter(i)
        print(delay.get_delay())
