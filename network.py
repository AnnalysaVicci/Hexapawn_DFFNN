#network.py
import random
import numpy as np


#layer i of the network
class Layer:
    def __init__(self,):
        self.matrix = matrix
        
        #NxM matrix of weights
        #N = num of neurons on layer i
        #M = num of neurons on layer i-1
        matrix = []
    
    def create_layer(self, is_first_in, ):
        matrix = []
        if is_first_in:
            for i in range(9):
                for j in range(10):
                    matrix.append(random.random())
        else:
            for i in range(9):
                for j in range(9):
                    matrix.append(random.random())
        self.matrix = matrix

    def create_bias(self):
        bias = []
        for i in range(9):
            for j in range(1):
                bias.append(random.random())
        self.bias = bias

#this is the directed graph
class Network:
    def __init__(self):
        self.layers = []

    def add_layer(self, is_first_layer):
        layer = Layer()
        layer.create_layer()
        layer.create_bias()
        self.layers.append(layer)


def sigmoid_activation(x):
    return 1 / (1 + np.exp(-x))

def relu_activation(x):
    return np.maximum(0,x)

def sigmoid_derivative(x):
    sig = sigmoid_activation(x)
    return sig * (1 - sig)

def relu_derivative(x):
    return 1 if x > 0 else 0

#(Xj is the input vector for the jth example and Yj is the output),
def classify(network, input_vector):
    network = Network()
    l1 = Layer(input_vector, None, True)
    network.layers.append(l1)
    #455, 474, 1040, 1057, 1063, 1115, 1200, 1219

#payoff function: matrix, row for each possible action of one player, column
#for each possible choice of the other player
#payoff matrix: which each cell is labeled with payoffs for both players. pg 1115

#Testing
def main():
    network = Network()
    network.add_layer(True, False)
    network.add_layer(False, True)