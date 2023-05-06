import turtle
import random
import numpy as np
import sounddevice as sd


# sound
sr = 44100
length = 1.6
sd.query_devices()


def square(frq, a, d):
    sr = 44100
    env = np.concatenate((np.linspace(0, 0.5, int(round(sr * a, 0))),
                          np.linspace(0.5, 0, int(round(sr * d, 0)))))
    t = np.arange(int(round(d * sr + a * sr, 0))) / sr
    sine = 1 * np.sin(2 * np.pi * frq * t)
    square = np.where(sine < 0, - 1, 1)
    return square * env


freqs_sp = [261.62, 329.63, 391.995, 523.251, 391.995, 523.251]
freqs_sp_2 = np.array([square(f, length * 0.01, length * 0.09) for f in freqs_sp])
success_pattern = np.concatenate(freqs_sp_2)


freqs_lose = [369, 349, 329]
freqs_lose_2 = np.array([square(fl, length * 0.01, length * 0.09) for fl in freqs_lose])
lose_pattern = np.concatenate(freqs_lose_2)

# set up screen


win = turtle.Screen()
win.title('hangman')
win.bgcolor('black')


# setting up the drawing mechanism


mitch = turtle.Turtle()
mint = turtle.Turtle()
mitch.color('red')
mint.color('green')
mitch.hideturtle()
mint.hideturtle()

# game logic preparations

word = input()

solution = [x for x in word]
compare_sol = solution.copy()


d = 0
mint.penup()
mint.goto(-200, -100)

for spacee in solution:
    mint.pendown()
    mint.forward(20)
    mint.penup()
    mint.forward(20)

mint.goto(-200, -100)
mint.penup()

level = 2

rand_letters_num = [random.randint(0, len(solution) - 1) for y in range(level)]
rand_letters = [solution[x] for x in rand_letters_num]


for i in range(len(solution)):
    if solution[i] in rand_letters:
        mint.forward(i * 40)
        mint.pendown()
        mint.write(solution[i], font=("Arial", 12, "normal"))
        mint.penup()
        mint.goto(-200, -100)

for w in range(len(solution)):
    if solution[w % len(solution)] in rand_letters:
        solution.pop(w % len(solution))

mitch.goto(0, 0)

# game logic

while len(solution) != 0:
    inp = input('Guess a letter')
    if inp in compare_sol and inp not in solution:
        print('that is already there')
    elif inp in solution:
        for a in range(len(solution)):
            if solution[a % len(solution)] == inp:
                solution.pop(a % len(solution))
        for b in range(len(compare_sol)):
            mint.goto(-200, -100)
            if compare_sol[b] == inp:
                mint.forward(b * 40)
                mint.pendown()
                mint.write(inp, font=("Arial", 12, "normal"))
                mint.penup()
        print('Good Job')
        sd.play(success_pattern, sr)
    else:
        sd.play(lose_pattern, sr)
        d += 1
        mitch.pendown()
        if d == 1:
            mitch.left(90)
            mitch.forward(100)
        elif d == 2:
            mitch.right(90)
            mitch.forward(200)
        elif d == 3:
            mitch.right(90)
            mitch.forward(20)
        elif d == 4:
            mitch.right(90)
            mitch.circle(10)
        elif d == 5:
            mitch.left(90)
            mitch.penup()
            mitch.forward(20)
            mitch.pendown()
            mitch.forward(20)
        elif d == 6:
            mitch.penup()
            mitch.backward(15)
            mitch.left(90)
            mitch.pendown()
            mitch.forward(15)
        elif d == 7:
            mitch.penup()
            mitch.backward(15)
            mitch.left(180)
            mitch.pendown()
            mitch.forward(15)
        elif d == 8:
            mitch.penup()
            mitch.backward(15)
            mitch.left(90)
            mitch.forward(15)
            mitch.pendown()
            mitch.right(45)
            mitch.forward(20)
        elif d == 9:
            mitch.penup()
            mitch.backward(20)
            mitch.left(90)
            mitch.pendown()
            mitch.forward(20)
            mitch.penup()
            mitch.goto(160, -20)
            mitch.write('the game has ended', font=("Arial", 12, "normal"))
            break


win.mainloop()
