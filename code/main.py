from settings import *
from sprites import TmxMap, Player
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # sprites
        self.player = None

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # setup
        self.setup()


    def setup(self):
        tmx_map = load_pygame(join('..', 'data', 'maps', 'world.tmx'))

        # ground look of map
        for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
            TmxMap((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        # elements of decoration on the map
        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            TmxMap((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        # spawners on the map
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj. y), self.all_sprites, self.collision_sprites)


    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.all_sprites.update(dt)

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 