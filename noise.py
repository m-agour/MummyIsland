import numpy as np
from PIL import Image

SHAPE = (256, 256)

noise = np.random.normal(255./2,255./10,SHAPE)
image = Image.fromarray(noise)
image = image.convert('RGB')
image.save("gaussian_noise.png")