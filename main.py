import sys

import pygame

pygame.init()

# Title and Icon
pygame.display.set_caption("RPG-Zork")
icon = pygame.image.load('game_image.png')
pygame.display.set_icon(icon)

FPS = 30
FramePerSec = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)
end_font = pygame.font.SysFont('Arial', 175)
game_over = False

canvas = pygame.display.set_mode((1200, 700))


class Venue(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.Surface((200, 100))
        self.rect = pygame.draw.rect(self.image,(0,255,0),(0,0,200,100),25)
        self.rect = self.rect.move(location)


class Horizontal_Connectors(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.Surface((100, 30))
        self.image.fill(pygame.color.Color('green'))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(location)


class Vertical_Connectors(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.Surface((30, 100))
        self.image.fill(pygame.color.Color('green'))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(location)


venue_spritegroup = pygame.sprite.Group()
venue_spritegroup.add(Venue((610, 100)))
for i in range(0, 3):
    venue_spritegroup.add(Venue((10 + 300 * i, 300)))
    venue_spritegroup.add(Venue((310 + 300 * i, 500)))

horizontal_connectors_spritegroup = pygame.sprite.Group()
for i in range(0,2):
    horizontal_connectors_spritegroup.add(Horizontal_Connectors((210 + 300 * i, 340)))
horizontal_connectors_spritegroup.add(Horizontal_Connectors((810, 540)))

vertical_connectors_spitegroup = pygame.sprite.Group()
for i in range(0,2):
     vertical_connectors_spitegroup.add(Vertical_Connectors((410+i*300,400)))
vertical_connectors_spitegroup.add(Vertical_Connectors((710,200)))


#text inside the box
def name_the_place():
    canvas.blit(font.render("Bedroom", False, (255, 255, 255)), (40, 325))
    canvas.blit(font.render("Hall", False, (255, 255, 255)), (390, 325))
    canvas.blit(font.render("Kitchen", False, (255, 255, 255)), (360, 525))
    canvas.blit(font.render("Dining Room", False, (255, 255, 255)), (625, 325))
    canvas.blit(font.render("Pantry", False, (255, 255, 255)), (670, 125))
    canvas.blit(font.render("Garden", False, (255, 255, 255)), (660, 525))
    canvas.blit(font.render("Forest", False, (255, 255, 255)), (970, 525))

class Player(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.Surface((30, 30),pygame.SRCALPHA)
        pygame.draw.circle(self.image,pygame.Color('red'),(15,15),15)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(location)


        self.vel=8
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.move_ip(0,-self.vel)
            if not (pygame.sprite.spritecollide(self,venue_spritegroup,False) or pygame.sprite.spritecollide(self,horizontal_connectors_spritegroup,False) \
               or pygame.sprite.spritecollide(self,vertical_connectors_spitegroup,False)):
                self.rect.move_ip(0,40)
        elif keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.vel)
            if not (pygame.sprite.spritecollide(self, venue_spritegroup, False) or pygame.sprite.spritecollide(self,horizontal_connectors_spritegroup,False) \
                    or pygame.sprite.spritecollide(self, vertical_connectors_spitegroup, False)):
                self.rect.move_ip(0,-40)
        elif keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.vel, 0)
            if not (pygame.sprite.spritecollide(self, venue_spritegroup, False) or pygame.sprite.spritecollide(self,horizontal_connectors_spritegroup,False) \
                    or pygame.sprite.spritecollide(self, vertical_connectors_spitegroup, False)):
                self.rect.move_ip(-40,0)
        elif keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.vel, 0)
            if not (pygame.sprite.spritecollide(self, venue_spritegroup, False) or pygame.sprite.spritecollide(self,horizontal_connectors_spritegroup,False) \
                    or pygame.sprite.spritecollide(self, vertical_connectors_spitegroup, False)):
                self.rect.move_ip(40,0)


player_spritegroup = pygame.sprite.Group()
player_spritegroup.add(Player((390,360)))

class Monster(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.Surface((30, 30),pygame.SRCALPHA)
        pygame.draw.circle(self.image,pygame.Color('brown'),(15,15),15)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(location)


        self.vel=5
    def update(self):
        self.rect.move_ip(self.vel,0)
        global game_over
        if not pygame.sprite.spritecollide(self, venue_spritegroup, False):
            self.vel=-self.vel
        elif (pygame.sprite.spritecollide(self, player_spritegroup, True)):
            game_over = True

        if game_over:
            canvas.blit(end_font.render("GAME OVER", False, (255, 255, 255)), (40, 325))

monster_spritegroup = pygame.sprite.Group()
monster_spritegroup.add(Monster((390, 530)))

# Game Loop -displays the screen
while True:
    canvas.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    venue_spritegroup.draw(canvas)
    horizontal_connectors_spritegroup.draw(canvas)
    vertical_connectors_spitegroup.draw(canvas)
    name_the_place()
    player_spritegroup.draw(canvas)
    monster_spritegroup.draw(canvas)
    player_spritegroup.update()
    monster_spritegroup.update()
    pygame.display.update()
    FramePerSec.tick(FPS)
