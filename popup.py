
import pygame, sys, random, snakeclass
from snakeclass import Megasnakes, Minisnakes, Boomerangs, Endscreen, Heart, Randoctopus
from pygame.locals import *

def makesnakerand(speed):
    positionchoose = random.randint(1, 4)
    if positionchoose == 1:
        x = 0
        y = 0
    if positionchoose == 2:
        x = width
        y = 0
    if positionchoose == 3:
        x = 0
        y = height
    if positionchoose == 4:
        x = width
        y = height
    return Minisnakes(speed,x,y)

def octopusrandmake(speed):
    positionchoose = random.randint(1, 2)
    if positionchoose == 1:
        x = 0
        y = random.randint(0, height)
    if positionchoose == 2:
        x = width
        y = random.randint(0, height)
    if positionchoose == 3:
        x = 0
        y = height
    if positionchoose == 4:
        x = width
        y = height
    return Randoctopus(speed,x,y)



pygame.init()
random.seed()
pygame.display.init()
pygame.mixer.init()
pygame.font.init()


# size = width, height = 600, 600 #nothing changes if you remove this
width = 900
height = 600
screen = pygame.display.set_mode((width, height) ,0)
blue = (174, 198, 207)
colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) #for random colour change
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(blue)
# screen.fill(blue)
#making a clock
clock = pygame.time.Clock()

# Make the big snake
snake = Megasnakes(450, 300)



#making lives snakecounter
# counter = Lives(600, 400)

# for x in range(numofsnakes): # For 0 to numofsnakes - 1
numofsnakes = 20

#making the groups so that they display
mini_snakes = pygame.sprite.Group([])
sprites = pygame.sprite.RenderPlain(snake)
octopuses = pygame.sprite.Group([])
enemies = pygame.sprite.Group([])
hearts = pygame.sprite.Group([])
playerthings = pygame.sprite.Group([])
# lifebar = pygame.sprite.Group(counter)
# sprites.add(counter)
# sprites.add(boomerang)

#making a sound work
sound = pygame.mixer.Sound("jump.wav")
hitsound = pygame.mixer.Sound("hit.wav")

# minisnake.rect.move_ip([60, 300])
# making the lives counter!!
myfont = pygame.font.Font(None, 30)
mylives = 10
# below is making lives counter
textsurface = myfont.render('Lives = ' + str(mylives) , False, (0, 0, 0))
# making a point system
mypoints = 0
pointsurface = myfont.render('Points = ' + str(mypoints) , False, (0, 0, 0))

#making a clock that spawns snakes
snakespawntimedelay = 2000

snakespawn = USEREVENT + 1
pygame.time.set_timer(snakespawn, snakespawntimedelay)




boomerang_on = False
starttimer = 0
snakecounter = 0
prevhashit = False
boomhashit = False
counter = 0
spawnincrease = 0
spawnsnakenow = False
octocounter = 2
heartcounter = 0
hearton = False
octohit = 0
oct = False
boomerang_id = 0


while True:
    # print(clock.get_fps())
    clock.tick(50)
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == snakespawn:
            spawnsnakenow = True
    if mylives > 0:

        snake.key_move()
        boomhashit = False
        if spawnsnakenow:
            starttimer += 1
            if starttimer >= 3:
                # print('p' + str(mypoints))
                # print(starttimer)
                newsnake = makesnakerand(random.randint(1 ,4) + spawnincrease)

                if (mypoints % 10 == 0):
                    # snakespawntimedelay -= 100
                    spawnincrease += 1
                    pygame.time.set_timer(snakespawn, snakespawntimedelay)
                sprites.add(newsnake)
                mini_snakes.add(newsnake)
                enemies.add(newsnake)
                snakecounter += 1

            spawnsnakenow = False

            # newoctopus = octopusrandmake(random.randint(1, 4)
            # print(starttimer)

            if (starttimer > 10 or starttimer == 10):
                if (octocounter % 2 == 0 or octocounter == 2):
                    newoctopus = octopusrandmake(random.randint(1, 4))
                    octopuses.add(newoctopus)
                    sprites.add(newoctopus)
                    enemies.add(newoctopus)
                    octocounter += 1
                else:
                    octocounter +=1




        if boomerang_on == True:
            # If the boomerang is being fired
            boomerang.update(snake) # Then we fire out and follow the snake
            # If we're done firing then we reset boomerang_on to False
            if boomerang.done == True:
                boomerang_on = False
            # Checking if the boomerang collides with the mini snakes
            snakecrashes = pygame.sprite.spritecollide(boomerang, mini_snakes, False)
            for collided in snakecrashes:
                collided.hide()
                mypoints += 1
                pointsurface = myfont.render('Points = ' + str(mypoints) , False, (0, 0, 0))

            octocrashes = pygame.sprite.spritecollide(boomerang, octopuses, False)
            for x in octocrashes:
                x.saveboomerang(boomerang_id)
                #if x.saveboomerang(boomerang_id) == True:
                    # we've hit the octopus for the first time

                # If they're not equal (!=)
                if x.saved_boomerang != boomerang_id:
                    x.hide()
                    mypoints += 1
                    pointsurface = myfont.render('Points = ' + str(mypoints) , False, (0, 0, 0))

                # print(mypoints)

            if boomerang.rect.top == 0 or boomerang.rect.bottom == height or boomerang.rect.left == 0 or boomerang.rect.right == width:
                if boomhashit == False:
                    background.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                    pygame.mixer.Sound.play(sound)
                    boomhashit = True
            else:
                boomhashit = False

            # Drawing boomerang on screen
            rangerz = pygame.sprite.Group(boomerang)
            rangerz.draw(screen)

        else:
            # Checks for key presses
            key = pygame.key.get_pressed()
            speed = 30
            maxdistance = 10
            if key[pygame.K_w]:
                boomerang = Boomerangs(speed,maxdistance,snake.rect.centerx, snake.rect.centery, 0)
                boomerang_on = True
                boomerang_id = boomerang_id + 1
            if key[pygame.K_a]:
                boomerang = Boomerangs(speed,maxdistance,snake.rect.centerx, snake.rect.centery, 3)
                boomerang_on = True
                boomerang_id = boomerang_id + 1
            if key[pygame.K_d]:
                boomerang = Boomerangs(speed,maxdistance,snake.rect.centerx, snake.rect.centery, 1)
                boomerang_on = True
                boomerang_id = boomerang_id + 1
            if key[pygame.K_s]:
                boomerang = Boomerangs(speed,maxdistance,snake.rect.centerx, snake.rect.centery, 2)
                boomerang_on = True
                boomerang_id = boomerang_id + 1

        lifelost = pygame.sprite.spritecollide(snake, enemies, False)
        for x in lifelost:
            mylives -= 1
            # print(mylives)
            x.killyou()
            textsurface = myfont.render('Lives = ' + str(mylives) , False, (0, 0, 0))



        for x in mini_snakes.sprites():
            x.follow(snake.rect)

        for x in octopuses.sprites():
            x.movement()

        # For all mini snakes
        for eachenemy in enemies.sprites():
            #making the snakes avoid each other?
            crashes = pygame.sprite.spritecollide(eachenemy, enemies, False)
            for collided in crashes:
                eachenemy.avoid(collided.rect)



        #making colour change when you hit the side
        if snake.rect.top == 0 or snake.rect.bottom == height or snake.rect.left == 0 or snake.rect.right == width:
            if prevhashit == False:
                background.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                pygame.mixer.Sound.play(sound)
                prevhashit = True
        else:
            prevhashit = False


        if  heartcounter % 353 ==0 and heartcounter != 0 and hearton == False:
            heartcounter += random.randint(1, 20)
            newheart = Heart(random.randint(0, 900), random.randint(0,600))
            # it didnt like using the integers width and height got a value error
            # print(heartcounter)
            sprites.add(newheart)
            hearts.add(newheart)
            hearton = True

        else:
            heartcounter += random.randint(1, 20)
            # print(heartcounter)

        # print(playerthings)
        lifegained = pygame.sprite.spritecollide(snake, hearts, False)
        # print(len(lifegained))
        for x in lifegained:
            mylives += 1
            x.hide()
            textsurface = myfont.render('Lives = ' + str(mylives) , False, (0, 0, 0))
            hearton = False

        sprites.draw(screen)
        # lifebar.draw(screen)
        screen.blit(textsurface,(0,0))
        text_width, text_height = myfont.size('Points = ' + str(mypoints)) #txt being whatever str you're renderin
        screen.blit(pointsurface, (width - text_width,0))

    else:
        stopscreen = Endscreen(width, height)
        stopit = pygame.sprite.RenderPlain(stopscreen)
        stopit.draw(screen)
        pygame.mixer.stop()
        for x in mini_snakes.sprites():
            x.die()
    pygame.display.update()
    pygame.display.flip()
# for x in mini_snakes.sprites():
#     x.die()
#     pygame.mixer.stop()
