def input_lpp():
    # Input number of variables and constraints
    n = int(input("Enter the number of variables: "))
    m = int(input("Enter the number of constraints: "))

    # Input coefficients of the objective function
    print("Enter the coefficients of the objective function (space-separated):")
    c = list(map(float, input().split()))

    # Input coefficients of the constraints row-wise
    print("Enter the coefficients of the constraints row-wise (Ax ≤ b):")
    A = []
    for i in range(m):
        row = list(map(float, input().split()))
        A.append(row)

    # Input the right-hand side values
    print("Enter the right-hand side values (b):")
    b = list(map(float, input().split()))

    # Input the approximation accuracy (epsilon)
    epsilon = float(input("Enter the approximation accuracy (epsilon): "))

    return A, b, c, epsilon


def construct_tableau(A, b, c):
    # Initializing the tableau
    num_constraints = len(A)
    num_variables = len(c)

    # Create the tableau with slack variables
    tableau = []

    # Add each constraint row (A_i | slack variables | b_i)
    for i in range(num_constraints):
        row = A[i] + [1 if j == i else 0 for j in range(num_constraints)] + [b[i]]
        tableau.append(row)

    # Add the objective function row (c | slack variables | 0)
    objective_row = [-x for x in c] + [0] * (num_constraints + 1)
    tableau.append(objective_row)

    return tableau


def print_tableau(tableau):
    print("Tableau:")
    for row in tableau:
        print(row)
    print()

def find_pivot_column(tableau, epsilon):
    # Find the most negative value in the objective row (excluding the last column)
    objective_row = tableau[-1]
    min_value = min(objective_row[:-1])
    if min_value >= -epsilon:
        return -1  # If all values are non-negative or close to zero, the solution is optimal
    return objective_row.index(min_value)

def find_pivot_row(tableau, pivot_col, epsilon):
    num_rows = len(tableau) - 1
    min_ratio = float('inf')
    pivot_row = -1
    for i in range(num_rows):
        if tableau[i][pivot_col] > epsilon:  # Only consider positive entries in the pivot column
            ratio = tableau[i][-1] / tableau[i][pivot_col]
            if ratio < min_ratio:
                min_ratio = ratio
                pivot_row = i
    return pivot_row

def pivot_operation(tableau, pivot_row, pivot_col):
    pivot_value = tableau[pivot_row][pivot_col]
    tableau[pivot_row] = [x / pivot_value for x in tableau[pivot_row]]

    num_rows = len(tableau)
    num_cols = len(tableau[0])
    
    for i in range(num_rows):
        if i != pivot_row:
            row_factor = tableau[i][pivot_col]
            tableau[i] = [tableau[i][j] - row_factor * tableau[pivot_row][j] for j in range(num_cols)]