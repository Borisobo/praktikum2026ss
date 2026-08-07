BOAT_LEVELS = {
    1: {
        "max_cats": 2,
        "speed": 3.0,
        "upgrade_cost": 10
    },
    2: {
        "max_cats": 4,
        "speed": 3.5,
        "upgrade_cost": 20
    },
    3: {
        "max_cats": 6,
        "speed": 4.0,
        "upgrade_cost": 35
    },
    4: {
        "max_cats": 8,
        "speed": 4.5,
        "upgrade_cost": 50
    },
    5: {
        "max_cats": 10,
        "speed": 5.0,
        "upgrade_cost": None
    }
}


class Boat :
  def __init__ (self) :
    self.level = 1
    self.current_cats = []

    self.load_level()

  def load_level(self):
    stats = BOAT_LEVELS[self.level]

    self.max_cats = stats["max_cats"]
    self.speed = stats["speed"]
    self.upgrade_cost = stats["upgrade_cost"]

  def upgrade(self):
    if self.level < 5:
        self.level += 1
        self.load_level()

  def has_free_space(self):
    return len(self.current_cats) < self.max_cats

  def add_cat(self, cat):
    if self.has_free_space():
        self.current_cats.append(cat)
        return True
    return False

  def remove_cat(self, cat):
    if cat in self.current_cats:
        self.current_cats.remove(cat)
    
