# Импортируем модуль ursina, который содержит все необходимые классы и функции для работы с игровым движком
from ursina import *

# Создаем объект app, который представляет собой приложение Ursina
app = Ursina()

# Создаем объект cube, который представляет собой сущность (Entity) - основной класс для создания игровых объектов
# Указываем параметры сущности, такие как модель (model), текстура (texture), цвет (color), размер (scale)
cube = Entity(
    model="cube",
    texture="white_cube",
    color=color.red,
    scale=2,
)


# Создаем функцию spin, которая будет вызываться при клике на куб
def spin():
    # Анимируем поворот куба по оси Y на 360 градусов за 2 секунды с помощью метода animate
    cube.animate(
        "rotation_y",
        cube.rotation_y + 360,
        duration=2,
        curve=curve.in_out_expo,
    )


# Привязываем функцию spin к событию on_click куба с помощью оператора присваивания
cube.on_click = spin

# Создаем объект camera, который представляет собой камеру редактора (EditorCamera) - специальный класс для управления камерой в режиме разработки
camera = EditorCamera()

# Запускаем приложение Ursina с помощью метода run объекта app
app.run()