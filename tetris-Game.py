import pygame
import random
import time
import math
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Load sounds
try:
    move_sound = mixer.Sound('move.wav')
    rotate_sound = mixer.Sound('rotate.wav')
    drop_sound = mixer.Sound('drop.wav')
    clear_sound = mixer.Sound('clear.wav')
    gameover_sound = mixer.Sound('gameover.wav')
except:
    print("Sound files not found. Continuing without sound.")
    move_sound = rotate_sound = drop_sound = clear_sound = gameover_sound = None

# Shapes of the blocks with more standard Tetris shapes
shapes = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[4, 5, 9, 10], [2, 6, 5, 9]],   # Z
    [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
    [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
    [[0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 8, 9]],  # J
    [[1, 2, 5, 6]],  # O
]

# More vibrant colors
shapeColors = [
    (0, 240, 240),   # I - Cyan
    (240, 0, 0),     # Z - Red
    (0, 240, 0),     # S - Green
    (160, 0, 240),   # T - Purple
    (240, 160, 0),   # L - Orange
    (0, 0, 240),     # J - Blue
    (240, 240, 0),   # O - Yellow
]

# Game constants
width = 800
height = 700
gameWidth = 10 * 30  # 10 blocks wide
gameHeight = 20 * 30  # 20 blocks tall
blockSize = 30
topLeft_x = (width - gameWidth) // 2
topLeft_y = height - gameHeight - 50

# Particle class for line clear effects
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, math.pi * 2)
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1
        return self.life > 0
    
    def draw(self, screen):
        alpha = min(255, self.life * 6)
        s = pygame.Surface((self.size, self.size))
        s.set_alpha(alpha)
        s.fill(self.color)
        screen.blit(s, (self.x, self.y))

class Block:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.type = n
        self.color = n
        self.rotation = 0
        self.last_move_time = time.time()
    
    def image(self):
        return shapes[self.type][self.rotation]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(shapes[self.type])
        if rotate_sound:
            rotate_sound.play()

class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.state = "start"
        self.zoom = blockSize
        self.x = topLeft_x
        self.y = topLeft_y
        self.block = None
        self.nextBlock = None
        self.holdBlock = None
        self.can_hold = True
        self.particles = []
        self.last_drop_time = time.time()
        self.drop_delay = 1.0  # Initial drop delay in seconds
        self.move_delay = 0.1  # Delay for horizontal movement
        self.last_move_time = 0
        self.ghost_y = 0
    
    def new_block(self):
        self.block = Block(3, 0, random.randint(0, len(shapes) - 1))
        self.update_ghost()
        self.can_hold = True
    
    def next_block(self):
        self.nextBlock = Block(3, 0, random.randint(0, len(shapes) - 1))
    
    def hold_current(self):
        if not self.can_hold:
            return
        
        if self.holdBlock is None:
            self.holdBlock = Block(3, 0, self.block.type)
            self.new_block()
        else:
            temp_type = self.holdBlock.type
            self.holdBlock = Block(3, 0, self.block.type)
            self.block = Block(3, 0, temp_type)
        
        self.can_hold = False
        self.update_ghost()
    
    def update_ghost(self):
        if self.block is None:
            return
        
        self.ghost_y = self.block.y
        while not self.intersects(self.block.x, self.ghost_y + 1, self.block.rotation):
            self.ghost_y += 1
    
    def intersects(self, x=None, y=None, rotation=None):
        if x is None:
            x = self.block.x
        if y is None:
            y = self.block.y
        if rotation is None:
            rotation = self.block.rotation
        
        for i in range(4):
            for j in range(4):
                if i * 4 + j in shapes[self.block.type][rotation]:
                    if (i + y > self.height - 1 or 
                        j + x > self.width - 1 or 
                        j + x < 0 or 
                        self.field[i + y][j + x] > 0):
                        return True
        return False
    
    def break_lines(self):
        lines = 0
        particles = []
        
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            
            if zeros == 0:
                lines += 1
                # Create particles for cleared line
                for j in range(self.width):
                    color = shapeColors[self.field[i][j]-1] if self.field[i][j] > 0 else (255, 255, 255)
                    for _ in range(5):
                        particles.append(Particle(
                            self.x + j * self.zoom + self.zoom//2,
                            self.y + i * self.zoom + self.zoom//2,
                            color
                        ))
                
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        
        self.particles.extend(particles)
        
        if lines > 0:
            self.lines_cleared += lines
            # Update score based on lines cleared
            if lines == 1:
                self.score += 100 * self.level
            elif lines == 2:
                self.score += 300 * self.level
            elif lines == 3:
                self.score += 500 * self.level
            elif lines == 4:
                self.score += 800 * self.level
            
            # Update level every 10 lines
            self.level = self.lines_cleared // 10 + 1
            # Increase speed with level
            self.drop_delay = max(0.05, 1.0 - (self.level * 0.05))
            
            if clear_sound:
                clear_sound.play()
    
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.field[i + self.block.y][j + self.block.x] = self.block.color + 1
        
        self.break_lines()
        self.block = self.nextBlock
        self.next_block()
        self.can_hold = True
        
        if self.intersects():
            self.state = "gameover"
            if gameover_sound:
                gameover_sound.play()
    
    def move(self, dx):
        now = time.time()
        if now - self.last_move_time > self.move_delay:
            old_x = self.block.x
            self.block.x += dx
            if self.intersects():
                self.block.x = old_x
            else:
                if move_sound:
                    move_sound.play()
                self.last_move_time = now
            self.update_ghost()
    
    def rotate(self):
        old_rotation = self.block.rotation
        self.block.rotate()
        if self.intersects():
            self.block.rotation = old_rotation
        self.update_ghost()
    
    def drop(self):
        now = time.time()
        if now - self.last_drop_time > self.drop_delay:
            self.block.y += 1
            if self.intersects():
                self.block.y -= 1
                self.freeze()
            self.last_drop_time = now
            self.update_ghost()
    
    def hard_drop(self):
        while not self.intersects():
            self.block.y += 1
        self.block.y -= 1
        self.freeze()
        if drop_sound:
            drop_sound.play()
    
    def draw_ghost(self, screen):
        if self.block is None:
            return
        
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.block.image():
                    pygame.draw.rect(screen, shapeColors[self.block.color],
                                    [self.x + self.zoom * (j + self.block.x) + 1,
                                     self.y + self.zoom * (i + self.ghost_y) + 1,
                                     self.zoom - 2, self.zoom - 2], 1)
    
    def draw_hold(self, screen):
        if self.holdBlock is None:
            return
        
        font = pygame.font.SysFont("Calibri", 30)
        label = font.render("Hold", 1, (200, 200, 200))
        sx = topLeft_x - 150
        sy = topLeft_y + 100
        screen.blit(label, (sx, sy - 40))
        
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in shapes[self.holdBlock.type][0]:  # Only show first rotation
                    pygame.draw.rect(screen, shapeColors[self.holdBlock.color],
                                    (sx + j * 30 + 15, sy + i * 30, 30, 30), 0)
                    pygame.draw.rect(screen, (50, 50, 50),
                                    (sx + j * 30 + 15, sy + i * 30, 30, 30), 1)
    
    def draw_next_block(self, screen):
        if self.nextBlock is None:
            return
        
        font = pygame.font.SysFont("Calibri", 30)
        label = font.render("Next", 1, (200, 200, 200))
        sx = topLeft_x + gameWidth + 50
        sy = topLeft_y + 100
        screen.blit(label, (sx, sy - 40))
        
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in shapes[self.nextBlock.type][0]:  # Only show first rotation
                    pygame.draw.rect(screen, shapeColors[self.nextBlock.color],
                                    (sx + j * 30, sy + i * 30, 30, 30), 0)
                    pygame.draw.rect(screen, (50, 50, 50),
                                    (sx + j * 30, sy + i * 30, 30, 30), 1)
    
    def update_particles(self):
        self.particles = [p for p in self.particles if p.update()]

def draw_game_info(screen, game):
    # Draw score
    font = pygame.font.SysFont('Arial', 30, bold=True)
    score_text = font.render(f"Score: {game.score}", True, (240, 240, 240))
    screen.blit(score_text, [30, 30])
    
    # Draw level
    level_text = font.render(f"Level: {game.level}", True, (240, 240, 240))
    screen.blit(level_text, [30, 70])
    
    # Draw lines
    lines_text = font.render(f"Lines: {game.lines_cleared}", True, (240, 240, 240))
    screen.blit(lines_text, [30, 110])

def startGame():
    done = False
    clock = pygame.time.Clock()
    game = Tetris(20, 10)
    game.new_block()
    game.next_block()
    
    # Game loop
    while not done:
        # Automatic dropping
        if game.state == "start":
            game.drop()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_DOWN:
                    game.drop()
                elif event.key == pygame.K_LEFT:
                    game.move(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                elif event.key == pygame.K_c:
                    game.hold_current()
                elif event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)
                    game.new_block()
                    game.next_block()
        
        # Continuous movement when key is held
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            game.drop()
        if keys[pygame.K_LEFT]:
            game.move(-1)
        if keys[pygame.K_RIGHT]:
            game.move(1)
        
        # Update particles
        game.update_particles()
        
        # Draw everything
        screen.fill((20, 20, 40))  # Dark blue background
        
        # Draw game area border
        pygame.draw.rect(screen, (100, 100, 120), 
                        [game.x - 3, game.y - 3, gameWidth + 6, gameHeight + 6], 3)
        
        # Draw grid
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, (40, 40, 60), 
                                [game.x + game.zoom * j, game.y + game.zoom * i, 
                                 game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, shapeColors[game.field[i][j] - 1],
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, 
                                     game.zoom - 2, game.zoom - 2])
        
        # Draw ghost piece
        game.draw_ghost(screen)
        
        # Draw current piece
        if game.block is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.block.image():
                        pygame.draw.rect(screen, shapeColors[game.block.color],
                                        [game.x + game.zoom * (j + game.block.x) + 1,
                                         game.y + game.zoom * (i + game.block.y) + 1,
                                         game.zoom - 2, game.zoom - 2])
                        # Add highlight to blocks
                        highlight = pygame.Surface((game.zoom - 4, game.zoom - 4))
                        highlight.set_alpha(80)
                        highlight.fill((255, 255, 255))
                        screen.blit(highlight, 
                                   (game.x + game.zoom * (j + game.block.x) + 2,
                                    game.y + game.zoom * (i + game.block.y) + 2))
        
        # Draw particles
        for particle in game.particles:
            particle.draw(screen)
        
        # Draw next and hold pieces
        game.draw_next_block(screen)
        game.draw_hold(screen)
        
        # Draw game info
        draw_game_info(screen, game)
        
        # Game over message
        if game.state == "gameover":
            font = pygame.font.SysFont('Arial', 50, bold=True)
            text_game_over = font.render("GAME OVER", True, (240, 50, 50))
            text_restart = font.render("Press ESC", True, (200, 200, 200))
            screen.blit(text_game_over, [width//2 - 150, height//2 - 60])
            screen.blit(text_restart, [width//2 - 100, height//2 + 10])
        
        pygame.display.flip()
        clock.tick(60)

# Main menu
def show_menu():
    run = True
    title_font = pygame.font.SysFont("Arial", 80, bold=True)
    instruction_font = pygame.font.SysFont("Arial", 30)
    
    while run:
        screen.fill((20, 20, 40))
        
        # Title
        title = title_font.render("TETRIS", True, (240, 240, 240))
        screen.blit(title, (width//2 - title.get_width()//2, 150))
        
        # Instructions
        instructions = [
            "CONTROLS:",
            "← → : Move",
            "↑ : Rotate",
            "↓ : Soft Drop",
            "SPACE : Hard Drop",
            "C : Hold Piece",
            "ESC : Restart Game",
            "",
            "Press any key to start"
        ]
        
        for i, line in enumerate(instructions):
            text = instruction_font.render(line, True, (200, 200, 200))
            screen.blit(text, (width//2 - text.get_width()//2, 250 + i * 35))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                startGame()
                run = False
    
    pygame.quit()

# Initialize and run the game
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Enhanced Tetris")
show_menu()