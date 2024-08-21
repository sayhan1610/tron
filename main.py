# Inspired by Zach Latta's SSH Tron Game
# https://github.com/zachlatta/sshtron

import pygame
import sys
import random

pygame.init()  # Initiate Pygame

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up  screen
pygame.display.set_caption("Tron Game")  # Set window title

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRID_COLOR = (87, 246, 212)  # Grid color

# Game settings
FPS = 15  # Frames per second. Higher value = faster game.
TRAIL_SIZE = 10  # Size of trail left by players
GRID_SIZE = 40  # Size of grid cells in bg

# Load images
def load_image(filename, width=None, height=None):
    image = pygame.image.load(f"images/{filename}")  # Load image
    if width and height:  
        image = pygame.transform.scale(image, (width, height))  # Resize image
    return image

# Load player images and bg
tron_red = load_image("tron_red.png", 20, 30)
tron_blue = load_image("tron_blue.png", 20, 30)
bg_image = load_image("bg.jpg", WIDTH, HEIGHT)

CLOCK = pygame.time.Clock()  # Clock to control frame rate

# Direction vectors
UP = (0, -TRAIL_SIZE)
DOWN = (0, TRAIL_SIZE)
LEFT = (-TRAIL_SIZE, 0)
RIGHT = (TRAIL_SIZE, 0)

# Sound effects
theme_music = pygame.mixer.Sound("audio/theme.mp3")
countdown_sound = pygame.mixer.Sound("audio/count.mp3")
game_over_sound = pygame.mixer.Sound("audio/game.mp3")
game_music_choices = ["audio/song1.mp3", "audio/song2.mp3"]

# Player class
class Player:
    def __init__(self, color, start_pos, image):
        self.color = color  # Player color
        self.image = image  # Player image
        self.positions = [start_pos]  # List of positions
        self.direction = UP  # Initial direction
        self.alive = True  # Player is alive

    def update(self):
        if self.alive:
            new_position = (self.positions[-1][0] + self.direction[0], self.positions[-1][1] + self.direction[1])
            self.positions.append(new_position)  # Move player
            # Check for collisions
            if new_position[0] < 0 or new_position[0] >= WIDTH or new_position[1] < 0 or new_position[1] >= HEIGHT:
                self.alive = False
            if self.positions.count(new_position) > 1:
                self.alive = False

    def draw(self):
        for i in range(len(self.positions) - 1):
            pygame.draw.rect(SCREEN, self.color, (*self.positions[i], TRAIL_SIZE, TRAIL_SIZE))
        # Draw player image at end of trail
        for position in [self.positions[-1]]:
            angle = self._get_rotation_angle()
            rotated_image = pygame.transform.rotate(self.image, angle)
            rect = rotated_image.get_rect(center=(position[0] + TRAIL_SIZE // 2, position[1] + TRAIL_SIZE // 2))
            SCREEN.blit(rotated_image, rect.topleft)

    def _get_rotation_angle(self):
        # Determine angle to rotate image based on direction
        if self.direction == UP:
            return 0
        elif self.direction == RIGHT:
            return 90
        elif self.direction == DOWN:
            return 180
        elif self.direction == LEFT:
            return 270

    def change_direction(self, direction):
        # Change direction if not directly opposite
        if (self.direction[0] * -1, self.direction[1] * -1) != direction:
            self.direction = direction

# Show home page
def show_home_page():
    theme_music.play(-1)  # Loop theme music
    SCREEN.blit(bg_image, (0, 0))  # Draw bg
    font = pygame.font.Font(None, 74)
    text = font.render("Press SPACE to Start", True, BLACK)
    
    text_bg = pygame.Surface((text.get_width(), text.get_height()))
    text_bg.fill(YELLOW)  # bg for text

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_bg_rect = text_bg.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    SCREEN.blit(text_bg, text_bg_rect)  # Draw text bg
    SCREEN.blit(text, text_rect)  # Draw text
    pygame.display.flip()

# Show instructions page
def show_instructions_page():
    SCREEN.blit(bg_image, (0, 0))  # Draw bg
    font = pygame.font.Font(None, 36)
    
    instructions = [
        "Tron Game Instructions",
        "1. Player 1 (Blue) controls:",
        "   - W: Move Up || - S: Move Down",
        "   - A: Move Left || - D: Move Right",
        "2. Player 2 (Red) controls:",
        "   - UP: Move Up || - DOWN: Move Down",
        "   - LEFT: Move Left || - RIGHT: Move Right",
        "3. Avoid hitting walls or your own trail.",
        "4. Press SPACE to start or restart game.",
        "5. Press ESC to quit game."
    ]
    
    y_offset = 50
    for line in instructions:
        text = font.render(line, True, WHITE)
        # Create bg surface for the text
        text_bg = pygame.Surface((text.get_width() + 20, text.get_height() + 10))
        text_bg.fill((50, 50, 50))  # bg color
        
        text_rect = text.get_rect(center=(WIDTH // 2, y_offset + text.get_height() // 2))
        text_bg_rect = text_bg.get_rect(center=(WIDTH // 2, y_offset + text.get_height() // 2))
        
        SCREEN.blit(text_bg, text_bg_rect)  # Draw text bg
        SCREEN.blit(text, text_rect)  # Draw text
        y_offset += text.get_height() + 20  # Move down for next line
    
    pygame.display.flip()
    
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    waiting_for_key = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# Show countdown before game starts
def show_countdown():
    countdown_sound.play()  # Play countdown sound
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        SCREEN.fill(BLACK)  # Clear screen
        draw_grid()  # Draw grid
        text = font.render(f"Starting in {i}", True, WHITE)
        SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait 1 second

# Draw grid on screen
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(SCREEN, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(SCREEN, GRID_COLOR, (0, y), (WIDTH, y))

# Main game loop
def game_loop():
    theme_music.stop()  # Stop theme music
    game_music = pygame.mixer.Sound(random.choice(game_music_choices))  # Choose random game music
    game_music.play(-1)  # Loop game music
    
    player1 = Player(BLUE, (100, 300), tron_blue)  # Player 1 (Blue)
    player2 = Player(RED, (700, 300), tron_red)  # Player 2 (Red)
    
    show_countdown()  # Show countdown before starting

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    player2.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    player2.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    player2.change_direction(RIGHT)
                elif event.key == pygame.K_w:
                    player1.change_direction(UP)
                elif event.key == pygame.K_s:
                    player1.change_direction(DOWN)
                elif event.key == pygame.K_a:
                    player1.change_direction(LEFT)
                elif event.key == pygame.K_d:
                    player1.change_direction(RIGHT)
                elif event.key == pygame.K_SPACE and (not player1.alive or not player2.alive):
                    return  # Restart game if SPACE is pressed

        player1.update()  # Update player 1
        player2.update()  # Update player 2

        # Check for collisions
        if player1.positions[-1] in player2.positions:
            player1.alive = False
        if player2.positions[-1] in player1.positions:
            player2.alive = False

        SCREEN.fill(BLACK)  # Clear screen
        draw_grid()  # Draw grid
        player1.draw()  # Draw player 1
        player2.draw()  # Draw player 2

        # Check if game is over
        if not player1.alive or not player2.alive:
            game_music.stop()  # Stop game music
            game_over_sound.play()  # Play game over sound
            
            font = pygame.font.Font(None, 74)
            if not player1.alive and not player2.alive:
                text = font.render("It's a Tie!", True, WHITE)
            elif not player1.alive:
                text = font.render("Red Wins!", True, RED)
            else:
                text = font.render("Blue Wins!", True, BLUE)
            SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)  # Wait 3 seconds
            return

        pygame.display.flip()  # Update screen
        CLOCK.tick(FPS)  # Control frame rate

# Main function to run game
def main():
    theme_music.play(-1)  # Loop theme music
    while True:
        show_home_page()  # Show home page
        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        show_instructions_page()  # Show instructions
                    elif event.key == pygame.K_SPACE:
                        waiting_for_start = False  # Start game
        game_loop()  # Run game loop

if __name__ == "__main__":
    main()  # Run game
