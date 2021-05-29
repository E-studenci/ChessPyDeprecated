import time


class PlayerClock:
    def __init__(self):
        self.timer = 0
        self.pause = True

    def start(self):
        while True:
            while self.pause:
                time.sleep(0.01)
            self.timer += 100
            time.sleep(0.1)

    def get_time(self):
        seconds = int((self.timer / 1000) % 60)
        minutes = int((self.timer / 1000 / 60) % 60)
        return f'{["", "0"][minutes <= 9]}{minutes}:' + f'{["", "0"][seconds <= 9]}{seconds}'
