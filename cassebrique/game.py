WIDTH = 800
HEIGHT = 600
lines = 7

player = Actor("player")
player.pos = [400, 550]

ball = Actor("ball")
ball.pos = [400, 500]
ball_speed = [3, -3]
all_bricks = []
all_super_bricks =[]

for x in range(0, 800, 100):
    for y in range (0, 30* lines, 30):

        brick = Actor("brick", anchor=["left","top"])
        brick.pos = [x, y]
        all_bricks.append(brick)

for x in range(0, 800, 100):
    super_brick = Actor("brick2-1", anchor = ["left", "top"])
    super_brick.pos = [x, 30*lines+1]
    all_super_bricks.append(super_brick)

def draw():
    screen.clear()


    for brick in all_bricks:
        brick.draw()

    for super_brick in all_super_bricks:
        super_brick.draw()

    player.draw()
    ball.draw()

def on_mouse_move(pos):
    player.pos = pos[0], player.pos[1]

def invert_horizontal_speed():
    ball_speed[0] = ball_speed[0]*-1

def invert_vertical_speed():
    ball_speed[1] = ball_speed[1]*-1



def update():
    new_x = ball.pos[0] + ball_speed[0]
    new_y = ball.pos[1] + ball_speed[1]

    ball.pos = [new_x,new_y]

    if ball.right > WIDTH or ball.left <= 0 :
        invert_horizontal_speed()

    if ball.top <= 0:
        invert_vertical_speed()

    if ball.colliderect(player):
        invert_vertical_speed()

    for brick in all_bricks:
        if brick.colliderect(ball):

            invert_vertical_speed()
            all_bricks.remove(brick)

    for super_brick in all_super_bricks:
        if super_brick.collederect(ball):
            invert_vertical_speed()
            all_super_bricks.remove(super_brick)

            brick = Actor("brick2-2", anchor = ["left", "top"]
            brick.pos = super_brick.pos
            all_bricks.append(brick)