import pygame

class Home(pygame.sprite.Sprite):
    """大本营精灵"""
    def __init__(self, rel,ret):
        super().__init__()
        self.image = pygame.image.load("pic/home.jpg")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(rel,ret)

    def getRect(self):
        return self.rect