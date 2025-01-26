import asyncio
import pygame
import sys
import spritesheet
import player
import bullet
import enemyship
import explosion

class TestSprite(pygame.sprite.Sprite):
    group = pygame.sprite.Group()

    def __init__(self):
        super().__init__()
        sheet = spritesheet.spritesheet("explosions.png", "explosions.json")
        self.image = sheet.image_name("bigred-3", scale2x=True)
        self.rect = self.image.get_rect()
        self.group.add(self)

class Game:

    def __init__(self):

        # set a Display Surface
        # https://www.pygame.org/docs/ref/display.html#pygame.display.update
        # coord (0, 0) is top left
        self.screen = pygame.display.set_mode((800, 720))
        pygame.display.set_caption("my game")

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        bullet.BulletSprite.load()
        enemyship.ShipSprite.load()
        explosion.ExplosionSprite.load()

        sheet = spritesheet.spritesheet("sheet1.png", "sheet1.json")

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(player.PlayerSprite(sheet))

        enemyship.ShipSprite("tri", 100, 100)
        enemyship.ShipSprite("tri", 150, 100)
        # enemyship.ShipSprite("tri", 200, 100)

        self.x_cool_down = 0

    def game_loop(self):
        # drain the event queue
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                self.running = False
                return False
            
            if event.type == pygame.FINGERDOWN:
                print(f"finger down id:{event.finder_id} x:{event.x} y:{event.y} dx:{event.dx} dy:{event.dy}")
            elif event.type == pygame.FINGERUP:
                print(f"finger up id:{event.finder_id} x:{event.x} y:{event.y} dx:{event.dx} dy:{event.dy}")
            elif event.type == pygame.FINGERMOTION:
                print(f"finger motion id:{event.finder_id} x:{event.x} y:{event.y} dx:{event.dx} dy:{event.dy}")
            elif event.type == pygame.MOUSEBUTTONUP:
                print(f"mouse button up pos:{event.pos} button:{event.button} touch:{event.touch}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"mouse button down pos:{event.pos} button:{event.button} touch:{event.touch}")
            elif event.type == pygame.MOUSEMOTION:
                print(f"mouse motion pos:{event.pos} rel:{event.rel} button:{event.buttons} touch:{event.touch}")

        keys = pygame.key.get_pressed()
        self.x_cool_down = max(self.x_cool_down - self.dt, 0)
        if (keys[pygame.K_x]) and self.x_cool_down == 0:
            # TestSprite()
            explosion.ExplosionSprite("bigred", 400, 400)
            self.x_cool_down = 200

        self.all_sprites.update(self.dt)
        bullet.BulletSprite.group.update(self.dt)
        enemyship.ShipSprite.group.update(self.dt)
        explosion.ExplosionSprite.group.update(self.dt)
        TestSprite.group.update()

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("white")

        self.all_sprites.draw(self.screen)
        enemyship.ShipSprite.group.draw(self.screen)
        bullet.BulletSprite.group.draw(self.screen)
        explosion.ExplosionSprite.group.draw(self.screen)
        TestSprite.group.draw(self.screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # Returns how many milliseconds have elapsed since the last call to tick().
        # Passing framerate will delay returning from tick() to ensure framerate is
        # not exceeded.
        self.dt = self.clock.tick(60)

        return True

async def main():
    """ pygbag main function """
    pygame.init()
    g = Game()
    while(g.game_loop()):    
        await asyncio.sleep(0)
    pygame.quit()
    exit()

if sys.platform == "emscripten":
    """ Running under pygbag in the browser, so use asyncio """
    asyncio.run(main())
else:
    """ Command line main """
    pygame.init()
    g = Game()
    while(g.game_loop()):
        pass
    pygame.quit()
