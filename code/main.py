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

        # None declarations
        self.player = None
        self.bee = None
        self.worm = None
        self.bullet_surf = None
        self.player_frames = None
        self.worm_frames = None
        self.bee_frames = None
        self.fire_surf = None
        self.level_height = None
        self.level_width = None
        self.audio = {}

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # setup
        self.load_assets()
        self.setup()

        # timer
        self.bee_timer = Timer(200, func = self.create_bee, autostart = True, repeat = True)


    def create_bee(self):
        """Creates Bee instance and calls on parameters such as frames, position of spawning, sprite groups, and speed."""

        Bee(frames=self.bee_frames,
            pos=((self.level_width + WINDOW_WIDTH), randint(0, self.level_height)),
            groups=(self.all_sprites, self.enemy_sprites),
            speed=randint(300, 500))


    def create_bullet(self, pos, direction):
        """Creates aa Bullet instance with parameters like bullet surface, position of spawning, sprite groups.
        Fire instance with surface, position of spawn, sprite groups, and player instance.
        Adds audio to the shoot."""

        # custom x value to fit the height of player's pistol
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet(surf=self.bullet_surf,
               pos=(x, pos[1]),
               direction=direction,
               groups=(self.all_sprites, self.bullet_sprites))
        Fire(surf=self.fire_surf,
             pos=pos,
             groups=self.all_sprites,
             player=self.player)
        self.audio['shoot'].play()


    def load_assets(self):
        """Loads animation frames and sounds into the game"""

        # graphics
        self.player_frames = import_folder('..', 'images', 'player')
        self.bee_frames = import_folder('..', 'images', 'enemies', 'bee')
        self.worm_frames = import_folder('..', 'images', 'enemies', 'worm')
        self.bullet_surf = import_image('..', 'images', 'gun', 'bullet')
        self.fire_surf = import_image('..', 'images', 'gun', 'fire')

        # sounds
        self.audio = import_sound('..', 'audio')


    def collision(self):
        """Manages collision logic between Player vs. Enemies sprite group.
        Manages bullet collisions with Enemy sprite group."""

        # bullet collision
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()

        # player collision
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False


    def setup(self):
        """Loads tmx map and 3 layers: ground, decorations, spawners for player and worms.
        Loads background audio for the game."""

        tmx_map = load_pygame(join('..', 'data', 'maps', 'world.tmx'))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE

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
                Worm(self.worm_frames, pygame.FRect(obj.x, obj.y, obj.width, obj.height), (self.all_sprites, self.enemy_sprites))

        self.audio['music'].play(loops=-1)


    def run(self):
        """Runs game (represents main loop)."""

        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run() 