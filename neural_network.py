# -*- coding: utf-8 -*-
"""neural network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h5r3LrqhDojdqDQzAHRhkNJbf7a6KXX-
"""

import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch as t

class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    self.conv1 = nn.Conv2d(1, 6, 5) #1为输入通道，6为输出通道，5为卷积核大小
    self.conv2 = nn.Conv2d(6, 16, 5)
    self.fc1 = nn.Linear(16*5*5, 120)
    self.fc2 = nn.Linear(120, 84)
    self.fc3 = nn.Linear(84, 10)
    
  def forward(self, x):
    x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
    x = F.max_pool2d(F.relu(self.conv2(x)), 2)
    x = x.view(x.size()[0], -1)
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = self.fc3(x)
    return x

net = Net()
print(net)

# net.parameters()函数可求得网络的所有学习函数
params = list(net.parameters())
print(len(params))
for name,parameters in net.named_parameters():
  print(name, ':',parameters.size())

#forward函数的输入输出都是Variable，只有Variable才有自动求导功能，所以在输入时需要将Tensor封装成Variable
input = Variable(t.randn(1, 1, 32, 32))
out = net(input)
out.size()

#清零梯度
net.zero_grad()
out.backward(Variable(t.ones(1,10)))

#损失函数
output = net(input)
target = Variable(t.arange(0, 10))
criterion = nn.MSELoss()
loss = criterion(output, target)
loss

net.zero_grad()
print('反向传播之前清零梯度')
print(net.conv1.bias.grad)
print('反向传播之后的梯度')
print(net.conv1.bias.grad)

#实现优化
# weight = weight - learning_rate * gradient
#手动实现
#learning_rate = 0.01
#for f in net.parameters():
#  f.data.sub_(f.grad.data * learning_rate)
#torch.optim封装了很多优化算法
import torch.optim as optim
optimizer = optim.SGD(net.parameters(), lr=0.01)
#梯度清零
optimizer.zero_grad()
output = net(input)
loss = criterion(output, target)

loss.backward()
optimizer.step()