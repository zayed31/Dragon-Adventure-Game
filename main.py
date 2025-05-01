import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced Dragon Adventure Game")

# Load assets
dragon_img = pygame.image.load("dragonmain.png")
fireball_img = pygame.image.load("fireball.png")
enemy_img = pygame.image.load("dragon1.png")
enemy_fast_img = pygame.image.load("enemy_fast.png")
enemy_shooter_img = pygame.image.load("enemy_shooter.png")
enemy_dodger_img = pygame.image.load("dragon2.png")
enemy_chaser_img = pygame.image.load("dragon1.png")
boss_img = pygame.image.load("dragonboss.png")
background_img = pygame.image.load("background.jpg")
shield_img = pygame.image.load("coin.png")
double_fire_img = pygame.image.load("coin.png")
enemy_fireball_img = pygame.image.load("fireball.png")

# Scale images (Adjust dragon size and add new enemies)
dragon_img = pygame.transform.scale(dragon_img, (120, 90))
fireball_img = pygame.transform.scale(fireball_img, (30, 15))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
enemy_fast_img = pygame.transform.scale(enemy_fast_img, (50, 50))
enemy_shooter_img = pygame.transform.scale(enemy_shooter_img, (50, 50))
enemy_dodger_img = pygame.transform.scale(enemy_dodger_img, (50, 50))
enemy_chaser_img = pygame.transform.scale(enemy_chaser_img, (50, 50))
boss_img = pygame.transform.scale(boss_img, (150, 150))
shield_img = pygame.transform.scale(shield_img, (40, 40))
double_fire_img = pygame.transform.scale(double_fire_img, (40, 40))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
enemy_fireball_img = pygame.transform.scale(enemy_fireball_img, (20, 10))

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Sound effects
pygame.mixer.init()
try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)  # Loop background music
    fireball_effect = pygame.mixer.Sound("fireball.mp3")
    collision_effect = pygame.mixer.Sound("collision.mp3")
    power_up_effect = pygame.mixer.Sound("power_up.mp3")
    boss_hit_effect = pygame.mixer.Sound("boss_hit.mp3")
except pygame.error as e:
    print(f"Sound error: {e}")
    fireball_effect = None
    collision_effect = None
    power_up_effect = None
    boss_hit_effect = None

# Game variables
game_started = False
game_over = False 
dragon_x = 100
dragon_y = SCREEN_HEIGHT // 2
dragon_speed = 0
gravity = 0.5
fireballs = []
enemies = []
enemy_fireballs = []
power_ups = []
boss = None
boss_active = False
boss_health = 0
boss_cooldown = 0
enemy_spawn_time = 1500
last_enemy_spawn = pygame.time.get_ticks()
last_fireball_time = pygame.time.get_ticks()
last_power_up_spawn = pygame.time.get_ticks()
screen_shake_duration = 0
score = 0
level = 1
health = 3
double_fire = False
double_fire_time = 0
shield_active = False
shield_time = 0
boss_active = False

# Fireball properties
fireball_speed = 10
fireball_cooldown = 500

# Background scrolling
bg_x = 0

def apply_screen_shake():
    global screen_shake_duration
    if screen_shake_duration > 0:
        offset = random.randint(-5, 5)
        return offset, offset
    return 0, 0

# Display Game Over screen
def show_game_over():
    screen.fill(WHITE)
    title_font = pygame.font.Font(None, 72)
    text_font = pygame.font.Font(None, 48)
    title = title_font.render("Game Over", True, RED)
    score_text = text_font.render(f"Your Score: {score}", True, BLACK)
    restart_text = text_font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))
    pygame.display.flip()



# Collision detection function
def detect_collision(obj1, obj2, width1, height1, width2, height2):
    reduction_factor = 0.2
    reduced_width1 = width1 * reduction_factor
    reduced_height1 = height1 * reduction_factor
    reduced_width2 = width2 * reduction_factor
    reduced_height2 = height2 * reduction_factor
    
    return (
        obj1[0] + reduced_width1 < obj2[0] + width2 - reduced_width2
        and obj1[0] + width1 - reduced_width1 > obj2[0] + reduced_width2
        and obj1[1] + reduced_height1 < obj2[1] + height2 - reduced_height2
        and obj1[1] + height1 - reduced_height1 > obj2[1] + reduced_height2
    )



# Main game loop
running = True
while running:
    if game_over:
        show_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    dragon_x = 100
                    dragon_y = SCREEN_HEIGHT // 2
                    dragon_speed = 0
                    fireballs = []
                    enemies = []
                    enemy_fireballs = []
                    power_ups = []
                    boss = None
                    boss_active = False
                    score = 0
                    level = 1
                    health = 3
                    double_fire = False
                    shield_active = False
                    game_over = False
                    game_started = False
                elif event.key == pygame.K_q:  # Quit game
                    running = False
        continue

    if not game_started:
        screen.fill(WHITE)
        title_font = pygame.font.Font(None, 72)
        text_font = pygame.font.Font(None, 48)
        title = title_font.render("Dragon Adventure Game", True, BLACK)
        instructions = text_font.render("Press SPACE to Start", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 300))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True
        continue

    # Scroll background
    screen.blit(background_img, (bg_x, 0))
    screen.blit(background_img, (bg_x + SCREEN_WIDTH, 0))
    bg_x -= 2
    if bg_x <= -SCREEN_WIDTH:
        bg_x = 0

    # Reduce screen shake duration
    if screen_shake_duration > 0:
        screen_shake_duration -= 1

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls: Keep dragon in the air with spacebar
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        dragon_speed = -8

    # Update dragon position
    dragon_speed += gravity
    dragon_y += dragon_speed

    # Restrict dragon to screen bounds
    dragon_y = max(0, min(dragon_y, SCREEN_HEIGHT - 90))  # Adjusted for larger dragon size

    # Check if dragon falls below the screen
    if dragon_y > SCREEN_HEIGHT - 90:
        if collision_effect:
            collision_effect.play()
        game_over = True

    # Boss behavior
    if score == 1000 and not boss_active:
        boss = {"x": SCREEN_WIDTH - 200, "y": random.randint(50, SCREEN_HEIGHT - 200), "health": 10}
        boss_active = True
        boss_start_time = pygame.time.get_ticks()
        enemies = [] #clearig enemies

    if boss_active and boss:
        boss_time_elapsed = pygame.time.get_ticks() - boss_start_time

        # Delay movement toward the player for 15 seconds
        if boss_time_elapsed > 15000:
            if boss["y"] < dragon_y:
                boss["y"] += 2
            elif boss["y"] > dragon_y:
                boss["y"] -= 2

        boss["x"] -= 2
        screen.blit(boss_img, (boss["x"], boss["y"]))

        # Boss fires projectiles
        if random.random() < 0.0001:
            enemy_fireballs.append({"x": boss["x"], "y": boss["y"] + 75})

        # Check if boss is defeated
        if boss["health"] <= 0:
            boss = None
            boss_active = False
            score += 500

    # Prevent score increment if boss is active
    if not boss_active:
        score += 1                   
        # Spawn small enemies
        if pygame.time.get_ticks() - last_enemy_spawn > enemy_spawn_time:
            enemy_type = random.choice(["normal", "fast", "shooter", "dodger", "chaser"])
            enemy_x = SCREEN_WIDTH
            enemy_y = random.randint(50, SCREEN_HEIGHT - 50)
            enemies.append({"x": enemy_x, "y": enemy_y, "type": enemy_type})
            last_enemy_spawn = pygame.time.get_ticks()
            
    # Fireball shooting with cooldown
    current_time = pygame.time.get_ticks()
    if keys[pygame.K_f] and current_time - last_fireball_time >= fireball_cooldown:
        fireballs.append([dragon_x + 60, dragon_y + 20])
        if double_fire:
            fireballs.append([dragon_x + 60, dragon_y - 20])
        last_fireball_time = current_time
        if fireball_effect:
            fireball_effect.play()

    # Update fireballs
    for fireball in fireballs:
        fireball[0] += fireball_speed

    # Remove off-screen fireballs
    fireballs = [fireball for fireball in fireballs if fireball[0] < SCREEN_WIDTH]

    # Increase difficulty based on score
    if score > level * 100:
        level += 1
        enemy_spawn_time = max(500, enemy_spawn_time - 100)

    # Enemy spawning
    if current_time - last_enemy_spawn > enemy_spawn_time:
        enemy_type = random.choice(["normal", "fast", "shooter", "dodger", "chaser"])
        enemy_x = SCREEN_WIDTH
        enemy_y = random.randint(50, SCREEN_HEIGHT - 50)
        enemies.append({"x": enemy_x, "y": enemy_y, "type": enemy_type})
        last_enemy_spawn = current_time

    # Boss spawning
    if level % 5 == 0 and boss is None:
        boss = {"x": SCREEN_WIDTH, "y": SCREEN_HEIGHT // 2, "health": 20}

    # Update enemies
    for enemy in enemies[:]:
        if enemy["type"] == "normal":
            enemy["x"] -= 5
            screen.blit(enemy_img, (enemy["x"], enemy["y"]))
        elif enemy["type"] == "fast":
            enemy["x"] -= 8
            screen.blit(enemy_fast_img, (enemy["x"], enemy["y"]))
        elif enemy["type"] == "shooter":
            enemy["x"] -= 5
            screen.blit(enemy_shooter_img, (enemy["x"], enemy["y"]))
            if random.random() < 0.02:
                enemy_fireballs.append({"x": enemy["x"], "y": enemy["y"] + 20})
        elif enemy["type"] == "dodger":
            if fireballs:
                nearest_fireball = min(fireballs, key=lambda f: abs(f[0] - enemy["x"]))
                if nearest_fireball[1] < enemy["y"]:
                    enemy["y"] += 3
                elif nearest_fireball[1] > enemy["y"]:
                    enemy["y"] -= 3
            enemy["x"] -= 5
            screen.blit(enemy_dodger_img, (enemy["x"], enemy["y"]))
        elif enemy["type"] == "chaser":
            if enemy["y"] < dragon_y:
                enemy["y"] += 3
            elif enemy["y"] > dragon_y:
                enemy["y"] -= 3
            enemy["x"] -= 5
            screen.blit(enemy_chaser_img, (enemy["x"], enemy["y"]))

    # Update enemy fireballs
    for ef in enemy_fireballs:
        ef["x"] -= fireball_speed
        screen.blit(enemy_fireball_img, (ef["x"], ef["y"]))

    # Remove off-screen enemy fireballs
    enemy_fireballs = [ef for ef in enemy_fireballs if ef["x"] > 0]

    # Update boss
    if boss:
        boss["x"] -= 2
        screen.blit(boss_img, (boss["x"], boss["y"]))
        if random.random() < 0.03:
            enemy_fireballs.append({"x": boss["x"], "y": boss["y"] + 75})
        if boss["x"] < 0 or boss["health"] <= 0:
            boss = None
            score += 200

    # Collision checks
    for fireball in fireballs[:]:
        for enemy in enemies[:]:
            if detect_collision(fireball, (enemy["x"], enemy["y"]), 30, 15, 50, 50):
                fireballs.remove(fireball)
                enemies.remove(enemy)
                score += 10
                break
        if boss and detect_collision(fireball, (boss["x"], boss["y"]), 30, 15, 150, 150):
            fireballs.remove(fireball)
            boss["health"] -= 1

    for enemy in enemies[:]:
        if detect_collision((dragon_x, dragon_y), (enemy["x"], enemy["y"]), 120, 90, 50, 50):
            if collision_effect:
                collision_effect.play()
            health -= 1
            enemies.remove(enemy)
            if health <= 0:
                game_over = True

    for ef in enemy_fireballs[:]:
        if detect_collision((dragon_x, dragon_y), (ef["x"], ef["y"]), 120, 90, 20, 10):
            if collision_effect:
                collision_effect.play()
            health -= 1
            enemy_fireballs.remove(ef)
            if health <= 0:
                game_over = True

    # Update power-ups
    if current_time - last_power_up_spawn > 10000:  # Every 10 seconds
        power_up_type = random.choice(["shield", "double_fire"])
        power_ups.append({"x": SCREEN_WIDTH, "y": random.randint(50, SCREEN_HEIGHT - 50), "type": power_up_type})
        last_power_up_spawn = current_time

    for power_up in power_ups[:]:
        power_up["x"] -= 3
        if power_up["type"] == "shield":
            screen.blit(shield_img, (power_up["x"], power_up["y"]))
        elif power_up["type"] == "double_fire":
            screen.blit(double_fire_img, (power_up["x"], power_up["y"]))

        if detect_collision((dragon_x, dragon_y), (power_up["x"], power_up["y"]), 120, 90, 40, 40):
            if power_up["type"] == "shield":
                shield_active = True
                shield_time = current_time
            elif power_up["type"] == "double_fire":
                double_fire = True
                double_fire_time = current_time
            power_ups.remove(power_up)

    # Handle shield and double fire expiration
    if shield_active and current_time - shield_time > 5000:  # 5 seconds
        shield_active = False
    if double_fire and current_time - double_fire_time > 5000:  # 5 seconds
        double_fire = False

    # Drawing the dragon
    screen.blit(dragon_img, (dragon_x, dragon_y))

    # Drawing fireballs
    for fireball in fireballs:
        screen.blit(fireball_img, (fireball[0], fireball[1]))

    # Draw the score, level, and health
    score += 1  # Increase score over time
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    health_text = font.render(f"Health: {health}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(health_text, (10, 70))

    # Update the screen
    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
