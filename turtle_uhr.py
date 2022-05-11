import time
import turtle


screen = turtle.Screen()
screen.tracer(0)
screen.setup(width=800, height=800)
screen.bgcolor("black")
uhr = turtle.Turtle()
uhr.hideturtle()
uhr.speed(0)


def zeichne_ziffernblatt() -> None:
    global uhr

    uhr.up()
    uhr.goto(0, 360)
    uhr.seth(180)
    uhr.color("white")
    uhr.pensize(8)
    uhr.pendown()
    uhr.circle(360)
    uhr.seth(90)
    uhr.color("yellow")
    for r in range(60):
        uhr.up()
        uhr.goto(0, 0)
        uhr.forward(350)
        uhr.down()
        if r % 5:
            uhr.forward(10)
        else:
            uhr.forward(30)
        uhr.rt(6)
    return


def zeichne_zeiger(rotate, color, length, size):
    global uhr
    uhr.up()
    uhr.setpos(0, 0)
    uhr.seth(90)
    uhr.rt(rotate)
    uhr.color(color)
    uhr.pensize(size)
    uhr.pendown()
    uhr.forward(length)
    return


def zeichne_uhrzeit():
    global uhr
    sekunde = int(time.strftime("%S"))
    minute = int(time.strftime("%M"))
    stunde = int(time.strftime("%I"))

    zeichne_zeiger((stunde/12)*360, "green", 280, 6)
    zeichne_zeiger((minute/60)*360, "green", 300, 4)
    zeichne_zeiger((sekunde/60)*360, "red", 340, 2)
    return


def main():
    global uhr, screen

    while True:
        zeichne_ziffernblatt()
        zeichne_uhrzeit()
        screen.update()
        uhr.clear()
    pass


if __name__ == "__main__":
    main()
