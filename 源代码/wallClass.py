import pygame


class WhiteWall(pygame.sprite.Sprite):
    """白墙精灵"""
    def __init__(self, rel,ret):
        super().__init__()
        self.image = pygame.image.load("pic/whiteWall.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(rel,ret)



class RedWall(pygame.sprite.Sprite):
    """红墙精灵"""
    def __init__(self, rel, ret):
        super().__init__()
        self.image = pygame.image.load("pic/redWall.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(rel,ret)

    def getRect(self):
        return self.rect

