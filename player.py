import pygame

import bullet

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, sheet):
        super().__init__()
    
        self.images = sheet.image_names(["carrot-l2", "carrot-l1", "carrot", "carrot-r1", "carrot-r2"], scale2x=True)

        self.boundary = 20
        self.speed = 6
        self.max_acceleration = 1
        self.acceleration = 0
        self.acceleration_step = 0.07

        # time between shots (in ms)
        self.fire_rate = 500 
        self.cool_down = 0

        self.set_image()
        self.rect = self.image.get_rect()
        self.rect.x += pygame.display.get_surface().get_width() / 2
        self.rect.y += pygame.display.get_surface().get_height() / 2

    def set_image(self):

        if self.acceleration == 0:
            image = "carrot"
        elif self.acceleration > 0 and self.acceleration <= 0.5:
            image = "carrot-r1"
        elif self.acceleration > 0.5 and self.acceleration <= 1.0:
            image = "carrot-r2"        
        elif self.acceleration >= -0.5 and self.acceleration < 0:
            image = "carrot-l1"
        elif self.acceleration >= -1.0 and self.acceleration < 0.5:
            image = "carrot-l2"
        
        self.image = self.images[image]


    def update(self, dt):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x > self.boundary:
            self.acceleration = max(self.acceleration - self.acceleration_step, -self.max_acceleration)
            # print(self.rect.x)
            self.rect.x += self.speed * self.acceleration

        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and pygame.display.get_surface().get_width() - self.boundary > self.rect.x + self.rect.width:
            self.acceleration = min(self.acceleration + self.acceleration_step, self.max_acceleration)
            self.rect.x += self.speed * self.acceleration

        else:
            if self.acceleration != 0:
                if self.acceleration > 0:
                    self.acceleration = max(self.acceleration - 2*self.acceleration_step, 0)
                else:
                    self.acceleration = min(self.acceleration + 2*self.acceleration_step, 0)
                self.rect.x += self.speed * self.acceleration

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.y > self.boundary:
            self.rect.y -= self.speed

        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and pygame.display.get_surface().get_height() - self.boundary > self.rect.y + self.rect.height:
            self.rect.y += self.speed

        self.cool_down = max(self.cool_down - dt, 0)

        if (keys[pygame.K_SPACE]) and self.cool_down == 0:
            bullet.BulletSprite("red-1", self.rect.x, self.rect.y)
            self.cool_down = self.fire_rate

        self.set_image()