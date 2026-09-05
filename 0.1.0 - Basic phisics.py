import pygame
pygame.init()
running = True
screen = pygame.display.set_mode((800, 600)) 
keys = pygame.key.get_pressed()
block = pygame.Rect(0, 500, 800, 40)
class player():
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.VX = 0
        self.VY = 0
        self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        self.grounded = False
    def movement(self):
        self.VX += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 2 #caminar
        self.VX *= 0.7
        if keys[pygame.K_UP] and self.grounded: #salto
            self.VY = -15
        self.VY += 1 #gravedad
        if self.VY > 10:
            self.VY = 10
        self.collide()
    def collide(self):
        self.X += self.VX
        self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        collided = self.hitbox.colliderect(block)
        while self.hitbox.colliderect(block):
            self.X -= 1 if self.VX > 0 else -1
            self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        if collided:
            self.VX = 0
        
        self.Y += self.VY
        self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        collided = self.hitbox.colliderect(block)
        while self.hitbox.colliderect(block):
            self.Y -= 1 if self.VY > 0 else -1
            self.hitbox = pygame.Rect(self.X, self.Y, 30, 50)
        if collided:
            self.VY = 0
            self.grounded = True
        else:
            self.grounded = False


p1 = player(400, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    DT = pygame.time.Clock().tick(60) / 60 * 1000
    p1.movement()
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), p1.hitbox, 3, border_radius=20)
    pygame.draw.rect(screen, (0, 255, 0), block)
    pygame.display.flip()

pygame.quit()