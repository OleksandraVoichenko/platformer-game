from settings import *

class TmxMap(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.surf = pygame.Surface((40, 80))
        self.image = self.surf
        self.rect = self.image.get_frect(topleft=pos)

        # movement
        self.dir = pygame.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites


    def input(self):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.dir = self.dir.normalize() if self.dir else self.dir


    def move(self, dt):
        self.rect.x += self.dir.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.dir.y * self.speed * dt
        self.collision('vertical')


    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.dir.x > 0: self.rect.right = sprite.rect.left
                    if self.dir.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.dir.y > 0: self.rect.bottom = sprite.rect.top
                    if self.dir.y < 0: self.rect.top = sprite.rect.bottom



    def update(self, dt):
        self.input()
        self.move(dt)