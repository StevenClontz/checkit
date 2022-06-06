class Generator(BaseGenerator):
    def data(self):
        x=var("x")
        m = randrange(-9,10)
        b = randrange(-9,10)
        line = m*x+b
        lines = [{
            "line": line,
            "slope": m,
            "intercept": b,
            "findfunction": True,
            "filename": "find",
        }]
        m = randrange(-9,10)
        b = randrange(-9,10)
        line = m*x+b
        lines += [{
            "line": line,
            "slope": m,
            "intercept": b,
            "todraw": True,
            "filename": "todraw",
        }]
        shuffle(lines)
        return {
            "lines": lines,
        }

    @provide_data
    def graphics(data):
        """
        Variables generated above are available in the
        data dictionary (see `data["lines"]` below). Graphics
        take a long time to generate and take up a lot of
        space on the disk, so consider carefully if they are necessary.

        This should return a dictionary of the form
        `{filename_string: graphics_object}` which will each produce
        `f"{filename_string}.png}"`.
        """
        return {
            line_data["filename"]: plot(line_data["line"])
            for line_data in data["lines"]
        }
