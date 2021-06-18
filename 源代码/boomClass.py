import pygame


class Boom(pygame.sprite.Sprite):
    """boom精灵"""

    def __init__(self, rel, ret):
        super().__init__()
        self.image = pygame.image.load("pic/boom.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(rel-20, ret-20)
        self.time = 0

    def update(self):
        self.time += 1
        if self.time > 5:
            self.kill()
