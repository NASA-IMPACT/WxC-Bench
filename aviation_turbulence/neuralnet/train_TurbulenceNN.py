### This script trains the Turbulence Prediction Neural network
### Christopher Phillips

##### START OPTIONS #####

level = 'low'

# Location of training data
tpath = f'/rhome/cphillip/IMPACT/DL_WeatherForcast/Turbulence_Detection/training_data_20240126/training_data_{level}_fl.nc'

# Location to save the model checkpoint
sdir = f'/rhome/cphillip/IMPACT/DL_WeatherForcast/Turbulence_Detection/baseline/checkpoints_{level}/'

# Batch size
batch_size = 50

# Number of epochs
n_epochs = 100

#####  END OPTIONS  #####

### Import modules
import copy
from datetime import datetime
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split

from data_loader import load_training_data, load_all_training_data
from TurbulenceNN import TURBnet

# Load the training data
X, y = load_training_data(tpath)

# Initialize the model
# Model requires number of input features
net = TURBnet(X.shape[1])

# Create the training/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, shuffle=True)

# Normalize all of the data
u = np.mean(X_train, axis=0)
s = np.std(X_train, axis=0)
print(u.shape)
for i in range(u.size):
    X_train[:,i] = (X_train[:,i]-u[i])/s[i]
    X_test[:,i] = (X_test[:,i]-u[i])/s[i]

# Determine any class imbalance and set loss weights to compensate
frac = np.sum(y_train == 1)/y_train.size
weights = np.zeros(y_train.shape)
weights[y_train == 1] = (1.0-frac)
weights[y_train == 0] = frac
weights = torch.tensor(weights, dtype=torch.float32)
print(weights.shape)

# Convert to PyTorch Tensors (in case they're not already)
# Note the 32bit dtype. Model weights default to float32 and the data must be the same
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

# Set the optimizer
# The optimizer is what adjusts the model weights on each pass
optimizer = optim.Adam(net.model.parameters(), lr=0.001)

# Get training start date
start_date = datetime.utcnow()

# Create the log file
log_path = f'{sdir}/training_log_{start_date.strftime("%Y-%m-%d_%H%M")}.txt'
log = open(log_path, 'w')
log.write(f'Number of epochs: {n_epochs}\nBatch size: {batch_size}\nStart Date: {start_date.strftime("%Y-%m-%d_%H%M")}\nEpoch, Loss')
log.write(f'\nNumber of samples: {X.shape[0]}. Number of features: {X.shape[1]}.')
log.write(f'\nFraction of the "True" class: {frac*100.0:.2f}%')

# Save the normalization values
np.savez(f'{sdir}/norm_mean_std_{start_date.strftime("%Y-%m-%d_%H%M")}.npz', mean=u, std=s)

# Perform the actual training
best_loss = np.inf # Initialize a best loss metric
for epoch in range(n_epochs): # The Epoch loop. Each Epoch will loop through all training data
    
    # Set the model to training mode (some layers behave differently during training)
    net.model.train()

    # The batch loop, break the data into chunks for training
    for start in torch.arange(0, len(X_train), batch_size):

        # Get training batch
        X_batch = X_train[start:start+batch_size]
        y_batch = y_train[start:start+batch_size]
        w_batch = weights[start:start+batch_size]

        # Do a forward pass through the model
        # This is where the model makes prediction
        y_pred = net.model(X_batch)

        # Compute the loss
        loss_fn = nn.BCELoss(weight=w_batch)
        loss = loss_fn(y_pred.squeeze(), y_batch)

        # Back propgation
        # This is where the model evaluates it performance
        optimizer.zero_grad()
        loss.backward()

        # Update the model weights
        optimizer.step()

    # Evaluate model accuracy after the Epoch
    net.model.eval() # Set model to evaluation mode
    y_pred = net.model(X_test)
    loss_fn = nn.BCELoss()
    loss = loss_fn(y_pred, y_test.unsqueeze(1))
    loss = float(loss)
    log.write(f'\n{epoch},{loss:.4f}')

    # Check if best accuracy
    if (loss < best_loss):
        best_loss = loss
        best_weights = copy.deepcopy(net.model.state_dict())

# Get the training end date
end_date = datetime.utcnow()

# After training, restore model to best performance and save those checkpoints
net.model.load_state_dict(best_weights)
net.save_model(f"{sdir}/checkpoint_{datetime.utcnow().strftime('%Y-%m-%d_%H%M')}.pt")

# Get error statistics (true positive, etc.)
y_pred = np.squeeze(net.model(X_test).detach().numpy())
y_pred[y_pred >= 0.5] = 1
y_pred[y_pred < 0.5] = 0
y_pred = np.array(y_pred, dtype='bool')
y_test = np.array(np.squeeze(y_test.detach().numpy()), dtype='bool')

tp = np.sum(y_pred & y_test)
tn = np.sum((~y_pred) & (~y_test))
fp = np.sum(y_pred & (~y_test))
fn = np.sum((~y_pred) & y_test)

pod = tp/(tp+fn)*100.0
far = fp/(fp+tn)*100.0
prec = tp/(tp+fp)
recall = tp/(tp+fn)
f1 = (2*prec*recall)/(prec+recall)*100.0

# Print to log
log.write(f'\nTraining ended at {end_date.strftime("%Y-%m-%d_%H%M")}')
log.write(f'\nTotal training time: {(end_date-start_date).total_seconds()} s')
log.write(f'\nBest training loss: {best_loss:.4f}')
log.write(f'\nTrue Positives = {tp}')
log.write(f'\nTrue Negatives = {tn}')
log.write(f'\nFalse Positives = {fp}')
log.write(f'\nFalse Negatives = {fn}')
log.write(f'\nAccuracy = {(tp+tn)/(tp+tn+fp+fn)*100.0:.2f}%')
log.write(f'\nPoD = {pod:.2f}%')
log.write(f'\nFAR = {far:.2f}%')
log.write(f'\nF1 = {f1:.2f}%')
log.close()