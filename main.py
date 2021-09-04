import pygame
import os
import neat
# inspired by tech with tim youtube tutorial (pygame and flappy bird ones)
"""
For this challenge:
1) Build a game which is like brick breaker except you are controling a ball above the bricks influenced by gravity and you loose if you fall off the screen before hitting all the bricks
2) Use that flappy bird AI tutorial to build an AI that can play the game
3) add bricks that must be hit multiple times in order to fully break
"""

pygame.init()
window = pygame.display.set_mode((600, 600))  # creates window
pygame.display.set_caption("Jumpy Brick Breaker (AI Edition)")
myfont = pygame.font.SysFont('Comic Sans MS', 30)


class Ball:

    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.vel = 5
        self.radius = 10
        self.color = (100, 100, 100)
        self.time = 0
        self.score = 0
        self.board = board

    def move_left(self):
        self.x += self.vel

        self.time += 1
        d = self.vel * self.time + 1.5 * self.time ** 2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

    def move_right(self):
        self.x -= self.vel

        self.time += 1
        d = self.vel * self.time + 1.5 * self.time ** 2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

    def move_ball(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x > 10:
            self.move_left()
        elif keys[pygame.K_d] and self.x < 590:
            self.move_right()
        else:

            self.time += 1
            d = self.vel * self.time + 1.5 * self.time ** 2

            if d >= 16:
                d = 16

            if d < 0:
                d -= 2

            self.y = self.y + d

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, 0)

    def check_brick_collision(self, ge):  # I recall a more advanced way to do this from the Flappy Bird AI tutorial - look at the code
        #output= multiReturn(input.board, input.ge)

        row = 0
        col = 0
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[0])):
                if self.board[row][col] >= 1:
                    if (self.x < 60 * col + 58) and (self.x >= 60 * col):
                        if (self.y < 44 * row + 20) and (self.y >= 44 * row):
                            self.board[row][col] -= 1
                            self.score += 1
                            #for g in ge:
                            ge.fitness += 1

                            # if brick is hit from top
                            if self.y < 44 * row + 5:
                                self.vel = -10.5
                                self.time = 0

                            # if brick is hit from bottom
                            elif self.y >= 44 * row + 15:
                                self.vel = abs(self.vel)
                                self.time = 0

                            # if brick is hit from side
                                # nothing I guess
                            return ge
                col += 1
            row += 1

        return ge

"""
class multiReturn:
    def __init__(self, board, ge):
        self.board = board
        self.ge = ge
"""

def main(genomes, config):
    nets = []
    ge = []
    players = []

    #player = Ball(50, 50)

    # SET UP SCREEN
    fake_board = [[0 for x in range(12)] for y in range(13)]
    board = [[0 for x in range(12)] for y in range(13)]
    x = 0
    with open("level1.txt") as file:
        for row in fake_board:
            fake_board[x] = file.readline().rstrip().split(' ')
            x += 1

    for row in range(0, len(fake_board)):
        for col in range(0, len(fake_board[0])):
            board[row][col] = int(fake_board[row][col])

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Ball(50, 50, board))
        g.fitness = 0
        ge.append(g)

    # END SET UP

    runs = True

    while runs:
        for x, player in enumerate(players):
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            player.move_ball()
            #ge[x].fitness += 1

            output = nets[x].activate((player.x, player.y, player.vel)) # make each have its own board and add that as an input for more accuracy

            if output[0] > 0.5:
                player.move_left()
            elif output[0] < 0.15:
                player.move_right()

            ge[x] = player.check_brick_collision(ge[x])

            # RENDER SCREEN
            render_screen(players, board)

        #for player in players:
            # game over
            if player.y >= 600 or player.y < 0 or player.x < 0 or player.y >= 600:
                #ge[x].fitness -= 10
                players.pop(x)
                nets.pop(x)
                ge.pop(x)
                # pygame.quit()

        if len(players)<=0:
            runs = False

def render_screen(players, board):
    window.fill((0, 0, 0))

    #scoreText = myfont.render('Score: ' + str(player.score), False, (100, 100, 100))
    #window.blit(scoreText, (0, 560))

    for player in players:
        player.draw()

    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            if board[row][col] == 1:
                pygame.draw.rect(window, (255, 133, 133), [60*col, 44*row, 55, 20])

    pygame.display.update()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 500)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)  #gives path to current directory
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

"""
1) add board for each ball
2) save data
3) play around with brick numbers
5) party (upload this and the Unity game to GitHub to show my projects!!!)

https://www.youtube.com/watch?v=NPbHUyVDYDw&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&index=7
"""