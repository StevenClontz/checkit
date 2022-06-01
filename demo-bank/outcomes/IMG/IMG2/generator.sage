class Generator(BaseGenerator):
    def data(self):
        image_version = f"{randrange(1,4)}"
        return {
            "digit": image_version,
        }
