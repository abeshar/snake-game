#!/usr/bin/env python3
import turtle
import random
import time

# ----------------- CONFIG -----------------
d = 0.1          # delay
s = 0            # score
hs = 0           # high score

# Play area: wider horizontally
HALF_X = 450          # left/right (width 900)
HALF_Y = 350          # up/down (height 700)

OFF_Y = -200          

# Top and bottom of the border after offset
TOP = HALF_Y + OFF_Y
BOT = -HALF_Y + OFF_Y

COLL_X = HALF_X - 10
FOOD_X = HALF_X - 30

# ----------------- SCREEN -----------------
sc = turtle.Screen()
sc.title("Snake Game - PMU")
sc.bgcolor("gray")
sc.setup(width=1200, height=1200)
sc.tracer(0)




# ----------------- BORDER -----------------
border = turtle.Turtle()
border.speed(0)
border.color("white")
border.pensize(3)
border.penup()
border.goto(-HALF_X, BOT)          # bottom-left corner
border.pendown()
for _ in range(2):
    border.forward(HALF_X * 2)     # width (900)
    border.left(90)
    border.forward(HALF_Y * 2)     # height (700)
    border.left(90)
border.hideturtle()

# ----------------- NAMES (LEFT) -----------------
names_writer = turtle.Turtle()
names_writer.speed(0)
names_writer.color("white")
names_writer.penup()
names_writer.hideturtle()
names_writer.goto(0 ,TOP + 250)  

names_writer.write("Snake Game",align="center",font=("candara", 28, "normal")

#names_writer.goto(-570, TOP + 250) 
#names_writer.write(
   # "Group Members:\n"
   # "1) Mohammed H AlAteeq - 202200239\n"
   # "2) Abdurhman S Albeshar - 202002950\n"
   # "3) Mohammad T Alotaishan - 202301935\n"
   # "4) Mahdi M Bayleh - 201901622\n"
   # "5) ",
   # align="left",
   # font=("candara", 14, "normal")
)

# ----------------- SCORE (TOP CENTER) -----------------
p = turtle.Turtle()
p.speed(0)
p.shape("square")
p.color("white")
p.penup()
p.hideturtle()
p.goto(0, TOP + 80)                 
p.write("Score : 0  High Score : 0",
        align="center", font=("candara", 24, "bold"))

# ----------------- SNAKE & FOOD -----------------
h = turtle.Turtle()
h.shape("square")
h.color("white")
h.penup()
h.goto(0, 0)
h.direction = "Stop"

f = turtle.Turtle()
f.speed(0)
f.shape(random.choice(["square", "triangle", "circle"]))
f.color(random.choice(["red", "green", "black"]))
f.penup()
f.goto(0, TOP - 50)

seg = []   # body segments list


# ----------------- CONTROLS -----------------
def up():
    if h.direction != "down":
        h.direction = "up"


def down():
    if h.direction != "up":
        h.direction = "down"


def left():
    if h.direction != "right":
        h.direction = "left"


def right():
    if h.direction != "left":
        h.direction = "right"


def move():
    if h.direction == "up":
        h.sety(h.ycor() + 20)
    if h.direction == "down":
        h.sety(h.ycor() - 20)
    if h.direction == "left":
        h.setx(h.xcor() - 20)
    if h.direction == "right":
        h.setx(h.xcor() + 20)


def reset_game():
    global s, d, seg

    h.goto(0, 0)
    h.direction = "Stop"

    f.goto(
        random.randint(-FOOD_X, FOOD_X),
        random.randint(BOT + 30, TOP - 30)
    )

    # Clear body
    for segment in seg:
        segment.goto(1000, 1000)
    seg.clear()

    s = 0
    d = 0.1

    p.clear()
    p.write(f"Score : {s}  High Score : {hs}",
            align="center", font=("candara", 24, "bold"))


# ----------------- KEY BINDINGS -----------------
sc.listen()
sc.onkeypress(up, "Up")
sc.onkeypress(down, "Down")
sc.onkeypress(left, "Left")
sc.onkeypress(right, "Right")

reset_game()   # start immediately

# ----------------- MAIN LOOP -----------------
try:
    while True:
        sc.update()

        # boundary check (uses TOP/BOT now)
        if (h.xcor() > COLL_X or h.xcor() < -COLL_X or
                h.ycor() > TOP - 10 or h.ycor() < BOT + 10):
            time.sleep(1)
            reset_game()

        # food collision
        if h.distance(f) < 20:
            f.goto(
                random.randint(-FOOD_X, FOOD_X),
                random.randint(BOT + 30, TOP - 30)
            )

            # add new segment
            n_seg = turtle.Turtle()
            n_seg.speed(0)
            n_seg.shape("square")
            n_seg.color("orange")
            n_seg.penup()
            seg.append(n_seg)

            # increase difficulty
            d = max(0.01, d - 0.001)

            # update score
            s += 10
            if s > hs:
                hs = s

            p.clear()
            p.write(f"Score : {s}  High Score : {hs}",
                    align="center", font=("candara", 24, "bold"))

        # move segments
        for i in range(len(seg) - 1, 0, -1):
            x = seg[i - 1].xcor()
            y = seg[i - 1].ycor()
            seg[i].goto(x, y)

        if len(seg) > 0:
            seg[0].goto(h.xcor(), h.ycor())

        # move head
        move()

        # self-collision
        for segment in seg:
            if segment.distance(h) < 20:
                time.sleep(1)
                reset_game()

        time.sleep(d)

except turtle.Terminator:
    # window closed; exit cleanly
    pass
