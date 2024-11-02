import numpy as np
from numpy.linalg import LinAlgError

from simplex import simplex_solver


def interior_point_algorithm(A, b, c, x_initial, alpha,
                             convergence_threshold=1e-5,
                             max_iterations=1000) -> tuple[int, np.ndarray] | None:
    x = x_initial.copy()
    m, n = A.shape

    # Check initial feasibility
    Ax = A @ x
    if not np.all(Ax <= b):
        violated = np.where(Ax > b)[0] + 1
        raise Exception(f"Method not applicable! Constraint(s) {violated.tolist()} are violated.")

    iterations_data = []
    for iteration in range(1, max_iterations + 1):
        v = x.copy()

        # Construct Diagonal matrix D
        D = np.diag(x)

        # Compute AA = A * D
        AA = A @ D

        # Compute cc = D * c
        cc = D @ c

        # Compute F = AA * AA^T
        F = AA @ AA.T

        try:
            FI = np.linalg.inv(F)
        except LinAlgError:
            raise Exception(f"Matrix inversion failed in iteration {iteration}. The method is not applicable!")

        # Compute H = AA^T * F^-1
        H = AA.T @ FI

        # Compute P = I - H * AA
        I = np.eye(n)
        P = I - H @ AA

        # Compute cp = P * cc
        cp = P @ cc

        # Find nu = |min(cp)|
        min_cp = np.min(cp)
        nu = abs(min_cp)

        if nu == 0:
            raise Exception(f"Division by zero encountered in iteration {iteration}.")

        # Compute y = 1 + (alpha / nu) * cp
        y = np.add ( np.ones( n , float), ( alpha /nu ) * cp)

        # Compute yy = D * y
        yy = x * y

        # Store iteration data
        iterations_data.append((iteration, yy.copy()))

        # Check for convergence
        diff = yy - v
        norm_diff = np.linalg.norm(diff)
        if norm_diff < convergence_threshold:
            break

        # Update x for next iteration
        x = yy
    else:
        print("Maximum iterations reached without convergence.")
        return None

    return iterations_data[-1][0], iterations_data[-1][1].round(3)


def main():
    test_cases = [
        {
            "description": "Test Case 1",
            "c": np.array([5, 4, 0, 0]),
            "A": np.array([
                [3, 5, 1, 0],
                [4, 1, 0, 1]
            ]),
            "b": np.array([78, 36]),
            "x_initial": np.array([7, 6, 27, 0]),
            "epsilon_simplex": 1e-5,
            "convergence_threshold": 1e-5
        },
        {
            "description": "Test Case 2",
            "c": np.array([5, 4, 0, 0]),
            "A": np.array([
                [2, 3, 1, 0],
                [1, 1, 0, 1]
            ]),
            "b": np.array([12, 7]),
            "x_initial": np.array([2, 1, 6, 1]),
            "epsilon_simplex": 1e-5,
            "convergence_threshold": 1e-5
        },
        {
            "description": "Test Case 3",
            "c": np.array([1, 3, 0, 0]),
            "A": np.array([
                [1, 1, 1, 0],
                [1, 1, 0, 1]
            ]),
            "b": np.array([1, 3]),
            "x_initial": np.array([0.5, 0.5, 0, 0]),
            "epsilon_simplex": 1e-5,
            "convergence_threshold": 1e-5
        },
        {
            "description": "Test Case 4",
            "c": np.array([2, 1, 4, 3]),
            "A": np.array([
                [1, 2, 1, 0],
                [2, 1, 0, 1],
                [0, 1, 2, 1]
            ]),
            "b": np.array([4, 6, 5]),
            "x_initial": np.array([0, 0, 0, 0]),
            "epsilon_simplex": 1e-6,
            "convergence_threshold": 1e-6
        },
        {
            "description": "Test Case 5",
            "c": np.array([1, 1, 0, 0]),
            "A": np.array([
                [2, 4, 1, 0],
                [1, 3, 0, -1]
            ]),
            "b": np.array([16, 9]),
            "x_initial": np.array([0.5, 3.5, 1, 2]),
            "epsilon_simplex": 1e-5,
            "convergence_threshold": 1e-5
        }
    ]

    for case in test_cases:
        A = case["A"]
        b = case["b"]
        c = case["c"]
        epsilon_simplex = case["epsilon_simplex"]
        x_initial = case["x_initial"]
        convergence_threshold = case["convergence_threshold"]

        for alpha in [0.5, 0.9]:
            print(f"\nRunning {case['description']}, alpha = {alpha} :\n{'=' * 50}")
            try:
                iteration, answer = interior_point_algorithm(A, b, c, x_initial, alpha, convergence_threshold)
                print(f"\nInterior Point Algorithm converged in {iteration} iterations. X = {answer}")
            except Exception as e:
                print(e)

        # Run Simplex Method
        print("\nRunning Simplex Method:\n" + "-" * 50)
        answer = simplex_solver(c.tolist(), A.tolist(), b.tolist(), epsilon_simplex)
        print(f"\nSimplex Method converged. X = {answer['x*']}")


if __name__ == "__main__":
    main()
