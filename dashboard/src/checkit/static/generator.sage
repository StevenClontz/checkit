class Generator(BaseGenerator):
    def data(self):
        x = var('x')
        a = randrange(-9,10)
        b = randrange(-9,10)
        p = randrange(2,6)

        return {
            "sum": (a*x^p).add(b*x^p,hold=True),
            "result": (a+b)*x^p,
        }
