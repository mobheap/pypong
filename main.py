# Importing the libraries
import pygame as pg
from random import choice
import sys

# Game class
class PongGame:
    WIDTH, HEIGHT = 800, 600
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
    BALL_RADIUS = 15
    BALL_SPEED_X = BALL_SPEED_Y = 5
    PADDLE_SPEED = 10
    
    def __init__(self):
        # Game settings
        pg.font.init()
        pg.mixer.init()
        
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption("PyPong")
        
        pg.mixer.music.load('Ocarina_of_Time.mp3')
        pg.mixer.music.play(-1)
        
        # Game variables
        self.player1 = [50, (self.HEIGHT - self.PADDLE_HEIGHT)/2]
        self.player2 = [self.WIDTH-50-self.PADDLE_WIDTH, (self.HEIGHT - self.PADDLE_HEIGHT)/2]
        self.ball_pos = [self.WIDTH//2, self.HEIGHT//2]
        self.ball_speed = [self.BALL_SPEED_X, self.BALL_SPEED_Y]
        self.p1_score = 0
        self.p2_score = 0
        self.font = pg.font.Font(None, 74)
        
    def paddle(self, pos):
        pg.draw.rect(self.screen, self.WHITE, (pos[0], pos[1], self.PADDLE_WIDTH, self.PADDLE_HEIGHT))
    
    def ball(self):
        pg.draw.circle(self.screen, self.WHITE, self.ball_pos, self.BALL_RADIUS)
    
    # check if ball touches the paddle
    def hit_paddle(self, ball_pos, paddle_pos):
        return (paddle_pos[0] <= ball_pos[0] <= paddle_pos[0] + self.PADDLE_WIDTH and
                paddle_pos[1] <= ball_pos[1] <= paddle_pos[1] + self.PADDLE_HEIGHT)
    
    # move ball
    def update_ball(self):
        self.ball_pos[0] += self.ball_speed[0]    # x speed
        self.ball_pos[1] += self.ball_speed[1]    # y speed
        
        # Ball collision with top and bottom walls
        if self.ball_pos[1] <= self.BALL_RADIUS or self.ball_pos[1] >= self.HEIGHT - self.BALL_RADIUS:
            self.ball_speed[1] = -self.ball_speed[1]
        
        # Ball collision with paddles
        if self.hit_paddle(self.ball_pos, self.player1) or self.hit_paddle(self.ball_pos, self.player2):
            self.ball_speed[0] = -self.ball_speed[0]
        
        # Ball goes out of bounds
        if self.ball_pos[0] < 0:
            self.p2_score += 1
            self.reset_ball()
        elif self.ball_pos[0] > self.WIDTH:
            self.p1_score += 1
            self.reset_ball()
    
    def reset_ball(self):
        self.ball_pos = [self.WIDTH // 2, self.HEIGHT // 2]
        self.ball_speed = [self.BALL_SPEED_X * choice([-1, 1]), self.BALL_SPEED_Y * choice([-1, 1])]
    
    def move_paddles(self):                     # Controls for the game
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.player1[1] > 0:
            self.player1[1] -= self.PADDLE_SPEED
        if keys[pg.K_s] and self.player1[1] < self.HEIGHT - self.PADDLE_HEIGHT:
            self.player1[1] += self.PADDLE_SPEED
        if keys[pg.K_UP] and self.player2[1] > 0:
            self.player2[1] -= self.PADDLE_SPEED
        if keys[pg.K_DOWN] and self.player2[1] < self.HEIGHT - self.PADDLE_HEIGHT:
            self.player2[1] += self.PADDLE_SPEED
    
    def draw_scores(self):
        p1_text = self.font.render(str(self.p1_score), True, self.WHITE)
        p2_text = self.font.render(str(self.p2_score), True, self.WHITE)
        self.screen.blit(p1_text, (self.WIDTH // 4, 20))
        self.screen.blit(p2_text, (self.WIDTH * 3 // 4, 20))
    
    def run_game(self):
        run = True
        while run:
            for e in pg.event.get():            # to end the game
                if e.type == pg.QUIT:
                    run = False
                    sys.exit()
            
            self.screen.fill(self.BLACK)
            self.paddle(self.player1)
            self.paddle(self.player2)
            self.ball()
            self.draw_scores()
            self.update_ball()
            self.move_paddles()
            
            pg.display.update()
            self.clock.tick(60)
            
if __name__ == '__main__':
    game = PongGame()
    game.run_game()
