# -*- coding: utf-8 -*-
import torchvision.models as models
import torch
import numpy as np
from PIL import Image
import pandas as pd
import argparse
import torch.backends.cudnn as cudnn
from torch.optim import Adam, SGD
import torch.nn as nn
from torchvision import transforms
import matplotlib.pyplot as plt


def get_batch_data(image_list, batch_size):
    batch_x = []
    batch_y = []
    while len(batch_x) < batch_size:
        index = np.random.randint(args.num_classes)
        label = index

        image = Image.open('./standard_img/%s' % image_list[index]).convert('RGB')
        image = image.resize((128, 128), Image.ANTIALIAS)

        compose = [transforms.RandomAffine(180, shear=5, resample=Image.BILINEAR),
                   transforms.ColorJitter(brightness=0.6, contrast=0.6, saturation=0.6)
                   ]

        compose = transforms.Compose([transforms.RandomOrder(compose),
                                      transforms.ToTensor(),
                                      # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
                                      ])
        image = compose(image)

        batch_x.append(image.numpy())
        batch_y.append(label)

    batch_x = torch.Tensor(batch_x)
    batch_y = torch.Tensor(batch_y)
    return batch_x, batch_y


# 超参
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--EPOCHS", default=100, type=int, help="train epochs")
parser.add_argument("-b", "--BATCH", default=10, type=int, help="batch size")
parser.add_argument("-n", "--num_classes", default=200, type=int, help="amount of classes")
args = parser.parse_args()

# 判断gpu是否可用
if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'
device = torch.device(device)

net = models.resnet50(pretrained=True)
# net = models.resnet34(pretrained=True)

# 全连接层的输入通道in_channels个数
num_fc_in = net.fc.in_features

# 改变全连接层
net.fc = nn.Linear(num_fc_in, args.num_classes)
net = net.to(device)

if device == 'cuda':
    net = torch.nn.DataParallel(net)
    cudnn.benchmark = True

optimizer = Adam(net.parameters(), lr=0.0001, weight_decay=0.0001)
loss_fn = nn.CrossEntropyLoss()  # 定义损失函数

df = pd.read_csv('./coins.csv')
image_list = [x for x in df['similar_coin']]

plt.ion()
avg_losses = []
batch_steps = args.num_classes // args.BATCH
for epoch in range(args.EPOCHS):
    print('\nEpoch: %d' % (epoch + 1))
    net.train()
    train_loss = 0
    correct = 0
    total = 0
    for i in range(batch_steps):
        now_step = epoch * batch_steps + i

        batch_x, batch_y = get_batch_data(image_list, args.BATCH)

        # 观察训练集
        # tmp = batch_x.numpy()
        # tmp = tmp[0]
        # tmp = np.transpose(tmp, (2, 1, 0))
        # tmp = np.transpose(tmp, (1, 0, 2))
        # plt.imshow(tmp)
        # plt.show()

        batch_x, batch_y = batch_x.to(device), batch_y.to(device)

        output = net(batch_x)
        _, prediction = output.max(1)
        loss = loss_fn(output, batch_y.long())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        total += batch_y.size(0)
        correct += prediction.eq(batch_y).sum().item()

        # 打出来一些数据
        if i % 5 == 0:
            print('Step: %d | Total: %d' % (i, batch_steps))
            print('Loss: %.3f | Accuracy: %.3f%% (%d/%d)' % (train_loss / (i+1), 100.*correct/total, correct, total))
            print('-' * 30)
            avg_losses.append(train_loss / (i + 1))
            x1 = range(0, len(avg_losses))
            y1 = avg_losses
            plt.figure(1)
            plt.plot(x1, y1, color='brown', linestyle='-')
            # for text_x, text_y in zip(x1, y1):  # epoch多了之后会挤成一团，实际用的时候可以不显示
            #     plt.text(text_x, text_y, '%.4f' % text_y, ha='center', va='bottom', fontsize=7)
            plt.xlabel('epoch')
            plt.ylabel('average loss')
            plt.draw()
            plt.pause(0.05)
    torch.save(net.state_dict(), './net.pth')
plt.ioff()
plt.show()
