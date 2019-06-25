

class JohnPerson(object):

    def __init__(self, close:float, high:float, low:float):
        self.close = close
        self.high = high
        self.low = low
        calculate = self.calculate_john_person_pivots(close=close, high=high, low=low)
        self.pp = calculate['pp']
        self.r1 = calculate['r1']
        self.r2 = calculate['r2']
        self.r3 = calculate['r3']
        self.s1 = calculate['s1']
        self.s2 = calculate['s2']
        self.s3 = calculate['s3']

    def should_go_long(self, up_bound:float):
        if up_bound < self.r2:
            return 1
        else:
            return 0

    def should_go_short(self, low_bound:float):
        if low_bound > self.s2:
            return 1
        else:
            return 0

    def calculate_john_person_pivots(self, close: float, high: float, low: float):
        pp = (close + high + low) / 3
        r1 = 2 * pp - low
        r2 = pp + high - low
        r3 = r2 + high - low
        s1 = 2 * pp - high
        s2 = pp - high + low
        s3 = s2 - high + low
        return {'pp': pp, 'r1': r1, 'r2': r2, 'r3': r3, 's1': s1, 's2': s2, 's3': s3}