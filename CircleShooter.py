import random
import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Gamepad Example")

# Initialize the joystick module
pygame.joystick.init()

# Get the first connected gamepad
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Set up the player circle
player_x = 350
player_y = 250
player_radius = 20
player_color = (255, 255, 255)

# Set up the bullet
bullet_radius = 5
bullet_color = (0, 255, 0)
bullets = []

# Set up the enemy shapes
color = (255, 0, 0) # red
rect_size = (25, 25) # width, height
enemies = []
max_enemies = 8 # maximum number of enemies allowed on the screen at once

# Game loop
running = True
while running:
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the x and y position of the left joystick
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Move the player circle based on the joystick position
    player_x += x_axis * 5
    player_y += y_axis * 5

    # check if the player is within the screen boundaries
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    if player_x - player_radius <= 0:
        player_x = player_radius
    if player_x + player_radius >= screen_width:
        player_x = screen_width - player_radius
    if player_y - player_radius <= 0:
        player_y = player_radius
    if player_y + player_radius >= screen_height:
        player_y = screen_height - player_radius

    # Check if the A button is pressed
    if joystick.get_button(0):
        # Create a new bullet and add it to the bullets list
        bullet = {
            "x": player_x,
            "y": player_y,
            "radius": bullet_radius,
            "color": bullet_color
        }
        bullets.append(bullet)

    # Create new enemies if number of enemies is less than the max
    if len(enemies) < max_enemies:
        enemy = {
            "x": random.randint(0, screen_width - rect_size[0]*2),
            "y": random.randint(0, screen_height - rect_size[1]*3),
            "sizex": rect_size[0],
            "sizey": rect_size[1],
            "color": color
        }
        enemies.append(enemy)


    # Move the bullets
    for bullet in bullets:
        bullet["x"] += 10

        # check if button has left screen
        if bullet["x"] <= 0:
            bullets.remove(bullet)
        if bullet["x"] >= screen_width:
            bullets.remove(bullet)
        if bullet["y"] <= 0:
            bullets.remove(bullet)
        if bullet["y"] >= screen_height:
            bullets.remove(bullet)


    # Check for collisions between bullets and enemies
    for bullet in bullets:
        for enemy in enemies:
            if (bullet["x"] > enemy["x"] - enemy["sizex"] / 2 and
                    bullet["x"] < enemy["x"] + enemy["sizex"] / 2 and
                    bullet["y"] > enemy["y"] - enemy["sizey"] / 2 and
                    bullet["y"] < enemy["y"] + enemy["sizey"] / 2):
                enemies.remove(enemy)
                bullets.remove(bullet)
                break

    # Check if any enemies have reached the player
    for enemy in enemies:
        if (enemy["x"] > player_x - player_radius and
                enemy["x"] < player_x + player_radius and
                enemy["y"] > player_y - player_radius and
                enemy["y"] < player_y + player_radius):
            # Handle the player being hit by an enemy
            enemies.remove(enemy)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the player circle
    pygame.draw.circle(screen, player_color, (player_x, player_y), player_radius)

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.circle(screen, bullet["color"], (bullet["x"], bullet["y"]), bullet["radius"])
        
    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(screen, enemy["color"], (enemy["x"], enemy["y"], enemy["sizex"], enemy["sizey"]))
        
    # Update the screen
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
