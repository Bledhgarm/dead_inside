import turtle
import time
import random
from math import sin, cos
import os

def trying():
    try:
        with open('score.txt', 'a+') as f:
            if os.stat('score.txt').st_size == 0:
                f.write('0')
    except FileNotFoundError:
        print('файла не существует')


def up():
    if head.heading() != 270:
        head.setheading(90)


def down():
    if head.heading() != 90:
        head.setheading(-90)


def right():
    if head.heading() != 180:
        head.setheading(0)


def left():
    if head.heading() != 0:
        head.setheading(180)


def gameover():
    global max_score
    screen.bgcolor('red')
    draw.up()
    draw.goto(0, 0)
    draw.color('white')
    draw.write('YOU LOSE!', align='center',
               font=('Arial', 32, 'normal'))
    draw_score.clear()
    draw_score.write(f'Score: {count}   Max score: {max(count, max_score)}', align='center',
                     font=('Arial', 20, 'normal'))
    score_file = open(filename, 'w')
    score_file.write(str(max(count, max_score)))
    score_file.close()


def escape():
    score_file = open(filename, 'w')
    score_file.write(str(max(count, max_score)))
    score_file.close()
    screen.bye()
    screen.exitonclick('Escape')




def boom():
    g = 0.5
    t = 0.015
    ky = 0.93
    kx = 0.5
    for segment in snake + [food] + enemies:
        segment.dx = cos(head.heading() + 90) * random.randint(3, 12)
        segment.dy = sin(head.heading() + 90) * random.randint(3, 12)

    while True:
        for segment in snake + [food] + enemies:
            segment.goto(segment.xcor() + segment.dx,
                         segment.ycor() + segment.dy)
            if segment.ycor() > half_field - half_cell:
                segment.sety(half_field - half_cell)
                segment.dy = -segment.dy * ky
            elif segment.ycor() < -half_field + half_cell:
                segment.sety(-half_field + half_cell)
                segment.dy = -segment.dy * ky
            if segment.xcor() > half_field - half_cell:
                segment.setx(half_field - half_cell)
                segment.dx = -segment.dx * kx
            elif segment.xcor() < -half_field + half_cell:
                segment.setx(-half_field + half_cell)
                segment.dx = -segment.dx * kx
            if abs(segment.dx) < 0.25:
                segment.dx = 0
            segment.dy -= g
        screen.update()
        time.sleep(t)


def place_enemy():
    for enemy in enemies:
        x = random.randrange(-half_field + half_cell,
                             half_field - half_cell, cell)
        y = random.randrange(-half_field + half_cell,
                             half_field - half_cell, cell)
        if (x, y) == food.pos() or head.pos():
            x = random.randrange(-half_field + half_cell,
                                 half_field - half_cell, cell)
            y = random.randrange(-half_field + half_cell,
                                 half_field - half_cell, cell)
        enemy.setheading(random.choice((0, 90, 180, 270)))
        enemy.goto(x, y)


screen = turtle.Screen()
screen.setup(500, 500)
screen.colormode(255)
screen.bgcolor('olive drab')
screen.title('SNAKE')
screen.tracer(0)
# some variables
count = 0
n = 21
field = 420
cell = field / n
half_cell = cell / 2
half_field = field // 2
filename = 'score.txt'
draw = turtle.Turtle()
draw.hideturtle()
draw.color('gold')
draw.shapesize(2)
draw.penup()
draw.goto(-half_field, half_field)
draw.pendown()
draw.pensize(3)
draw.goto(half_field, half_field)
draw.goto(half_field, -half_field)
draw.goto(-half_field, -half_field)
draw.goto(-half_field, half_field)

trying()
score_file = open(filename, 'r')
max_score = int(score_file.read())
score_file.close()

draw.pensize(1)
# we draw our playing board
for i in range(n):
    draw.goto(draw.xcor(), draw.ycor() - cell)
    draw.goto(draw.xcor() + field * (-1) ** i, draw.ycor())
for i in range(n):
    draw.goto(draw.xcor() - cell, draw.ycor())
    draw.goto(draw.xcor(), draw.ycor() + field * (-1) ** i)
# for playing with buttons
screen.onkeypress(up, 'w')
screen.onkeypress(down, 's')
screen.onkeypress(left, 'a')
screen.onkeypress(right, 'd')
screen.onkeypress(escape, 'Escape')
screen.onkeypress(up, 'Up')
screen.onkeypress(down, 'Down')
screen.onkeypress(left, 'Left')
screen.onkeypress(right, 'Right')
screen.listen()

screen.tracer(500, 0)

snake = []
for i in range(3):
    segment = turtle.Turtle()
    segment.shape('square')
    segment.penup()
    if i == 0:
        segment.color('black', '#000de6')
    else:
        segment.color('black', '#00c0e6')
    snake.append(segment)
# spawn some food
food = turtle.Turtle()
food.color('black', 'yellow')
food.shape('square')
food.penup()
food.goto(random.randrange(-half_field + half_cell,
                           half_field - half_cell, cell),
          random.randrange(-half_field + half_cell,
                           half_field - half_cell, cell))
head = snake[0]
GAMEOVER = False
draw_score = turtle.Turtle()
draw_score.hideturtle()
draw_score.penup()
draw_score.goto(0, half_field + 10)
draw_score.color('white')
draw_score.write(f'Score: {count}   Max score: {max_score}', align='center', font=('Arial', 20, 'normal'))

enemies = []

while True:
    if head.distance(food) < 10:
        segment = turtle.Turtle()
        segment.shape('square')
        segment.color('black', '#00c0e6')
        segment.penup()
        snake.append(segment)
        count += 100
        if count % 300 == 0:
            place_enemy()
        if count % 500 == 0:
            enemy = turtle.Turtle()
            enemy.penup()
            enemy.color('black', 'red')
            enemy.shape('square')
            enemy.setheading(random.choice((0, 90, 180, 270)))
            enemies.append(enemy)
        draw_score.clear()
        food.goto(random.randrange(-half_field + half_cell,
                                   half_field - half_cell, cell),
                  random.randrange(-half_field + half_cell,
                                   half_field - half_cell, cell))

    for i in range(len(snake) - 1, 0, -1):
        snake[i].goto(snake[i - 1].position())
    head.forward(cell)
    # in which moments we lose
    for segment in snake[1:]:
        if head.distance(segment) < 10:
            GAMEOVER = True

    for enemy in enemies:
        enemy.forward(cell)
        if enemy.xcor() > half_field:
            enemy.goto(-half_field, enemy.ycor())
        elif enemy.xcor() < -half_field:
            enemy.goto(half_field, enemy.ycor())
        if enemy.ycor() > half_field:
            enemy.goto(enemy.xcor(), - half_field)
        elif enemy.ycor() < -half_field:
            enemy.goto(enemy.xcor(), half_field)
        if head.distance(enemy) < 10:
            GAMEOVER = True
            break

    if GAMEOVER:
        gameover()
        break

    if (abs(head.xcor()) >= half_field or
            abs(head.ycor()) >= half_field):
        gameover()
        break

    draw_score.clear()
    draw_score.write(f'Score: {count}   Max score: {max(count, max_score)}', align='center',
                     font=('Arial', 20, 'normal'))
    screen.update()
    time.sleep(0.1)

boom()
screen.mainloop()
