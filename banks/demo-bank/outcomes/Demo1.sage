def generator():
    x,y = var("x y")

    # Genereate random line with slope -B/A
    A = randrange(1,10)*choice([-1,1])
    B = A
    while A==B:
        B = randrange(1,10)*choice([-1,1])
    C = randrange(-9,10)
    # standard equation
    line1 = {
        'equation': (A*x+B*y==C),
        'slope': -B/A,
    }

    # Genereate random line with slope m
    m = randrange(1,10)*choice([-1,1])
    b = randrange(-9,10)
    # slope-intercept equation
    line2 = {
        'equation': (y==m*x+b),
        'slope': m,
    }

    lines = [line1,line2]
    shuffle(lines)

    return {"lines": lines}
