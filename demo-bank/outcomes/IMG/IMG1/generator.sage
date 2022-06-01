class Generator(BaseGenerator):
    def data(self):
        x=var("x")
        m = randrange(-9,10)
        b = randrange(-9,10)
        line = m*x+b
        return {
            "line": line,
            "slope": m,
            "intercept": b,
        }

    @provide_data
    def graphics(data):
        return plot(data["line"])
