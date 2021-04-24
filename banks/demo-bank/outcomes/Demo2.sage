def generator():
    x = var("x")

    # define possible factors
    factors = [
        x^randrange(2,10),
        e^x,
        cos(x),
        sin(x),
        log(x),
    ]
    shuffle(factors)
    f = choice([-1,1])*randrange(2,5)*factors[0]*factors[1]

    return {
        "f": f,
        "df": f.diff(),
    }
