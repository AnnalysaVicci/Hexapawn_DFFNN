#network.py

#layer i of the network
class Layer:
    def __init__(self, parent, neurons, first_in):
        self.parent = parent
        self.n = neurons
        self.m = parent.n
        
        #NxM matrix of weights
        #N = num of neurons on layer i
        #M = num of neurons on layer i-1
        matrix = []

class Network:
    def __init__(self):
        layers = []

def classify(in_vector):
    pass

#Testing
def main():
    pass