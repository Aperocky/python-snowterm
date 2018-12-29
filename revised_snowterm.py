import curses
import time
import random

class Sim:

    def __init__(self, length, width, **kwargs):
        self.length = length
        self.width = width
        self.flakes = []
        # Intensity of the storm.
        self.intensity = kwargs['intensity'] if 'intensity' in kwargs else 0.05
        self.falls = [0] * width 

    # This generate new frame from top.
    def generate(self):
        newpos = [i for i in range(self.width) if random.uniform(0,1) < self.intensity]
        # Adding dummy vars at the end of tuples for potential usage
        newflakes = [(random.choice(['*','+','.']), 0, j, 0, 0) for j in newpos]
        return newflakes

    def run(self):
        # Add falls.
        newfalls = [t[2] for t in self.flakes if t[1]+1 >= self.length]
        for i in newfalls:
            self.falls[i] += 1

        # Move flakes down
        #self.flakes = [(t[0], t[1]+1, t[2], 0, 0) for t in self.flakes if t[1]+1 < self.length]
        newflakes = []
        for each in self.flakes:
            if each[1]+1 < self.length:
                vertpos = each[1] + 1
                horipos = each[2]
                if random.uniform(0,1) < 0.5: # drift
                    drift = random.choice([-1,1])
                    if 0 <= horipos + drift < self.width:
                        horipos += drift
                newflake = (each[0], vertpos, horipos, 0, 0)
                newflakes.append(newflake)
        self.flakes = newflakes

        # Add new flakes
        newflakes = self.generate()
        self.flakes.extend(newflakes) 


def main(window):
    if curses.can_change_color():
        curses.init_color(curses.COLOR_BLACK, 0,0,0)
        curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)
    curses.init_pair(1, curses.COLOR_YELLOW, 0)    
    try:
        curses.curs_set(0)
    except Exception:
        pass  # Can't hide cursor in 2019 huh?
    window.border()
    length, width = window.getmaxyx()
    sim = Sim(length-2, width-1)
    while True:
        sim.run()
        window.clear()
        for each in sim.flakes:
            window.addch(each[1], each[2], each[0])
        for i in range(width-1):
            rows = sim.falls[i]//10
            for j in range(rows):
                window.addch(length-1-j, i,'H') 
        window.refresh()
        time.sleep(0.1)
    print(sim.falls)

curses.wrapper(main)
        

