class Generator(BaseGenerator):
    def data(self):
        x=var("x")
        m = randrange(-9,10)
        b = randrange(-9,10)
        line = m*x+b
        return {
            "line": line,
        }

    @provide_data
    def graphics(data):
        return plot(data["line"])
