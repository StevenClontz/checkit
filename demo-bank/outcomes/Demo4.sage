def generator():
    n = randrange(4,11)
    # wheel graph with n+1 vertices
    filename = f"{n:02}.png"

    return {
        "vertices": n,
        "outer_vertices": n-1,
        "edges": n*2-2,
        "filename": filename,
    }
