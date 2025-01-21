import pygame

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

        self.add(ShipSprite.group)

    def update(self, dt):
        hit_list = pygame.sprite.spritecollide(self, bullet.BulletSprite.group, True)
        if len(hit_list) > 0:
            self.kill()
            explosion.ExplosionSprite(
                "bigred", self.rect.x + self.rect.w/2, self.rect.y + self.rect.h/2)
