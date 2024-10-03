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
