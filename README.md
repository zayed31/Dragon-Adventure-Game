# 🐉 Dragon Adventure Game

**Dragon Adventure** is a 2D side-scrolling shooter game built with Pygame, where you control a mighty dragon battling waves of enemies and powerful bosses. Dodge, shoot, collect power-ups, and aim for the highest score!

## 🎮 Features

- Smooth side-scrolling dragon flight mechanics
- Multiple enemy types (chaser, shooter, dodger, etc.)
- Fireball shooting with power-ups (double fire, shield)
- Epic boss battles with unique behaviors
- Health and score tracking
- Game over and restart functionality
- Sound effects and background music

## 🛠️ Technologies Used

- Python
- Pygame (for graphics, sound, and game loop)

## 📂 Project Structure

```
dragon-adventure-game/
├── main.py
├── assets/
│   ├── dragonmain.png
│   ├── fireball.png
│   ├── dragon1.png
│   ├── enemy_fast.png
│   ├── enemy_shooter.png
│   ├── dragon2.png
│   ├── dragonboss.png
│   ├── background.jpg
│   ├── coin.png
│   ├── background_music.mp3
│   ├── fireball.mp3
│   ├── collision.mp3
│   ├── power_up.mp3
│   └── boss_hit.mp3
```

> 📌 _Make sure to place all required image and sound files in an `assets/` folder for better organization._

## 🚀 How to Run the Game

### 1. Install Pygame

Make sure you have Python installed. Then install Pygame:

```bash
pip install pygame
```

### 2. Run the Game

Navigate to the project folder and run:

```bash
python main.py
```

### 3. Controls

- `SPACE`: Jump / Fly upward
- `F`: Shoot fireball
- `R`: Restart (when game over)
- `Q`: Quit (when game over)

## 🏆 Game Mechanics

- Score increases over time and with enemy kills
- Boss appears after reaching a score threshold
- Health decreases on collisions or hits
- Power-ups spawn every 10 seconds:
  - 🛡️ Shield: Temporary invincibility
  - 🔥 Double Fire: Fires two projectiles at once

## 📜 License

This project is open-source. Feel free to modify and build upon it!
