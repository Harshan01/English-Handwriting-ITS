import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms


class CharRecogModel(nn.Module):

    def __init__(self, out_feats=26):
        super().__init__()
        # Input dimension is (B, 1, 28, 28)
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.fc1 = nn.Linear(9216, 256)
        self.dropout2 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, out_feats)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = x
        return output

    @staticmethod
    def get_trans_transform():
        transform = transforms.Compose([
            lambda img: transforms.functional.rotate(img, -90),
            lambda img: transforms.functional.hflip(img),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        return transform

    @staticmethod
    def get_transform():
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        return transform
