class Generator(BaseGenerator):
    def data(self):
        x = var("x")

        # define possible factors
        factors = [
            x^randrange(2,10),
            e^x,
            cos(x),
            sin(x),
            log(x),
        ]
        shuffle(factors)
        f = choice([-1,1])*randrange(2,5)*factors[0]*factors[1]

        variant = choice(["derivative", "rate of change"])


        return {
            "f": f,
            "dfdx": f.diff(),
            "d_synonym": variant,
        }
