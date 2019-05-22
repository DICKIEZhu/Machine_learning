# -*- coding: utf-8 -*-
"""RNN_MNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RIhUcN6emHLht23QTHemSuH3EPBnzp6A
"""

import torch 
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper-parameters
sequence_length = 28
input_size = 28
hidden_size = 128
num_layers = 2
num_classes = 10
num_direction = 1 # set to 2 if bidirectional == True; set to 1 if bidirectional == False
batch_size = 200
num_epochs = 2
learning_rate = 0.01/10

# select RNN structure (RNN/LSTM/GRU)
rnn_structure_list = ['RNN','LSTM','GRU']
rnn_structure = rnn_structure_list[1]

# MNIST dataset
train_dataset = torchvision.datasets.MNIST(root='../../data/',
                                           train=True,                                            
                                            transform=transforms.Compose(
                                                [transforms.ToTensor(),
                                                 transforms.Normalize((0.1307, ), (0.3081, ))]),
                                           download=True)

test_dataset = torchvision.datasets.MNIST(root='../../data/',
                                          train=False,                                           
                                          transform=transforms.Compose(
                                              [transforms.ToTensor(),
                                              transforms.Normalize((0.1307, ), (0.3081, ))]))

# Data loader
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size, 
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size, 
                                          shuffle=False)

# Recurrent neural network (many-to-one)
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        if rnn_structure == 'RNN':
            self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True , dropout=0.5, bidirectional=False) 
        elif rnn_structure == 'LSTM':
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.5, bidirectional=False)
        elif rnn_structure == 'GRU':
            self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True , dropout=0.5, bidirectional=False)       

        self.fc = nn.Linear(hidden_size*num_direction, num_classes)
    
    def forward(self, x):
        # Set initial hidden and cell states 
        h0 = torch.zeros(self.num_layers*num_direction, x.size(0), self.hidden_size).to(device) 
        c0 = torch.zeros(self.num_layers*num_direction, x.size(0), self.hidden_size).to(device)
        
        # Forward propagate RNN/LSTM/GRU
        if rnn_structure == 'RNN':
            out, _ = self.rnn(x, h0)
        elif rnn_structure == 'LSTM':
            out, _ = self.lstm(x, (h0, c0))  # out: tensor of shape (batch_size, seq_length, hidden_size)
        elif rnn_structure == 'GRU':
            out, _ = self.gru(x, h0)  # out: tensor of shape (batch_size, seq_length, hidden_size)
        
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out

# Train the model
def train(model,device,train_loader,criterion,optimizer,num_epochs):

    Loss_list = []
    Loss_i = 0;

    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            images = images.reshape(-1, sequence_length, input_size).to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i+1) % 100 == 0:
                print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                       .format(epoch+1, num_epochs, i+1, total_step, loss.item()))
                Loss_list.append(loss.item())
                Loss_i = Loss_i+1

    x = range(Loss_i)
    plt.plot(x, Loss_list, '.-')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    np.save('loss_of_'+ rnn_structure,Loss_list)

# Test the model
def test(model,device,test_loader,criterion):
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.reshape(-1, sequence_length, input_size).to(device)
            labels = labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        print('Test Accuracy of the model on the 10000 test images: {} %'.format(100 * correct / total)) 
        print('Loss: ', loss.item())

# Create instance of the recurrent network
model = RNN(input_size, hidden_size, num_layers, num_classes).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train and test 
train(model,device,train_loader,criterion,optimizer,num_epochs);
test(model,device,test_loader,criterion);

# Save and download the model checkpoint
torch.save(model.state_dict(), 'model.ckpt')
files.download( 'loss_of_'+ rnn_structure+'.npy' ) 
files.download( "model.ckpt" )