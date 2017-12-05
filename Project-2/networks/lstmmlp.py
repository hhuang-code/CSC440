import torch
import torch.nn as nn
from torch.autograd import Variable

class LSTMMLP(nn.Module):
    def __init__(self, input_size, hidden_size, batch_size):
        super(Model, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size

        # num_layers = 1, bidirectional = False
        self.lstm = nn.LSTM(input_size, hidden_size)

        self.mlp = nn.Linear(hidden_size, 1)

    """
    Args:
        x: vectors of words in a title, (seq_len, batch_size, input_size)
    Return:
        
    """
    def forward(self, x):
        # h_n: encoded representation, (1, batch_size, hidden_size)
        _, (h_n, c_n) = self.lstm(x)
        # reshape h_n to shape (batch_size, 1, hidden_size)
        h_n_reshape = h_n.view(batch_size, 1, hidden_size)
        # out: a scalar, represent the change of stock price
        out = self.mlp(h_n_reshape)

        return out

