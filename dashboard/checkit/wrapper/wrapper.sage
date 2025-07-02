import sys,json,os,datetime,hashlib,argparse,shutil

# Library of helpful functions
class CheckIt:
    @staticmethod
    def vars(*latex_names, random_order=True):
        """
        Given one or more `latex_names` of strings, returns a tuple
        of Sage variables. `random_order` names them so that they appear
        in expressions in a random order.
        """
        stamp = randrange(100000,999999)
        indices = list(range(len(latex_names)))
        if random_order:
            shuffle(indices)
        import string
        random_letter = choice(list(string.ascii_lowercase))
        return (var(f"{random_letter}_mi_var_{stamp}_{indices[i]}", latex_name=name) for i, name in enumerate(latex_names))

    @staticmethod
    def shuffled_equation(*terms):
        """
        Represents the equation sum(terms)==0, but with terms shuffled randomly
        to each side.
        """
        new_equation = (SR(0)==0)
        for term in terms:
            if choice([True,False]):
                new_equation += (SR(term)==0)
            else:
                new_equation += (0==-SR(term))
        return new_equation*choice([-1,1])

    @staticmethod
    def shuffled_inequality(*terms,strict=True):
        """
        Represents the equation sum(terms)>0 or >=0, but with terms shuffled randomly
        to each side, and random direction of inequality
        """
        if choice([True,False]):
            if strict:
                new_equation = (SR(0)>0)
            else:
                new_equation = (SR(0)>=0)
            for term in terms:
                if choice([True,False]):
                    new_equation += (SR(term)==0)
                else:
                    new_equation += (0==-SR(term))
        else:
            if strict:
                new_equation = (SR(0)<0)
            else:
                new_equation = (SR(0)<=0)
            for term in terms:
                if choice([True,False]):
                    new_equation += (-SR(term)==0)
                else:
                    new_equation += (0==SR(term))
        return new_equation

    @staticmethod
    def latex_system_from_matrix(matrix, variables="x", alpha_mode=False, variable_list=None):
        # Augment with zero vector if not already augmented
        if not matrix.subdivisions()[1]:
            matrix=matrix.augment(zero_vector(QQ, len(matrix.rows())), subdivide=true)
        num_vars = matrix.subdivisions()[1][0]
        # Start using requested variables
        if variable_list is None:
            system_vars = []
        else:
            system_vars = variable_list
        # Conveniently add xyzwv if requested
        if alpha_mode:
            system_vars += list(var("x y z w v"))
        # Finally fall back to x_n as needed
        system_vars += [var(f"{variables}_{n+1}") for n in range(num_vars)]
        # Build matrix
        latex_output = "\\begin{matrix}\n"
        for row in matrix.rows():
            if row[0]!= 0:
                latex_output += latex(row[0]*system_vars[0])
                previous_terms = True
            else:
                previous_terms = False
            for n,cell in enumerate(row[1:num_vars]):
                latex_output += " & "
                if cell < 0:
                    latex_output += " - "
                elif cell > 0 and previous_terms:
                    latex_output += " + "
                latex_output += " & "
                if cell != 0:
                    latex_output += latex(cell.abs()*system_vars[n+1])
                if not previous_terms:
                    previous_terms = bool(cell!=0)
            if not previous_terms:
                latex_output += " 0 "
            latex_output += " & = & "
            latex_output += latex(row[num_vars])
            latex_output += "\\\\\n"
        latex_output += "\\end{matrix}"
        return latex_output

    @staticmethod
    def latex_solution_set_from_matrix(matrix):
        # Augment with zero vector if not already augmented
        if not matrix.subdivisions()[1]:
            matrix=matrix.augment(zero_vector(QQ, len(matrix.rows())), subdivide=true)
        if (len(matrix.columns())-1) in matrix.pivots():
            return r" \{\} "
        solution_dimension = len(matrix.columns())-1
        free_variables = list(var("a b c d e f g h i j"))
        kernel_basis=matrix.subdivision(0,0).right_kernel(basis='pivot').basis()
        span = sum([kernel_basis[i]*free_variables[i] for i in range(len(kernel_basis))])
        offset = zero_vector(QQ,solution_dimension)
        for row_index,col_index in enumerate(matrix.pivots()):
            offset[col_index] = matrix.rref().columns()[-1][row_index]
        rep = column_matrix(span+offset)
        predicate = ",".join([latex(a) for a in free_variables[:len(kernel_basis)]])
        return r" \left\{ " + latex(rep) + r" \,\middle|\, " + predicate + r" \in\mathbb R \right\} "

    @staticmethod
    def simple_random_matrix_of_rank(rank,rows=1,columns=1,augmented=False):
        # get extra rows and columns, at least zero
        extra_rows = max(0,rows-rank)
        extra_columns = max(0,columns-rank)
        # create matrix with terms between -5 and 5 inclusive, rank in every column, and integer entries RREF
        A = random_matrix(QQ,rank+extra_rows,rank,algorithm='echelonizable',rank=rank,upper_bound=6)
        # randomly choose pivot indices where dependent columns are injected afterward
        inserts = [randrange(rank) for _ in range(extra_columns)]
        # pedagogically we want final column to be dependent at least half the time
        if extra_columns>0 and choice([True,False]):
            inserts[0]=rank-1
        # we'll insert columns backwards to avoid messing up where to inject columns
        inserts.sort(reverse=True)
        # we won't repeat dependent columns
        inserted_columns = []
        for pivot in inserts:
            while True:
                # get random numbers for pivot rows
                rref_pivot_entries = [randrange(-3,4) for _ in range(pivot+1)]
                # ensure at least one is nonzero
                rref_pivot_entries[randrange(pivot+1)] = randrange(1,4)*choice([-1,1])
                # create vector
                dependent_vector = sum([rref_pivot_entries[_]*A.column(_) for _ in range(pivot+1)])
                if dependent_vector not in inserted_columns:
                    inserted_columns.append(dependent_vector)
                    A = matrix(A.columns()[:pivot+1]+[dependent_vector]+A.columns()[pivot+1:]).transpose()
                    break
        if augmented:
            A.subdivide([],[columns-1])
        return A

# decorator to help authors avoid confusing .data() with .get_data() in a Generator
def provide_data(func):
    return lambda self: func(self.get_data())

# BaseGenerator class inherited by each outcome's Generator class to minimize boilerplate
class BaseGenerator:
    def __init__(self):
        self.__data = None
        self.__seed = None

    def data(self):
        return {}

    @provide_data
    def graphics(data):
        return None
    
    def roll_data(self,seed=None):
        if seed is None:
            set_random_seed()
            seed = randrange(1000)
        self.__seed = seed
        set_random_seed(seed)
        self.__data = self.data()

    def get_data(self):
        data = self.__data
        data["__seed__"] = f"{self.__seed:04}"
        return self.__data

# converts SageMath objects into latexified strings
# note Python numbers are latexified into strings as well
def json_ready(obj):
    if isinstance(obj,str) or isinstance(obj,bool):
        return obj
    elif isinstance(obj,list):
        return [json_ready(item) for item in obj]
    elif isinstance(obj,dict):
        return {key:json_ready(obj[key]) for key in obj.keys()}
    else:
        return str(latex(obj))






# this script should be called from the root directory of the bank
# so loads in the generator file work as intended
def cli(_generator_path, _build_path, _slug, _amount=1000, _random=True, _gen_images=False):
    seeds_path = os.path.join(_build_path, _slug, "generated", "seeds.json")

    load(_generator_path) # must provide Generator class extending BaseGenerator
    generator = Generator()

    # Get hash of generator file
    with open(_generator_path, 'rb') as f:
        generator_bytes = f.read()
    generator_hash = hashlib.sha256(generator_bytes).hexdigest()
    cache_dir = os.path.join(_build_path, ".cache", f"{generator_hash}")
    cache_exists = os.path.exists(cache_dir)
    if cache_exists:
        shutil.copytree(cache_dir,os.path.dirname(seeds_path), dirs_exist_ok=True)

    # preview/build to specified JSON file
    seeds = []
    for i in range(_amount):
        if i > 0 and (i % 50) == 0:
            print(f"Generating seed {i}")
        if _random:
            set_random_seed()
            seed_int = int(randrange(1_000))
        else:
            seed_int = int(i)
        generator.roll_data(seed=seed_int)
        seed  = {
            "seed":seed_int,
            "hash":generator_hash,
            "data":json_ready(generator.get_data())
        }
        if _gen_images and not cache_exists:
            graphics = generator.graphics()
            if graphics is not None:
                directory = os.path.join(os.path.dirname(seeds_path))
                if not os.path.exists(directory):
                    os.makedirs(directory)
                for filename in graphics:
                    seed_path = os.path.join(directory,f"{seed_int:04}")
                    if not os.path.exists(seed_path):
                        os.makedirs(seed_path)
                    graphics[filename].save(os.path.join(seed_path,f"{filename}.png"))
        seeds.append(seed)
    data = {
        "seeds": seeds,
        "generated_on": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    os.makedirs(os.path.dirname(seeds_path), exist_ok=True)
    with open(os.path.join(seeds_path), 'w') as f:
        json.dump(data, f)
    if _amount==1000:
        shutil.copytree(os.path.dirname(seeds_path),cache_dir, dirs_exist_ok=True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate seeds for CheckIt bank.")
    parser.add_argument("generator_path", type=str, help="Path to the generator file.")
    parser.add_argument("build_path", type=str, help="Path to save generated assets.")
    parser.add_argument("slug", type=str, help="Slug for the outcome.")
    parser.add_argument("--amount", type=int, default=1000, help="Number of seeds to generate (default: 1000).")
    parser.add_argument("--random", action='store_true', help="Generate seeds randomly.")
    parser.add_argument("--gen_images", action='store_true', help="Generate images for each seed.")

    args = parser.parse_args()
    
    cli(
        args.generator_path, 
        args.build_path, 
        args.slug,
        _amount=args.amount, 
        _random=args.random, 
        _gen_images=args.gen_images
    )
