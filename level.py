import pygame

from settings import HEIGHT, WIDTH

from islands import Island

from levels.level1 import islands as level1_islands
from levels.level2 import islands as level2_islands
from levels.level3 import islands as level3_islands
from levels.level4 import islands as level4_islands
from levels.level5 import islands as level5_islands

from cat import Cat
from obstacles import Obstacle
from obstacles_data import OBSTACLES


class Level:

    def __init__(self, level_number=1):

        # ==========================================
        # ОСНОВНЫЕ ДАННЫЕ
        # ==========================================

        self.width = WIDTH
        self.height = HEIGHT

        # Номер текущего уровня
        self.level_number = level_number

        # Списки объектов текущего уровня
        self.islands = []
        self.cats = []
        self.obstacles = []

        # Локации котов
        self.catlocations = set()

        # ==========================================
        # ОСТРОВА
        # ==========================================

        LEVEL_ISLANDS = {
            1: level1_islands,
            2: level2_islands,
            3: level3_islands,
            4: level4_islands,
            5: level5_islands
        }

        # Проверяем, существует ли такой уровень
        if level_number not in LEVEL_ISLANDS:
            raise ValueError(
                f"Уровень {level_number} не существует"
            )

        # Получаем острова текущего уровня
        current_islands = LEVEL_ISLANDS[level_number]

        # ==========================================
        # СОЗДАЁМ ОСТРОВА
        # ==========================================

        for island_data in current_islands:

            island = Island(
                island_data["type"],
                island_data["image"],
                island_data["x"],
                island_data["y"],
                island_data["width"],
                island_data["height"]
            )

            self.islands.append(island)

        # ==========================================
        # СОЗДАЁМ КОТОВ
        # ==========================================

        for island in self.islands:

            cats = Cat.create_cat(
                level_number,
                island.type
            )

            self.cats.extend(cats)

        # ==========================================
        # СОЗДАЁМ ПРЕПЯТСТВИЯ
        # ==========================================

        if level_number in OBSTACLES:

            for obstacle_data in OBSTACLES[level_number]:

                obstacle = Obstacle(
                    obstacle_data["image"],
                    obstacle_data["x"],
                    obstacle_data["y"],
                    obstacle_data["width"],
                    obstacle_data["height"]
                )

                self.obstacles.append(obstacle)

        # ==========================================
        # ФЛАГ ФИНИША
        # ==========================================

        self.finish_flag = pygame.image.load(
            "assets/finishflag.png"
        ).convert_alpha()

        self.finish_flag = pygame.transform.scale(
            self.finish_flag,
            (100, 100)
        )

        self.finish_flag_rect = self.finish_flag.get_rect(
            center=(400, 300)
        )

    # ==========================================
    # ГРАНИЦЫ КАРТЫ
    # ==========================================

    def check_boundaries(self, boat):

        if boat.rect.left < 0:
            boat.rect.left = 0

        if boat.rect.right > self.width:
            boat.rect.right = self.width

        if boat.rect.top < 0:
            boat.rect.top = 0

        if boat.rect.bottom > self.height:
            boat.rect.bottom = self.height

        # Синхронизируем координаты
        boat.x = boat.rect.x
        boat.y = boat.rect.y

    # ==========================================
    # ОТРИСОВКА
    # ==========================================

    def draw(self, screen):

        # Острова
        for island in self.islands:
            island.draw(screen)

        # Препятствия
        for obstacle in self.obstacles:
            obstacle.draw(screen)

        # Коты текущего уровня
        for cat in self.cats:
            cat.draw(screen)

        # Флаг
        screen.blit(
            self.finish_flag,
            self.finish_flag_rect
        )

    # ==========================================
    # СТОЛКНОВЕНИЕ С ОСТРОВАМИ
    # ==========================================

    def check_collision(self, boat):

        for island in self.islands:

            if boat.rect.colliderect(island.rect):

                offset_x = (
                    island.rect.x -
                    boat.rect.x
                )

                offset_y = (
                    island.rect.y -
                    boat.rect.y
                )

                offset = (
                    offset_x,
                    offset_y
                )

                if boat.mask.overlap(
                    island.mask,
                    offset
                ):
                    return True

        return False

    # ==========================================
    # ПОИСК БЛИЖАЙШЕГО КОТА
    # ==========================================

    def get_nearby_cat(self, boat):

        for cat in self.cats:

            # Если кот уже спасён,
            # его нельзя выбрать снова
            if cat.is_taken:
                continue

            if boat.rect.colliderect(
                cat.rect.inflate(80, 80)
            ):
                return cat

        return None

    # ==========================================
    # СТОЛКНОВЕНИЕ С ПРЕПЯТСТВИЯМИ
    # ==========================================

    def check_obstacle_collision(self, boat):

        for obstacle in self.obstacles:

            if boat.rect.colliderect(
                obstacle.rect
            ):
                return True

        return False

    # ==========================================
    # ЗАБРАТЬ КОТА
    # ==========================================

    def take_cat(self, cat, boat):

        # Пытаемся добавить кота на лодку
        if boat.add_cat(cat):

            # Кот теперь спасён
            cat.take()

            # Запоминаем его локацию
            self.catlocations.add(
                cat._location
            )

            return True

        return False

    # ==========================================
    # ПРОВЕРКА ФИНИША
    # ==========================================

    def finishlev(self, boat):

        return boat.rect.colliderect(
            self.finish_flag_rect
        )

    # ==========================================
    # ПРОВЕРКА ЗАДАНИЯ
    # ==========================================
    #
    # ВАЖНО:
    #
    # Здесь мы НЕ проверяем self.cats.
    #
    # self.cats = коты ТЕКУЩЕГО уровня.
    #
    # Нам нужно проверить ВСЕХ котов,
    # которые находятся на лодке.
    #
    # Поэтому используем:
    #
    # boat.current_cats
    #
    # ==========================================

    def check_mission(self, boat):

        # На лодке должно быть минимум 2 кота
        if len(boat.current_cats) < 2:
            return False

        # Проверяем каждого кота на лодке
        for cat in boat.current_cats:

            # Если хотя бы у одного кота
            # рейтинг меньше 4.5,
            # уровень провален
            if cat._rating < 4.5:
                return False

        # Если мы дошли сюда,
        # значит все коты подходят
        return True
