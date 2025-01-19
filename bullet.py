import pygame
import spritesheet

class BulletSprite(pygame.sprite.Sprite):

    images = {}
    group = pygame.sprite.Group()

    @staticmethod
    def load():
        sheet = spritesheet.spritesheet("assets/bullets.png", "assets/bullets.json")
        BulletSprite.images = sheet.image_names(["red-1"], scale2x=True)

    def __init__(self, image_name, start_x, start_y):
        super().__init__()

        self.image = BulletSprite.images[image_name]
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        self.add(BulletSprite.group)

    def update(self, dt):
        self.rect.y -= 10
        if self.rect.y < 0:
            self.kill()
