import pygame
import spritesheet
import player
import bullet
import enemyship
import explosion

pygame.init()

# set a Display Surface
# https://www.pygame.org/docs/ref/display.html#pygame.display.update
# coord (0, 0) is top left
screen = pygame.display.set_mode((800, 720))
pygame.display.set_caption("my game")

clock = pygame.time.Clock()
dt = 0
running = True

bullet.BulletSprite.load()
enemyship.ShipSprite.load()
explosion.ExplosionSprite.load()

sheet = spritesheet.spritesheet("assets/sheet1.png", "assets/sheet1.json")

all_sprites = pygame.sprite.Group()
all_sprites.add(player.PlayerSprite(sheet))

enemyship.ShipSprite("tri", 100, 100)
enemyship.ShipSprite("tri", 150, 100)
enemyship.ShipSprite("tri", 200, 100)

x_cool_down = 0

class TestSprite(pygame.sprite.Sprite):
    group = pygame.sprite.Group()

    def __init__(self):
        super().__init__()
        sheet = spritesheet.spritesheet("assets/explosions.png", "assets/explosions.json")
        self.image = sheet.image_name("bigred-3", scale2x=True)
        self.rect = self.image.get_rect()
        self.group.add(self)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    x_cool_down = max(x_cool_down - dt, 0)
    if (keys[pygame.K_x]) and x_cool_down == 0:
        # TestSprite()
        explosion.ExplosionSprite("bigred", 400, 400)
        x_cool_down = 200

    all_sprites.update(dt)
    enemyship.ShipSprite.group.update(dt)
    bullet.BulletSprite.group.update(dt)
    explosion.ExplosionSprite.group.update(dt)
    TestSprite.group.update()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    all_sprites.draw(screen)
    enemyship.ShipSprite.group.draw(screen)
    bullet.BulletSprite.group.draw(screen)
    explosion.ExplosionSprite.group.draw(screen)
    TestSprite.group.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Returns how many milliseconds have elapsed since the last call to tick().
    # Passing framerate will delay returning from tick() to ensure framerate is
    # not exceeded.
    dt = clock.tick(60)

pygame.quit()
