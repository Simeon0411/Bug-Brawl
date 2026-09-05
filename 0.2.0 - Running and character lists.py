import pygame
pygame.init()
#player stats#
CharacterWalkSpeed = [2]
CharacterRunSpeed = [4]
CharacterAirSpeed = [0.6]
CharacterJumpHeight = [1]
CharacterGravity = [1]
CharacterFlight = [30]
running = True
screen = pygame.display.set_mode((800, 600)) 
keys = pygame.key.get_pressed()
block = [pygame.Rect(0, 500, 800, 40), pygame.Rect(400, 460, 80, 80), pygame.Rect(400, 460, 80, 80)]
class player():
    def __init__(self, X, Y, character):
        self.character = character
        self.X = X
        self.Y = Y
        self.VX = 0
        self.VY = 0
        self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        self.grounded = False
        self.jumpTimer = 0
        self.dashTimer = 0
        self.dashing = 0
        self.flight = 0
        self.flightTimer = 0
    def movement(self):
        if keys[pygame.K_LEFT]:
            if self.dashTimer < 0 and self.dashTimer > -9:
                self.dashing = -1
            else:
                self.dashTimer = -10
        if keys[pygame.K_RIGHT]:
            if self.dashTimer > 0 and self.dashTimer < 9:
                self.dashing = 1
            else:
                self.dashTimer = 10
        self.dashTimer -= 1 if self.dashTimer > 0 else -1 if self.dashTimer < 0 else 0
        if not(keys[pygame.K_RIGHT]) and not(keys[pygame.K_LEFT]) or keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] or not(self.grounded == 1):
            self.dashing = 0
        self.VX += ((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] - self.dashing) * CharacterWalkSpeed[self.character] if self.dashing == 0 else CharacterRunSpeed[self.character] * -1 if self.VX < 0 else CharacterRunSpeed[self.character]) if self.grounded == 1 else (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * CharacterAirSpeed[self.character]  #caminar
        self.VX *= 0.7 if self.grounded == 1 else 0.9
        if keys[pygame.K_UP] and self.grounded: #salto
            self.VY = -10 * CharacterJumpHeight[self.character]
            self.jumpTimer = 10
            self.flight = CharacterFlight[self.character]
            self.flightTimer = 20
        if keys[pygame.K_UP] and not(self.grounded) and self.jumpTimer > 0:
            self.VY -= 1
        elif keys[pygame.K_UP] and not(self.grounded) and self.flight > 0 and self.flightTimer == 0:
            self.VY -= 2 if self.VY > 0 else 1.5
            if self.VY < -8:
                self.VY = -8
            self.flight -= 1 if self.flight > 0 else 0
        self.VY += 1 * CharacterGravity[self.character] #gravedad
        if self.VY > 10:
            self.VY = 10
        self.jumpTimer -= 1 if self.jumpTimer > 0 else 0
        self.flightTimer -= 1 if self.flightTimer > 0 else 0
        self.collide()

    def collide(self):
        self.X += self.VX
        self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        collided = any(self.hitbox.colliderect(rect) for rect in block)
        while any(self.hitbox.colliderect(rect) for rect in block):
            self.X -= 1 if self.VX > 0 else -1
            self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        if collided:
            self.VX = 0
        
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


p1 = player(400, 300, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    DT = pygame.time.Clock().tick(60) / 60 * 1000
    p1.movement()
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), p1.hitbox, 3, border_radius=20)
    pygame.draw.rect(screen, (0, 255, 0), block[0])
    pygame.draw.rect(screen, (0, 255, 0), block[1])
    pygame.display.flip()
    print(f"{p1.VY} - {p1.flight} - {p1.jumpTimer}")
pygame.quit()