import random
import pygame

#global vars
win_width = 500
win_height = 500
block_size = 20
q_number = 16
play_size = block_size*q_number
top_left_x = (win_width - play_size) / 2
top_left_y = (win_height - play_size) /3 *2
colors = {"black":(0,0,0), "white":(255,255,255), "red":(255,0,0), "green":(0,0,255), "grey":(128,128,128)}

#each sublist of snake contains following info:
#x_coordinate, y_coordinate, if_food var
#first element of snake is its tail
snake = []
food = [15,15]

#       0
#   3       1
#       2
#that means turning left:   direction = (direction + 3) % 4
#           turning right:  direction = (direction + 1) % 4
direction = 0

def get_new_food():
    good_pos = False
    while not(good_pos):
        x = random.randint(0,30) % q_number
        y = random.randint(0,30) % q_number
        check = True
        for sublist in snake:
            if sublist[0] == y and sublist[1] == x:
                check = False
        good_pos = check
    return [x,y]


def create_grid(food):
    grid = [[(112, 112, 112) for x in range(q_number)] for x in range(q_number)]

    for sublist in snake:
        if sublist[2] == 0:
            grid[sublist[1]][sublist[0]] = (0, 255, 255)
        else:
            grid[sublist[1]][sublist[0]] = (0, 0, 255)

    grid[food[0]][food[1]] = (255,0,0)
    return grid


def draw_lines(surface):
    sx = top_left_x
    sy = top_left_y
    for i in range(q_number):
        # horizontal lines
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size), (sx + play_size, sy + i*block_size))
        for j in range(q_number):
            # vertical lines
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_size))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_size/2 - label.get_width()/2, top_left_y*3/4 + play_size/2 - label.get_height()/2))

def draw_window(surface):
    surface.fill((50, 50, 50))

    # draw title
    font = pygame.font.SysFont('purisa', 60)
    label = font.render('SNAKE', 1, (230,230,230))
    surface.blit(label, (top_left_x + play_size / 2 - label.get_width()/2, top_left_y/2 - label.get_height()/2))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    # draw lines
    draw_lines(surface)

    # draw border
    pygame.draw.rect(surface, (0, 0, 0), (top_left_x, top_left_y, play_size, play_size), 5)

    pygame.display.update()


def get_new_pos(turn):
    new_pos_x = snake[0][0]
    new_pos_y = snake[0][1]

    global direction
    direction += turn
    direction %= 4
    if direction == 0:      #go up
        new_pos_y -= 1
    elif direction == 2:    #go down
        new_pos_y += 1
    elif direction == 3:    #go left
        new_pos_x -= 1
    elif direction == 1:    #go right
        new_pos_x +=1

    new_pos_x %= q_number
    new_pos_y %= q_number

    return [new_pos_x, new_pos_y]


def snake_move(new_pos):
    global food
    if new_pos[0] == food[1] and new_pos[1] == food[0]:
        snake.insert(0, [new_pos[0], new_pos[1], 1])
        food = get_new_food()

    else:
        for sublist in snake:
            if sublist[0] == new_pos[0] and sublist[1] == new_pos[1]:
                return False

        snake.insert(0, [new_pos[0], new_pos[1], 0])

    if snake[-1][2] == 0:
        del snake [-1]
    else:
        snake[-1][2] = 0

    return True

def main(win):
    global grid
    global snake
    global food
    global direction

    grid = create_grid(food)
    run = True

    not_lost = True
    direction = 0
    sx = int(play_size/2/block_size)
    snake = [[sx, sx, 0], [sx, sx+1, 0], [sx, sx+2, 0], [sx, sx+3, 0], [sx, sx+4, 0]]
    food = get_new_food()

    clock = pygame.time.Clock()
    time_since_last_move = 0

    while run:
        run_speed = 0.4

        time_since_last_move += clock.get_rawtime()
        clock.tick()

        # Just running forward
        if time_since_last_move / 1000 >= run_speed:
            new_pos = get_new_pos(0)
            not_lost = snake_move(new_pos)
            time_since_last_move = 0

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_pos = get_new_pos(3)
                    not_lost = snake_move(new_pos)

                elif event.key == pygame.K_RIGHT:
                    new_pos = get_new_pos(1)
                    not_lost = snake_move(new_pos)

                elif event.key == pygame.K_DOWN:
                    snake2 = []
                    for i in range(len(snake)):
                        snake2.append(snake[-i-1])
                    snake = snake2
                    direction += 2
                    direction %= 4

        grid = create_grid(food)
        draw_window(win)

        # Check if user lost
        if not_lost == False:
            run = False

    draw_text_middle("You Lost", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)

def main_menu(win):
    run_main_menu = True
    while run_main_menu:
        win.fill((0,0,0))
        draw_text_middle('Press any key to begin.', 40, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_main_menu = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.quit()


pygame.font.init()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Snake_by_wisnia')
main_menu(win)  # start game
