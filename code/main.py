import pygame.sprite

from settings import *
from sprites import Sprite, Player, Worm, Bee, Bullet, Fire
from timer import Timer
from groups import AllSprites
from support import *
from random import randint

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # sprites
        self.player = None
        self.bee = None
        self.worm = None
        self.bullet_surf = None
        self.player_frames = None
        self.worm_frames = None
        self.bee_frames = None
        self.fire_surf = None
        self.audio = {}

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        # setup
        self.load_assets()
        self.setup()

        # timer
        self.bee_timer = Timer(200, func = self.create_bee, autostart = True, repeat = True)


    def create_bee(self):
        Bee((randint(300, 600), randint(300, 600)), self.all_sprites, self.bee_frames)


    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, (x, pos[1]), direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, pos, self.all_sprites, self.player)


    def load_assets(self):
        # graphics
        self.player_frames = import_folder('..', 'images', 'player')
        self.bullet_surf = import_image('..', 'images', 'gun', 'bullet')
        self.fire_surf = import_image('..', 'images', 'gun', 'fire')
        self.bee_frames = import_folder('..', 'images', 'enemies', 'bee')
        self.worm_frames = import_folder('..', 'images', 'enemies', 'worm')

        # sounds
        self.audio = import_sound('..', 'audio')


    def setup(self):
        tmx_map = load_pygame(join('..', 'data', 'maps', 'world.tmx'))

        # ground look of map
        for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        # elements of decoration on the map
        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        # spawners on the map
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj. y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)
            elif obj.name == 'Worm':
                self.worm = Worm((obj.x, obj.y), self.all_sprites, self.worm_frames)


    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 