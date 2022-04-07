class Generator(BaseGenerator):
    def data(self):
        return {
                "first": {
                    "first": randrange(10),
                    "second": randrange(10),
                    "third": randrange(10),
                },
                "second": randrange(10),
            }
