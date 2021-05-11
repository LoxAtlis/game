from random import randint

WIDTH = 800
HEIGHT = 600
lines = 0
power_up_apparition =  50# percent

time_bigger_player = 0
vie = 5
heart = Actor("heart")
heart.pos = [30, 580]
gameover = Actor("gameover")
gameover.pos = [400,300]


bg = Actor("fond")
bg.pos = [400, 300]

end = Actor("end")
end.pos = [400, 300]

player = Actor("player")
player.pos = [400, 550]

ball = Actor("ball")
ball.pos = [400, 500]
ball_speed = [3, -3]
power_up_speed = [0, 3]

all_bricks = []
all_super_bricks = []
all_power_up_bigger_player = []

for x in range(0, 800, 100):
    for y in range(0, 30 * lines, 30):
        brick = Actor("brick", anchor=["left", "top"])
        brick.pos  = [x, y]
        all_bricks.append(brick)

for x in range(0, 800, 100):
     super_brick = Actor("brick2-1", anchor=["left", "top"])
     super_brick.pos = [x, 30 * lines + 1]
     all_super_bricks.append(super_brick)

    #son pour le jeu
def reboot():
    global ball_speed
    ball.pos = [400, 500]
    ball_speed = [3, -3]

def draw():
    screen.clear()
    bg.draw()
    for brick in all_bricks:
        brick.draw()

    for super_brick in all_super_bricks:
        super_brick.draw()

    for power_up_bigger_player in all_power_up_bigger_player:
        power_up_bigger_player.draw()

    player.draw()
    ball.draw()

    if vie == 0:
        gameover.draw()

    if all_bricks == [] and all_super_bricks == []:
        end.draw()

def on_mouse_move(pos):
    player.pos = [pos[0], player.pos[1]]


def invert_horizontal_speed():
    ball_speed[0] = ball_speed[0] * -1


def invert_vertical_speed():
    ball_speed[1] = ball_speed[1] * -1

def upgrade_ball_speed(upgrade):
    if ball_speed[0] > 0:
        ball_speed[0] = ball_speed[0] + upgrade
    else:
        ball_speed[0] = ball_speed[0] - upgrade

    if ball_speed[1] > 0:
        ball_speed[1] = ball_speed[1] + upgrade
    else:
        ball_speed[1] = ball_speed[1] - upgrade

def update(dt):
    global time_bigger_player
    global player
    global vie
    global brick
    global music
    if time_bigger_player > 0:
        time_bigger_player = time_bigger_player - dt

        if time_bigger_player <= 0:
            player = Actor("player", player.pos)

    # move ball
    new_x = ball.pos[0] + ball_speed[0]
    new_y = ball.pos[1] + ball_speed[1]

    ball.pos = [new_x, new_y]

    if ball.bottom >= HEIGHT and vie >= 1:
        vie = vie - 1
        reboot()
    # move power up
    for power_up_bigger_player in all_power_up_bigger_player:
        new_x = power_up_bigger_player.pos[0] + power_up_speed[0]
        new_y = power_up_bigger_player.pos[1] + power_up_speed[1]

        power_up_bigger_player.pos = [new_x, new_y]

    # check boundaries
    if ball.right >= WIDTH or ball.left <= 0:
        invert_horizontal_speed()

    if all_bricks == [] and all_super_bricks == []:
        music.play("end")

    if ball.top <= 0:
        invert_vertical_speed()
    # check collision with other actors

    if ball.colliderect(player):
        invert_vertical_speed()
        upgrade_ball_speed(0.25)
        print(ball_speed)

    for brick in all_bricks:
        if brick.colliderect(ball):
            invert_vertical_speed()
            all_bricks.remove(brick)



            rnd = randint(0, 100)

            # check si une power up apparait
            if rnd <= power_up_apparition:
                power_up = Actor("powerup1", anchor=["left", "top"])
                power_up.pos  = brick.pos
                all_power_up_bigger_player.append(power_up)

    for super_brick in all_super_bricks:
        if super_brick.colliderect(ball):
            invert_vertical_speed()
            all_super_bricks.remove(super_brick)



            brick = Actor("brick2-2", anchor=["left", "top"])
            brick.pos  = super_brick.pos
            all_bricks.append(brick)

    for power_up_bigger_player in all_power_up_bigger_player:
        if player.colliderect(power_up_bigger_player):
            all_power_up_bigger_player.remove(power_up_bigger_player)
            time_bigger_player = 3
            player = Actor("bigger_player", player.pos)