import pygame

from settings import HEIGHT, WIDTH

from islands import Island

from levels.level1 import islands as level1_islands
from levels.level2 import islands as level2_islands
from levels.level3 import islands as level3_islands
from levels.level4 import islands as level4_islands
from levels.level5 import islands as level5_islands

from levels.level1 import spawn as level1_spawn
from levels.level2 import spawn as level2_spawn
from levels.level3 import spawn as level3_spawn 
from levels.level4 import spawn as level4_spawn
from levels.level5 import spawn as level5_spawn

from cat import Cat
from obstacles import Obstacle
from obstacles_data import OBSTACLES


class Level:

    def __init__(self, level_number=1):

        self.level_spawn = {
                    1: level1_spawn,
                    2: level2_spawn,
                    3: level3_spawn,
                    4: level4_spawn,
                    5: level5_spawn,
                }
        self.width = WIDTH
        self.height = HEIGHT
        self.level_number = level_number
        self.islands = []
        self.cats = []
        self.obstacles = []
        self.catlocations = set()

        self.level_islands = {1: level1_islands, 2: level2_islands, 3: level3_islands, 4: level4_islands, 5: level5_islands}
        if level_number not in self.level_islands:
            raise ValueError(f"Уровень {level_number} не существует")
        current_islands = self.level_islands[level_number]
        for island_data in current_islands:

            island = Island(
                island_data["type"],
                island_data["image"],
                island_data["x"],
                island_data["y"],
                island_data["width"],
                island_data["height"],
            )

            self.islands.append(island)

        for island in self.islands:

            cats = Cat.create_cat(level_number, island.type)

            self.cats.extend(cats)

        if level_number in OBSTACLES:

            for obstacle_data in OBSTACLES[level_number]:

                obstacle = Obstacle(
                    obstacle_data["image"],
                    obstacle_data["x"],
                    obstacle_data["y"],
                    obstacle_data["width"],
                    obstacle_data["height"],
                )

                self.obstacles.append(obstacle)


        self.finish_flag = pygame.image.load("assets/finishflag.png").convert_alpha()

        self.finish_flag = pygame.transform.scale(self.finish_flag, (100, 100))

        self.finish_flag_rect = self.finish_flag.get_rect(center=(400, 300))


    def check_boundaries(self, boat):

        if boat.rect.left < 0:
            boat.rect.left = 0

        if boat.rect.right > self.width:
            boat.rect.right = self.width

        if boat.rect.top < 0:
            boat.rect.top = 0

        if boat.rect.bottom > self.height:
            boat.rect.bottom = self.height
        boat.x = boat.rect.x
        boat.y = boat.rect.y

    def draw(self, screen):

        for island in self.islands:
            island.draw(screen)

        for obstacle in self.obstacles:
            obstacle.draw(screen)

        for cat in self.cats:
            cat.draw(screen)


        screen.blit(self.finish_flag, self.finish_flag_rect)

    def check_collision(self, boat):

        for island in self.islands:

            if boat.rect.colliderect(island.rect):

                offset_x = island.rect.x - boat.rect.x

                offset_y = island.rect.y - boat.rect.y

                offset = (offset_x, offset_y)

                if boat.mask.overlap(island.mask, offset):
                    return True

        return False

    def get_nearby_cat(self, boat):

        for cat in self.cats:

            # Если кот уже спасён,
            # его нельзя выбрать снова
            if cat.is_taken:
                continue

            if boat.rect.colliderect(cat.rect.inflate(80, 80)):
                return cat

        return None


    def check_obstacle_collision(self, boat):
        for obstacle in self.obstacles:
            if boat.rect.colliderect(obstacle.rect):
                if not boat.rect.colliderect(obstacle.rect):
                    continue
            offset_x = obstacle.rect.x - boat.rect.x
            offset_y = obstacle.rect.y - boat.rect.y
            if boat.mask.overlap(obstacle.mask, (offset_x, offset_y)):
                return True
        return False


    def take_cat(self, cat, boat):
        if boat.add_cat(cat):
            cat.take()
            self.catlocations.add(cat._location)

            return True

        return False


    def finishlev(self, boat):

        return boat.rect.colliderect(self.finish_flag_rect)


      def check_mission(self, boat):
        cats = boat.current_cats
        if not cats:
            return False
        if self.level_number == 1:
            return (len(cats) >= 2 and all(cat._rating >= 4.1 for cat in cats))
        if self.level_number == 2:
            if len(cats) < 2:
                return False
            avg_rate = sum(cat._rating for cat in cats) / len(cats)
            lager = any(cat._beruf == "Lagerarbeiterin" for cat in cats)
            elektrik = any(cat._beruf == "Elektriker" for cat in cats)
            return (avg_rate >= 4.2 and lager and elektrik)
        if self.level_number == 3:
            avg_rate = sum(cat._rating for cat in cats) / len(cats)
            handwerker = any(cat._beruf == "Handwerker" for cat in cats)
            konzentration = any("konzentriert" in cat._qualities or "aufmerksam" in cat._qualities for cat in cats)
            return (avg_rate >= 4.3 and handwerker and konzentration)
        if self.level_number == 4:
            avg_rate = sum(cat._rating for cat in cats) / len(cats)
            fitnes = any(cat._beruf == "Trainer" for cat in cats)
            kellner  = any(cat._beruf == "Kellnerin" for cat in cats)
            barista = any(cat._beruf == "Barista" for cat in cats)
            return (avg_rate >= 4.4 and fitnes and kellner and barista)
        if self.level_number == 5:
            avg_rate = sum(cat._rating for cat in cats) / len(cats)
            buergermeister = any(cat._beruf == "Bürgermeister" for cat in cats)
            return (avg_rate >= 4.5 and buergermeister)


