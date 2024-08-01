import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball in a Ball")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ball settings
inner_ball_radius = 20
outer_ball_radius = 200
inner_ball_speed = 5
max_balls = 1  # Maximum number of balls (set to 1)

# Initial positions and velocities
outer_ball_center = (WIDTH // 2, HEIGHT // 2)

ball = {
    'position': [
        outer_ball_center[0] + (outer_ball_radius - inner_ball_radius) * math.cos(random.uniform(0, 2 * math.pi)),
        outer_ball_center[1] + (outer_ball_radius - inner_ball_radius) * math.sin(random.uniform(0, 2 * math.pi))
    ],
    'velocity': [
        inner_ball_speed * math.cos(random.uniform(0, 2 * math.pi)),
        inner_ball_speed * math.sin(random.uniform(0, 2 * math.pi))
    ],
    'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    'last_positions': []  # Track last positions for the trail effect
}

# Run the game
running = True
clock = pygame.time.Clock()


def change_inner_ball_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def random_velocity():
    angle = random.uniform(0, 2 * math.pi)
    return [inner_ball_speed * math.cos(angle), inner_ball_speed * math.sin(angle)]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the inner ball
    ball['position'][0] += ball['velocity'][0]
    ball['position'][1] += ball['velocity'][1]

    # Save last position for effect
    ball['last_positions'].append((ball['position'][0], ball['position'][1]))
    if len(ball['last_positions']) > 10:  # Keep last 10 positions
        ball['last_positions'].pop(0)

    # Check for collision with the outer ball boundary
    distance_to_center = math.hypot(ball['position'][0] - outer_ball_center[0],
                                    ball['position'][1] - outer_ball_center[1])

    if distance_to_center + inner_ball_radius >= outer_ball_radius:
        # Reflect the velocity vector
        normal = [ball['position'][0] - outer_ball_center[0],
                  ball['position'][1] - outer_ball_center[1]]
        normal_magnitude = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
        normal = [normal[0] / normal_magnitude, normal[1] / normal_magnitude]
        dot_product = (ball['velocity'][0] * normal[0] +
                       ball['velocity'][1] * normal[1])
        ball['velocity'][0] -= 2 * dot_product * normal[0]
        ball['velocity'][1] -= 2 * dot_product * normal[1]

        ball['color'] = change_inner_ball_color()

        # Duplicate the ball if under the limit (not used since max_balls is 1)
        # No new balls to add

    # Clear the screen
    window.fill(BLACK)

    # Draw the outer ball
    pygame.draw.circle(window, WHITE, outer_ball_center, outer_ball_radius, 2)

    # Draw the inner ball and its trail
    for i, pos in enumerate(ball['last_positions']):
        # Create a fading effect by adjusting the color
        fade_color = tuple([int(c * (1 - i / len(ball['last_positions']))) for c in ball['color']])
        pygame.draw.circle(window, fade_color, (int(pos[0]), int(pos[1])), inner_ball_radius, 1)

    # Draw the current inner ball
    pygame.draw.circle(window, ball['color'], (int(ball['position'][0]), int(ball['position'][1])), inner_ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()