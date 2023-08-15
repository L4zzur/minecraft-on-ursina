# Необходимые импорты
from ursina import *
from perlin_noise import PerlinNoise

# импортируем объект игрока
from ursina.prefabs.first_person_controller import FirstPersonController

# Инициализация окна игры
app = Ursina()


# Убираем кнопку закрытия окна
window.exit_button.visible = False

# Создаем глобальную переменную block_pick, которая хранит номер выбранного блока
block_pick = 1


# Определяем функцию input с одним параметром key
def input(key):
    # Объявляем, что мы будем использовать глобальную переменную block_pick внутри функции
    global block_pick
    # Проверяем, равна ли переменная key строке "q" или "escape"
    if key == "q" or key == "escape":
        # Если да, то вызываем функцию quit, которая завершает работу приложения Ursina
        quit()

    # Трава
    if key == "1":
        block_pick = 1
    # Земля
    if key == "2":
        block_pick = 2
    # Камень
    if key == "3":
        block_pick = 3
    # Кирпичи
    if key == "4":
        block_pick = 4
    # Доски
    if key == "5":
        block_pick = 5


# Загружаем текстуру для руки
arm_texture = load_texture("textures/arm.png")

# Создаем сущность в виде руки и присваиваем ее переменной hand
hand = Entity(
    # Указываем камеру, чтобы рука всегда была видна на экране
    parent=camera.ui,
    # Указываем модель
    model="models/arm",
    # Указываем текстуру
    texture=arm_texture,
    # Указываем масштаб сущности как 0.2, чтобы рука не была слишком большой или маленькой
    scale=0.2,
    # Указываем поворот, чтобы рука имела правильную ориентацию
    rotation=Vec3(150, -10, 0),
    # Указываем позицию, чтобы рука была в нижнем правом углу
    position=Vec2(0.6, -0.6),
)


# Загружаем текстуру
sky_texture = load_texture("textures/sky.png")

# Создаем сущность в виде неба и присваиваем ее переменной sky
sky = Entity(
    # Указываем модель сферы
    model="sphere",
    # Указываем текстуру
    texture=sky_texture,
    # Указываем масштаб, чтобы небо было достаточно большим
    scale=1000,
    # Указываем, чтобы текстура неба была видна с обеих сторон сферы
    double_sided=True,
)


# Загружаем текстуру для травы
grass_texture = load_texture("textures/grass.png")
# Загружаем текстуры для остальных блоков
stone_texture = load_texture("textures/stone.png")
brick_texture = load_texture("textures/brick.png")
dirt_texture = load_texture("textures/dirt.png")
wood_texture = load_texture("textures/wood.png")

# Загружаем звук
punch_sound = Audio("sounds/punch.wav", loop=False, autoplay=False)


# Создаем класс Voxel, специальный класс для создания интерактивных объектов
class Voxel(Button):
    # Определяем конструктор
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            # Указываем сцену, чтобы объект был виден в игре
            parent=scene,
            # Указываем модель объекта
            model="models/block",
            # Указываем масштаб объекта
            scale=0.5,
            # Указываем текстуру объекта
            texture=texture,
            # Указываем позицию объекта
            position=position,
            # Указываем точку опоры объекта
            origin_y=0.5,
            # Указываем цвет объекта как случайный оттенок зеленого
            color=color.color(0, 0, random.uniform(0.9, 1)),
        )

    # Определяем метод input класса, который принимает один параметр: key
    def input(self, key):
        # Проверяем, наведен ли курсор мыши на объект
        if self.hovered:
            # Проверяем, нажата ли правая кнопка мыши
            if key == "right mouse down":
                # Воспроизводим звук
                punch_sound.play()
                # Создаем объект Voxel с нужной текстурой и позицией
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

            # Проверяем, нажата ли левая кнопка мыши
            if key == "left mouse down":
                # Воспроизводим звук
                punch_sound.play()
                # Уничтожаем текущий объект
                destroy(self)


# Создаем объект noise, который представляет собой шум Перлина
# Указываем параметры шума, такие как количество октав (octaves) - уровней детализации шума, и зерно (seed) - начальное значение для генерации
noise = PerlinNoise(octaves=2, seed=2023)
# Создаем переменную am которая определяет амплитуду шума - максимальное отклонение от среднего значения
amp = 6
# Создаем переменную, которая определяет частоту шума - количество повторений шума на единицу длины
freq = 24
# Указываем ширину и длину
terrain_width = 30

# Создаем двумерный список landscale, который будет хранить высоты блоков по координатам x и z
# Инициализируем список нулевыми значениями размером terrain_width на terrain_width
landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

# Создаем цикл for, который перебирает все позиции блоков
for position in range(terrain_width**2):
    # Вычисляем координату x
    x = floor(position / terrain_width)
    # Вычисляем координату z
    z = floor(position % terrain_width)
    # Вычисляем координату y
    # Для получения значения шума Перлина используем noise
    y = floor(noise([x / freq, z / freq]) * amp)

    # Присваиваем значение y в списке landscale по индексам x и z
    landscale[int(x)][int(z)] = int(y)


# Создаем двойной цикл for, который перебирает все координаты x и z
for x in range(terrain_width):
    for z in range(terrain_width):
        # Создаем объект block класса Voxel, который представляет собой интерактивный блок в игре
        # Указываем параметры блока, такие как позицию по трем осям (x, y и z), используя значение y из списка landscale по индексам x и z
        block = Voxel(position=(x, landscale[x][z], z))


# Создаем объект player, который представляет собой контроллер от первого лица (FirstPersonController) - специальный класс для управления персонажем в 3D-играх
player = FirstPersonController()


# Запускаем проект
app.run()
