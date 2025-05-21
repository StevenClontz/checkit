class Generator(BaseGenerator):
    def data(self):
        x=var("x")

        m = randrange(-9,10)
        b = randrange(-9,10)
        line = m*x+b
        findfunction_line = {
            "line": line,
            "slope": m,
            "intercept": b,
        }

        m = randrange(-9,10)
        b = randrange(-9,10)
        line = m*x+b
        todraw_line = {
            "line": line,
            "slope": m,
            "intercept": b,
        }

        return {
            "findfunction_line": findfunction_line,
            "todraw_line": todraw_line,
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
            "find": plot(data["findfunction_line"]["line"]),
            "draw": plot(data["todraw_line"]["line"]),
        }
