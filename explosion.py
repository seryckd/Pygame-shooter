import pygame

import spritesheet

class ExplosionSprite(pygame.sprite.Sprite):

    sheet = None
    group = pygame.sprite.Group()

    @staticmethod
    def load():
        ExplosionSprite.sheet = spritesheet.spritesheet("explosions.png", "explosions.json")

    def __init__(self, name, start_x, start_y):
        """
            animation sequence name
            start point
            animation speed
        """
        super().__init__()

        self.images = ExplosionSprite.sheet.image_sequence(name, scale2x=True)

        self.image_idx = 1
        self.image_dt = 0
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.x = start_x - self.rect.w/2
        self.rect.y = start_y - self.rect.h/2


        self.add(ExplosionSprite.group)

    def update(self, dt):
        
        self.image_dt = max(self.image_dt - dt, 0)

        if self.image_dt == 0:
            self.image_idx += 1
            self.image_dt = 25

            if self.image_idx < len(self.images):
                self.image = self.images[self.image_idx]
            else:
                self.kill()
