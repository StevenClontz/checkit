class Generator(BaseGenerator):
    def data(self):
        x = var("x")
        a,b = sample(range(-9,10),2)
        exercise = (a*x).add(b*x, hold=True)
        correct = a*x+b*x
        incorrects = sample([correct+i*x for i in range(-3,4) if i != 0],3)
        return {
                "exercise": exercise,
                "correct": correct,
                "distractorA": incorrects[0],
                "distractorB": incorrects[1],
                "distractorC": incorrects[2]
            }
