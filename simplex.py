def input_lpp():
    m = int(input("Enter the number of constraints: "))

    print("Enter the coefficients of the objective function (space-separated):")
    c = list(map(float, input().split()))

    print("Enter the coefficients of the constraints row-wise (Ax ≤ b):")
    a = []
    for i in range(m):
        row = list(map(float, input().split()))
        a.append(row)

    print("Enter the right-hand side values (b):")
    b = list(map(float, input().split()))

    epsilon = float(input("Enter the approximation accuracy (epsilon): "))

    return a, b, c, epsilon


def construct_tableau(a, b, c):
    num_constraints = len(a)

    tableau = []

    for i in range(num_constraints):
        row = a[i] + [1 if j == i else 0 for j in range(num_constraints)] + [b[i]]
        tableau.append(row)

    objective_row = [-x for x in c] + [0] * (num_constraints + 1)
    tableau.append(objective_row)

    return tableau


def print_tableau(tableau):
    print("Tableau:")
    for row in tableau:
        print(row)
    print()

def find_pivot_column(tableau, epsilon):
    objective_row = tableau[-1]
    min_value = min(objective_row[:-1])
    if min_value >= -epsilon:
        return -1
    return objective_row.index(min_value)

def find_pivot_row(tableau, pivot_col, epsilon):
    num_rows = len(tableau) - 1
    min_ratio = float('inf')
    pivot_row = -1
    for i in range(num_rows):
        if tableau[i][pivot_col] > epsilon:
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


def simplex_method(tableau, epsilon):
    while True:
        pivot_col = find_pivot_column(tableau, epsilon)
        if pivot_col == -1:
            break

        pivot_row = find_pivot_row(tableau, pivot_col, epsilon)
        if pivot_row == -1:
            return "The method is not applicable!"

        pivot_operation(tableau, pivot_row, pivot_col)

    return tableau


def extract_solution(tableau, num_variables):
    num_constraints = len(tableau) - 1
    solution = [0] * num_variables
    for i in range(num_constraints):
        non_zero_col = [j for j in range(num_variables) if tableau[i][j] == 1]
        if len(non_zero_col) == 1 and tableau[i][non_zero_col[0]] == 1:
            solution[non_zero_col[0]] = tableau[i][-1]
    return solution


def solve_lpp():
    a, b, c, epsilon = input_lpp()

    tableau = construct_tableau(a, b, c)
    print_tableau(tableau)

    result = simplex_method(tableau, epsilon)

    if isinstance(result, str):
        print(result)
    else:
        optimal_value = result[-1][-1]
        num_variables = len(c)
        solution = extract_solution(result, num_variables)
        print("Optimal solution (X*):", solution)
        print("Optimal value:", optimal_value)


if __name__ == "__main__":
    solve_lpp()
