from __future__ import annotations
import os
from typing import Any, List
import re

class Board():
    end: int
    score: dict
    overall: dict
    turn: int
    def __init__(self, end_score: int = 501, p1 : str = "P1", p2: str = "P2") -> None:
        self.end = end_score
        self.score = {p1 : self.end, p2 : self.end}
        self.overall = {p1 : 0, p2 : 0}
        self.turn = 0
    
    def __str__(self) -> str:
        p1 = list(self.score.keys())[0]
        p2 = list(self.score.keys())[1]
        spacing_1 = 3 + len(p1) + 4 + 3
        spacing_2 = 3 + len(p2) + 4 + 3

        out = "   {}: {:<5}|   {}: {}\n".format(p1, self.overall[p1] , p2, self.overall[p2])
        out += "{}|{}\n".format("-" * spacing_1, "-" * spacing_2)
        out += "{}{}|{}\n\n".format(" " * (spacing_1 - len(str(self.score[p1]))), self.score[p1], self.score[p2])

        return out

    def add_points(self, turn_score: int) -> (str, bool):
        p = list(self.score.keys())[self.turn]
        temp = self.score[p]
        self.score[p] -= turn_score
        s = self.score[p]
        if s < 0: 
            self.score[p] = temp
        elif s == 0:
            self.overall[p] += 1
            return "Congratulations! {} wins!\n\n {}Play again? [Y/n]\n".format(p, self), True
        self.turn = abs(self.turn - 1)
        return "{}It's {}'s turn. Input their score and press enter.".format(self, list(self.score.keys())[self.turn]), False

def clear() -> None:
    """ Clears the console
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def ask_num(prompt : str) -> str:
    a = ""
    while not re.split('[+*]+', a)[0].isnumeric():
        a = input(prompt).replace(" ", "")
    return add(a)

def add(s: str) -> int:
    l = s.split('+')
    t = 0
    for i in l:
        if i.isnumeric():
            t += int(i)
        else:
            t += mult(i)
    return t

def mult(s : str) -> int:
    l = s.split("*")
    t = 1
    for i in l:
        t *= int(i)
    return t

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    e = ask_num("End score: ")
    p1 = input("Name of Player One: ")
    p2 = input("Name of Player Two: ")
    print("Success!\n")
    b = Board(e, p1, p2)
    first = True

    while first:    
        score = 0
        b.add_points(0)
        a, win = b.add_points(0)
        clear()
        print(a)
        while first or not win:
            first = False
            score = ask_num("")
            a, win = b.add_points(score)
            clear()
            print(a)

        a = input("")
        while a.lower() != "y" and a.lower() != "n":
            a = input("Play again? [Y/n]\n")
        if a.lower() == "y":
            first = True
            b = Board(e, p1, p2)