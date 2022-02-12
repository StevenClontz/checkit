def generator():
    x=var("x")
    m = randrange(-9,10)
    b = randrange(-9,10)
    line = m*x+b

    return {
        "data": { "line": line },
        "image": { "object": plot(line) },
    }
