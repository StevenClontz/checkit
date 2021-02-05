# Generator helpers
def mi_vars(*latex_names, random_order=True):
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

def base64_graphic(obj, file_format="svg"):
    """
    Generates Base64 encoding of the graphic in the requested file_format.
    """
    if not isinstance(obj,Graphics):
        raise TypeError("Only graphics may be encoded as base64")
    if file_format not in ["svg", "png"]:
        raise ValueError("Invalid file format")
    filename = tmp_filename(ext=f'.{file_format}')
    obj.save(filename)
    with open(filename, 'rb') as f:
        from base64 import b64encode
        b64 = b64encode(f.read())
    return b64

def data_url_graphic(obj, file_format="svg"):
    """
    Generates Data URL representing the graphic in the requested file_format.
    """
    b64 = base64_graphic(obj, file_format=file_format).decode('utf-8')
    if file_format=="svg":
        file_format = "svg+xml"
    return f"data:image/{file_format};base64,{b64}"

def latex_system_from_matrix(matrix, variables="x", alpha_mode=False, variable_list=[]):
    # Augment with zero vector if not already augmented
    if not matrix.subdivisions()[1]:
        matrix=matrix.augment(zero_vector(QQ, len(matrix.rows())), subdivide=true)
    num_vars = matrix.subdivisions()[1][0]
    # Start using requested variables
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

def json_ready(obj):
    if isinstance(obj,str) or isinstance(obj,bool):
        return obj
    elif isinstance(obj,list):
        return [json_ready(item) for item in obj]
    elif isinstance(obj,dict):
        return {key:json_ready(obj[key]) for key in obj.keys()}
    else:
        return str(latex(obj))

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

import sys,json,os
if sys.argv[4]:
    generator_directory_path = sys.argv[1]
    current_dir = os.getcwd()
    os.chdir(generator_directory_path)
    generator_filename = sys.argv[2]
    amount = int(sys.argv[3])
    public = (sys.argv[4]=="PUBLIC")
    load(generator_filename) # provides generator() function
    seeds = []
    for i in range(amount):
        if public:
            seed = i % 1000
        else:
            set_random_seed()
            seed = randrange(1000,10000)
        set_random_seed(seed)
        seeds.append({"seed":int(seed),"values":json_ready(generator())})
    print(json.dumps(seeds))
    os.chdir(current_dir)
