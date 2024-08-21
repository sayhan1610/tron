# Inspired by Zach Latta's SSH Tron Game
# https://github.com/zachlatta/sshtron

import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tron Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

CLOCK = pygame.time.Clock()
FPS = 15

UP = (0, -10)
DOWN = (0, 10)
LEFT = (-10, 0)
RIGHT = (10, 0)

class Player:
    def __init__(self, color, start_pos):
        self.color = color
        self.positions = [start_pos]
        self.direction = RIGHT
        self.alive = True

    def update(self):
        if self.alive:
            new_position = (self.positions[-1][0] + self.direction[0], self.positions[-1][1] + self.direction[1])
            self.positions.append(new_position)
            if new_position[0] < 0 or new_position[0] >= WIDTH or new_position[1] < 0 or new_position[1] >= HEIGHT:
                self.alive = False
            if self.positions.count(new_position) > 1:
                self.alive = False

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(SCREEN, self.color, (*position, 10, 10))

    def change_direction(self, direction):
        if (self.direction[0] * -1, self.direction[1] * -1) != direction:
            self.direction = direction

player1 = Player(BLUE, (100, 300))
player2 = Player(RED, (700, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                player1.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                player1.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                player1.change_direction(RIGHT)
            elif event.key == pygame.K_w:
                player2.change_direction(UP)
            elif event.key == pygame.K_s:
                player2.change_direction(DOWN)
            elif event.key == pygame.K_a:
                player2.change_direction(LEFT)
            elif event.key == pygame.K_d:
                player2.change_direction(RIGHT)

    player1.update()
    player2.update()

    if player1.positions[-1] in player2.positions:
        player1.alive = False
    if player2.positions[-1] in player1.positions:
        player2.alive = False

    SCREEN.fill(BLACK)
    player1.draw()
    player2.draw()

    if not player1.alive or not player2.alive:
        font = pygame.font.Font(None, 74)
        if not player1.alive and not player2.alive:
            text = font.render("It's a Tie!", True, WHITE)
        elif not player1.alive:
            text = font.render("Red Wins!", True, RED)
        else:
            text = font.render("Blue Wins!", True, BLUE)
        SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    CLOCK.tick(FPS)
