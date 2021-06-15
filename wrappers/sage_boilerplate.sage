def generator():
    random_int = randrange(2,10)
    return {
        "number": random_int,
        "hellos": "hello "*random_int,
    }