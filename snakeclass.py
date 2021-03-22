
import pygame, sys, random
from pygame.locals import *
pygame.init()
random.seed()
pygame.display.init()
# size = width, height = 600, 600 #nothing changes if you remove this
screen = pygame.display.set_mode((1280, 700) ,0)

class Megasnakes (pygame.sprite.Sprite):
    """ snakes?? """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sophie.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speed = 15


    def key_move(self):
        dist = 1
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.move_ip([0, -self.speed])
        if key[pygame.K_LEFT]:
            self.rect.move_ip([-self.speed, 0])
        if key[pygame.K_RIGHT]:
            self.rect.move_ip([self.speed, 0])
        if key[pygame.K_DOWN]:
            self.rect.move_ip([0, self.speed])
# making background change colour when you hit the edge of the screen
        self.rect.clamp_ip(screen.get_rect())





class Minisnakes (pygame.sprite.Sprite):
    """the snakes that follow the biggo snake (mega snake)"""
    def __init__(self, speed, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cutesnake.jpg").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (20, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def follow(self, snakerect):
        if self.rect.centerx < snakerect.centerx:
            self.rect.move_ip([self.speed, 0])
        if self.rect.centerx > snakerect.centerx:
            self.rect.move_ip([-self.speed, 0])
        if self.rect.centery < snakerect.centery:
            self.rect.move_ip([0, self.speed])
        if self.rect.centery > snakerect.centery:
            self.rect.move_ip([0, -self.speed])
        self.rect.clamp_ip(screen.get_rect())

    def avoid(self, snakerect):
        if self.rect.centerx < snakerect.centerx:
            self.rect.move_ip([-self.speed, 0])
        if self.rect.centerx > snakerect.centerx:
            self.rect.move_ip([self.speed, 0])
        if self.rect.centery < snakerect.centery:
            self.rect.move_ip([0, -self.speed])
        if self.rect.centery > snakerect.centery:
            self.rect.move_ip([0, self.speed])
        self.rect.clamp_ip(screen.get_rect())

    def killyou(self):
        """when they hit you"""
        self.kill()
        hitsound = pygame.mixer.Sound("splat.wav")
        pygame.mixer.Sound.play(hitsound)

    def hide(self):
        self.kill()
        hitsound = pygame.mixer.Sound("hit.wav")
        pygame.mixer.Sound.play(hitsound)
        # print(self.visible)

    def runaway(self):
        self.rect.move_ip([1000,1000])

    def die(self):
        self.kill()


class Boomerangs (pygame.sprite.Sprite):
    """the object that will kill the minisnakes"""

    def __init__(self, speed, maxdist, x, y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("boomerang2.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.distance = 0
        self.maxdistance = maxdist
        self.direction = dir
        self.rect.centerx = x
        self.rect.centery = y
        self.done = False

    def update(self, snake):
        if (self.distance < self.maxdistance):
            # print("yes down")
            if self.direction == 0:
                self.rect.move_ip([0,-self.speed])
            if self.direction == 1:
                self.rect.move_ip([self.speed,0])
            if self.direction == 2:
                self.rect.move_ip([0,self.speed])
            if self.direction == 3:
                self.rect.move_ip([-self.speed,0])

            self.distance = self.distance + 1
        elif pygame.sprite.collide_rect(self,snake):
            self.done = True
            self.distance = 0
        else:
            # print("no down")
            self.follow(snake.rect)

    def follow(self, snakerect):
        if self.rect.centerx < snakerect.centerx:
            self.rect.move_ip([self.speed, 0])
        if self.rect.centerx > snakerect.centerx:
            self.rect.move_ip([-self.speed, 0])
        if self.rect.centery < snakerect.centery:
            self.rect.move_ip([0, self.speed])
        if self.rect.centery > snakerect.centery:
            self.rect.move_ip([0, -self.speed])
        self.rect.clamp_ip(screen.get_rect())

# class Lives (pygame.sprite.Sprite):
#     """the counter thats on the thingy"""
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load("one.png").convert_alpha()
#         self.image.set_colorkey((255, 255, 255))
#         self.image = pygame.transform.scale(self.image, (100, 50))
#         self.rect = self.image.get_rect()
#         self.rect.centerx = x
#         self.rect.centery = y



class Endscreen (pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gameover.jpg").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()

    def stopgame(self):
        # pygame.mixer.Sound.stop()
        pygame.mixer.stop()


class Randoctopus (pygame.sprite.Sprite):

    def __init__(self, speed, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("6.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed
        self.move = 0
        self.hit = False
        self.saved_boomerang = -1

    def movement(self):
        distance = 1
        if self.move < 30:
            self.rect.move_ip([self.speed, -self.speed])
            self.move += 1
        if self.move >= 30 and self.move < 60:
            self.move += 1
            self.rect.move_ip([self.speed, self.speed])
            if self.move == 60:
                self.move = 0
        if (self.rect.right >= pygame.display.get_surface().get_width() or self.rect.left <= 0):
            self.speed = -self.speed
        self.rect.clamp_ip(screen.get_rect())

    def avoid(self, octorect):
        if self.rect.centerx < octorect.centerx:
            self.rect.move_ip([-self.speed, 0])
        if self.rect.centerx > octorect.centerx:
            self.rect.move_ip([self.speed, 0])
        if self.rect.centery < octorect.centery:
            self.rect.move_ip([0, -self.speed])
        if self.rect.centery > octorect.centery:
            self.rect.move_ip([0, self.speed])
        self.rect.clamp_ip(screen.get_rect())

    def saveboomerang(self, boomerang_id):
        if self.hit == False:
            self.saved_boomerang = boomerang_id
            self.hit = True
            return True
        return False

    def hide(self):
        '''when you hit them'''
        self.kill()
        hitsound = pygame.mixer.Sound("angrychipmunk.wav")
        pygame.mixer.Sound.play(hitsound)

    def killyou(self):
        """when they hit you"""
        self.kill()
        hitsound = pygame.mixer.Sound("splat.wav")
        pygame.mixer.Sound.play(hitsound)

    def die(self):
        self.kill()

class Heart (pygame.sprite.Sprite):
    '''they give you more lives'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("heart.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (40, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def hide(self):
        '''when you get them'''
        self.kill()
        hitsound = pygame.mixer.Sound("bob.wav")
        pygame.mixer.Sound.play(hitsound)
