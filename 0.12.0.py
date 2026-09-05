import pygame 
import os
import random
os.chdir(os.path.abspath(os.path.dirname(__file__)))
pygame.init()
#player stats#
CharacterWalkSpeed = [2]
CharacterRunSpeed = [4]
CharacterAirSpeed = [0.7]
CharacterJumpHeight = [0.7]
CharacterGravity = [0.7]
CharacterFlight = [30]
CharacterClimb = [0]
CharacterHP = [100]
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
block = [pygame.Rect(0, 500, 800, 40), pygame.Rect(760, 0, 40, 600), pygame.Rect(0, 0, 40, 600)]
attacks = []
projectiles = []
particles = []
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
for sprite in bbbSprites:
    bbbSprites[bbbSprites.index(sprite)] = pygame.transform.scale(sprite, (sprite.get_width() * 3, sprite.get_height() * 3))
class player():
    def __init__(self, X, Y, character, playerNumber, sizeX, sizeY):
        self.character = character
        self.X = X
        self.Y = Y
        self.playerNumber = playerNumber
        self.VX = 0
        self.VY = 0
        self.sizeX = sizeX
        self.sizeY = sizeY
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
        self.shieldHP = 30
        self.animFrame = 0
        self.bounced = 0
        self.dashed = 1
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
                                if self.marck == 0:
                                    self.marck = self.frame
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
                        self.Attack = player.attack(self, -15, -15, 40, 40, 10, 0, 22, 0, self.sender, 1, pygame.Rect(self.X - 20, self.Y - 20, 40, 40), 0, 1, 5, 0)
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
        if SUPER and self.superMeter > 24 and self.state != 11:
            if self.state != 10:
                self.state = 10
                self.superMeter -= 25
                self.frame = 20
        # Special #
        if ATTACK and SHIELD and self.frame > (self.maxFrame - 3) and self.state != 11 or self.SPECIAL and self.state != 11:
            if self.state != 9:
                self.state = 9
                if self.playerNumber == 0:
                    self.frame = 30
                else:
                    self.frame = 15
        # Shield #
        if self.grounded == 1 and self.state != 11 and self.state != 9 and self.state != (19 + self.playerNumber * 2):
            if SHIELD and not(ATTACK):
                self.frame = 3
                self.maxFrame = 4
                self.state = 12
        # Grab #
        if self.grounded == 1 and self.state != 11 and self.state == 12:
            if DOWN:
                self.frame = 20
                self.maxFrame = 20
                self.state = 19 + self.playerNumber * 2
        # Airdodge #
        elif self.grounded == 0 and self.state != 11 and self.state != 9:
            if SHIELD and self.dashed == 0:
                self.dashed = 1
                self.frame = 10
                if (LEFT or RIGHT) and UP:
                    self.state = 16
                elif (LEFT or RIGHT) and DOWN:
                    self.state = 17
                elif LEFT or RIGHT:
                    self.state = 13
                elif UP:
                    self.state = 14
                elif DOWN and not(UP):
                    self.state = 15
        if ATTACK and self.frame == 0 and self.wallGrab == 0:
            if self.grounded == 1:
                # Jab #
                if not(LEFT) and not(RIGHT) and not(DOWN):
                    self.frame = 15
                    self.maxFrame = 15
                    self.state = 1
                    self.attackTimer = 30
                # Dtilt #
                elif DOWN:
                    self.frame = 18
                    self.maxFrame = 18
                    self.state = 3
                # Ftilt #
                elif (LEFT or RIGHT) and self.dashing == 0:
                    self.frame = 20
                    self.maxFrame = 20
                    self.state = 2
                # Dash attack #
                elif (LEFT or RIGHT) and not(self.dashing == 0):
                    self.frame = 20
                    self.maxFrame = 20
                    self.state = 4
            else:
                # Nair #
                if not(LEFT) and not(RIGHT) and not(DOWN) and not(UP):
                    self.frame = 15
                    self.maxFrame = 15
                    self.state = 5
                # Dair #
                elif DOWN:
                    self.frame = 20
                    self.maxFrame = 20
                    self.state = 6
                # Uair #
                elif UP:
                    self.frame = 18
                    self.maxFrame = 18
                    self.state = 7
                # Fair #
                elif LEFT or RIGHT and not(DOWN):
                    self.frame = 15
                    self.maxFrame = 15
                    self.state = 8
        # Attacks #
        if self.character == 0:
            if self.state == 1:
                if self.frame > 11 and self.frame < 14:
                    if ATTACK and self.attackTimer > 0:
                        self.attackTimer -= 1
                        self.charge += 1
                        if self.frame < 13:
                            self.frame += 1
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, 20, 0, 30, 15, self.charge + 10, self.charge + 1, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, self.charge + 5, 0)
                    self.charge = 0
            elif self.state == 2:
                if self.frame > 9 and self.frame < 14:
                    self.Attack = self.attack(self, 20, -5, 40, 20, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
            elif self.state == 3:
                if self.frame > 5 and self.frame < 10:
                    self.VX = 7 * self.facing
                if self.frame > 8 and self.frame < 12:
                    self.Attack = self.attack(self, 20, 0, 40, 60, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
                if self.frame < 6:
                    if (RIGHT or LEFT) and not(RIGHT and LEFT):
                        self.facing = (RIGHT - LEFT)
            elif self.state == 4:
                if self.frame > 7 and self.frame < 12:
                    self.VX = CharacterRunSpeed[self.character] * self.facing
                    self.Attack = self.attack(self, 20, 10, 40, 40, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
                    self.dashing = 0
            elif self.state == 5:
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, -20, -10, 50, 50, 10, 15, -12, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 15, 0)
            elif self.state == 6:
                if self.frame > 8 and self.frame < 12:
                    self.Attack = self.attack(self, -10, 60, 70, 60, 10, 0, 22, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)  
            elif self.state == 7:
                if self.frame > 7 and self.frame < 11:
                    self.Attack = self.attack(self, -10, -60, 80, 60, 10, 0, -22, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0) 
            elif self.state == 8:
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, 30, 0, 70, 60, 10, 22.5, -7.5, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 10, 0)
            elif self.state == 9:
                if self.playerNumber == 0:
                    if self.frame == 10:
                        if (RIGHT and self.facing == -1) or (LEFT and self.facing == 1):
                            self.Projectile = self.projectile(self.X, self.Y, 10, 10, 3 * self.facing, -8, 0.98, 1, 0.5, 60, self.playerNumber, 10, 10, 5, self.facing, 1, 2, 0, 0, 2)
                        else:
                            self.Projectile = self.projectile(self.X, self.Y, 10, 10, 8 * self.facing, -5, 0.98, 1, 0.5, 60, self.playerNumber, 10, 10, 5, self.facing, 1, 2, 0, 0, 2)
                elif self.playerNumber == 1:
                    if self.frame == 15:
                        self.Projectile = self.projectile(self.X, self.Y, 10, 10, 8 * self.facing, 0, 1, 0, 0, 30, self.playerNumber, 10, 10, 5, self.facing, 1, 1, 0, 0, 5)
            elif self.state == 10:
                if self.playerNumber == 0:
                    if self.frame == 20:
                        self.Projectile = self.projectile(self.X, self.Y, 20, 20, 8 * self.facing, -3, 0.98, 1, 0.5, 60, self.playerNumber, 0, 0, 0, self.facing, 1, 4, 0, 1, 12)
                elif self.playerNumber == 1:
                    if self.frame == 15:
                        self.Projectile = self.projectile(self.X, self.Y, 20, 20, 8 * self.facing, 0, 1, 0, 0, 30, self.playerNumber, 30, 10, 5, self.facing, 1, 3, 0, 1, 12)
            elif self.state == 12:
                self.shielding = 1
                if SHIELD and self.grounded and self.state != 11:
                    self.frame += 1
            elif self.state == 13:
                if self.frame > 3:
                    self.VX = 15 * self.facing
                    self.VY = 0
            elif self.state == 14:
                if self.frame > 3:
                    self.VX = 0
                    self.VY = -15
            elif self.state == 15:
                if self.frame > 3:
                    self.VX = 0
                    self.VY = 15
            elif self.state == 16:
                if self.frame > 3:
                    self.VX = 10 * self.facing
                    self.VY = -10
            elif self.state == 17:
                if self.frame > 3:
                    self.VX = 10 * self.facing
                    self.VY = 10
            if self.state == 19 + self.playerNumber * 2:
                if self.frame == 13:
                    self.Attack = self.attack(self, 20, -5, 40, 20, 0, 0, 0, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 0, self.state)
                if self.frame == 8:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 2 * self.facing
                            pl.Y = self.Y - 2
                if self.frame == 7:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 10 * self.facing
                            pl.Y = self.Y - 10
                if self.frame == 6:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 20 * self.facing
                            pl.Y = self.Y - 20
                if self.frame == 5:
                    for pl in players:
                        if pl.state == self.state - 1:
                            pl.X = self.X + 30 * self.facing
                            pl.Y = self.Y - 30
                if self.frame == 2:
                    if any([pl.state == self.state - 1 for pl in players]):
                        self.attack(self, 30, -30, 40, 20, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox, 0, 0, 8, 0)
        if self.frame < 0:
            self.frame = 0
            self.state = 0
        # Movement #
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
            # Walk #
            if not(DOWN and self.grounded == 1):
                self.VX += ((RIGHT - LEFT - self.dashing) * CharacterWalkSpeed[self.character] if self.dashing == 0 else CharacterRunSpeed[self.character] * -1 if self.VX < 0 else CharacterRunSpeed[self.character]) if self.grounded == 1 else (RIGHT - LEFT) * CharacterAirSpeed[self.character]
            # Facing check #
            if (RIGHT or LEFT) and not(RIGHT and LEFT):
                self.facing = (RIGHT - LEFT)
            elif RIGHT and LEFT:
                self.facing = 1
            # Filght update #
            if self.grounded == 1:
                self.flight = CharacterFlight[self.character]
            # Jump #
            if UP and self.grounded and self.wallGrab == 0:
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
        else:
            self.frame -= 1
        # Friction #
        self.VX *= 0.7 if self.grounded == 1 else 0.9
        # Gravity #
        if self.state != 13:
            self.VY += (CharacterGravity[self.character] * 1.5 if DOWN else CharacterGravity[self.character] * 1) if self.wallGrab == 0 else (0.6 * CharacterGravity[self.character]) if (CharacterClimb[self.character] == 0 and self.wallGrab != 0) else 0
        # Fall and fastfall #
        if self.state != 11:
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
        # X collision #
        self.X += self.VX
        self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
        collided = any(self.hitbox.colliderect(rect) for rect in block)
        while any(self.hitbox.colliderect(rect) for rect in block):
            self.X -= 0.1 if self.VX > 0 else -0.1
            self.wallStopDir = 1 if self.VX > 0 else -1
            self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
        # Wall bounce #
        if collided:
            if self.VX > 10 or self.VX < -10 and self.state < 13 and self.state != 0:
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
        collided = any(self.hitbox.colliderect(rect) for rect in block)
        if collided:
            if self.VY > (CharacterGravity[self.character] * 20):
                self.VY *= 0.8
        #Landing lag#
            if self.frame > 0 and self.VY > 3 and self.state != 10 and self.state != 11 and self.state != 12 and self.state != 9 and self.frame > self.maxFrame- self.maxFrame / 2:
                self.frame = 8
                self.state = 11
            elif self.frame > 0 and self.VY > 3 and self.state != 10 and self.state != 11 and self.state != 12 and self.state != 9:
                self.state = 0
                self.frame = 0
        while any(self.hitbox.colliderect(rect) for rect in block):
            self.Y -= 0.1 if self.VY > 0 else -0.1
            self.hitbox = pygame.Rect(self.X, self.Y, self.sizeX, self.sizeY)
        if collided:
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
        self.wallHitbox = pygame.Rect(self.X -1, self.Y, self.sizeX + 2, self.sizeY)
        self.touchingWall = any(self.wallHitbox.colliderect(rect) for rect in block)
    def checkAttacks(self):
            for attack in attacks:
                if self.hitbox.colliderect(attack[0]) and not(attack[5] == self.playerNumber):
                    if self.gotHit == 0 and self.DgotHit == 0 and attack[9] <= 0 or (attack[6] == 1 and self.DgotHit == 0) and attack[9] <= 0:
                        if self.state != 12:
                            self.VX = attack[2]
                            self.VY = attack[3]
                            particle(self.X, self.Y)
                            self.frame = attack[8]
                            if self.frame < 0:
                                self.frame = 10
                            self.state = 11
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
                                players[attack[5]].superMeter += round(attack[1] * 1)
                        else:
                            self.shieldHP -= attack[1]
                            if attack[6] == 1:
                                self.DgotHit = 2
                            else:
                                self.gotHit += 2
                            if self.shieldHP <= 0:
                                self.state = 11
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
            if self.HPHealTimer == 0 and self.HPHealing > 0 and self.HPHealTimer == 0:
                self.HP += 1
                self.HPHealing -= 1
                self.HPHealTimer = 30
    def revive(self):
            self.X = 425
            self.Y = 0
            self.VX = 0
            self.VY = 0
            self.HP = CharacterHP[self.character]
            self.HPHealTimer = 0
            self.HPHealing = 0
            self.frame = 0
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
        if self.frame == 0 and self.state == 0:
            if self.grounded and abs(self.VX) < 1:
                return 0, 0, 0
            elif self.grounded and abs(self.VX) >= 1:
                self.animFrame += 1
                if self.animFrame < 10:
                    return 0, 0, 0
                elif self.animFrame >= 10 and self.animFrame < 20:
                    return 1, 0, 0
                elif self.animFrame >= 20:
                    self.animFrame = 0
                    return 0, 0, 0
            elif self.grounded == 0 and self.flight < 30 and self.flight > 0 and self.UP:
                self.animFrame += 1
                if self.flight == 29:
                    self.animFrame = 0
                if self.animFrame > 30:
                    return 10, 0, 0
                elif self.animFrame > 27:
                    return 11, 0, 0
                elif self.animFrame > 24:
                    return 10, 0, 0
                elif self.animFrame > 21:
                    return 11, 0, 0
                elif self.animFrame > 18:
                    return 10, 0, 0
                elif self.animFrame > 15:
                    return 11, 0, 0
                elif self.animFrame > 12:
                    return 10, 0, 0
                elif self.animFrame > 9:
                    return 11, 0, 0
                elif self.animFrame > 6:
                    return 10, 0, 0
                elif self.animFrame > 3:
                    return 11, 0, 0
                else:
                    return 11, 0, 0
            else:
                return 6, 0, 0
        else:
            if self.state == 1:
                if self.frame > 10:
                    return 2, 0, 0
                else:
                    return 3, 0, 0
            elif self.state == 2:
                if self.frame > 10:
                    return 4, 0, 0
                else:
                    return 5, 20, 0
            elif self.state == 5:
                if (self.frame // 2) % 2 == 0:
                    return 14, 0, 0
                else:
                    return 15, 0, 0
            elif self.state == 6:
                if self.frame > 10:
                    return 7, 0, 0
                else:
                    return 8, 0, 0
            elif self.state == 9 or self.state == 10:
                return 12, 0, 0
            elif self.state == 12:
                return 13, 0, 0
            else:
                return 5, 0, 0
def particle(X, Y):
    rand = random.randint(-10, 10)
    surf1 = pygame.Surface((40, 40), pygame.SRCALPHA)
    Xrand = random.randint(-30, 30)
    Yrand = random.randint(-30, 30)
    life = random.randint(-30, 30)
    pygame.draw.circle(surf1, (100, 100, 100, 255), (30 + rand, 30 + rand), 10)
    particles.append((surf1, life, X + Xrand, Y + Yrand, (1 if Xrand >= 0 else -1) * life, (1 if Yrand >= 0 else -1) * life))
    Xrand = random.randint(-30, 30)
    Yrand = random.randint(-30, 30)
    life = random.randint(-30, 30)
    particles.append((surf1, life, X + Xrand, Y + Yrand, (1 if Xrand >= 0 else -1) * life, (1 if Yrand >= 0 else -1) * life))
    Xrand = random.randint(-30, 30)
    Yrand = random.randint(-30, 30)
    life = random.randint(-30, 30)
    particles.append((surf1, life, X + Xrand, Y + Yrand, (1 if Xrand >= 0 else -1) * life, (1 if Yrand >= 0 else -1) * life))
players = [player(400, 300, 0, 0, 35, 20), player(400, 300, 0, 1, 35, 20)]
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
        particles[particles.index(particl)] = (particl[0], particl[1] - 1, particl[2], particl[3], particl[4] - ((particl[4] / abs(particl[4]) if particl[4] != 0 else 0)), particl[5] - (((particl[5] / abs(particl[5])) if particl[5] != 0 else 0.1)))
        particl = (particl[0], particl[1] - 1, particl[2], particl[3], particl[4] - ((particl[4] / abs(particl[4]) if particl[4] != 0 else 0)), particl[5] - (((particl[5] / abs(particl[5])) if particl[5] != 0 else 0.1)))
        particl[0].set_alpha(particl[1] * 255 / 20)
        if particl[1] <= 0:
            particles.pop(particles.index(particl))
        screen.blit(pygame.transform.scale_by(particl[0], CamZ), ((particl[2] - particl[4] - CamX) * CamZ + 400, (particl[3] - particl[5] - CamY) * CamZ + 300))
    for blk in block:
        pygame.draw.rect(screen, (0, 255, 0), ((blk[0] - CamX) * CamZ + 400, (blk[1] - CamY) * CamZ + 300, blk[2] * CamZ, blk[3] * CamZ))
    for pl in players:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(50 + 150 * pl.playerNumber, 550, pl.HP, 25))
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(50 + 150 * pl.playerNumber + pl.HP, 550, pl.HPHealing, 25))
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(50 + 150 * pl.playerNumber, 510, pl.superMeter, 25))
        screen.blit(pygame.transform.scale_by(pygame.transform.flip(bbbSprites[pl.animation()[0]], True if pl.facing == -1 else False, False), CamZ), ((((pl.X + pl.animation()[1] * pl.facing - CamX) * CamZ + 400, ((pl.Y - 28 - CamY) * CamZ + 300)))))
    pygame.display.flip()
    print(players[0].state, players[0].frame)
pygame.quit()