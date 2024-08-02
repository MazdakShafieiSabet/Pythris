import pygame
import random
import os

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 540, 720
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BG = (20, 20, 20)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

TITLE_COLORS = [BLUE, RED, GREEN, YELLOW, ORANGE]
LEVEL_COLORS = {
    1: [
        (0, 0, 255),  # Blue
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (255, 165, 0),# Orange
    ],
    2: [
        (128, 0, 128), # Purple for Blue
        (255, 105, 180), # Pink for Red
        (0, 255, 255),  # Cyan for Green
        (255, 20, 147), # Deep Pink for Orange
    ],
    3: [
        (54, 186, 152),  # Teal for Blue
        (233, 196, 106),  # Yellow for Red
        (244, 162, 97),  # Orange for Green
        (231, 111, 81),# Terracota for Orange
    ],
    # To be completely honest, I forgot what these colors are so mystery colors I guess!
    4: [
        (128, 136, 54),
        (255, 191, 0),
        (255, 154, 0),
        (209, 3, 99),
    ],
    5: [
        (255, 127, 62),
        (255, 246, 233),
        (128, 196, 233),
        (96, 76, 195),
    ],
    6: [
        (20, 40, 80),
        (39, 73, 109),
        (12, 123, 147),
        (0, 168, 204),
    ],
    7: [
        (82, 34, 88),
        (140, 48, 97),
        (198, 60, 81),
        (217, 95, 89),
    ],
    8: [
        (180, 214, 205),
        (255, 218, 118),
        (255, 140, 158),
        (255, 78, 136),
    ],
    9: [
        (26, 26, 26),
        (18, 17, 17),
        (31, 31, 31),
        (20, 20, 20),
    ],
}

SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1, 1]],          # I
    [[1, 1], [1, 1]],        # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pythris")

# Load pixelated font
font_path = "fonts/Minimal3x5.ttf"
font_size = 48
pixel_font = pygame.font.Font(font_path, font_size)

# High score file
highscore_file = "highscores.txt"

def load_highscores():
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as f:
            highscores = [line.strip().split(",") for line in f.readlines()]
        return sorted(highscores, key=lambda x: int(x[1]), reverse=True)
    return []

def save_highscore(name, score):
    highscores = load_highscores()
    highscores.append([name, str(score)])
    highscores = sorted(highscores, key=lambda x: int(x[1]), reverse=True)[:5]  # Keep top 5
    with open(highscore_file, "w") as f:
        for entry in highscores:
            f.write(",".join(entry) + "\n")

def get_background_color(level):
    # Define a dictionary with level-specific background colors
    level_backgrounds = {
        9: (80, 80, 80),
        # Add more levels and colors as needed
    }
   
    # Return the background color for the current level, or to default if not specified
    return level_backgrounds.get(level, BG)

def draw_multi_colored_title(text, font, x, y):
    color_index = 0
    for char in text:
        char_surface = font.render(char, True, TITLE_COLORS[color_index % len(TITLE_COLORS)])
        screen.blit(char_surface, (x, y))
        x += char_surface.get_width()
        color_index += 1

def check_and_award_hole_points(grid, score):
    holes = 0
    for x in range(GRID_WIDTH):
        column_holes = 0
        block_found = False
        for y in range(GRID_HEIGHT):
            if grid[y][x] != 0:
                block_found = True
            elif block_found and grid[y][x] == 0:
                column_holes += 1
        holes += column_holes

    # Calculate points for rows with 18 rows considered
    rows_with_holes = GRID_HEIGHT // GRID_SIZE  # This is 18 for a 540x720 window
    points_per_row = 72
    total_points = rows_with_holes * points_per_row

    # Calculate points to be deducted for holes
    points_deducted = holes * 4

    # Calculate net points to be awarded
    net_points = total_points - points_deducted

    return score + net_points

# Function to draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

# Function to check if the position is valid
def valid_position(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= GRID_WIDTH or y + off_y >= GRID_HEIGHT:
                    return False
                if grid[y + off_y][x + off_x]:
                    return False
    return True

# Function to rotate the shape
def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

# Function to draw text in the center of the screen
def draw_text(text, size, color, y_offset=0):
    font = pixel_font
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset))
    screen.blit(text_surface, text_rect)

# Main menu function
def main_menu():
    while True:
        screen.fill(BLACK)
        draw_multi_colored_title("Pythris",pixel_font, 190, 225)
        draw_multi_colored_title("Press any key to start",pixel_font, 50, 275)
        draw_text("Credits", 25, WHITE, 0)
        draw_text("Font by", 25, WHITE, 75)
        draw_text("kheftel", 25, WHITE, 125)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                name = enter_name()
                main(name)
                return

# Game over function
def game_over_screen(score, name):
    save_highscore(name, score)
    highscores = load_highscores()
    while True:
        screen.fill(BG)
        draw_text("Game Over", 50, WHITE, -100)
        draw_text(f"Score: {score}", 30, WHITE, -50)
        draw_text("Highscores", 25, WHITE, 0)
        for i, entry in enumerate(highscores):
            draw_text(f"{entry[0]}: {entry[1]}", 25, WHITE, 50 + i * 25)
        draw_text("Press any key to restart", 25, WHITE, 200)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                main_menu()
                return

# Enter name function
def enter_name():
    name = ""
    while True:
        screen.fill(BG)
        draw_text("Enter name (3 chars.):", 25, WHITE, -50)
        draw_text(name, 50, WHITE, 50)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(name) == 3:
                        return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 3:
                    name += event.unicode.upper()

# Main game function
def main(player_name):
    global grid

    clock = pygame.time.Clock()
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_shape = random.choice(SHAPES)
    current_color = random.choice(LEVEL_COLORS[1])
    current_pos = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
    fall_time = 0
    fall_speed = 50
    score = 0
    level = 1
    rows_cleared = 0

    while True:
        screen.fill(get_background_color(level))
        draw_grid()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_pos = [current_pos[0] - 1, current_pos[1]]
                    if valid_position(current_shape, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = [current_pos[0] + 1, current_pos[1]]
                    if valid_position(current_shape, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = [current_pos[0], current_pos[1] + 1]
                    if valid_position(current_shape, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_UP:
                    new_shape = rotate_shape(current_shape)
                    if valid_position(new_shape, current_pos):
                        current_shape = new_shape

        # Move shape down
        fall_time += clock.get_rawtime()
        if fall_time > fall_speed:
            fall_time = 0
            new_pos = [current_pos[0], current_pos[1] + 1]
            if valid_position(current_shape, new_pos):
                current_pos = new_pos
            else:
                for y, row in enumerate(current_shape):
                    for x, cell in enumerate(row):
                        if cell:
                            grid[current_pos[1] + y][current_pos[0] + x] = current_color
                current_shape = random.choice(SHAPES)
                current_color = random.choice(LEVEL_COLORS.get(level, LEVEL_COLORS[1]))
                current_pos = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                if not valid_position(current_shape, current_pos):
                    game_over_screen(score, player_name)
                    return

        # Clear full lines
        new_grid = [row for row in grid if any(cell == 0 for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        rows_cleared += lines_cleared
        score += lines_cleared * 1000
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(lines_cleared)] + new_grid
        grid = new_grid

        # Increase level and fall speed every 3 rows cleared
        if rows_cleared >= 3:
            # Award points based on holes before leveling up
            score = check_and_award_hole_points(grid, score)
            level += 1
            rows_cleared = 0
            if fall_speed > 5:
                fall_speed -= 5

        # Draw the shape
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_color, (current_pos[0] * GRID_SIZE + x * GRID_SIZE, current_pos[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the grid cells
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the score and level
        score_text = pixel_font.render(f"Score: {score}", True, WHITE)
        level_text = pixel_font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (5, 5))
        screen.blit(level_text, (5, 45))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
    
