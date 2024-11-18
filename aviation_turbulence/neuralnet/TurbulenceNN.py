### This class is a NueralNet for turbulence classification
### using profiles from MERRA 2 re-analysis and trained on
### PIREPS turbulence reports
### Christopher Phillips

### Import required modules
import copy
from datetime import datetime
import pandas
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize

### The Neural Network
class TURBnet(nn.Module):

    # The initialization function
    def __init__(self, n_features):

        # Need to call the init of the base Module function
        super(TURBnet, self).__init__()

        # Define the model architecture
        # This is more art than science, unfortunately.
        # Multiple hidden layers are called Deep Learning
        # More layers typically work better than fewer but larger layers.
        self.model = nn.Sequential(
            nn.Linear(n_features, 100),
            nn.LeakyReLU(),
            nn.Linear(100, 60),
            nn.LeakyReLU(),
            nn.Linear(60, 60),
            nn.LeakyReLU(),
            nn.Linear(60, 40),
            nn.LeakyReLU(),
            nn.Linear(40, 20),
            nn.LeakyReLU(),
            nn.Linear(20, 1),
            nn.Sigmoid()
        )

    # A function to load a previous model state
    def load_model(self, fpath):
        self.model.load_state_dict(torch.load(fpath))
        self.model.eval()

    # A function to save the current model state
    def save_model(self, spath=None):
        if (spath == None):
            spath = f"checkpoint_{datetime.utcnow().strftime('%Y-%m-%d_%H%M')}.pt"

        torch.save(self.model.state_dict(), spath)

    # A function for inferrencing
    def predict(self, X):

        X = torch.tensor(X, dtype=torch.float32)
        
        return self.model(X)