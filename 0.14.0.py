import pygame 
import os
import random
import sys
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
pygame.init()
#player stats#
CharacterWalkSpeed = [2, 1.7, 2.4]
CharacterRunSpeed = [4, 4.5, 5.5]
CharacterAirSpeed = [0.5, 0.6, 0.7]
CharacterJumpHeight = [0.7, 0.8, 0.7]
CharacterGravity = [0.7, 0.7, 0.7]
CharacterFlight = [30, 0, 45]
CharacterClimb = [0, 0, 0]
CharacterHP = [130, 100, 110]
running = True
screen = pygame.display.set_mode((800, 600)) 
keys = pygame.key.get_pressed()
MaxPLX = 0
MinPLX = 0
MaxPLY = 0
MinPLY = 0
TargetX = 0
TargetY = 0
CamX = 0
CamY = 0
CamZX = 0
CamZY = 0
CamZ = 0
killcount = 0
block = [pygame.Rect(150, 350, 500, 200)]
attacks = []
projectiles = []
platforms = [pygame.Rect(325, 275, 150, 3), pygame.Rect(0, 450, 75, 3), pygame.Rect(750, 450, 75, 3)]
particles = []
homing = []
bbbSprites = [pygame.image.load("sprites/walk1.png").convert_alpha(),
              pygame.image.load("sprites/walk2.png").convert_alpha(),
              pygame.image.load("sprites/jab1.png").convert_alpha(),
              pygame.image.load("sprites/jab2.png").convert_alpha(),
              pygame.image.load("sprites/ftilt1.png").convert_alpha(),
              pygame.image.load("sprites/ftilt2.png").convert_alpha(),
              pygame.image.load("sprites/air.png").convert_alpha(),
              pygame.image.load("sprites/dair-uair1.png").convert_alpha(),
              pygame.image.load("sprites/dair2.png").convert_alpha(),
              pygame.image.load("sprites/uair2.png").convert_alpha(),
              pygame.image.load("sprites/fly1.png").convert_alpha(),
              pygame.image.load("sprites/fly2.png").convert_alpha(),
              pygame.image.load("sprites/special.png").convert_alpha(),
              pygame.image.load("sprites/shield.png").convert_alpha(),
              pygame.image.load("sprites/nair1.png").convert_alpha(),
              pygame.image.load("sprites/nair2.png").convert_alpha(),]
mantisSprites = [pygame.image.load("sprites/mantis-walk1.png").convert_alpha(),
              pygame.image.load("sprites/mantis-walk2.png").convert_alpha(),
              pygame.image.load("sprites/mantis-jab.png").convert_alpha(),
              pygame.image.load("sprites/mantis-ftilt.png").convert_alpha(),
              pygame.image.load("sprites/mantis-dtilt.png").convert_alpha(),
              pygame.image.load("sprites/mantis-idunno.png").convert_alpha()]
for sprite in bbbSprites:
    bbbSprites[bbbSprites.index(sprite)] = pygame.transform.scale(sprite, (sprite.get_width() * 3, sprite.get_height() * 3))
for sprite in mantisSprites:
    mantisSprites[mantisSprites.index(sprite)] = pygame.transform.scale(sprite, (sprite.get_width() * 2.5, sprite.get_height() * 2.5))
class player():
    def __init__(self, X, Y, character, playerNumber):
        self.character = character
        self.X = X
        self.Y = Y
        self.playerNumber = playerNumber
        self.VX = 0
        self.VY = 0
        self.sizeX = 45 if self.character == 0 else 50 if self.character == 1 else 30
        self.sizeY = 35 if self.character == 0 else 40 if self.character == 1 else 25
        self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
        self.grounded = False
        self.jumpTimer = 0
        self.dashTimer = 0
        self.dashing = 0
        self.flight = 0
        self.flightTimer = 0
        self.atktest = 1
        self.wallStopDir = 0
        self.wallGrab = 0
        self.wallGrabTimer = 0
        self.frame = 0
        self.state = 0
        self.charge = 0
        self.attackTimer = 0
        self.facing = -1
        self.coyote = 0
        self.gotHit = 0
        self.DgotHit = 0
        self.HPHealing = 0
        self.HPHealTimer = 0
        self.HP = CharacterHP[self.character]
        self.touchingWall = 0
        self.wallHitbox = pygame.Rect(self.X -1, self.Y, self.sizeX + 2, self.sizeY)
        self.maxFrame = 0
        self.superMeter = 0
        self.shielding = 0
        self.shieldHP = 50
        self.shieldHPHealTimer = 0
        self.animFrame = 0
        self.bounced = 0
        self.dashed = 1
        self.wavedash = 0
        self.platHitbox = pygame.Rect(self.X, self.Y - self.sizeX + 20, self.sizeX, 20)
        self.no_special = 0
    class attack:
        def __init__(self, pl, attackX, attackY, atkSizeX, atkSizeY, damage, angleX, angleY, launch, sender, direction, hitbox, block, super, hitstun, grab):
            self.direction = direction
            self.X = pl.X
            self.Y = pl.Y
            self.attackX = attackX
            self.attackY = attackY
            self.atkSizeX = atkSizeX
            self.atkSizeY = atkSizeY
            self.damage = damage
            self.angleX = angleX * direction
            self.angleY = angleY
            self.launch = launch
            self.sender = sender
            self.hitbox = hitbox
            self.block = block
            self.super = super
            self.hitstun = hitstun
            self.grab = grab
            attacks.append((pygame.Rect(self.X + self.attackX, self.Y + self.attackY, self.atkSizeX, self.atkSizeY), self.damage, self.angleX, self.angleY, self.launch, self.sender, self.block, self.super, self.hitstun, self.grab)) if direction == 1 else attacks.append((pygame.Rect(self.X - self.attackX - self.atkSizeX + self.hitbox.width, self.Y + self.attackY, self.atkSizeX, self.atkSizeY), self.damage, self.angleX, self.angleY, self.launch, self.sender, self.block, self.super, self.hitstun, self.grab))
    class projectile:
        def __init__(self, X, Y, Xsize, Ysize, VX, VY, FX, FY, gravity, frame, sender, damage, angleX, angleY, direction, launch, type, block, super, hitstun):
            self.X = X
            self.Y = Y
            self.Xsize = Xsize
            self.Ysize = Ysize
            self.VX = VX
            self.VY = VY
            self.FX = FX
            self.FY = FY
            self.gravity = gravity
            self.frame = frame
            self.sender = sender
            self.damage = damage
            self.angleX = angleX * direction
            self.angleY = angleY
            self.launch = launch
            self.attack = pygame.Rect(self.X, self.Y, Xsize, Ysize)
            self.type = type
            self.block = block
            self.super = super
            self.hitstun = hitstun
            self.marck = 0
            self.mode = 0
            projectiles.append(self)
        def update(self):
            if self.type == 1:
                # X collision #
                self.X += self.VX
                self.VX *= self.FX
                self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                if any(self.attack.colliderect(rect) for rect in block):
                    self.frame = 0
                # Attack and frame update #
                self.frame -= 1
                attacks.append((self.attack, self.damage, self.angleX, self.angleY, self.launch, self.sender, self.block, self.super, self.hitstun, 0))
                if self.frame <= 0:
                    projectiles.pop(projectiles.index(self))
            elif self.type == 2:
                # X collision #
                self.X += self.VX
                self.VX *= self.FX
                self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                if any(self.attack.colliderect(rect) for rect in block):
                    while any(self.attack.colliderect(rect) for rect in block):
                        self.X -= 1 if self.VX > 0 else -1
                        self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                    self.VX *= -0.4
                # Y collision #
                self.Y += self.VY
                self.VY *= self.FY
                self.VY += self.gravity
                if self.VY > 10:
                    self.VY = 10
                self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                if any(self.attack.colliderect(rect) for rect in block):
                    while any(self.attack.colliderect(rect) for rect in block):
                        self.Y -= 1 if self.VY > 0 else -1
                        self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                    self.VY *= -0.5
                    self.VX *= 0.8
                    if self.VY > 0.3:
                        self.VY = 0
                # Player collision #
                if any(self.attack.colliderect(pl.hitbox) for pl in players):
                    for pl in players:
                        if pl.playerNumber != self.sender and self.attack.colliderect(pl.hitbox):
                            self.frame = 2
                # Attack detection#
                for attack in attacks:
                    if any(self.attack.colliderect(attack[0]) for attack in attacks):
                        self.VX = attack[2] * 1.5
                        self.VY = attack[3] * 1.5
                        if self.VX > 20:
                            self.VX = 20
                        if self.VX < -20:
                            self.VX = -20
                        if self.VY > 20:
                            self.VY = 20
                        if self.VY < -20:
                            self.VY = -20
                        elif self.VY < 10:
                            self.VY = 2
                        self.mode = 1
                        self.sender = attack[5]
                if any(self.attack.colliderect(pl.hitbox) for pl in players):
                    for pl in players:
                        if pl.playerNumber != self.sender and self.attack.colliderect(pl.hitbox):
                                if self.marck == 0:
                                    self.marck = self.frame
                if self.frame == self.marck - 1:
                    self.VX *= -0.6
                    self.VY = -8
                    self.marck = 0
                    if self.mode == 1:
                        self.frame = 1
                if self.frame <= 3 and self.frame > 0:
                        self.Attack = player.attack(self, -15, -15, 40, 40, 17, 0, -14, 0, self.sender, 1, pygame.Rect(self.X - 20, self.Y - 20, 40, 40), 0, 1, 5, 0)
                self.damage = abs(self.VX) - 0.5
                if abs(self.damage) < 1:
                    self.damage = 1
                # Attack and frame update #
                self.frame -= 1
                if self.frame > 3:
                    attacks.append((self.attack, self.damage, self.angleX, self.angleY, self.launch, self.sender, self.block, self.super, self.hitstun, 0))
                if self.frame <= 0:
                    projectiles.pop(projectiles.index(self))
            elif self.type == 3:
                # X collision #
                self.X += self.VX
                self.VX *= self.FX
                self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                if any(self.attack.colliderect(rect) for rect in block):
                    self.frame = 0
                # Attack and frame update #
                self.frame -= 1
                attacks.append((self.attack, self.damage, self.angleX, self.angleY, self.launch, self.sender, self.block, self.super, self.hitstun, 0))
                if self.frame <= 0:
                    projectiles.pop(projectiles.index(self))
            elif self.type == 4:
                # X collision #
                self.X += self.VX
                self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                if any(self.attack.colliderect(rect) for rect in block):
                    while any(self.attack.colliderect(rect) for rect in block):
                        self.X -= 1 if self.VX > 0 else -1
                        self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                    if self.frame > 2:
                        self.frame = 2
                # Y collision #
                self.Y += self.VY
                self.VY += self.gravity
                self.VX *= self.FX
                self.VY *= self.FY
                self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                if any(self.attack.colliderect(rect) for rect in block):
                    while any(self.attack.colliderect(rect) for rect in block):
                        self.Y -= 1 if self.VY > 0 else -1
                        self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                    if self.frame > 2:
                        self.frame = 2
                # Player collision #
                if any(self.attack.colliderect(pl.hitbox) for pl in players):
                    for pl in players:
                        if pl.playerNumber != self.sender and self.attack.colliderect(pl.hitbox):
                            if self.frame > 2:
                                self.frame = 2
                # Explosion generation #
                if self.frame <= 1:
                    self.Attack = player.attack(self, -30, -30, 80, 80, 10, 0, 15, 1, self.sender, 1, pygame.Rect(self.X - 20, self.Y - 20, 40, 40), 0, 1, 0, 0)
                    self.frame = 0
                    self.projectile = player.projectile(self.X, self.Y - 5, 10, 10, 8, -3, 0.98, 1, 0.5, 10, self.sender, 10, 10, 5, 1, 1, 5, 0, 1, 6)
                    self.projectile = player.projectile(self.X, self.Y - 5, 10, 10, 3, -4, 0.98, 1, 0.5, 10, self.sender, 10, 10, 5, 1, 1, 5, 0, 1, 6)
                    self.projectile = player.projectile(self.X, self.Y - 5, 10, 10, -3, -4, 0.98, 1, 0.5, 10, self.sender, 10, 10, 5, 1, 1, 5, 0, 1, 6)
                    self.projectile = player.projectile(self.X, self.Y - 5, 10, 10, -8, -3, 0.98, 1, 0.5, 10, self.sender, 10, 10, 5, 1, 1, 5, 0, 1, 6)
                # Attack and frame update #
                self.frame -= 1
                if self.frame <= 0:
                    projectiles.pop(projectiles.index(self))
            elif self.type == 5:
                # X collision #
                self.X += self.VX
                self.VX *= self.FX
                self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                if any(self.attack.colliderect(rect) for rect in block):
                    while any(self.attack.colliderect(rect) for rect in block):
                        self.X -= 1 if self.VX > 0 else -1
                        self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                    self.VX *= -0.4
                if any(self.attack.colliderect(pl.hitbox) for pl in players):
                    for pl in players:
                        if pl.playerNumber != self.sender and self.attack.colliderect(pl.hitbox):
                                if self.marck == 0:
                                    self.marck = self.frame
                # Y collision #
                self.Y += self.VY
                self.VY *= self.FY
                self.VY += self.gravity
                if self.VY > 10:
                    self.VY = 10
                self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                if any(self.attack.colliderect(rect) for rect in block):
                    while any(self.attack.colliderect(rect) for rect in block):
                        self.Y -= 1 if self.VY > 0 else -1
                        self.attack = pygame.Rect(self.X, self.Y, self.Xsize, self.Ysize)
                    self.VY *= -0.5
                    self.VX *= 0.8
                    if self.VY > 0.3:
                        self.VY = 0
                if self.frame == self.marck - 1:
                    self.VX *= -0.6
                    self.VY = -8
                    self.marck = 0
                if self.frame <= 3 and self.frame > 0:
                        self.Attack = player.attack(self, -15, -15, 40, 40, 10, 0, 22, 0, self.sender, 1, pygame.Rect(self.X - 20, self.Y - 20, 40, 40), 1, 1, 0, 0)
                self.damage = abs(self.VX) - 0.5
                if abs(self.damage) < 1:
                    self.damage = 1
                # Attack and frame update #
                self.frame -= 1
                attacks.append((self.attack, self.damage, self.angleX, self.angleY, self.launch, self.sender, self.block, self.super, self.hitstun, 0))
                if self.frame <= 0:
                    projectiles.pop(projectiles.index(self))
            elif self.type == 6:
                homing.append((self.X, self.Y, self.sender, 2))
                while self.frame > 0:
                    self.X += self.VX
                    self.VX *= self.FX
                    if any(self.attack.colliderect(rect) for rect in block):
                        self.frame = 0
                    # Y collision #
                    self.Y += self.VY
                    self.VY *= self.FY
                    self.VY += self.gravity
                    if self.VY > 10:
                        self.VY = 10
                    if any(self.attack.colliderect(rect) for rect in block):
                        self.frame = 0
                    self.frame -= 1
                    homing.append((self.X, self.Y, self.sender, 2))
                if self.frame <= 0:
                    projectiles.pop(projectiles.index(self))
    def movement(self, UP, LEFT, DOWN, RIGHT, ATTACK, SHIELD, SUPER, SPECIAL):
        self.UP = UP
        self.LEFT = LEFT
        self.DOWN = DOWN
        self.RIGHT = RIGHT
        self.RIGHT = RIGHT
        self.ATTACK = ATTACK
        self.SHIELD = SHIELD
        self.SUPER = SUPER
        self.SPECIAL = SPECIAL
        # EX #
        if SUPER and self.superMeter > 24 and self.state != "HIT":
            if self.state != "EX":
                self.state = "EX"
                self.superMeter -= 25
                self.frame = 20
        # Side Special #
        if (((( ATTACK and SHIELD) or self.SPECIAL) and self.frame > (self.maxFrame - 1) and (self.state != "HIT" or self.state != "UFDH" or self.state != "DFDH" or self.state != "FDSH" or self.state != "UDSH" or self.state != "DDSH") and (LEFT or RIGHT) and not(LEFT and RIGHT)) or ((( ATTACK and SHIELD) or self.SPECIAL) and self.frame == self.maxFrame and self.state != "HIT" and (self.state == "UFDH" or self.state == "DFDH" or self.state == "FDSH" or self.state == "UDSH" or self.state == "DDSH") and (LEFT or RIGHT) and not(LEFT and RIGHT))) and self.no_special == 0:
            if self.state != "SPCN" and self.state != "SPCD":
                self.state = "SPCD"
                self.facing = -1 if LEFT else 1
                if self.character == 0:
                    self.frame = 40
                elif self.character == 1:
                    self.frame = 20
                    self.charge = 0
        # Special #
        elif (((( ATTACK and SHIELD) or self.SPECIAL) and self.frame > (self.maxFrame - 1) and (self.state != "HIT" or self.state != "UFDH" or self.state != "DFDH" or self.state != "FDSH" or self.state != "UDSH" or self.state != "DDSH") and not(LEFT and RIGHT)) or ((( ATTACK and SHIELD) or self.SPECIAL) and self.frame == self.maxFrame and (self.state == "UFDH" or self.state == "DFDH" or self.state == "FDSH" or self.state == "UDSH" or self.state == "DDSH") and not(LEFT and RIGHT))) and self.no_special == 0:
            if self.state != "SPCN" and self.state != "SPCD":
                self.state = "SPCN"
                if self.character == 0:
                    self.frame = 30
                elif self.character == 1:
                    self.frame = 18
        # Shield #
        if self.grounded == 1 and self.state != "HIT" and self.state != "SPCN" and self.state != "SPCD" and self.state != (2 + self.playerNumber * 2):
            if SHIELD and not(ATTACK):
                self.frame = 3
                self.maxFrame = 4
                self.state = "SHLD"
        # Grab #
        if self.grounded == 1 and self.state != "HIT" and self.state == "SHLD":
            if DOWN:
                self.frame = 30
                self.maxFrame = 30
                self.state = 2 + self.playerNumber * 2
        # Airdash #
        elif self.grounded == 0 and self.state != "HIT" and self.state != "SPCN" and self.state != "SPCD":
            if SHIELD and self.dashed == 0:
                self.dashed = 1
                self.frame = 10
                self.maxFrame = 10
                if (LEFT or RIGHT) and UP:
                    self.state = "UFDH"
                elif (LEFT or RIGHT) and DOWN:
                    self.state = "DFDH"
                elif LEFT or RIGHT:
                    self.state = "FDSH"
                elif UP:
                    self.state = "UDSH"
                elif DOWN and not(UP):
                    self.state = "DDSH"
        if ATTACK and self.wallGrab == 0:
            if self.grounded == 1 and self.state == 0:
                # Jab #
                if not(LEFT) and not(RIGHT) and not(DOWN): 
                    if self.character == 0:
                        self.frame = 15
                        self.maxFrame = 15
                        self.state = "JAB"
                        self.attackTimer = 30
                    elif self.character == 1:
                        self.frame = 8
                        self.maxFrame = 8
                        self.state = "JAB"
                    elif self.character == 2:
                        self.frame = 6
                        self.maxFrame = 6
                        self.state = "JAB"
                # Dtilt #
                elif DOWN:
                    if self.character == 0 or self.character == 1:
                        self.frame = 18
                        self.maxFrame = 18
                        self.state = "DTILT"
                    elif self.character == 2:
                        self.frame = 25
                        self.maxFrame = 25
                        self.state = "DTILT"
                # Ftilt #
                elif (LEFT or RIGHT) and self.dashing == 0:
                    self.frame = 20
                    self.maxFrame = 20
                    self.state = "FTILT"
                # Dash attack #
                elif (LEFT or RIGHT) and not(self.dashing == 0):
                    self.frame = 20
                    self.maxFrame = 20
                    self.state = "DASH"
            elif self.grounded != 1 and (self.state == 0 or self.state == "UFDH" or self.state == "DFDH" or self.state == "FDSH" or self.state == "UDSH" or self.state == "DDSH"):
                if self.state == "UFDH" or self.state == "DFDH" or self.state == "FDSH" or self.state == "UDSH" or self.state == "DDSH":
                    self.no_special = 1
                # Nair #
                if not(LEFT) and not(RIGHT) and not(DOWN) and not(UP):
                    self.frame = 15
                    self.maxFrame = 15
                    self.state = "NAIR"
                # Dair #
                elif DOWN:
                    if self.character == 0:
                        self.frame = 20
                        self.maxFrame = 20
                        self.state = "DAIR"
                    elif self.character == 1:
                        self.frame = 25
                        self.maxFrame = 25
                        self.state = "DAIR"
                    elif self.character == 2:
                        self.frame = 25
                        self.maxFrame = 25
                        self.state = "DAIR"
                # Uair #
                elif UP:
                    if self.character == 0:
                        self.frame = 18
                        self.maxFrame = 18
                        self.state = "UAIR"
                    elif self.character == 1:
                        self.frame = 25
                        self.maxFrame = 25
                        self.state = "UAIR"
                    elif self.character == 2:
                        self.frame = 25
                        self.maxFrame = 25
                        self.state = "UAIR"
                # Fair #
                elif LEFT or RIGHT and not(DOWN):
                    self.frame = 15
                    self.maxFrame = 15
                    self.state = "FAIR"
        # Attacks #
        if self.character == 0:
            if self.state == "JAB":
                if self.frame > 11 and self.frame < 14:
                    if ATTACK and self.attackTimer > 0:
                        self.attackTimer -= 1
                        self.charge += 1
                        if self.frame < 13:
                            self.frame += 1
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, 30, 15, 30, 15, self.charge + 10, self.charge + 1, 6, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, self.charge + 5, 0)
                    self.charge = 0
            elif self.state == "FTILT":
                if self.frame > 9 and self.frame < 14:
                    self.Attack = self.attack(self, 30, 10, 40, 20, 10, 20, 8, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
            elif self.state == "DTILT":
                if self.frame > 5 and self.frame < 10:
                    self.VX = 7 * self.facing
                if self.frame > 8 and self.frame < 12:
                    self.Attack = self.attack(self, 30, 15, 40, 60, 10, 15, 4, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
                if self.frame < 6:
                    if (RIGHT or LEFT) and not(RIGHT and LEFT):
                        self.facing = (RIGHT - LEFT)
            elif self.state == "DASH":
                if self.frame > 7 and self.frame < 12:
                    self.VX = CharacterRunSpeed[self.character] * self.facing
                    self.Attack = self.attack(self, 30, 25, 40, 40, 10, 24, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
                    self.dashing = 0
            elif self.state == "NAIR":
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, -10, 5, 50, 50, 10, 10, -10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 18, 0)
            elif self.state == "DAIR":
                if self.frame > 5 and self.frame < 9:
                    self.Attack = self.attack(self, 15, 35, 30, 40, 10, 0, 12, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 25, 0)  
            elif self.state == "UAIR":
                if self.frame > 3 and self.frame < 7:
                    self.Attack = self.attack(self, -15, -15, 80, 40, 18, 0, -16, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
            elif self.state == "FAIR":
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, 40, 15, 40, 30, 10, 22.5, -7.5, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)
            elif self.state == "SPCN":
                if self.frame == 30:
                    self.projectile(self.X, self.Y + 10, 5, 5, (4 + self.charge) * self.facing, -5, 0.98, 1, 0.5, 60, self.playerNumber, 5, 10, 5, self.facing, 1, 6, 0, 0, 2)
                if self.frame == 13 and self.charge < 10 and ATTACK and SHIELD:
                    self.charge += 1
                    self.frame = 15
                    self.projectile(self.X - (10 * self.facing), self.Y + 10, 5, 5, (4 + self.charge) * self.facing, -5, 0.98, 1, 0.5, 60, self.playerNumber, 5, 10, 5, self.facing, 1, 6, 0, 0, 2)
                if self.frame == 10:
                    self.Projectile = self.projectile(self.X, self.Y, 10, 10, (4 + self.charge) * self.facing, -5, 0.98, 1, 0.5, 60, self.playerNumber, 5, 10, 5, self.facing, 1, 2, 0, 0, 2)
                if self.frame == 1:
                    self.charge = 0
            elif self.state == "SPCD":
                if self.frame >= 4 and self.frame <= 6:
                    self.Attack = self.attack(self, 40, 10, 40, 30, 50, 30, -15, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)
            elif self.state == "EX":
                if self.frame == 20:
                    self.Projectile = self.projectile(self.X, self.Y, 20, 20, 8 * self.facing, -3, 0.98, 1, 0.5, 60, self.playerNumber, 0, 0, 0, self.facing, 1, 4, 0, 1, 12)
            elif self.state == "SHLD":
                self.shielding = 1
                if SHIELD and self.grounded and self.state != "HIT":
                    self.frame += 1
            elif self.state == "FDSH":
                if self.frame > 3:
                    self.VX = 15 * self.facing
                    self.VY = 0
            elif self.state == "UDSH":
                if self.frame > 3:
                    self.VX = 0
                    self.VY = -15
            elif self.state == "DDSH":
                if self.frame > 3:
                    self.VX = 0
                    self.VY = 15
            elif self.state == "UFDH":
                if self.frame > 3:
                    self.VX = 10 * self.facing
                    self.VY = -10
            elif self.state == "DFDH":
                self.wavedash = 5
                if self.frame > 3:
                    self.VX = 10 * self.facing
                    self.VY = 10
            if self.state == 2 + self.playerNumber * 2:
                if self.frame == 13:
                    self.Attack = self.attack(self, 30, 10, 40, 20, 0, 0, 0, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 0, self.state)
                if self.frame == 18:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 2 * self.facing
                            pl.Y = self.Y - 2
                if self.frame == 17:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 10 * self.facing
                            pl.Y = self.Y - 10
                if self.frame == 16:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 20 * self.facing
                            pl.Y = self.Y - 20
                elif self.frame > 4:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 30 * self.facing
                            pl.Y = self.Y - 30
                if self.frame == 4:
                    if any([pl.state == self.state - 1 for pl in players]):
                        self.attack(self, 30, -30, 40, 20, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
        if self.character == 1:
            if self.state == "JAB":
                if self.frame > 3 and self.frame < 6:
                    self.Attack = self.attack(self, 40, 20, 30, 15, 0.5, 1, -0.1, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, self.charge + 5, 0)
                    if ATTACK:
                        self.frame = 7
            elif self.state == "FTILT":
                if self.frame > 9 and self.frame < 14:
                    self.Attack = self.attack(self, 50, 5, 40, 40, 10, 8, -8, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 18, 0)
            elif self.state == "DTILT":
                if self.frame > 8 and self.frame < 12:
                    self.Attack = self.attack(self, 40, 30, 45, 10, 10, 0, -9, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 20, 0)
                if self.frame < 6:
                    if (RIGHT or LEFT) and not(RIGHT and LEFT):
                        self.facing = (RIGHT - LEFT)
            elif self.state == "DASH":
                if self.frame > 7 and self.frame < 12:
                    self.VX = CharacterRunSpeed[self.character] * self.facing
                    self.Attack = self.attack(self, 45, 10, 40, 30, 10, 5, 20, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
                    self.dashing = 0
            elif self.state == "NAIR":
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, 5, 10, 50, 50, 10, 15, -12, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 15, 0)
            elif self.state == "DAIR":
                if self.frame > 15 and self.frame < 18:
                    self.Attack = self.attack(self, 0, 30, 60, 50, 5, 0, self.VY / 2, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
                if self.frame > 7 and self.frame < 10:
                    self.Attack = self.attack(self, 0, 30, 60, 50, 10, 0, 17, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)  
            elif self.state == "UAIR":
                if self.frame > 15 and self.frame < 18:
                    self.Attack = self.attack(self, 10, -15, 35, 60, 10, 0, self.VY / 2, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
                if self.frame > 7 and self.frame < 11:
                    self.Attack = self.attack(self, 10, -15, 35, 60, 10, 0, -16, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
            elif self.state == "FAIR":
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, 30, 0, 75, 60, 10, 22.5, -7.5, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)
            elif self.state == "SPCN":
                if self.frame == 14:
                    self.Projectile = self.projectile(self.X, self.Y, 10, 10, 8 * self.facing, 0, 1, 0, 0, 30, self.playerNumber, 5, 10, 5, self.facing, 1, 1, 0, 0, 5)
            elif self.state == "SPCD":
                if self.frame == 20 or self.frame == 40 or self.frame == 60 or self.frame == 80:
                    self.charge = 10
                elif not((ATTACK and SHIELD) or SPECIAL):
                    self.charge -= 1 if self.charge > 0 else 0
                if self.frame == 15 or self.frame == 35 or self.frame == 55:
                    self.Attack = self.attack(self, 30, 5, 55, 45, 5, 0, self.VY, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 16, 0) 
                if ((ATTACK and SHIELD) or SPECIAL) and self.charge < 9 and (self.frame <= 14 or (self.frame <= 34 and self.frame >= 21) or (self.frame <= 54 and self.frame >= 41)):
                    if self.frame <= 14:
                        self.frame = 40
                    elif self.frame <= 34 and self.frame >= 21:
                        self.frame = 60
                    else:
                        self.frame = 80
                if self.frame == 73:
                    self.Attack = self.attack(self, 30, 5, 55, 45, 10, 10, -5, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
                if self.frame == 21 or self.frame == 41 or self.frame == 61 or self.frame == 71:
                    self.frame = 0
            elif self.state == "EX":
                if self.frame == 20:
                    self.Projectile = self.projectile(self.X, self.Y, 20, 20, 8 * self.facing, -3, 0.98, 1, 0.5, 60, self.playerNumber, 0, 0, 0, self.facing, 1, 4, 0, 1, 12)
            elif self.state == "SHLD":
                self.shielding = 1
                if SHIELD and self.grounded and self.state != "HIT":
                    self.frame += 1
            elif self.state == "FDSH":
                if self.frame > 3:
                    self.VX = 15 * self.facing
                    self.VY = 0
            elif self.state == "UDSH":
                if self.frame > 3:
                    self.VX = 0
                    self.VY = -15
            elif self.state == "DDSH":
                if self.frame > 3:
                    self.VX = 0
                    self.VY = 15
            elif self.state == "UFDH":
                if self.frame > 3:
                    self.VX = 10 * self.facing
                    self.VY = -10
            elif self.state == "DFDH":
                self.wavedash = 5
                if self.frame > 3:
                    self.VX = 10 * self.facing
                    self.VY = 10
            if self.state == 2 + self.playerNumber * 2:
                if self.frame == 13:
                    self.Attack = self.attack(self, 20, 10, 40, 20, 0, 0, 0, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 0, self.state)
                if self.frame == 18:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 2 * self.facing
                            pl.Y = self.Y - 2
                if self.frame == 17:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 10 * self.facing
                            pl.Y = self.Y - 10
                if self.frame == 16:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 20 * self.facing
                            pl.Y = self.Y - 20
                elif self.frame > 4:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 30 * self.facing
                            pl.Y = self.Y - 30
                if self.frame == 4:
                    if any([pl.state == self.state - 1 for pl in players]):
                        self.attack(self, 30, -30, 40, 20, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
        elif self.character == 2:
            if self.state == "JAB":
                if self.frame > 3 and self.frame < 6:
                    self.Attack = self.attack(self, 20, 0, 30, 15, 2, 2, -0.1, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
                    if ATTACK:
                        self.frame = 12
            elif self.state == "FTILT":
                if self.frame > 9 and self.frame < 14:
                    self.Attack = self.attack(self, 20, 0, 25, 25, 8, 8, -8, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 18, 0)
            elif self.state == "DTILT":
                if self.frame > 12 and self.frame < 14:
                    self.Attack = self.attack(self, 40, 15, 50, 9, 10, 0, -9, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 20, 0)
                if self.frame < 6:
                    if (RIGHT or LEFT) and not(RIGHT and LEFT):
                        self.facing = (RIGHT - LEFT)
            elif self.state == "DASH":
                if self.frame > 7 and self.frame < 12:
                    self.VX = CharacterRunSpeed[self.character] * self.facing
                    self.Attack = self.attack(self, 20, 0, 25, 25, 12, 8, -8, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 18, 0)
                    self.dashing = 0
            elif self.state == "NAIR":
                if (self.frame > 10 and self.frame < 12) or (self.frame > 7 and self.frame < 9):
                    self.Attack = self.attack(self, 5, 10, 50, 50, 3, 0, self.VY / 2, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 15, 0)
                if (self.frame > 4 and self.frame < 6):
                    self.Attack = self.attack(self, 5, 10, 50, 50, 5, 5, -11.5, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 15, 0)
            elif self.state == "DAIR":
                if self.frame == 20:
                    self.Attack = self.attack(self, 0, 30, 40, 20, 0, 0, 0, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 0, 1000)
                if self.frame == 19:
                    for pl in players:
                        if pl.state == 999:
                            pl.X = self.X
                            pl.Y = self.Y + 50
                if self.frame > 5 and self.frame < 19:
                    for pl in players:
                        if pl.state == 999:
                            pl.VX = self.VX
                            pl.VY = self.VY
                if self.frame == 5:
                    self.Attack = self.attack(self, 0, 30, 40, 40, 10, 0, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
            elif self.state == "UAIR":
                if self.frame > 13 and self.frame < 16:
                    self.Attack = self.attack(self, -30, 0, 55, 30, 10, 0, -10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
                elif self.frame > 11 and self.frame < 14:
                    self.Attack = self.attack(self, -15, -15, 30, 30, 10, 0, -10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)
                    self.Attack = self.attack(self, -28, -30, 30, 30, 10, 0, -10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)  
                elif self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, -5, -25, 30, 30, 10, 0, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)
                    self.Attack = self.attack(self, -9, -35, 30, 30, 10, 0, -10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)  
                elif self.frame > 7 and self.frame < 10:
                    self.Attack = self.attack(self, 18, -25, 30, 30, 10, 0, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)
                    self.Attack = self.attack(self, 13, -35, 30, 30, 10, 0, -10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
            elif self.state == "FAIR":
                if self.frame == 12:
                    self.charge = self.VX
                if self.frame > 9 and self.frame < 12:
                    if self.frame == 11:
                        self.VX = 12 * self.facing
                    self.Attack = self.attack(self, 30, 0, 30, 25, 10, 22.5, -7.5, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)
            elif self.state == "SPCN":
                if self.frame == 14:
                    self.Projectile = self.projectile(self.X, self.Y, 10, 10, 8 * self.facing, 0, 1, 0, 0, 30, self.playerNumber, 5, 10, 5, self.facing, 1, 1, 0, 0, 5)
            elif self.state == "SPCD":
                if self.frame == 20 or self.frame == 40 or self.frame == 60 or self.frame == 80:
                    self.charge = 10
                elif not((ATTACK and SHIELD) or SPECIAL):
                    self.charge -= 1 if self.charge > 0 else 0
                if self.frame == 15 or self.frame == 35 or self.frame == 55:
                    self.Attack = self.attack(self, 30, 5, 55, 45, 5, 0, self.VY, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 16, 0) 
                if ((ATTACK and SHIELD) or SPECIAL) and self.charge < 9 and (self.frame <= 14 or (self.frame <= 34 and self.frame >= 21) or (self.frame <= 54 and self.frame >= 41)):
                    if self.frame <= 14:
                        self.frame = 40
                    elif self.frame <= 34 and self.frame >= 21:
                        self.frame = 60
                    else:
                        self.frame = 80
                if self.frame == 73:
                    self.Attack = self.attack(self, 30, 5, 55, 45, 10, 10, -5, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
                if self.frame == 21 or self.frame == 41 or self.frame == 61 or self.frame == 71:
                    self.frame = 0
            elif self.state == "EX":
                if self.frame == 20:
                    self.Projectile = self.projectile(self.X, self.Y, 20, 20, 8 * self.facing, -3, 0.98, 1, 0.5, 60, self.playerNumber, 0, 0, 0, self.facing, 1, 4, 0, 1, 12)
            elif self.state == "SHLD":
                self.shielding = 1
                if SHIELD and self.grounded and self.state != "HIT":
                    self.frame += 1
            elif self.state == "FDSH":
                if self.frame > 3:
                    self.VX = 15 * self.facing
                    self.VY = 0
            elif self.state == "UDSH":
                if self.frame > 3:
                    self.VX = 0
                    self.VY = -15
            elif self.state == "DDSH":
                if self.frame > 3:
                    self.VX = 0
                    self.VY = 15
            elif self.state == "UFDH":
                if self.frame > 3:
                    self.VX = 10 * self.facing
                    self.VY = -10
            elif self.state == "DFDH":
                self.wavedash = 5
                if self.frame > 3:
                    self.VX = 10 * self.facing
                    self.VY = 10
            if self.state == 2 + self.playerNumber * 2:
                if self.frame == 13:
                    self.Attack = self.attack(self, 20, 10, 40, 20, 0, 0, 0, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 0, self.state)
                if self.frame == 18:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 2 * self.facing
                            pl.Y = self.Y - 2
                if self.frame == 17:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 10 * self.facing
                            pl.Y = self.Y - 10
                if self.frame == 16:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 20 * self.facing
                            pl.Y = self.Y - 20
                elif self.frame > 4:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 30 * self.facing
                            pl.Y = self.Y - 30
                if self.frame == 4:
                    if any([pl.state == self.state - 1 for pl in players]):
                        self.attack(self, 30, -30, 40, 20, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
        if self.frame <= 0:
            self.frame = 0
            self.state = 0
        self.wavedash -= 1 if self.wavedash > 0 else 0
        if self.frame == 1 and self.no_special == 1:
            self.no_special = 0
        # Movement #
        if self.frame == 0:
                if self.frame == 0:
                    self.state = 0
                    self.maxFrame = 0
                # Dash #
                if LEFT:
                    if self.dashTimer < 0 and self.dashTimer > -9:
                        self.dashing = -1
                    else:
                        self.dashTimer = -10
                if RIGHT:
                    if self.dashTimer > 0 and self.dashTimer < 9:
                        self.dashing = 1
                    else:
                        self.dashTimer = 10
                self.dashTimer -= 1 if self.dashTimer > 0 else -1 if self.dashTimer < 0 else 0
                if not(RIGHT) and not(LEFT) or LEFT and RIGHT or not(self.grounded == 1):
                    self.dashing = 0
                # Facing check #
                if (RIGHT or LEFT) and not(RIGHT and LEFT):
                    self.facing = (RIGHT - LEFT)
                elif RIGHT and LEFT:
                    self.facing = 1
                # Filght update #
                if self.grounded == 1:
                    self.flight = CharacterFlight[self.character]
                # Jump #
                if UP and self.grounded and self.wallGrab == 0 and self.wavedash == 0:
                    self.VY = -10 * CharacterJumpHeight[self.character]
                    self.jumpTimer = 10
                    self.flightTimer = 20
                    self.wallGrab = 0
                # Wall jump #
                elif UP and self.coyote > 0:
                    self.coyote = 0
                    self.VY = -10 * CharacterJumpHeight[self.character]
                    self.VX = -5 if self.LEFT else 5
                    self.flight = CharacterFlight[self.character]
                    self.jumpTimer = 10
                    self.flightTimer = 20
                    self.wallGrab = 0
                # Climb #
                elif (self.touchingWall == True) and (CharacterClimb[self.character] == 1) and (not(self.wallGrab == 0)):
                    self.VY = (DOWN - UP) * 3
                # progressive jump #
                elif UP and not(self.grounded) and self.jumpTimer > 0:
                    self.VY -= 1
                # Flight #
                elif UP and not(self.grounded) and self.flight > 0 and self.flightTimer == 0 and self.wallGrab == 0:
                    self.VY -= 2 if self.VY > 0 else 1.5
                    if self.VY < -8:
                        self.VY = -8
                    self.flight -= 1 if self.flight > 0 else 0
                # Wavedash #
                elif UP and self.grounded and self.wallGrab == 0 and self.wavedash:
                    self.VY = 5
                    self.VX = 10 * self.facing
                    self.dashed = 1
        else:
            self.frame -= 1
        # Walk #
        if not(DOWN and self.grounded == 1) and (self.state == 0 or self.state == "FAIR"):
            self.VX += ((RIGHT - LEFT - self.dashing) * CharacterWalkSpeed[self.character] if self.dashing == 0 else CharacterRunSpeed[self.character] * -1 if self.VX < 0 else CharacterRunSpeed[self.character]) if self.grounded == 1 else (RIGHT - LEFT) * CharacterAirSpeed[self.character]
        # Friction #
        self.VX *= 0.7 if self.grounded == 1 else 0.9
        # Gravity #
        if self.state != "HIT" and self.state != "FDSH":
            self.VY += (CharacterGravity[self.character] * 1.5 if DOWN else CharacterGravity[self.character] * 1) if self.wallGrab == 0 else (0.6 * CharacterGravity[self.character]) if (CharacterClimb[self.character] == 0 and self.wallGrab != 0) else 0
        elif self.state == "HIT":
            self.VY += CharacterGravity[self.character] * 0.6
        # Fall and fastfall #
        if self.state != "HIT":
            if self.VY > 10 and self.wallGrab == 0 and not(DOWN):
                self.VY = 10
            elif self.VY > 15 and self.wallGrab == 0 and DOWN:
                self.VY = 15
        # Wall slide #
        if self.VY > 2 and self.wallGrab == 1 or self.VY > 2 and self.wallGrab == -1:
            self.VY = 2
        # Update variables #
        self.jumpTimer -= 1 if self.jumpTimer > 0 else 0
        self.flightTimer -= 1 if self.flightTimer > 0 else 0
        self.coyote -= 1 if self.coyote > 0 else 0
        self.collide()
    def collide(self):
        # Update Hitboxes#
        self.wallHitbox = pygame.Rect(self.X -1, self.Y, self.sizeX + 2, self.sizeY)
        if self.DOWN:
            self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 1, self.sizeX, 1)
        else:
            self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 10, self.sizeX, 10)
        # X collision #
        self.X += self.VX
        self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
        self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY, self.sizeX, 10)
        collided = any(self.hitbox.colliderect(rect) for rect in block)
        while any(self.hitbox.colliderect(rect) for rect in block):
            self.X -= 0.1 if self.VX > 0 else -0.1
            self.wallStopDir = 1 if self.VX > 0 else -1
            self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
            self.wallHitbox = pygame.Rect(self.X -1, self.Y, self.sizeX + 2, self.sizeY)
            if self.DOWN:
                self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 1, self.sizeX, 1)
            else:
                self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 10, self.sizeX, 10)
        # Wall bounce #
        if collided:
            if (self.VX > 10 or self.VX < -10) and self.state == "HIT":
                self.VX *= -0.8
            else:
                self.VX = 0
            # Wall grab gravity #
            if self.wallGrab == 0:
                self.VY = 0
            # Wall grab update #
            if (self.RIGHT and self.wallStopDir == 1 or self.LEFT and self.wallStopDir == -1) and self.wallGrabTimer == 0 and not(self.grounded) and self.touchingWall == 1:
                self.wallGrab = self.wallStopDir
        # Wall drop #
        if self.wallGrab == 1 and not(self.RIGHT) or self.wallGrab == -1 and not(self.LEFT):
            self.coyote = 10
            self.wallGrab = 0
            self.wallStopDir = 0
            self.dashed = 0
            self.flight = CharacterFlight[self.character]
        # No more wall #
        elif self.touchingWall == 0:
            self.wallGrab = 0
            self.wallStopDir = 0
        self.wallGrabTimer -= 1 if self.wallGrabTimer > 0 else 0
        # Y collision #
        self.Y += self.VY
        self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
        self.wallHitbox = pygame.Rect(self.X -1, self.Y, self.sizeX + 2, self.sizeY)
        if self.DOWN:
            self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 1, self.sizeX, 1)
        else:
            self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 10, self.sizeX, 10)
        collided = any(self.hitbox.colliderect(rect) for rect in block)
        if collided:
            if self.VY > (CharacterGravity[self.character] * 20):
                self.VY *= 0.8
        #Landing cancel#
            elif self.frame > 0 and self.VY > 3 and self.state != "EX" and self.state != "HIT" and self.state != "SHLD" and self.state != "SPCN" and self.state != "SPCD":
                self.state = 0
                self.frame = 0
        while any(self.hitbox.colliderect(rect) for rect in block):
            self.Y -= 0.1 if self.VY > 0 else -0.1
            self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
            self.wallHitbox = pygame.Rect(self.X -1, self.Y, self.sizeX + 2, self.sizeY)
            if self.DOWN:
                self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 1, self.sizeX, 1)
            else:
                self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 10, self.sizeX, 10)
        if any(self.platHitbox.colliderect(rect)for rect in platforms) and self.VY >= 0 and not(self.DOWN):
            self.VY = 0
            while any(self.hitbox.colliderect(rect)for rect in platforms):
                self.Y -= 0.1
                self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
                self.wallHitbox = pygame.Rect(self.X -1, self.Y, self.sizeX + 2, self.sizeY)
                if self.DOWN:
                    self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 1, self.sizeX, 1)
                else:
                    self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 10, self.sizeX, 10)
            self.Y += 1
            self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
            self.wallHitbox = pygame.Rect(self.X -1, self.Y, self.sizeX + 2, self.sizeY)
            if self.DOWN:
                self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 1, self.sizeX, 1)
            else:
                self.platHitbox = pygame.Rect(self.X, self.Y + self.sizeY - 10, self.sizeX, 10)
            self.grounded = True
            self.flight = CharacterFlight[self.character]
        if collided or (any(self.platHitbox.colliderect(rect)for rect in platforms) and self.VY >= 0):
            self.VY = 0
            self.grounded = True
            self.bounced = 0
            self.dashed = 0
        else:
            self.grounded = False
        if self.Y > 700:
            self.blastzone("Y")
        if self.X > 1200 or self.X < -400:
            self.blastzone("X")
        self.touchingWall = any(self.wallHitbox.colliderect(rect) for rect in block)
    def checkAttacks(self):
            for attack in attacks:
                if self.hitbox.colliderect(attack[0]) and not(attack[5] == self.playerNumber):
                    if self.gotHit == 0 and self.DgotHit == 0 and attack[9] <= 0 or (attack[6] == 1 and self.DgotHit == 0) and attack[9] <= 0:
                        if self.state != "SHLD":
                            self.VX = attack[2]
                            self.VY = attack[3]
                            particle(self.X, self.Y, 1)
                            self.frame = attack[8]
                            if self.frame < 0:
                                self.frame = 10
                            self.state = "HIT"
                            if self.grounded == 1 and attack[3] > 0:
                                self.VY = attack[3] * -1 * 0.8
                            self.HP -= attack[1]
                            self.HPHealing += attack[1] * 0.5
                            self.HPHealTimer = 30
                            if self.HPHealing > 20:
                                self.HPHealing = 20
                            if self.HP <= 0:
                                self.revive()
                            if attack[6] == 1:
                                self.DgotHit = 2
                            else:
                                self.gotHit += 2
                            if attack[7] == 0:
                                players[attack[5]].superMeter += attack[1]
                        else:
                            self.shieldHP -= attack[1]
                            if attack[6] == 1:
                                self.DgotHit = 2
                            else:
                                self.gotHit += 2
                            if self.shieldHP <= 0:
                                self.state = "HIT"
                                self.frame = 200
                                self.VY = -20
                                self.shieldHP = 30
                    elif self.gotHit == 1 and attack[9] == 0:
                        self.gotHit += 1
                    elif attack[9] >= 1:
                        self.state = attack[9] - 1
                        self.frame = 100
                    self.p = players[attack[5]]
                    if self.p.superMeter > 100:
                        self.p.superMeter = 100
            self.gotHit -= 1 if self.gotHit > 0 else 0
            self.DgotHit -= 1 if self.DgotHit > 0 else 0
            self.HPHealTimer -= 1 if self.HPHealTimer > 0 else 0
            self.shieldHPHealTimer -= 1 if self.shieldHPHealTimer > 0 else 0
            if self.HPHealTimer == 0 and self.HPHealing > 0 and self.HPHealTimer == 0:
                self.HP += 1
                self.HPHealing -= 1
                self.HPHealTimer = 30
            if self.shieldHP < 50 and self.shieldHPHealTimer == 0:
                self.shieldHPHealTimer = 10
                self.shieldHP += 1
    def revive(self):
            global killcount
            self.X = 425
            self.Y = 0
            self.VX = 0
            self.VY = 0
            self.HP = CharacterHP[self.character]
            self.HPHealTimer = 0
            self.HPHealing = 0
            self.frame = 0
            if self.playerNumber == 0:
                killcount += 1
            elif self.playerNumber == 1:
                killcount -= 1
    def blastzone(self, type):
        self.type = type
        self.HP -= 30
        if self.type == "X":
            self.X = -380 if self.VX > 0 else 1180
            self.VX *= 2
        else:
            self.Y = 700 if self.VY < 0 else -100
            self.VY *= 2
        if self.HP <= 0:
            self.revive()
    def animation(self):
        if self.character == 0:
            if self.frame == 0:
                if self.grounded and abs(self.VX) < 1:
                    return 0, 0, -13
                elif self.grounded and abs(self.VX) >= 1:
                    self.animFrame += 1
                    if self.animFrame < 10:
                        return 0, 0, -13
                    elif self.animFrame >= 10 and self.animFrame < 20:
                        return 1, 0, -13
                    elif self.animFrame >= 20:
                        self.animFrame = 0
                        return 0, 0, -13
                elif self.grounded == 0 and self.flight < 30 and self.flight > 0 and self.UP:
                    self.animFrame += 1
                    if self.flight == 29:
                        self.animFrame = 0
                    if self.animFrame > 30:
                        return 10, 0, -13
                    elif self.animFrame > 27:
                        return 11, 0, -13
                    elif self.animFrame > 24:
                        return 10, 0, -13
                    elif self.animFrame > 21:
                        return 11, 0, -13
                    elif self.animFrame > 18:
                        return 10, 0, -13
                    elif self.animFrame > 15:
                        return 11, 0, -13
                    elif self.animFrame > 12:
                        return 10, 0, -13
                    elif self.animFrame > 9:
                        return 11, 0, -13
                    elif self.animFrame > 6:
                        return 10, 0, -13
                    elif self.animFrame > 3:
                        return 11, 0, -13
                    else:
                        return 11, 0, -13
                else:
                    return 6, 0, -13
            else:
                if self.state == "JAB":
                    if self.frame > 10:
                        return 2, 0, -13
                    else:
                        return 3, 0, -13
                elif self.state == "FTILT":
                    if self.frame > 10:
                        return 4, 0, -13
                    else:
                        return 5, 20, -13
                elif self.state == "NAIR":
                    if (self.frame // 2) % 2 == 0:
                        return 14, 0, -13
                    else:
                        return 15, 0, -13
                elif self.state == "DAIR":
                    if self.frame > 10:
                        return 7, 0, -13
                    else:
                        return 8, 0, -13
                elif self.state == "SPCN" or self.state == "EX":
                    return 12, 0, -13
                elif self.state == "SHLD":
                    return 13, 0, -13
                else:
                    return 5, 0, -13
        elif self.character == 1:
            if self.frame == 0:
                if self.grounded and abs(self.VX) < 1:
                    return 0, 0, -18
                elif self.grounded and abs(self.VX) >= 1:
                    self.animFrame += 1
                    if self.animFrame < 10:
                        return 0, 0, -18
                    elif self.animFrame >= 10 and self.animFrame < 20:
                        return 1, 0, -18
                    elif self.animFrame >= 20:
                        self.animFrame = 0
                        return 0, 0, -18
            else:
                if self.state == "JAB":
                    self.animFrame += 1
                    if self.animFrame >= 3:
                        if self.animFrame >= 5:
                            self.animFrame = 0
                        return 2, 0, -18
                    else:
                        return 0, 0, -18
                elif self.state == "FTILT":
                    if self.frame >= 13 and self.frame <= 15:
                        return 3, 0, -18
                    elif self.frame >= 8 and self.frame <= 12:
                        return 2, 0, -18
                elif self.state == "DTILT":
                    if self.frame >= 7 and self.frame <= 11:
                        return 4, 0, -18
            return 0, 0, -18
        return 0, 0, 0

def particle(X, Y, type):
    if type == 1:
        rand = random.randint(-10, 10)
        surf1 = pygame.Surface((100, 100), pygame.SRCALPHA)
        Xrand = random.randint(-30, 30)
        Yrand = random.randint(-30, 30)
        life = random.randint(-30, 30)
        pygame.draw.circle(surf1, (100, 100, 100, 255), (30 + rand, 30 + rand), 10)
        particles.append((surf1, life, X + Xrand, Y + Yrand, (1 if Xrand >= 0 else -1) * life, (1 if Yrand >= 0 else -1) * life, type))
        Xrand = random.randint(-30, 30)
        Yrand = random.randint(-30, 30)
        life = random.randint(-30, 30)
        particles.append((surf1, life, X + Xrand, Y + Yrand, (1 if Xrand >= 0 else -1) * life, (1 if Yrand >= 0 else -1) * life, type))
        Xrand = random.randint(-30, 30)
        Yrand = random.randint(-30, 30)
        life = random.randint(-30, 30)
        particles.append((surf1, life, X + Xrand, Y + Yrand, (1 if Xrand >= 0 else -1) * life, (1 if Yrand >= 0 else -1) * life, type))
def HomingTrail_0():
    points = []
    if len(homing) > 0:
        for p in homing:
            if p[2] == homing[0][2]:
                if p[3] > 0:
                    homing[homing.index(p)] = (p[0], p[1], p[2], p[3] - 1)
                    p = (p[0], p[1], p[2], p[3] - 1)
                    points.append((((p[0] - CamX) * CamZ + 400), ((p[1] - CamY) * CamZ) + 300))
                    if len(points) > 1:
                        pygame.draw.lines(screen, (0, 0, 255), False, points, 6)
                        pygame.draw.lines(screen, (150, 150, 255), False, points, 4)
                else:
                    homing.remove(p)
players = [player(200, 0, int(input("Player 0 character(0-2): ")), 0), player(600, 0, int(input("Player 1 character(0-2): ")), 1)]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    attacks = []
    keys = pygame.key.get_pressed()
    DT = pygame.time.Clock().tick(60) / 60 * 100
    screen.fill((255, 255, 255))
    #camera#
    MaxPLX = float("-inf") 
    MinPLX = float("inf") 
    MaxPLY = float("-inf") 
    MinPLY = float("inf")
    for pl in players:
        if pl.X > MaxPLX:
            MaxPLX = pl.X
        if pl.X < MinPLX:
            MinPLX = pl.X
        if pl.Y > MaxPLY:
            MaxPLY = pl.Y
        if pl.Y < MinPLY:
            MinPLY = pl.Y
    TargetX = (MaxPLX + MinPLX) / 2
    TargetY = (MaxPLY + MinPLY) / 2
    CamX += (TargetX - CamX) * 0.05
    CamY += (TargetY - CamY) * 0.05
    CamZX = MaxPLX - MinPLX + 200
    CamZY = MaxPLY - MinPLY + 400
    CamZ = 800 / max(1, CamZX, CamZY)
    CamZ = max(0.5, min(CamZ, 2))
    for pl in players:
        if pl.playerNumber == 0:
            pl.movement(keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d], keys[pygame.K_f], keys[pygame.K_g], keys[pygame.K_h], keys[pygame.K_j])
        elif pl.playerNumber == 1:
            pl.movement(keys[pygame.K_UP], keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_RIGHT], keys[pygame.K_COMMA], keys[pygame.K_PERIOD], keys[pygame.K_MINUS], keys[pygame.K_l])
        #flight bar#
        if not(pl.flight == CharacterFlight[pl.character]) and pl.grounded == 0 and pl.wallGrab == 0:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((pl.X + pl.hitbox.width / 2 - pl.flight - CamX) * CamZ + 400, (pl.Y - 75 / 2 - CamY) * CamZ + 300, (pl.flight * 2) * CamZ, 25 * CamZ))
    for proj in projectiles:
        proj.update()
    for pl in players:
        pl.checkAttacks()
    for attack in attacks:
        pygame.draw.rect(screen, (122 * attack[5] + 123, 0, 0), ((attack[0][0] - CamX) * CamZ + 400, (attack[0][1] - CamY) * CamZ + 300, attack[0][2] * CamZ, attack[0][3] * CamZ))
    for proj in projectiles:
        if proj.type == 2 and (proj.frame // 2) % 2 == 0 and proj.frame < 21:
            pygame.draw.rect(screen, (128, 0, 128), ((proj.attack[0] - CamX) * CamZ + 400, (proj.attack[1] - CamY) * CamZ + 300, proj.attack[2] * CamZ, proj.attack[3] * CamZ))
        else:
            pygame.draw.rect(screen, (0, 0, 0), ((proj.attack[0] - CamX) * CamZ + 400, (proj.attack[1] - CamY) * CamZ + 300, proj.attack[2] * CamZ, proj.attack[3] * CamZ))
    for particl in particles:
        if particl[6] == 1:
            particles[particles.index(particl)] = (particl[0], particl[1] - 1, particl[2], particl[3], particl[4] - ((particl[4] / abs(particl[4]) if particl[4] != 0 else 0)), particl[5] - (((particl[5] / abs(particl[5])) if particl[5] != 0 else 0.1)), particl[6])
            particl = (particl[0], particl[1] - 1, particl[2], particl[3], particl[4] - ((particl[4] / abs(particl[4]) if particl[4] != 0 else 0)), particl[5] - (((particl[5] / abs(particl[5])) if particl[5] != 0 else 0.1)), particl[6])
            particl[0].set_alpha(particl[1] * 255 / 20)
            if particl[1] <= 0:
                particles.pop(particles.index(particl))
            screen.blit(pygame.transform.scale_by(particl[0], CamZ), ((particl[2] - particl[4] - CamX) * CamZ + 400, (particl[3] - particl[5] - CamY) * CamZ + 300))
    HomingTrail_0()
    for blk in block:
        pygame.draw.rect(screen, (0, 255, 0), ((blk[0] - CamX) * CamZ + 400, (blk[1] - CamY) * CamZ + 300, blk[2] * CamZ, blk[3] * CamZ))
    for plat in platforms:
        pygame.draw.rect(screen, (0, 0, 255), ((plat[0] - CamX) * CamZ + 400, (plat[1] - CamY) * CamZ + 300, plat[2] * CamZ, plat[3] * CamZ))
    for pl in players:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(50 + 150 * pl.playerNumber, 550, pl.HP, 25))
        pygame.draw.rect(screen, (200, 255, 0), pygame.Rect(50 + 150 * pl.playerNumber, 580, (pl.shieldHP / 50) * CharacterHP[pl.character], 10))
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(50 + 150 * pl.playerNumber + pl.HP, 550, pl.HPHealing, 25))
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(50 + 150 * pl.playerNumber, 510, pl.superMeter, 25))
        pygame.draw.rect(screen, (0, 0, 255), ((pl.X - CamX) * CamZ + 400, (pl.Y - CamY) * CamZ + 300, pl.sizeX * CamZ, pl.sizeY * CamZ))
    for pl in players:
        screen.blit(pygame.transform.scale_by(pygame.transform.flip((bbbSprites[pl.animation()[0]] if pl.character == 0 else mantisSprites[pl.animation()[0]]), True if pl.facing == -1 else False, False), CamZ), ((((pl.X + pl.animation()[1] * pl.facing - CamX) * CamZ + 400, ((pl.Y + pl.animation()[2] - CamY) * CamZ + 300)))))
    pygame.display.flip()
    print(players[0].frame, players[0].state)
pygame.quit()