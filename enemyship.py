import pygame
import math

import spritesheet
import bullet
import explosion

class ShipSprite(pygame.sprite.Sprite):

    images = {}
    group = pygame.sprite.Group()

    @staticmethod
    def load():
        sheet = spritesheet.spritesheet("ships.png", "ships.json")
        ShipSprite.images = sheet.image_names(["tri"], scale2x=True)

    def __init__(self, image_name, start_x, start_y):
        super().__init__()

        self.image = ShipSprite.images[image_name]
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        self.update_dt = 0
        self.update_x = 5

        self.add(ShipSprite.group)

    def update(self, dt):
        hit_list = pygame.sprite.spritecollide(self, bullet.BulletSprite.group, True)
        if len(hit_list) > 0:
            self.kill()
            explosion.ExplosionSprite(
                "bigred", self.rect.x + self.rect.w/2, self.rect.y + self.rect.h/2)

        self.update_dt = max(self.update_dt - dt, 0)

        if self.update_dt == 0:
            self.update_dt = 30

            self.rect.x += self.update_x

            if self.rect.x > (pygame.display.get_surface().get_width() - self.rect.width) or self.rect.x < 0:
                self.update_x = -self.update_x
            