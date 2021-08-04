def generator():
    n = randrange(4,11)
    # wheel graph with n+1 vertices
    filename = f"{n:02}.png"

    return {
        "vertices": n+1,
        "outer_vertices": n,
        "edges": n*2,
        "filename": filename,
    }
