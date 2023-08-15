# Генерация «красивого» шума Перлина

from numpy import floor
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt

noise = PerlinNoise(octaves=2, seed=2023)
amp = 6
freq = 24
terrain_width = 64

landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

for position in range(terrain_width**2):
    x = floor(position / terrain_width)
    z = floor(position % terrain_width)
    y = floor(noise([x / freq, z / freq]) * amp)

    landscale[int(x)][int(z)] = int(y)

plt.imshow(landscale)
plt.show()
