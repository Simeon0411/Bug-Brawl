import pygame
pygame.init()
#player stats#
CharacterWalkSpeed = [2]
CharacterRunSpeed = [4]
CharacterAirSpeed = [0.6]
CharacterJumpHeight = [1]
CharacterGravity = [1]
CharacterFlight = [30]
CharacterClimb = [1]
CharacterHP = [100]
running = True
screen = pygame.display.set_mode((800, 600)) 
keys = pygame.key.get_pressed()
block = [pygame.Rect(0, 500, 800, 40), pygame.Rect(400, 460, 80, 80), pygame.Rect(400, 360, 80, 300), pygame.Rect(760, 0, 40, 600), pygame.Rect(0, 0, 40, 600)]
attacks = []
class player():
    def __init__(self, X, Y, character, playerNumber):
        self.character = character
        self.X = X
        self.Y = Y
        self.playerNumber = playerNumber
        self.VX = 0
        self.VY = 0
        self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
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
        self.facing = 0
        self.coyote = 0
        self.gotHit = 0
        self.HPHealing = 0
        self.HPHealTimer = 0
        self.HP = CharacterHP[self.character]
    class attack:
        def __init__(self, pl, attackX, attackY, atkSizeX, atkSizeY, damage, angleX, angleY, launch, sender, direction, hitbox):
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
            attacks.append((pygame.Rect(self.X + self.attackX, self.Y + self.attackY, self.atkSizeX, self.atkSizeY), self.damage, self.angleX, self.angleY, self.launch, self.sender)) if direction == 1 else attacks.append((pygame.Rect(self.X - self.attackX - self.atkSizeX + self.hitbox.width, self.Y + self.attackY, self.atkSizeX, self.atkSizeY), self.damage, self.angleX, self.angleY, self.launch, self.sender))
    def movement(self, UP, LEFT, DOWN, RIGHT, ATTACK, SHIELD):
        self.UP = UP
        self.LEFT = LEFT
        self.DOWN = DOWN
        self.RIGHT = RIGHT
        self.RIGHT = RIGHT
        self.ATTACK = ATTACK
        self.SHIELD = SHIELD
        if ATTACK and self.frame == 0:
            if self.grounded == 1:
                if not(LEFT) and not(RIGHT) and not(DOWN):
                    self.frame = 15
                    self.state = 1
                    self.attackTimer = 30
                elif DOWN:
                    self.frame = 18
                    self.state = 3
                elif (LEFT or RIGHT) and self.dashing == 0:
                    self.frame = 20
                    self.state = 2
                elif (LEFT or RIGHT) and not(self.dashing == 0):
                    self.frame = 20
                    self.state = 4
            else:
                if not(LEFT) and not(RIGHT) and not(DOWN) and not(UP):
                    self.frame = 15
                    self.state = 5
                elif DOWN:
                    self.frame = 20
                    self.state = 6
                elif UP:
                    self.frame = 18
                    self.state = 7
                elif LEFT or RIGHT and not(DOWN):
                    self.frame = 15
                    self.state = 8
        if self.character == 0:
            if self.state == 1:
                if self.frame > 11 and self.frame < 14:
                    if ATTACK and self.attackTimer > 0:
                        self.attackTimer -= 1
                        self.charge += 1
                        if self.frame < 13:
                            self.frame += 1
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, 0, 10, 100, 100, self.charge + 1, self.charge + 1, 10, 0, self.playerNumber, self.facing, self.hitbox)
                    self.charge = 0
            elif self.state == 2:
                if self.frame > 9 and self.frame < 14:
                    self.Attack = self.attack(self, 20, 10, 80, 40, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox)
            elif self.state == 3:
                if self.frame > 8 and self.state < 11:
                    self.VX = 7 * self.facing
                    self.Attack = self.attack(self, 20, 0, 40, 60, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox)
            elif self.state == 4:
                if self.frame > 7 and self.frame < 12:
                    self.VX = CharacterRunSpeed[self.character] * self.facing
                    self.Attack = self.attack(self, 20, 10, 40, 40, 10, 30, 10, 0, self.playerNumber, self.facing, self.hitbox)
            elif self.state == 5:
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, -10, 0, 70, 60, 10, 22.5, 7.5, 0, self.playerNumber, self.facing, self.hitbox)
            elif self.state == 6:
                if self.frame > 8 and self.frame < 12:
                    self.Attack = self.attack(self, -10, 60, 70, 60, 10, 0, 22, 0, self.playerNumber, self.facing, self.hitbox)  
            elif self.state == 7:
                if self.frame > 7 and self.frame < 11:
                    self.Attack = self.attack(self, -10, -60, 80, 60, 10, 0, -22, 0, self.playerNumber, self.facing, self.hitbox) 
            elif self.state == 8:
                if self.frame > 9 and self.frame < 12:
                    self.Attack = self.attack(self, 30, 0, 70, 60, 10, 22.5, 7.5, 0, self.playerNumber, self.facing, self.hitbox)

            
        if self.frame == 0:
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
            if not(DOWN and self.grounded == 1):
                self.VX += ((RIGHT - LEFT - self.dashing) * CharacterWalkSpeed[self.character] if self.dashing == 0 else CharacterRunSpeed[self.character] * -1 if self.VX < 0 else CharacterRunSpeed[self.character]) if self.grounded == 1 else (RIGHT - LEFT) * CharacterAirSpeed[self.character]  #caminar
            self.facing = (RIGHT - LEFT) if RIGHT or LEFT else self.facing
            if self.grounded == 1:
                self.flight = CharacterFlight[self.character]
            if UP and self.grounded and self.wallGrab == 0: #salto
                self.VY = -10 * CharacterJumpHeight[self.character]
                self.jumpTimer = 10
                self.flightTimer = 20
                self.wallGrab = 0
            elif UP and self.coyote > 0:
                self.coyote = 0
                self.VY = -10 * CharacterJumpHeight[self.character]
                self.VX = -5 if self.LEFT else 5
                self.flight = CharacterFlight[self.character]
                self.jumpTimer = 10
                self.flightTimer = 20
                self.wallGrab = 0
            if UP and not(self.grounded) and self.jumpTimer > 0:
                self.VY -= 1
            elif UP and not(self.grounded) and self.flight > 0 and self.flightTimer == 0 and self.wallGrab == 0:
                self.VY -= 2 if self.VY > 0 else 1.5
                if self.VY < -8:
                    self.VY = -8
                self.flight -= 1 if self.flight > 0 else 0
        else:
            self.frame -= 1
        self.VX *= 0.7 if self.grounded == 1 else 0.9
        self.VY += (1 * CharacterGravity[self.character] * (2 if DOWN else 1)) if self.wallGrab == 0 else (0.6 * CharacterGravity[self.character]) if CharacterClimb[self.character] == 0 else 0 #gravedad
        if self.VY > 10 and self.wallGrab == 0:
            self.VY = 10
        elif self.VY > 2 and self.wallGrab == 1 or self.VY > 2 and self.wallGrab == -1:
            self.VY = 2
        self.jumpTimer -= 1 if self.jumpTimer > 0 else 0
        self.flightTimer -= 1 if self.flightTimer > 0 else 0
        self.coyote -= 1 if self.coyote > 0 else 0
        self.collide()

    def collide(self):
        self.X += self.VX
        self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        collided = any(self.hitbox.colliderect(rect) for rect in block)
        while any(self.hitbox.colliderect(rect) for rect in block):
            self.X -= 1 if self.VX > 0 else -1
            self.wallStopDir = 1 if self.VX > 0 else -1
            self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        if collided:
            if self.VX > (6) or self.VX < (-6):
                self.VX *= -0.8
            else:
                self.VX = 0
            if self.wallGrab == 0:
                self.VY = 0
            if (self.RIGHT and self.wallStopDir == 1 or self.LEFT and self.wallStopDir == -1) and self.wallGrabTimer == 0:
                self.wallGrab = self.wallStopDir
        if self.wallGrab == 1 and not(self.RIGHT) or self.wallGrab == -1 and not(self.LEFT):
            self.coyote = 10
            self.wallGrab = 0
            self.wallStopDir = 0
        self.wallGrabTimer -= 1 if self.wallGrabTimer > 0 else 0
        
        self.Y += self.VY
        self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        collided = any(self.hitbox.colliderect(rect) for rect in block)
        if collided:
            if self.VY > (CharacterGravity[self.character] * 20):
                self.VY *= 0.8
        while any(self.hitbox.colliderect(rect) for rect in block):
            self.Y -= 1 if self.VY > 0 else -1
            self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        if collided:
            self.VY = 0
            self.grounded = True
        else:
            self.grounded = False
        if self.Y > 700:
            self.revive()
    def checkAttacks(self):
        for attack in attacks:
            if self.hitbox.colliderect(attack[0]) and not(attack[5] == self.playerNumber):
                if self.gotHit == 0:
                    self.VX = attack[2]
                    self.VY = attack[3]
                    if self.grounded == 1 and attack[3] > 0:
                        self.VY = attack[3] * -1 * 0.8
                    self.HP -= attack[1]
                    self.HPHealing += attack[1] * 0.5
                    self.HPHealTimer = 30
                    if self.HPHealing > 20:
                        self.HPHealing = 20
                    if self.HP <= 0:
                        self.revive()
                    self.gotHit += 2
                elif self.gotHit == 1:
                    self.gotHit += 1
        self.gotHit -= 1 if self.gotHit > 0 else 0
        self.HPHealTimer -= 1 if self.HPHealTimer > 0 else 0
        if self.HPHealTimer == 0 and self.HPHealing > 0:
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

players = [player(400, 300, 0, 0), player(400, 300, 0, 1)]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    attacks = []
    keys = pygame.key.get_pressed()
    DT = pygame.time.Clock().tick(60) / 60 * 100
    screen.fill((0, 0, 0))
    for pl in players:
        if pl.playerNumber == 0:
            pl.movement(keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d], keys[pygame.K_f], keys[pygame.K_g])
        elif pl.playerNumber == 1:
            pl.movement(keys[pygame.K_UP], keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_RIGHT], keys[pygame.K_COMMA], keys[pygame.K_PERIOD])
        pygame.draw.rect(screen, (255, 0, 0) if pl.playerNumber == 0 else (0, 0, 255), pl.hitbox, 100, border_radius=20)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(50 + 150 * pl.playerNumber, 550, pl.HP, 25))
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(50 + 150 * pl.playerNumber + pl.HP, 550, pl.HPHealing, 25))
        if not(pl.flight == CharacterFlight[pl.character]) and pl.grounded == 0 and pl.wallGrab == 0:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(pl.X + pl.hitbox.width / 2 - pl.flight, pl.Y - 75 / 2, pl.flight * 2, 25))
    for pl in players:
        pl.checkAttacks()
    for blk in block:
        pygame.draw.rect(screen, (0, 255, 0), blk)
    for attack in attacks:
        pygame.draw.rect(screen, (122 * attack[5] + 123, 0, 0), attack[0])
    pygame.display.flip()
    print(players[1].VY)
pygame.quit()