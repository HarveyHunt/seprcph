import pygame
from seprcph.event import EventManager


class Renderable(pygame.sprite.Sprite):
    """
    All objects that want to be rendered must inherit from this.
    """
    def __init__(self, pos, image):
        """
        Convert the alpha of image and set pos.
        """
        super(Renderable, self).__init__()
        # We can't use convert_alpha without a screen being set up, so test
        # if a screen is set up.
        try:
            image = image.convert_alpha()
        except pygame.error:
            pass
        finally:
            self.image = image

        self.pos = pos
        EventManager.add_listener('ui.clicked', self.click)

    @property
    def rect(self):
        """
        Calculate the rect based upon the image size and
        object's position.
        """
        rect = self.image.get_rect()
        rect.centerx = self.pos[0]
        rect.centery = self.pos[1]
        return rect

    def update(self):
        """
        A hook that is called once per turn.
        """
        pass

    def click(self, event):
        """
        A hook that is called once the Renderable is clicked on.
        """
        pass
