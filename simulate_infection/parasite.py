import numpy

class ParasitePop:
    """
    """
    def __init__(self, count= 1, resistance= 0, repr_rate= 2, transmissibility= 1):
        if count < 1:
            raise Exception('Start population must have at least one individual')
        if resistance < 0 or resistance > 1:
            raise Exception("Resistance must be >= 0 and <= 1 (i.e. it's the % of parasites surviving drug treatment)")
        if transmissibility < 0 or transmissibility > 1:
            raise Exception("Transmissibility must be >= 0 and <= 1 (i.e. it's the % of parasites surviving the mosquito gut and being transmissed)")

        self.count = count
        self.resistance = resistance
        self.repr_rate = repr_rate
        self.transmissibility = transmissibility

    def __str__(self):
        return 'count %s | resistance %.2f | reproduction rate %.2f | transmissibility %.2f' % (self.count, self.resistance, self.repr_rate, self.transmissibility)
