from ursina import *
from perlin_noise import PerlinNoise
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
window.exit_button.visible = False
block_pick = 1


def input(key):
    global block_pick
    if key == "q" or key == "escape":
        quit()
    if key == "1":
        block_pick = 1
    if key == "2":
        block_pick = 2
    if key == "3":
        block_pick = 3
    if key == "4":
        block_pick = 4
    if key == "5":
        block_pick = 5


arm_texture = load_texture("textures/arm.png")
hand = Entity(
    parent=camera.ui,
    model="models/arm",
    texture=arm_texture,
    scale=0.2,
    rotation=Vec3(150, -10, 0),
    position=Vec2(0.6, -0.6),
)

sky_texture = load_texture("textures/sky.png")
sky = Entity(
    model="sphere",
    texture=sky_texture,
    scale=1000,
    double_sided=True,
)

grass_texture = load_texture("textures/grass.png")
stone_texture = load_texture("textures/stone.png")
brick_texture = load_texture("textures/brick.png")
dirt_texture = load_texture("textures/dirt.png")
wood_texture = load_texture("textures/wood.png")

punch_sound = Audio("sounds/punch.wav", loop=False, autoplay=False)


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            model="models/block",
            scale=0.5,
            texture=texture,
            position=position,
            origin_y=0.5,
            color=color.color(0, 0, random.uniform(0.9, 1)),
        )

    def input(self, key):
        if self.hovered:
            if key == "right mouse down":
                punch_sound.play()
                if block_pick == 1:
                    Voxel(position=self.position + mouse.normal, texture=grass_texture)
                if block_pick == 2:
                    Voxel(position=self.position + mouse.normal, texture=dirt_texture)
                if block_pick == 3:
                    Voxel(position=self.position + mouse.normal, texture=stone_texture)
                if block_pick == 4:
                    Voxel(position=self.position + mouse.normal, texture=brick_texture)
                if block_pick == 5:
                    Voxel(position=self.position + mouse.normal, texture=wood_texture)

            if key == "left mouse down":
                punch_sound.play()
                destroy(self)


noise = PerlinNoise(octaves=2, seed=2023)
amp = 6
freq = 24
terrain_width = 30
landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

for position in range(terrain_width**2):
    x = floor(position / terrain_width)
    z = floor(position % terrain_width)
    y = floor(noise([x / freq, z / freq]) * amp)
    landscale[int(x)][int(z)] = int(y)

for x in range(terrain_width):
    for z in range(terrain_width):
        block = Voxel(position=(x, landscale[x][z], z))

player = FirstPersonController()
app.run()
