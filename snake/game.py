import sys
import pygame
import random
import time

pygame.init()

# Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Game variables
score = 0
level = 1
speed = 200  # Initial snake speed (milliseconds per movement)
done = False

# Initial snake body
squares = [
    [30, 100], [40, 100], [50, 100], [60, 100], [70, 100],
    [80, 100], [90, 100], [100, 100]
]
head_square = [100, 100]

# Movement directions
direction = "right"
next_dir = "right"

# Fruit types with different points and lifespan
fruit_types = {
    "apple": {"color": (0, 255, 0), "points": 10, "time_to_live": 5000},  # 5 sec
    "banana": {"color": (255, 255, 0), "points": 20, "time_to_live": 7000},  # 7 sec
    "cherry": {"color": (255, 0, 0), "points": 30, "time_to_live": 10000}  # 10 sec
}

# Generate a fruit at a valid position
def generate_fruit():
    while True:
        fr_x = random.randrange(width // 4, 3 * width // 4, 10)  # Орталық аймақ
        fr_y = random.randrange(height // 4, 3 * height // 4, 10)
        fruit_type = random.choice(list(fruit_types.keys()))
        fruit_data = fruit_types[fruit_type]
        fruit_coor = [fr_x, fr_y, fruit_type, time.time()]
        
        # Ensure fruit does not spawn on the snake
        if [fr_x, fr_y] not in squares:
            return fruit_coor


fruit_coor = generate_fruit()

# Game over function
def game_over():
    global done
    font = pygame.font.SysFont("times new roman", 45)
    text_surface = font.render(f"Game Over, Score: {score}", True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

# Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                next_dir = "down"
            if event.key == pygame.K_UP:
                next_dir = "up"
            if event.key == pygame.K_LEFT:
                next_dir = "left"
            if event.key == pygame.K_RIGHT:
                next_dir = "right"
    
    # Prevent reversing direction
    if next_dir == "right" and direction != "left":
        direction = "right"
    if next_dir == "up" and direction != "down":
        direction = "up"
    if next_dir == "left" and direction != "right":
        direction = "left"
    if next_dir == "down" and direction != "up":
        direction = "down"
    
    # Move head
    if direction == "right":
        head_square[0] += 10
    if direction == "left":
        head_square[0] -= 10
    if direction == "up":
        head_square[1] -= 10
    if direction == "down":
        head_square[1] += 10
    
    new_square = list(head_square)
    
    # Check collision with itself
    if new_square in squares[:-1]:
        game_over()
    
    # Check collision with boundaries
    if head_square[0] < 0 or head_square[0] >= width or head_square[1] < 0 or head_square[1] >= height:
        game_over()
    
    squares.append(new_square)
    
    # Check if the snake eats the fruit
    if head_square[:2] == fruit_coor[:2]:  # Compare only X, Y
        score += fruit_types[fruit_coor[2]]["points"]
        
        # Increase speed every 30 points
        if score % 30 == 0:
            level += 1
            speed = max(50, speed - 20)  # Limit minimum speed
        
        fruit_coor = generate_fruit()  # Generate new fruit
    else:
        squares.pop(0)  # Remove tail if fruit is not eaten
    
    # Remove fruit if time expires
    if time.time() - fruit_coor[3] > fruit_types[fruit_coor[2]]["time_to_live"] / 1000:
        fruit_coor = generate_fruit()
    
    # Drawing section
    screen.fill((0, 0, 0))
    
    # Display score and level
    score_font = pygame.font.SysFont("times new roman", 20)
    score_surface = score_font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    
    # Draw fruit
    pygame.draw.circle(screen, fruit_types[fruit_coor[2]]["color"], (fruit_coor[0] + 5, fruit_coor[1] + 5), 5)
    
    # Draw snake
    for el in squares:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))
    
    pygame.display.flip()
    pygame.time.delay(speed)

pygame.quit()
