def generator():
    # randomly choose from one of two images
    filename = choice(["20200102/puzzle.png","dice.png"])

    return {
        "filename": filename,
    }
