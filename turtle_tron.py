import functools
import time
import turtle


class Spieler:
    speed = float()
    tur = object()
    last_pos = tuple()
    running = bool()

    def __init__(self, color, pos, rot):
        self.tur = turtle.Turtle()
        self.tur.penup()
        self.tur.color(color)
        self.tur.pencolor(color)
        self.tur.setpos(pos[0], pos[1])
        self.tur.setheading(0 + rot)
        self.tur.pensize(4)
        self.tur.pendown()
        self.tur.speed(0)
        self.speed = 4.0
        self.last_pos = self.tur.pos()

    def check_border(self):
        global width, height
        w = width / 2
        h = height / 2
        y = self.tur.ycor()
        x = self.tur.xcor()
        if y > h:
            self.tur.penup()
            self.tur.sety(-h)
            self.tur.pendown()
        elif y < -h:
            self.tur.penup()
            self.tur.sety(h)
            self.tur.pendown()
        if x > w:
            self.tur.penup()
            self.tur.setx(-w)
            self.tur.pendown()
        elif x < -w:
            self.tur.penup()
            self.tur.setx(w)
            self.tur.pendown()

    def update_spielfeld(self):
        global spielfeld, width, height
        pos = self.tur.pos()
        x_length = int(pos[0] - self.last_pos[0])
        y_length = int(pos[1] - self.last_pos[1])
        x = int(pos[0] + width / 2)
        y = int(pos[1] + height / 2)
        spielfeld[x][y] = True
        for yl in range(y_length):
            for xl in range(x_length):
                if x + xl > width:
                    print("greater")
                    pass
                elif x + xl < 0:
                    print("smaller")
                    pass
                else:
                    spielfeld[x + xl][y + yl] = True

    def check_collision(self) -> bool:
        global spielfeld, width, height
        return spielfeld[int(self.tur.xcor() + width / 2)][int(self.tur.ycor() + height / 2)]

    def forward(self):
        global running, global_speed
        self.tur.forward(self.speed + global_speed)
        if self.last_pos != self.tur.pos():
            self.check_border()
            if self.check_collision():
                print(self.last_pos, self.tur.pos())
                running = False
            self.update_spielfeld()
            self.last_pos = self.tur.pos()

    def left(self):
        self.tur.left(90)

    def right(self):
        self.tur.right(90)


screen = turtle.Screen()
width = 800
height = 600
tron = Spieler("yellow", (0 - (width / 2), 0), 0)
nort = Spieler("red", (0 + (width / 2), 0), 180)
spielfeld = [[False] * (height + 4) for _ in range(width + 4)]
playtime = int(0)
global_speed = int(0)


def intro():
    intro_turtle = turtle.Turtle()
    intro_turtle.showturtle()
    intro_turtle.pencolor("white")
    running = True

    intro_turtle.speed(0)
    intro_turtle.penup()
    intro_turtle.pensize(10)
    intro_turtle.showturtle()
    intro_turtle.goto(-width / 2, 200)
    intro_turtle.setheading(0)
    intro_turtle.pendown()
    intro_turtle.speed("slow")

    tron_map = [0, 150, 0,
                180, -100, 0,
                270, 0, -140,
                0, 40, 0,
                90, 0, 80,
                270, 0, -20,
                0, 50, 0,
                270, 0, -10,
                90, 0, 10,
                180, -50, 0,
                270, 0, -60,
                0, 140, 0,
                90, 0, 60,
                180, -50, 0,
                270, 0, -60,
                0, 90, 0,
                90, 0, 80,
                270, 0, -20,
                0, 50, 0,
                270, 0, -60]

    intro_turtle.goto(-200, intro_turtle.ycor())

    for i in range(0, len(tron_map), 3):
        intro_turtle.setheading(tron_map[i])
        intro_turtle.goto(intro_turtle.xcor() + tron_map[i + 1], intro_turtle.ycor() + tron_map[i + 2])

    intro_turtle.setheading(0)
    intro_turtle.goto(width / 2, intro_turtle.ycor())

    def start_game():
            nonlocal running
            running = False

    while running:
        turtle.onkeyrelease(start_game, "space")
        turtle.listen()
        screen.update()

    intro_turtle.clear()
    del intro_turtle


def restart():
    global tron, nort, spielfeld, running
    tron = Spieler("yellow", (0 - (width / 2), 0), 0)
    nort = Spieler("red", (0 + (width / 2), 0), 180)
    spielfeld = [[False] * (height + 4) for _ in range(width + 4)]
    running = True


def turn_left(player: Spieler):
    player.left()
    return


def turn_right(player: Spieler):
    player.right()
    return


def spiel():
    global running, global_speed, playtime
    utime = int(time.time())

    while running:
        turtle.onkey(functools.partial(turn_left, nort), "a")
        turtle.onkey(functools.partial(turn_right, nort), "d")
        turtle.onkey(functools.partial(turn_left, tron), "4")
        turtle.onkey(functools.partial(turn_right, tron), "6")
        turtle.listen()

        tron.forward()
        nort.forward()

        playtime += (int(time.time()) - utime)
        utime = int(time.time())

        if playtime > 20:
            global_speed += 1


if __name__ == "__main__":
    screen.setup(width=width, height=height)
    screen.bgcolor("black")
    running = True
    intro()
    spiel()
    turtle.done()
