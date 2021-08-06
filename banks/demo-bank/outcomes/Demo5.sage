def generator():
    x = var('x')
    ints = list(IntegerRange(-9,0))+list(IntegerRange(1,10))
    shuffle(ints)
    fs = list('fghjklmn')
    shuffle(fs)

    # continuous
    continuous = True
    left = ints[0]*x+ints[1]
    right = ints[2]*x+ints[1]
    functions = [{
        'left': left,
        'right': right,
        'continuous': continuous,
        'f': fs[0],
    }]

    # discontinuous
    continuous = False
    left = ints[3]*x+ints[4]
    right = ints[5]*x+ints[6]
    functions += [{
        'left': left,
        'right': right,
        'continuous': continuous,
        'f': fs[1],
    }]

    return { "functions": functions }
