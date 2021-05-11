from random import randint

WIDTH = 800
HEIGHT = 600
lines = 6
vie = 5
heart = Actor("heart")
heart.pos = [30, 580]
end = Actor("end")
end.pos = [400, 300]
power_up_apparition = 20
power_upd_apparition = 20
malus_apparition = 10
time_bigger_player = 0
time_bigger_ball = 0
player = Actor("player")
player.pos = [400, 550]

game_over = Actor("gameover")
game_over.pos = [400, 300]


bg = Actor("fond")
bg.pos = [400, 300]

ball = Actor("ball")
ball.pos = [400, 500]
ball_speed = [3, -3]
bigger_ball = Actor("superball")
bigger_ball_speed = [3, -3]
power_up_speed = [0, 3]
malus_speed = [0, 3]
power_upd_speed = [0, 3]

all_bricks = []
all_super_bricks = []
all_triple_bricks = []
all_power_up_bigger_player = []
all_power_up_bigger_ball = []
all_malus_player = []
all_heart = []
all_pbrick = []

for x in range(0, 800, 100):
    for y in range(0, 30 *2, 30):
        triple_brick = Actor("brick3-1", anchor=["left", "top"])
        triple_brick.pos  = [x, y]
        all_triple_bricks.append(triple_brick)


for x in range(0, 800, 100):
    super_brick = Actor("brick2-1", anchor=["left", "top"])
    super_brick.pos = [x, 30 *3+1 ]
    all_super_bricks.append(super_brick)
for x in range(0, 800, 100):
    brick = Actor("brick", anchor = ["left","top"])
    brick.pos =[x, 30*5]
    all_bricks.append(brick)
for x in range(0, 800, 100):
    brick = Actor("brick", anchor = ["left","top"])
    brick.pos =[x, 30*7]
    all_bricks.append(brick)

for x in range(0, 800, 100):
    super_brick = Actor("brick2-1", anchor=["left", "top"])
    super_brick.pos = [x, 30 *4 ]
    all_super_bricks.append(super_brick)
for x in range(0, 800, 100):
    super_brick = Actor("brick2-1", anchor=["left", "top"])
    super_brick.pos = [x, 30 *6 ]
    all_super_bricks.append(super_brick)

for x in range(0, 800, 100):
    pbrick = Actor("pbrick", anchor=["left", "top"])
    pbrick.pos = [x, 30 *10 ]
    all_pbrick.append(pbrick)

for x in range(0, 800, 100):
    for x in range(0, 30*26, 60):
        pbrick = Actor("pbrick", anchor=["left", "top"])
        pbrick.pos = [x, 250]
        all_pbrick.append(pbrick)


def reboot():
    global ball_speed
    ball.pos = [400, 500]
    ball_speed = [3, -3]

music.play("cavern")

def draw():
    screen.clear()
    bg.draw()

    for brick in all_bricks:
        brick.draw()

    #for super_brick in all_super_bricks:
       # super_brick.draw()

    for triple_brick in all_triple_bricks:
        triple_brick.draw()

    for pbrick in all_pbrick:
        pbrick.draw()

    for power_up_bigger_player in all_power_up_bigger_player:
        power_up_bigger_player.draw()

    for power_up_bigger_ball in all_power_up_bigger_ball:
        power_up_bigger_ball.draw()

    for malus in all_malus_player:
        malus.draw()



    player.draw()
    ball.draw()

    if vie == 0:
        game_over.draw()

    if all_bricks == [] and all_super_bricks == [] and all_triple_bricks == [] and all_pbrick == []:
        end.draw()

def on_mouse_move(pos):
    player.pos = [pos[0], player.pos[1]]

def update_power_up():
    for power_up_bigger_player in all_power_up_bigger_player:
        new_x = power_up_bigger_player.pos[0]+ power_up_speed[0]
        new_y = power_up_bigger_player.pos[1]+ power_up_speed[1]
        power_up_bigger_player.pos = [new_x, new_y]

def updade_power_upd():
    for power_up_bigger_ball in all_power_up_bigger_ball:
        new_x = power_up_bigger_ball.pos[0]+ power_upd_speed[0]
        new_y = power_up_bigger_ball.pos[1]+ power_upd_speed[1]
        power_up_bigger_ball.pos = [new_x, new_y]

def degat_malus():
    for malus_player in all_malus_player:
        new_x = malus_player.pos[0]+ malus_speed[0]
        new_y = malus_player.pos[1]+ malus_speed[1]
        malus_player.pos = [new_x, new_y]


def invert_horizontal_speed():
    ball_speed[0] = ball_speed[0] * -1
    bigger_ball_speed[0] = bigger_ball_speed[0] *-1

def invert_vertical_speed():
    ball_speed[1] = ball_speed[1] * -1
    bigger_ball_speed[1] = bigger_ball_speed[1] *-1

def updade_ball_speed(ratio):
        ball_speed[0] = ball_speed[0] * ratio
        ball_speed[1] = ball_speed[1] * ratio

def update(dt):
    global time_bigger_player
    global time_bigger_ball
    global player
    global vie
    global ball
    global music

    if time_bigger_player > 0:
        time_bigger_player = time_bigger_player - dt
        if time_bigger_player <= 0:
            player = Actor("player", player.pos)

    if time_bigger_ball > 0:
        time_bigger_ball = time_bigger_ball - dt
        if time_bigger_ball <= 0:
            ball = Actor("ball", ball.pos)

    new_x = ball.pos[0] + ball_speed[0]
    new_y = ball.pos[1] + ball_speed[1]

    ball.pos = [new_x, new_y]

    update_power_up()
    updade_power_upd()
    degat_malus()



    if ball.bottom >= HEIGHT and vie >= 1:
        vie = vie - 1
        reboot()
        if vie == 0 :
            music.play("go")

    if ball.right >= WIDTH or ball.left <= 0:
        invert_horizontal_speed()

    if ball.top <= 0:
        invert_vertical_speed()


    if ball.colliderect(player):
        invert_vertical_speed()
        updade_ball_speed(1.05)
        print(ball_speed)
        sounds.jump.play()

    for brick in all_bricks:
        if brick.colliderect(ball):
            all_bricks.remove(brick)
            if ball.pos[0] >= brick.left and ball.pos[0] <= brick.right:
                invert_vertical_speed()
            else:
                invert_horizontal_speed()
            sounds.exp.play()
            rnd = randint(0,100)
            if rnd <= power_up_apparition:
                power_up = Actor("powerup1",anchor=["left", "top"])
                power_up.pos = brick.pos
                all_power_up_bigger_player.append(power_up)

            rnd1 = randint(0,100)
            if rnd1 <= malus_apparition:
                malus = Actor("malus",anchor=["left", "top"])
                malus.pos = brick.pos
                all_malus_player.append(malus)


            rnd2 = randint(0,100)
            if rnd2 <= power_upd_apparition:
                power_upd = Actor("powerup2",anchor=["left", "top"])
                power_upd.pos = brick.pos
                all_power_up_bigger_ball.append(power_upd)

    for super_brick in all_super_bricks:
        if super_brick.colliderect(ball):
            all_super_bricks.remove(super_brick)
            if ball.pos[0] >= super_brick.left and ball.pos[0] <= super_brick.right:
                invert_vertical_speed()
            else:
                invert_horizontal_speed()


            brick = Actor("brick2-2", anchor=["left", "top"])
            brick.pos  = super_brick.pos
            all_bricks.append(brick)

    for triple_brick in all_triple_bricks:
        if triple_brick.colliderect(ball):
            all_triple_bricks.remove(triple_brick)
            if ball.pos[0] >= triple_brick.left and ball.pos[0] <= triple_brick.right:
                invert_vertical_speed()
            else:
                invert_horizontal_speed()

            brick = Actor("brick3-2", anchor=["left", "top"])
            brick.pos  = triple_brick.pos
            all_bricks.append(brick)

    for pbrick in all_pbrick:
        if pbrick.colliderect(ball):
            all_pbrick.remove(pbrick)
            if ball.pos[0] >= pbrick.left and ball.pos[0] <= pbrick.right:
                invert_vertical_speed()
            else:
                invert_horizontal_speed()


    for power_up_bigger_ball in all_power_up_bigger_ball:
        if player.colliderect(power_up_bigger_ball):
            all_power_up_bigger_ball.remove(power_up_bigger_ball)
            time_bigger_ball = 8
            ball = Actor("superball", ball.pos)
            sounds.pupsb.play()

    for malus_player in all_malus_player:
        if player.colliderect(malus_player)and vie >= 1:
            all_malus_player.remove(malus_player)
            vie = vie - 1
            sounds.maluson.play()
            if vie == 0:
                music.play("go")

    for power_up_bigger_player in all_power_up_bigger_player:
        if player.colliderect(power_up_bigger_player):
            all_power_up_bigger_player.remove(power_up_bigger_player)
            time_bigger_player =8
            player = Actor("bigger_player", player.pos)
            sounds.pup.play()