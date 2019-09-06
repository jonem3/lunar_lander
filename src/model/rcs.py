class RCS(Sprite):
    def __init__(self, lander):
        super(RCS, self).__init__()
        self.RCS_left = pygame.image.load(".../images/rcs.png").convert()
        self.RCS_right = pygame.transform.flip(RCS_left, True, False)
        self.lander = lander

    def render_right(self, image_number):
        self.image = pygame.Surface([4, 4]).convert()
        offset = image_number * 4
        self.image.blit(self.rcs, (0,0), (offset, 0, 8, 10))
        self.rect = self.image.get_rect()
        self.rect.x = self.lander.rect.x + 8
        self.rect.y = self.lander.rect.y + 10

    def render_left(self, image_number):
        self.image = pygame.Surface([4,4]).convert()
        offset = imagenumber * 4
        self.image.blit(self.rcs, (0,0), (offset, 0, 8, 10))
        self.rect.x = self.lander.rect.x
        self.rect.y = self.lander.rect.y +10
