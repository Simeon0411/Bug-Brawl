import pygame
pygame.init()
#player stats#
CharacterWalkSpeed = [2]
CharacterRunSpeed = [4]
CharacterAirSpeed = [0.6]
CharacterJumpHeight = [1]
CharacterGravity = [1]
CharacterFlight = [30]
CharacterClimb = [0]
running = True
screen = pygame.display.set_mode((800, 600)) 
keys = pygame.key.get_pressed()
block = [pygame.Rect(0, 500, 800, 40), pygame.Rect(400, 460, 80, 80), pygame.Rect(400, 360, 80, 300)]
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
        self.busyTimer = 0
        self.facing = 0
        self.coyote = 0
    class attack:
        def __init__(self, pl, attackX, attackY, atkSizeX, atkSizeY, damage, angleX, angleY, launch, sender, direction):
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
            attacks.append((pygame.Rect(self.X + self.attackX, self.Y + self.attackY, self.atkSizeX, self.atkSizeY), self.damage, self.angleX, self.angleY, self.launch, self.sender)) if direction == 1 else attacks.append((pygame.Rect(self.X + self.attackX - self.atkSizeX, self.Y + self.attackY, self.atkSizeX, self.atkSizeY), self.damage, self.angleX, self.angleY, self.launch, self.sender))
    def movement(self, UP, LEFT, DOWN, RIGHT, ATTACK, SHIELD):
        self.UP = UP
        self.LEFT = LEFT
        self.DOWN = DOWN
        self.RIGHT = RIGHT
        self.RIGHT = RIGHT
        self.ATTACK = ATTACK
        self.SHIELD = SHIELD
        if ATTACK and self.busyTimer == 0:
            if self.grounded == 1:
                self.busyTimer = 10
                if self.busyTimer > 2:
                    self.Attack = self.attack(self, 0, 10, 100, 100, 100, 30, 10, 0, self.playerNumber, self.facing)
            
        if self.busyTimer == 0:
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
            self.VX += ((RIGHT - LEFT - self.dashing) * CharacterWalkSpeed[self.character] if self.dashing == 0 else CharacterRunSpeed[self.character] * -1 if self.VX < 0 else CharacterRunSpeed[self.character]) if self.grounded == 1 else (RIGHT - LEFT) * CharacterAirSpeed[self.character]  #caminar
            self.facing = (RIGHT - LEFT) if RIGHT or LEFT else self.facing
            if UP and self.grounded and self.wallGrab == 0: #salto
                self.VY = -10 * CharacterJumpHeight[self.character]
                self.jumpTimer = 10
                self.flight = CharacterFlight[self.character]
                self.flightTimer = 20
                self.wallGrab = 0
            elif UP and self.coyote > 0:
                self.coyote = 0
                self.VY = -10 * CharacterJumpHeight[self.character]
                self.VX = -8 if self.LEFT else 8
                self.jumpTimer = 10
                self.flight = CharacterFlight[self.character]
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
            self.busyTimer -= 1
        self.VX *= 0.7 if self.grounded == 1 else 0.9
        self.VY += (1 * CharacterGravity[self.character]) if self.wallGrab == 0 else (0.6 * CharacterGravity[self.character]) if CharacterClimb[self.character] == 0 else 0 #gravedad
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
        while any(self.hitbox.colliderect(rect) for rect in block):
            self.Y -= 1 if self.VY > 0 else -1
            self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        if collided:
            self.VY = 0
            self.grounded = True
        else:
            self.grounded = False
    def checkAttacks(self):
        for attack in attacks:
            if self.hitbox.colliderect(attack[0]):
                if not(attack[5] == self.playerNumber):
                    self.VX = attack[2]
                    self.VY = attack[3]


p1 = player(400, 300, 0, 0)
p2 = player(400, 300, 0, 1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    attacks = []
    keys = pygame.key.get_pressed()
    DT = pygame.time.Clock().tick(60) / 60 * 1000
    p1.movement(keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d], keys[pygame.K_f], keys[pygame.K_g])
    p2.movement(keys[pygame.K_UP], keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_RIGHT], keys[pygame.K_COMMA], keys[pygame.K_PERIOD])
    p1.checkAttacks()
    p2.checkAttacks()
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), p1.hitbox, 100, border_radius=20)
    pygame.draw.rect(screen, (0, 0, 255), p2.hitbox, 100, border_radius=20)
    pygame.draw.rect(screen, (0, 255, 0), block[0])
    pygame.draw.rect(screen, (0, 255, 0), block[2])
    for attack in attacks:
        pygame.draw.rect(screen, (122 * attack[5], 0, 0), attack[0])
    pygame.display.flip()
    for attack in attacks:
        if p1.hitbox.colliderect(attack[0]):
            print(f"{attack[0]}")
pygame.quit()