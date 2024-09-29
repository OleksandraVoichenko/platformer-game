import pygame.sprite
from settings import *

class AllSprites(pygame.sprite.Group):
    """Creates a sprite group for all sprites. Handles camera movement synced with player movement."""

    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset =pygame.Vector2()


    def draw(self, target_pos):
        """Manages camera movement in sync with player movement."""

        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)