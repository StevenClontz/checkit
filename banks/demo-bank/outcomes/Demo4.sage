def generator():
    # randomly choose from one of two images
    filename = f"{randrange(4,11):02}.png"

    return {
        "filename": filename,
    }
