import msvcrt
import random

spieler = random.randint(1, 2)
spielfeld = [[0] * 6 for _ in range(7)]


class Font:

    cls = "\033[2J\033[H"
    reset = "\033[0m"
    blau = "\033[34m"
    white = "\033[37m"
    red = "\033[91m"
    yellow = "\033[93m"
    black = "\033[30m"

    bg_black = "\033[40m"
    bg_blue = "\033[44m"

    sp1_chip = bg_blue + red + "● "
    sp2_chip = bg_blue + yellow + "● "
    frei = bg_blue + black + "● "


def my_input(text, chars):
    print(text, end="\r")
    ok = False
    char = str()
    while not ok:
        pressed = msvcrt.kbhit()
        char = msvcrt.getch().decode()
        ok = char in chars
    return char


def output():
    feld = Font.reset+Font.cls+"\n\n\n        1 2 3 4 5 6 7\n       --------------\n"
    for y in range(0, 6, 1):
        feld += "       "
        for x in range(0, 7, 1):
            f = spielfeld[x][y]
            if f == 0:
                feld += Font.frei
            elif f == 1:
                feld += Font.sp1_chip
            else:
                feld += Font.sp2_chip
            feld += Font.reset
        feld = feld + " \n"
    print(feld)


def valid(x):
    return spielfeld[x][0] == 0


def setze_chip(x):
    for y in range(0, 6, 1):
        if y == 5 and spielfeld[x][y] == 0:
            spielfeld[x][y] = spieler
            return y
        if spielfeld[x][y] != 0:
            spielfeld[x][y-1] = spieler
            return y-1


def eingabe():
    while True:
        e = my_input("Spieler-"+str(spieler)+" am Zug:", "1234567")
        e = int(e)
        if spielfeld[e-1][0] == 0:
            return e-1
        output()


def unentschieden():
    for x in range(0, 7, 1):
        if spielfeld[x][0] == 0:
            return False
    return True


def diagonalen():
    rechts = [[] for _ in range(12)]
    links = [[] for _ in range(24)]

    for y in range(6):
        for x in range(7):
            rechts[x+y].append(spielfeld[x][y])
            links[(x-y)+11].append(spielfeld[x][y])

    d = list()
    print(links)
    for c in range(12):
        if len(rechts[c]) > 3:
            d.append(rechts[c])
        if len(links[c]) > 3:
            d.append(links[c])

    return d


def gewonnen(spalte, reihe):
    steine = 0
    for y in range(0, 6, 1):
        if spielfeld[spalte][y] == spieler:
            steine += 1
        else:
            steine = 0
        if steine == 4:
            return True

    steine = 0
    for x in range(0, 7, 1):
        if spielfeld[x][reihe] == spieler:
            steine += 1
        else:
            steine = 0
        if steine == 4:
            return True

    diagonal = diagonalen()
    for r in diagonal:
        steine = 0
        for s in r:
            if s == spieler:
                steine += 1
            else:
                steine = 0
            if steine == 4:
                return True

    return False


def main():
    global spieler
    global spielfeld
    sieg = False
    while not sieg:
        output()

        if unentschieden():
            print("Unentschieden!")
            break

        x = eingabe()
        y = setze_chip(x)

        sieg = gewonnen(x, y)

        if sieg:
            output()
            print("Spieler-"+str(spieler)+" hat gewonnen!")

        spieler = (1+2) - spieler


if __name__ == '__main__':

    main()

