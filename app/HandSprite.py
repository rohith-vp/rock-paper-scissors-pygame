import pygame


class HandSprite(pygame.sprite.Sprite):
    """A sprite class for the rock, paper, scissors hands."""
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.type = None  # 0: rock, 1: paper, 2: scissors

