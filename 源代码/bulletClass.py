import pygame
import globals

class Bullet(pygame.sprite.Sprite):
    """子弹精灵"""

    def __init__(self, map, dir, re):
        super().__init__()
        self.image = pygame.image.load("pic/bullet.png")
        self.image = pygame.transform.rotate(self.image, 90 * dir)
        self._direction = dir  # 0123 上左下右
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(re.left + 17, re.top + 14)
        self.speed = globals.bulletSpeed
        self._mapSize = self._mapWidth, self._mapHeight = map
        self._life = 5
        step = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        self.rect = self.rect.move(30 * step[self._direction][0], 30 * step[self._direction][1])

    def update(self):
        step = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        newRect = self.rect.move(self.speed * step[self._direction][0], self.speed * step[self._direction][1])
        self.rect = newRect
