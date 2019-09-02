import numpy as np

import torch
import torch.nn as nn
from PIL import Image

# Constants
cats_weights   = 'generatorcats.pt'
humans_weights = 'generatorhumans.pt'
dogs_weights   = 'generatordogs.pt'


class Generator(nn.Module):
    def __init__(self, nz=128, channels=3):
        super(Generator, self).__init__()

        self.nz = nz
        self.channels = channels

        def convlayer(n_input, n_output, k_size=4, stride=2, padding=0):
            block = [
                nn.ConvTranspose2d(n_input, n_output, kernel_size=k_size, stride=stride, padding=padding, bias=False),
                nn.BatchNorm2d(n_output),
                nn.ReLU(inplace=True),
            ]
            return block

        self.model = nn.Sequential(
            *convlayer(self.nz, 1024, 4, 1, 0),  # Fully connected layer via convolution.
            *convlayer(1024, 512, 4, 2, 1),
            *convlayer(512, 256, 4, 2, 1),
            *convlayer(256, 128, 4, 2, 1),
            *convlayer(128, 64, 4, 2, 1),
            nn.ConvTranspose2d(64, self.channels, 3, 1, 1),
            nn.Tanh()
        )

    def forward(self, z):
        z = z.view(-1, self.nz, 1, 1)
        img = self.model(z)
        return img

catGan   =  Generator()
humanGan =  Generator()
dogGan   =  Generator()

catGan.load_state_dict(torch.load(cats_weights, map_location='cpu'))
humanGan.load_state_dict(torch.load(humans_weights, map_location='cpu'))
dogGan.load_state_dict(torch.load(dogs_weights, map_location='cpu'))


def predict(model):
    gen_z = torch.randn(1, 128, 1, 1, ).cpu()
    gen_img = (model(gen_z).to("cpu").clone().detach() + 1) / 2
    gen_img = gen_img.data.clamp_(0, 1)
    gen_img = gen_img.numpy().transpose(0, 2, 3, 1)
    gen_img = Image.fromarray((gen_img[0] * 255).astype(np.uint8))
    gen_img = gen_img.resize((128, 128), Image.BILINEAR)
    return gen_img

