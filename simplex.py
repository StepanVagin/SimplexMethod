import math

def simplex_solver(C, A, b, eps=1e-6):
    """
    Solves the Linear Programming Problem using the Simplex method.

    Input:
    - C: A list of coefficients of the objective function
    - A: A list of lists representing the matrix of coefficients of the constraint functions
    - b: A list of right-hand side values
    - eps: Approximation accuracy (optional, default = 1e-6)

    Returns:
    - solver_state: 'solved' or 'unbounded'
    - x*: Optimal vector of decision variables (if solved)
    - z: Maximum value of the objective function (if solved)
    """

    def print_problem(C, A, b):
        n = len(C)
        obj_function = "max z = "
        obj_terms = []
        for i in range(n):
            coeff = C[i]
            if coeff != 0:
                term = f"{coeff}*x{i + 1}"
                obj_terms.append(term)
        obj_function += " + ".join(obj_terms)
        print(obj_function)
        print("\nSubject to:")

        m = len(A)
        for i in range(m):
            constraint_terms = []
            for j in range(n):
                coeff = A[i][j]
                if coeff != 0:
                    term = f"{coeff}*x{j + 1}"
                    constraint_terms.append(term)
            constraint = " + ".join(constraint_terms)
            constraint += f" <= {b[i]}"
            print(constraint)
        print()

    def construct_initial_tableau(C, A, b):
        m = len(A)
        n = len(C)

        tableau = []

        for i in range(m):
            # Add slack variables
            row = A[i] + [0] * m + [b[i]]
            row[n + i] = 1
            tableau.append(row)

        # Objective function row
        obj_row = [-c for c in C] + [0] * m + [0]
        tableau.append(obj_row)

        return tableau

    def find_pivot_column(tableau):
        last_row = tableau[-1][:-1]
        min_value = min(last_row)
        if min_value >= -eps:
            return -1  # Optimal solution found
        else:
            return last_row.index(min_value)

    def find_pivot_row(tableau, pivot_col):
        num_rows = len(tableau) - 1
        ratios = []
        for i in range(num_rows):
            element = tableau[i][pivot_col]
            rhs = tableau[i][-1]
            if element > eps:
                ratio = rhs / element
                ratios.append((ratio, i))
        if not ratios:
            return -1  # Unbounded
        else:
            # Choose the pivot row with the smallest ratio
            min_ratio, min_index = min(ratios, key=lambda x: x[0])
            return min_index

    def pivot_operation(tableau, pivot_row, pivot_col):
        pivot_element = tableau[pivot_row][pivot_col]
        tableau[pivot_row] = [element / pivot_element for element in tableau[pivot_row]]
        for i in range(len(tableau)):
            if i != pivot_row:
                row_factor = tableau[i][pivot_col]
                tableau[i] = [tableau[i][j] - row_factor * tableau[pivot_row][j] for j in range(len(tableau[0]))]

    def extract_solution(tableau, num_variables, total_variables):
        num_rows = len(tableau) - 1  # Exclude objective function row
        solution = [0] * num_variables
        for j in range(num_variables):
            column = [tableau[i][j] for i in range(num_rows)]
            if column.count(1) == 1 and column.count(0) == num_rows - 1:
                row_index = column.index(1)
                solution[j] = tableau[row_index][-1]
            else:
                solution[j] = 0
        return solution


    def round_to_eps(x, eps):
        """
        Rounds the number x to the nearest multiple based on eps.
        """
        if eps >= 1:
            return round(x / eps) * eps
        else:
            decimal_places = max(-int(math.floor(math.log10(eps))), 0)
            return round(x, decimal_places)

    def round_solution(solution, eps):
        return [round_to_eps(x, eps) for x in solution]

    def round_value(value, eps):
        return round_to_eps(value, eps)
    
    if any(bi < 0 for bi in b):
        print("The method is not applicable!")
        return
    print_problem(C, A, b)

    tableau = construct_initial_tableau(C, A, b)
    num_variables = len(C)
    total_variables = len(tableau[0]) - 1  # Exclude RHS

    while True:
        pivot_col = find_pivot_column(tableau)
        if pivot_col == -1:
            break
        pivot_row = find_pivot_row(tableau, pivot_col)
        if pivot_row == -1:
            print("The method is not applicable!")
            return
        pivot_operation(tableau, pivot_row, pivot_col)

    solution = extract_solution(tableau, num_variables, total_variables)
    solution = round_solution(solution, eps)
    optimal_value = tableau[-1][-1]
    optimal_value = round_value(optimal_value, eps)

    print("x*:", solution)
    print("z:", optimal_value)

    return

def main():
    # Objective function coefficients
    C = [3, 2, 4]

    # Constraints coefficients
    A = [
        [-1, 2, 1],
        [4, 1, 2],
        [-2, 0, 1],
    ]

    # Right-hand side values
    b = [-1, 8, 3]

    # Approximation accuracy
    eps = 1e-4

    simplex_solver(C, A, b, eps)


if __name__ == '__main__':
    main()
