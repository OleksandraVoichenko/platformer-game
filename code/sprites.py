from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_idx, self.anim_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_idx], groups)


    def animate(self, dt):
        self.frame_idx += self.anim_speed * dt
        self.image = self.frames[int(self.frame_idx) % len(self.frames)]


class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames):
        super().__init__(frames, pos, groups)
        self.flip = False

        # movement
        self.dir = pygame.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites
        self.gravity = 50
        self.on_floor = False


    def input(self):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if keys[pygame.K_SPACE] and self.on_floor:
            self.dir.y = -20


    def move(self, dt):
        # horizontal movement
        self.rect.x += self.dir.x * self.speed * dt
        self.collision('horizontal')

        # vertical movement
        self.dir.y += self.gravity * dt
        self.rect.y += self.dir.y
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
                    self.dir.y = 0


    def check_floor(self):
        bottom_rect = pygame.FRect((0, 0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_floor = True if bottom_rect.collidelist(level_rects) >= 0 else False


    def animate(self, dt):
        if self.dir.x != 0:
            self.frame_idx += self.anim_speed * dt
            self.flip = self.dir.x < 0
        else:
            self.frame_idx = 0

        self.frame_idx = 1 if not self.on_floor else self.frame_idx

        self.image = self.frames[int(self.frame_idx) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)


    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)