# -*- coding: utf-8 -*-
import torchvision.models as models
import torch
import numpy as np
import cv2


# net = models.resnext101_32x8d(pretrained=True)
net = models.densenet201(pretrained=True)

img1 = cv2.imread('./4.png')
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img1 = cv2.resize(img1, (224, 224))
img1 = np.transpose(img1, (2, 0, 1))
img1 = np.expand_dims(img1, axis=0)
img1 = torch.from_numpy(img1).float()
outputs = net(img1)
x = outputs.data.numpy()

img2 = cv2.imread('./sri_lanka-5-cents-1991.jpg')
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img2 = cv2.resize(img2, (224, 224))
img2 = np.transpose(img2, (2, 0, 1))
img2 = np.expand_dims(img2, axis=0)
img2 = torch.from_numpy(img2).float()
outputs = net(img2)
y = outputs.data.numpy()

dist = np.dot(x, y.transpose())/(np.linalg.norm(x) * np.linalg.norm(y))
print(dist)

# img = cv2.imread('./3.png')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img = cv2.resize(img, (224, 224))
# img = img / 255.0
# batch_x = np.reshape(img, (-1, img.shape[0], img.shape[1], img.shape[2]))
# pred = model.predict(batch_x)[0]
# pred_label = np.argmax(pred)


