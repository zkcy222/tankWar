import pygame


class Gamer(pygame.sprite.Sprite):
    """玩家坦克精灵"""

    def __init__(self, map):
        super().__init__()
        self.image = pygame.image.load("pic/gamer.png")
        self.rect = self.image.get_rect().move(160,480)
        self.speed = 0
        self._mapSize = self._mapWidth, self._mapHeight = map
        self._direction = 0  # 0123 上左下右
        self._life = 5
        self._lastRect = self.rect

    # 更新玩家坦克速度
    def setSpeed(self, s):
        self.speed = s

    # 更新玩家坦克速度方向
    def setInfo(self, s, dir):
        re = self.rect
        self.image = pygame.transform.rotate(self.image, 90 * (dir - self._direction))
        self.rect = re
        self._direction = dir
        self.speed = s

    # 获取坦克方向
    def getDir(self):
        return self._direction

    # 获取坦克rect
    def getRect(self):
        return self.rect

    # 获取坦克生命
    def getLife(self):
        return self._life

    # 中弹生命-1
    def gotShot(self):
        self._life -= 1

    def update(self):
        step = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        newRect = self.rect.move(self.speed * step[self._direction][0], self.speed * step[self._direction][1])
        if newRect.top >= 0 and newRect.left >= 0 and newRect.bottom <= self._mapHeight and newRect.right <= self._mapWidth:
            self._lastRect = self.rect
            self.rect = newRect

    def backOff(self):
        # step = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        # newRect = self.rect.move(self.speed * step[self._direction][0], self.speed * step[self._direction][1])
        # self.rect = newRect
        self.rect = self._lastRect
