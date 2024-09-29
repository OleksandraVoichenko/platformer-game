from random import randint
from settings import *
from timer import Timer
from math import sin


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class Bullet(Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(pos, surf, groups)

        # movement
        self.dir = direction
        self.speed = 850

        # rotation
        self.image = pygame.transform.flip(self.image, direction == -1, False)


    def update(self, dt):
       self.rect.x += self.dir * self.speed * dt


class Fire(Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(100, autostart=True, func = self.kill)
        self.y_offset = pygame.Vector2(0, 5)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset


    def update(self, dt):
        self.timer.update()

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.flip != self.player.flip:
            self.kill()


class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_idx, self.anim_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_idx], groups)


    def animate(self, dt):
        self.frame_idx += self.anim_speed * dt
        self.image = self.frames[int(self.frame_idx) % len(self.frames)]


class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)


    def update(self, dt):
        self.move(dt)
        self.animate(dt)


class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames, create_bullet):
        super().__init__(frames, pos, groups)
        self.flip = False
        self.create_bullet = create_bullet

        # movement
        self.dir = pygame.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites
        self.gravity = 50
        self.on_floor = False

        # timer
        self.shoot_timer = Timer(500)


    def input(self):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if keys[pygame.K_SPACE] and self.on_floor:
            self.dir.y = -20

        if keys[pygame.K_s] and not self.shoot_timer:
            self.create_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()


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
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)


class Bee(Enemy):
    def __init__(self, frames, pos, groups, speed):
        super().__init__(frames, pos, groups)
        self.speed = speed


    def move(self, dt):
        self.rect.x -= self.speed * dt


class Worm(Enemy):
    def __init__(self, frames, pos, groups ):
        super().__init__(frames, pos, groups)


    def move(self, dt):
        pass